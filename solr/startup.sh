#!/bin/bash

# This script expects a container started with the following command. In the ANIMAL-EXPLORATION directory run the following command before running this script(only one time)):
# docker run -p 8983:8983 --name animal_exploration_solr -v ${PWD}:/home -d solr:9.3 solr-precreate animals

docker start animal_exploration_solr

sleep 5

### questão é preciso dar sempre map do dir ?
### is there a better way to do this?
#delete the existing core
docker exec animal_exploration_solr bin/solr delete -c animals

# Create a new core
docker exec animal_exploration_solr bin/solr create -c animals


# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./schema.json" \
    http://localhost:8983/solr/animals/schema


# Populate collection using mapped path inside container.
docker exec -it animal_exploration_solr bin/post -c animals /home/data/output_clean.csv

echo "Press Enter to stop the container..."
read -r dummy_var

docker stop animal_exploration_solr
