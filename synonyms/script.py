import pandas as pd
from collections import Counter
import re
from nltk.corpus import wordnet

# Load CSV file into a pandas DataFrame
file_path = 'data.csv'  # Update with your file path
df = pd.read_csv(file_path)

all_words = ' '.join(df['Text'].astype(str)).lower()  # Combine all text entries
word_list = re.findall(r'\b\w+\b', all_words)  # Extract words using regex

# Filter out words containing numbers
word_list = [word for word in word_list if not any(char.isdigit() for char in word)]

unique_words_set = set(word_list)

print("Starting synonyms...")

# ========================================================================

# Define the path for the synonym.txt file
synonym_file_path = 'synonym.txt'  # Update with your desired file path

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().lower()
            if synonym != word and synonym in unique_words_set:
                synonyms.add(synonym)
    return list(synonyms)

existing_lines = []


with open(synonym_file_path, 'w') as synonym_file:
    # Iterate through unique words and write word with its unique synonyms if not already present
    for word in unique_words_set:
        synonyms = get_synonyms(word)
        if synonyms:
            line_list = [*sorted(synonyms)]
            line_list.append(word)
            line_list.sort()
            
            # Check if the sorted line is not a subset of any existing line
            if not any(set(line_list).issubset(existing_line) for existing_line in existing_lines):
                synonym_file.write(', '.join(line_list) + '\n')
                existing_lines.append(set(line_list))
                print(f"appending line: {line_list}")
            else:
                print(f"Already have line: {line_list}")

print(f"Synonym file {synonym_file_path} updated successfully!")







