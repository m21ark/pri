#!/bin/bash

# Check if the schema name is provided as a command-line argument, otherwise use default 'schema.json'
SCHEMA_NAME=${1:-schemaV2.json}

# This script expects a container started with the following command. In the ANIMAL-EXPLORATION directory, run the following command before running this script (only one time)):
# docker run -p 8983:8983 --name animal_exploration_solr -v ${PWD}:/home -d solr:9.3 solr-precreate animals

docker start animal_exploration_solr

sleep 5

# Delete the existing core
docker exec animal_exploration_solr bin/solr delete -c animals

# Create a new core
docker exec animal_exploration_solr bin/solr create -c animals

# Schema definition via API, using the provided schema name
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./${SCHEMA_NAME}" \
    http://localhost:8983/solr/animals/schema

# Populate collection using a mapped path inside the container.
docker exec -it animal_exploration_solr bin/post -c animals /home/data/output_clean.csv

#sed -i -e 's/\r$//' scriptname.sh
echo "Press Enter to stop the container..."
read -r dummy_var

docker stop animal_exploration_solr
