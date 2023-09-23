import pandas as pd
import os
from bs4 import BeautifulSoup
import re
from collections import defaultdict

df = pd.DataFrame(columns=['Name', 'Kingdom', 'Phylum',
                  'Class', 'Order', 'Family', 'Genus', 'Scientific Name', 'Quote', 'Text', 'Pairs'])


def parser():

    directory_path = './animals'
    file_names = os.listdir(directory_path)
    file_names.sort()

    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents = file.read()
                print(f"Trying to parse {file_name}")
                file_parser(file_contents, file_name)


def add_row(new_row):
    global df
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)


def save_csv():
    global df
    df.to_csv('output.csv', index=False)


count_dict = defaultdict(int)

count_errors = 0


def file_parser(content, file_name):
    global count_errors

    soup = BeautifulSoup(content, 'html.parser')
    try:
        quote = soup.find('blockquote').find('p').text.strip()
    except:
        quote = ''
        count_errors += 1

    try:
        taxum = soup.find('dl', attrs={
            'class': 'row animal-facts'}).findAll('dd', attrs={'class': 'col-sm-9'})
        for i in range(len(taxum)):
            taxum[i] = taxum[i].text.strip()
    except:
        taxum = []
        count_errors += 1

    # if no taxum found, append empty strings
    if len(taxum) != 7:
        for i in range(7-len(taxum)):
            taxum.append('')

    try:
        text = soup.find('div', attrs={'id': 'single-animal-text'}).findAll(
            'p')
        for i in range(len(text)):
            text[i] = text[i].text.strip()
    except:
        text = []
        count_errors += 1

    pattern = re.compile(r'\s+')
    cleaned_text = [pattern.sub(' ', s.strip())
                    for s in text if not s.startswith('©')]

    combined_text = ' '.join(cleaned_text)

    pairs = []

    try:
        factsBox = soup.findAll(
            'div', attrs={'class': 'row animal-facts-box'})[1]
        dt_elements = factsBox.findAll('dt', class_='col-sm-6 text-md-right')
        dd_elements = factsBox.findAll('dd', class_='col-sm-6')

        for dt, dd in zip(dt_elements, dd_elements):
            dt_text = dt.text.strip()  # Extract and clean text from <dt>
            dd_text = dd.text.strip()  # Extract and clean text from <dd>
            global count_dict
            count_dict[dt_text] += 1
            # print(count_dict)
            pairs.append((dt_text, dd_text))

    except:
        count_errors += 1

    # print(pairs)

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
        'Text': combined_text,
        'Pairs': pairs,
    }

    add_row(new_row)


# parser()
save_csv()
# print(count_dict)
print(f"Number of errors: {count_errors}")

"""
Diet: 2519
Color: 2380
Skin Type: 2363
Fun Fact: 2352
Lifespan: 2147
Weight: 1843
Habitat: 1692
Common Name: 1587
Length: 1582
Most Distinctive Feature: 1541
Group Behavior: 1493
Predators: 1413
Prey: 1408
Biggest Threat: 1336
Name Of Young: 1247
Lifestyle: 1232
Type: 1182
Location: 1155
Other Name(s): 1100
Number Of Species: 1076
Favorite Food: 981
Estimated Population Size: 946
Age of Sexual Maturity: 859
Gestation Period: 810
Aggression: 809
Venomous: 784
Litter Size: 781
Main Prey: 771
Top Speed: 755
Distinctive Feature: 735
Slogan: 698
Height: 617
Average Litter Size: 600
Temperament: 542
Group: 539
Incubation Period: 440
Nesting Location: 439
Wingspan: 407
Age of Weaning: 402
Origin: 360
Special Features: 263
Average Clutch Size: 261
Migratory: 222
Age Of Independence: 210
Age of Molting: 182
Age Of Fledgling: 170
Average Spawn Size: 170
Diet for this Fish: 160
Optimum pH Level: 157
Training: 117
Optimum PH Level: 3
"""
