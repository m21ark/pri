import pandas as pd
import numpy as np
import re


def clean_text(df):
    # if NaN, replace with empty string
    df = df.replace(np.nan, '', regex=True)

    # remove all quotes, \n, and trailing spaces
    df = df.replace(r'\"', '', regex=True)
    df = df.replace('"', '', regex=False)
    df = df.replace(r'\n', '', regex=True)
    df = df.replace(r'\s+$', '', regex=True)

    return df


# Drops colums that are not needed for the analysis:
# Group: 539
# Average Litter Size: 600
# Training: 117
# Number Of Species: 1076
def drop_columns(df):
    df = df.drop(['Group', 'Average Litter Size', 'Litter Size'
                 'Training', 'Number Of Species'], axis=1)
    return df


# 1 Join these columns:
# Diet: 2519
# Prey: 1408
# Favorite Food: 981
# Main Prey: 771
# Diet for this Fish: 160
def join_food_cols(df):
    food_columns = ['Diet', 'Diet for this Fish', 'Prey', 'Favorite Food',
                    'Main Prey']

    phrase_mapping = {
        'Diet': '',
        'Diet for this Fish': '',
        'Prey': 'and eats',
        'Main Prey': 'and especially likes',
        'Favorite Food': 'and enjoys',
    }

    # iterate over all rows
    for index, row in df.iterrows():
        food = ''
        UsedThat = False

        for col in food_columns:
            if food.find('.') != -1:
                food = food.replace('.', '')
            if not pd.isna(row[col]) and row[col] != '':
                val = row[col].lower()
                if col == 'Diet' or col == 'Diet for this Fish':
                    val = val.capitalize()
                    if food.find(val) == -1:
                        food += f'{phrase_mapping[col]} {val} '
                elif food == "" and (col != 'Diet' and col != 'Diet for this Fish'):
                    food += f'Eats {val} '
                elif (food.find('that') == -1) and not UsedThat and (col != 'Diet' and col != 'Diet for this Fish'):
                    val = val.replace("they eat", '')
                    food += f'{phrase_mapping[col].replace("and", "that")} {val} '
                    UsedThat = True
                else:
                    # Add the food if it is not already in the string

                    if food.find(val) == -1:

                        for word in val.replace(',', '').split():

                            if food.find(word) != -1:
                                val = val.replace(word, '')

                        val = val.strip()
                        if val != '' and not val.isspace() and not val.lower() == 'and':
                            # if val starts with a comma, remove it
                            if val[0] == ',':
                                val = val[1:]

                            # if it starts with "and", remove it
                            if val[0:3] == 'and':
                                val = val[3:]

                            food += f'{phrase_mapping[col]} {val} '

        if food.find('that') == -1 and food != '' and food.find('eats') == -1 and food.find('Eats') == -1 and food.find('and') == -1:
            food += 'with no preference'

        # Remove consecutive commas with spaces
        food = re.sub(r'(, *)+,', ',', food)

        # remove trailing space
        food = food.strip()

        # If ends with a comma, remove it
        if food:
            if food[-1] == ',':
                food = food[:-1]

        # if ends with "and", remove it
        if food:
            if food[-4:] == ' and':
                food = food[:-4]

        food = food.replace('possibly', '')

        df.loc[index, 'Diet'] = re.sub(' +', ' ', food)

    # drop all left food columns
    df = df.drop(['Prey', 'Favorite Food', 'Main Prey',
                 'Diet for this Fish'], axis=1)
    return df


# Nao correr o codigo de novo porque alterei diretamente no output.csv para poupar espaço
"""
df = pd.read_csv('output.csv')
df = drop_columns(df)
df = clean_text(df)
df = join_food_cols(df)
df = df.replace(np.nan, '', regex=True)

# save to csv
df.to_csv('output.csv', index=False)
"""
