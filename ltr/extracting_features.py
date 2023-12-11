import numpy as np
import requests
import simplejson

# Number of documents to be re-ranked.
RERANK = 50
with open("RERANK.int", "w") as f:
    f.write(str(RERANK))

# Build query URL.

text = "natural habit"

url = "http://localhost:8983/solr/test/query"
url += "?q={0}&df=text&rq={{!ltr model=my_efi_model ".format(text)
url += "efi.text='{0}'}}".format(text)
url += "&fl=id,Name,score,[features]&rows={1}".format(text, RERANK)

# Get response and check for errors.
response = requests.request("GET", url)
json =[]
try:
    json = simplejson.loads(response.text)
except simplejson.JSONDecodeError:
    print(text)

if "error" in json:
    print(text)

# Extract the features.
results_features = []
results_targets = []
results_ranks = []
relevant = []
q_id = "Q1"
add_data = False

for (rank, document) in enumerate(json["response"]["docs"]):

    features = document["[features]"].split(",")
    feature_array = []
    for feature in features:
        feature_array.append(feature.split("=")[1])

    feature_array = np.array(feature_array, dtype = "float32")
    results_features.append(feature_array)

    doc_id = document["id"]
    # Check if document is relevant to query.
    if q_id in relevant.get(doc_id, {}):
        results_ranks.append(rank + 1)
        results_targets.append(1)
        add_data = True
    else:
        results_targets.append(0)

if add_data:
    np.save("{0}_X.npy".format(q_id), np.array(results_features))
    np.save("{0}_y.npy".format(q_id), np.array(results_targets))
    np.save("{0}_rank.npy".format(q_id), np.array(results_ranks))