import pandas as pd
import os

df = pd.DataFrame(columns=['Name', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Scientific Name'])

def parser():

    directory_path = './animals'
    file_names = os.listdir(directory_path)

    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents = file.read()
                file_parser(file_contents)
                print(f"File {file_name} parsed.")


def add_row(new_row):
    global df
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)
    
def save_csv():
    global df
    df.to_csv('output.csv', index=False)


def file_parser(f):

    
  
    add_row(new_row)







parser()



"""
 new_row = {
    'Name': 'Lion',
    'Kingdom': 'Animalia',
    'Phylum': 'Chordata',
    'Class': 'Mammalia',
    'Order': 'Carnivora',
    'Family': 'Felidae',
    'Genus': 'Panthera',
    'Scientific Name': 'Panthera leo'
    }
"""

            
            

