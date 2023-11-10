#!/bin/bash

# Check if required commands are available
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python 3 is required but not installed. Aborting."; exit 1; }

# Input parameters
json_file=$1
relevant_animals=$2
output_csv=$3

# Check if all required parameters are provided
if [ -z "$json_file" ] || [ -z "$relevant_animals" ] || [ -z "$output_csv" ]; then
    echo "Usage: $0 <json_file> <relevant_animals> <output_csv>"
    exit 1
fi

# Read JSON file using Python and extract animal names
animals=$(python3 -c "import json; data = json.load(open('$json_file')); print(','.join([animal['Name'] for animal in data]))")

# Calculate metrics
metrics_data=""
for ((i = 1; i <= $(echo $animals | tr ',' '\n' | wc -l); i++)); do
    subset_animals=$(echo $animals | tr ',' '\n' | head -n $i | tr '\n' ',')
    subset_animals=${subset_animals%,}  # Remove trailing comma
    precision=$(python3 -c "subset = set('$subset_animals'.split(',')); relevant = set('$relevant_animals'.split(',')); print(len(subset.intersection(relevant)) / len(subset) if len(subset) > 0 else 0)")
    recall=$(python3 -c "subset = set('$subset_animals'.split(',')); relevant = set('$relevant_animals'.split(',')); print(len(subset.intersection(relevant)) / len(relevant) if len(relevant) > 0 else 0)")
    f_measure=$(python3 -c "precision = $precision; recall = $recall; print(2 * precision * recall / (precision + recall) if precision + recall > 0 else 0)")
    metrics_data+="$i,$precision,$recall,$f_measure\n"
done

# Display metrics
echo -e "Metrics:\n$metrics_data"

# Export metrics to the specified CSV file
echo -e "N,Precision,Recall,F-Measure\n$metrics_data" > "$output_csv"

echo "Metrics exported to $output_csv"
