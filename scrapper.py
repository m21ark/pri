import pandas as pd
import os
from bs4 import BeautifulSoup
import re

df = pd.DataFrame(columns=['Name', 'Kingdom', 'Phylum',
                  'Class', 'Order', 'Family', 'Genus', 'Scientific Name', 'Quote', 'Text'])


def parser():

    directory_path = './animals'
    file_names = os.listdir(directory_path)
    file_names.sort()

    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents = file.read()
                file_parser(file_contents, file_name)
                print(f"File {file_name} parsed.")
        


def add_row(new_row):
    global df
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)


def save_csv():
    global df
    df.to_csv('output.csv', index=False)


def file_parser(content, file_name):

    soup = BeautifulSoup(content, 'html.parser')
    try:
        quote = soup.find('blockquote').find('p').text.strip()
    except:
        quote = ''

    try:
        taxum = soup.find('dl', attrs={
            'class': 'row animal-facts'}).findAll('dd', attrs={'class': 'col-sm-9'})
        for i in range(len(taxum)):
            taxum[i] = taxum[i].text.strip()
    except:
        taxum = []

    try:
        text = soup.find('div', attrs={'id': 'single-animal-text'}).findAll(
            'p')
        for i in range(len(text)):
            text[i] = text[i].text.strip()
    except:
        text = []

    pattern = re.compile(r'\s+')
    cleaned_text = [pattern.sub(' ', s.strip())
                    for s in text if not s.startswith('©')]

    combined_text = ' '.join(cleaned_text)

    # if no taxum found, append empty strings
    if len(taxum) != 7:
        for i in range(7-len(taxum)):
            taxum.append('')

    new_row = {
        'Name': file_name.split('.')[0],
        'Kingdom': taxum[0],
        'Phylum': taxum[1],
        'Class': taxum[2],
        'Order': taxum[3],
        'Family': taxum[4],
        'Genus': taxum[5],
        'Scientific Name': taxum[6],
        'Quote': quote,
        'Text': combined_text
    }

    add_row(new_row)


parser()
save_csv()
