#!/bin/bash

# Check if the schema name is provided as a command-line argument, otherwise use default 'schema.json'
SCHEMA_NAME=${1:-schemaV2.json}
mkdir /var/solr/data
chown -R solr:solr /var/solr/data
precreate-core animals

# This script expects a container started with the following command. In the ANIMAL-EXPLORATION directory, run the following command before running this script (only one time)):
# docker run -p 8983:8983 --name animal_exploration_solr -v ${PWD}:/home -d solr:9.3 solr-precreate animals -e SOLR_OPTS='-Dsolr.ltr.enabled=true' 

# enable -Dsolr.ltr.enabled=true in solr
# docker start animal_exploration_solr 
sed -i $'/<\/config>/{e cat /home/solr/ltr-plugin.xml\n}' /var/solr/data/animals/conf/solrconfig.xml


solr start -Dsolr.ltr.enabled=true
sleep 10

# Make the necessary changes to allow CORS
# docker exec -u 0 animal_exploration_solr apt-get update
# docker exec -u 0 animal_exploration_solr apt-get install -y nano

# Start bash in the container with root permissions
# docker exec -u 0 -it animal_exploration_solr /bin/bash

# Restart the container
# docker restart animal_exploration_solr

# sleep 10

# Delete the existing core
# solr delete -c animals

# Create a new core
# solr create -c animals

echo "SCHEMA ..."
echo "SYNONYM ..."
SYNONYMS_FILE="/home/solr/MySynonyms.txt"
cp "${SYNONYMS_FILE}"  animal_exploration_solr:/var/solr/data/animals/conf/MySynonyms.txt

# Schema definition via API, using the provided schema name
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@/home/solr/${SCHEMA_NAME}" \
    http://localhost:8983/solr/animals/schema

# Configure MLT handler
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@/home/solr/mlt-handler.json" \
    http://localhost:8983/solr/animals/config


curl -XPUT 'http://localhost:8983/solr/test/schema/model-store' \
    --data-binary "@/home/solr/ltr_model.json" -H 'Content-type:application/json'

# echo "Configuring solr config"
# echo "copying ..."
# docker cp ./ltr-plugin.xml animal_exploration_solr:/home/data/ltr-plugin.xml
# echo "configuring ..."
# sed -i $'/<\/config>/{e cat /home/data/ltr-plugin.xml\n}' /var/solr/data/animals/conf/solrconfig.xml
# sed -i $'/<\/config>/{e cat /home/solr/ltr-plugin.xml\n}' /var/solr/data/animals/conf/solrconfig.xml



echo "Feature store configuration..."

curl -XPUT 'http://localhost:8983/solr/animals/schema/feature-store' \
    --data-binary "@/home/solr/myFeatures.json" -H 'Content-type:application/json'

# Configure CORS
# curl -X POST -H 'Content-type:application/json' \
#     --data-binary "@./cors-config.json" \
#     http://localhost:8983/solr/animals/config

# Example of MLT query
# curl http://localhost:8983/solr/animals/mlt?q=id:1&mlt.fl=body
# curl http://localhost:8983/solr/animals/mlt?q=id:b73a3418-4c8a-4aa9-b58f-ac13de6d9bfe&fl=id,Name


# Populate collection using a mapped path inside the container.
post -c animals /home/data/output_clean.csv

#sed -i -e 's/\r$//' scriptname.sh
# echo "Press Enter to stop the container..."
# read -r dummy_var

# docker stop animal_exploration_solr

# Restart in foreground mode so we can access the interface
solr restart -f -Dsolr.ltr.enabled=true
