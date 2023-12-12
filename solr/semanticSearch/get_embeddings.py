import sys
import pandas as pd
from sentence_transformers import SentenceTransformer

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from transformers import GPT2Tokenizer, GPT2Model

# nltk.download('stopwords')
# stop_words = set(stopwords.words('english'))
# porter = PorterStemmer()

model = SentenceTransformer('all-MiniLM-L6-v2')

# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# model = GPT2Model.from_pretrained('gpt2')
# tokenizer.add_special_tokens({'pad_token': '[PAD]'})
# tokenizer.pad_token = tokenizer.eos_token

def process_text(text):
    return text.lower()

    # words = [word for word in text.split() if word not in stop_words]
    # stemmed_words = [porter.stem(word) for word in text.split()]

    # return ' '.join(stemmed_words)

def get_embedding(text):
    return model.encode(text.lower(), convert_to_tensor=False).tolist()

    # inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    # outputs = model(**inputs)

    # return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python get_embeddings.py input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    df = pd.read_csv(input_file)

    text_columns = ['Name', 'Features', 'Fun Fact', 'Diet', 'Text', 'Behavior', 'Origin', 'Genus']
    df['combined_text'] = df[text_columns].fillna('').agg(' '.join, axis=1)

    df['combined_text'] = df['combined_text'].apply(process_text)

    df['vector'] = df['combined_text'].apply(get_embedding)

    df.drop(columns=['combined_text'], inplace=True)

    json_data = df.to_json(orient='records')

    #df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
    with open(output_file + '.json', 'w') as json_file:
        json_file.write(json_data)

    