import requests

def send_solr_request(q):
    url = "http://localhost:8983/solr/animals/query"
    
    # Define the query parameters
    params = {
        'q': q,
        "defType": "edismax",
        "qf": "Name^2.5 Features^2.0 Fun_Fact^2.0 Diet^2.0 Text^1.5 Features^2.0 Behavior^2.0",
        "pf": "Name^2.5 Features^2.0 Fun_Fact^2.0 Diet^2.0 Text^1.5 Features^2.0 Behavior^2.0",
        "mm": "3<-25%",
        "ps": 5,
        "fl": "Name, score",
        "rows": "30"

    }

    try:
        # Send the HTTP GET request
        response = requests.get(url, params=params)

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
            if 'Name' in doc and 'score' in doc:
                animal = {
                    'Name': doc['Name'],
                    'score': doc['score']
                }
                animals.append(animal)

    return animals


txt = "Animals that walk in hierarchical groups or herds and how they deal with territory"

output = (parse_solr_response(send_solr_request(txt)))

if len(output) == 0:
    print("Zero results found!")
    exit(0) 

f = open(f"nosyn_{txt.replace(' ', '_')}.txt", "w")
f.write(str(output))
f.close()

print(f"Got {len(output)} results")



