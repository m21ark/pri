import requests

# 1. Bluetick Coonhound - id: 10b3d677-4415-4a84-8db7-e6d9ff81f24a
# 2. Cat Faced Spider   - id: d394ea2a-be83-4337-8989-af12341a1f2a
# 3. Lawnmower Blenny   - id: 86e0b8b5-6cfe-4cfe-9fe0-ffdb14def375
# 4. Olive Baboon       - id: fb40acbf-8567-4416-9412-0f42240effd4
# 5. Mule Deer          - id: 2cc37a98-aeed-4c76-9531-17f40366913a

# Ids
id1 = "10b3d677-4415-4a84-8db7-e6d9ff81f24a"
id2 = "d394ea2a-be83-4337-8989-af12341a1f2a"
id3 = "86e0b8b5-6cfe-4cfe-9fe0-ffdb14def375"
id4 = "fb40acbf-8567-4416-9412-0f42240effd4"
id5 = "2cc37a98-aeed-4c76-9531-17f40366913a"

def send_solr_request(id):
    url = f"http://localhost:8983/solr/animals/mlt?q=id:{id}"

    try:
        # Send the HTTP GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content
            # print("Response:")
            return (response.json())
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"Error: {e}")

def parse_solr_response(response_json):
    # Extract the list of animals from the Solr response
    animals = []

    # Check if 'response' and 'docs' keys exist in the response
    if 'response' in response_json and 'docs' in response_json['response']:
        for doc in response_json['response']['docs']:
            # Check if 'Name' and 'score' keys exist in the document
            if 'Name' in doc:
                animal = {
                    'Name': doc['Name'],
                    'Text': doc['Text'],
                }
                animals.append(animal)

    return animals


output = (parse_solr_response(send_solr_request(id5)))

if len(output) == 0:
    print("Zero results found!")
    exit(0) 

f = open(f"retrieved.txt", "w")
f.write(str(output))
f.close()

print(f"Got {len(output)} results")



