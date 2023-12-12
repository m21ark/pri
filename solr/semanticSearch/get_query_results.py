import json
import os
import requests
from sentence_transformers import SentenceTransformer

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')

from transformers import GPT2Tokenizer, GPT2Model

stop_words = set(stopwords.words('english'))
porter = PorterStemmer()

# model = SentenceTransformer('all-MiniLM-L6-v2')

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2Model.from_pretrained('gpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
tokenizer.pad_token = tokenizer.eos_token

def process_text(text):
    return text.lower()

    # words = [word for word in text.split() if word not in stop_words]

    # stemmed_words = [porter.stem(word) for word in text.split()]

    # return ' '.join(stemmed_words)

def text_to_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)

    return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    embedding = model.encode(text.lower(), convert_to_tensor=False).tolist()

    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_knn_query(endpoint, collection, embedding):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!knn f=vector topK=30}}{embedding}",
        "fl": "Name,Genus,Origin,Behavior,Diet,Features,Fun_Fact,Text,score",
        "rows": 30,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "animals"
    
    queries = {
        "q1":"energetic dog breeds suited for hunting",
        "q2":"animals native to North America that like to eat insects",
        "q3":"change the color of their skin, fur or feathers for the purpose of camouflage",
        "q4":"animals that walk in hierarchical groups or herds and how they deal with territory",
        "q5":"not birds migrate to Mexico or migrate to America"
    }

    for key, value in queries.items():
        processedText = process_text(value)
        embedding = text_to_embedding(processedText)

        try:
            results = solr_knn_query(solr_endpoint, collection, embedding)
            docs = results.get("response", {}).get("docs", [])

            with open("queries/" + key + "/retrieved_animals3.json", 'w') as json_file:
                if not docs:
                    json.dump({"msg": "no results"}, json_file, indent=4)
                else:
                    json.dump(docs, json_file, indent=4)
        except requests.HTTPError as e:
            print(f"Error {e.response.status_code}: {e.response.text}")

if __name__ == "__main__":
    main()
