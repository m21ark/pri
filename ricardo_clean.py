import pandas as pd
import numpy as np


df = pd.read_csv('output.csv')

#print(df['Age of Sexual Maturity'])

#def clean_intervals_features(df):

def clean_ph():
    global df

    ## join the 2 collumns together
    df['Optimum pH Level'] = df['Optimum pH Level'].fillna(df['Optimum PH Level'])
    #print(df['Optimum pH Level'].unique())
    
    
    df = df.drop(['Optimum PH Level'], axis=1)


# print(df['Litter Size']) .... what

def clean_feature():
    global df

    # Concatenate the features 'Most Distinctive Feature', 'Feature' and 'Special Features'
    df['Most Distinctive Feature'] = df['Most Distinctive Feature'].fillna(df['Distinctive Feature'])
    df['Most Distinctive Feature'] = df['Most Distinctive Feature'].fillna(df['Special Features'])
    
    df['Features'] = df['Most Distinctive Feature']
    # Concatenate the strings if both objects have the same features ... A lot of repetition
    # df['Features'] = df[['Most Distinctive Feature', 'Distinctive Feature', 'Special Features']].apply(lambda x: '. '.join(x.dropna().astype(str)), axis=1)
    
    # Drop the original columns
    df = df.drop(['Distinctive Feature', 'Special Features', 'Most Distinctive Feature'], axis=1)
    

def clean_location():
    #if location is Sub-Saharan Africa change to sub-Saharan Africa
    df['Location'] = df['Location'].str.replace('Sub-Saharan Africa', 'sub-Saharan Africa') 

def clean_names(): 
    global df
    # Urgente FALAR SOBRE VALORES ERRADOS principalmente na location
    # chat gpt ajuda a encontrar erros  

    #print every unique value of Other Name(s) that is contained in Common Name
    #print(df[df['Other Name(s)'].isin(df['Common Name'])]['Other Name(s)'].unique())

    x = df[df['Common Name'].isin(df['Other Name(s)'])]['Other Name(s)'].unique()

    # replace all the values on x for a empty string
    df['Common Name'] = df['Common Name'].replace(x, '')

    #df['Other Name(s)'] = df['Other Name(s)'].fillna(df['Common Name'])
    #print(df['Other Name(s)'].unique())

    #replace all nan with the empty string
    df['Other Name(s)'] = df['Other Name(s)'].fillna('')
    df['Common Name'] = df['Common Name'].fillna('')


    df['Other Name(s)'] = df['Other Name(s)'].astype(str) + ', ' + df['Common Name'].astype(str)
    # df['Other Name(s)'] = df['Other Name(s)'].fillna(df['Common Name']).fillna(df['Other Name(s)']).astype(str) + ', ' + df['Other Name(s)'].fillna('').astype(str)


    # take all the ' ' from the end and start of the string
    df['Other Name(s)'] = df['Other Name(s)'].str.strip(' ')
    # take all the ',' from the end and start of the string
    df['Other Name(s)'] = df['Other Name(s)'].str.strip(',')
    print(df['Other Name(s)'].unique())
    

    # drop the Common Name column
    df = df.drop(['Common Name'], axis=1)

    print(len(df['Other Name(s)'].unique()))

clean_names()

# print all the slogans that also have a fun fact
#print(df[df['Slogan'].notnull() & df['Fun Fact'].notnull()]['Slogan'].unique())
#print(df[df['Slogan'].notnull() & df['Fun Fact'].notnull()]['Fun Fact'].unique())

df.to_csv('output.csv', index=False)

