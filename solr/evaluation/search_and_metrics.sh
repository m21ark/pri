#!/bin/bash

# Input parameters
solr_url="http://localhost:8983/solr/animals"  # Replace with your Solr collection URL
request_file=$1
output_subdirectory=$2
output_directory="queries"

# Check if all required parameters are provided
if [ -z "$request_file" ] || [ -z "$output_subdirectory" ]; then
    echo "Usage: $0 <request_file> <output_subdirectory>"
    exit 1
fi

# Create the output directory and subdirectory if they don't exist
mkdir -p "$output_directory/$output_subdirectory"

# Send a search request to Solr and store the retrieved animals as an array of JSON objects
curl -H "Content-Type: application/json" --data-binary "@$request_file" "$solr_url/select" | jq '.response.docs' > "$output_directory/$output_subdirectory/retrieved_animals.txt"

# Call the metrics script
metrics_output_directory="$output_directory/$output_subdirectory/metrics"
mkdir -p "$metrics_output_directory"
./metrics.sh "$output_directory/$output_subdirectory/retrieved_animals.txt" "$output_directory/$output_subdirectory/relevant_animals.txt" "$metrics_output_directory/metrics.csv"

echo "Metrics and retrieved animals stored in $output_directory/$output_subdirectory"
