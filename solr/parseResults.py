import json

relevantAnimalsFile = 'relevant.txt'
retrievedAnimalsFile = 'retrieved.txt'


file_path = retrievedAnimalsFile
with open(file_path, 'r') as file:
    json_data = json.load(file)

def is_animal_in_file(animal_name, file_path):
    with open(file_path, 'r') as file:
        return any(animal_name.lower() in line.lower() for line in file)

count = 0
result_string = ""
for animal in json_data:
    if is_animal_in_file(animal['Name'], relevantAnimalsFile):
        result_string += "R"
        print(f"Animal '{animal['Name']}' is relevant")
        count += 1
    else:
        result_string += "N"

print("=============================")
print("Relevant count: " + str(count))
print("Animal count: " + str(len(result_string)))
print("=============================")
print(result_string)


