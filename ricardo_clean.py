import pandas as pd
import numpy as np


df = pd.read_csv('output.csv')

#print(df['Age of Sexual Maturity'])

#def clean_intervals_features(df):



## join the 2 collumns together
# df['Optimum pH Level'] = df['Optimum pH Level'].fillna(df['Optimum PH Level'])
# print(df['Optimum pH Level'].unique())
# 
# 
# df = df.drop(['Optimum PH Level'], axis=1)


# print(df['Litter Size']) .... what


# Concatenate the features 'Most Distinctive Feature', 'Feature' and 'Special Features'
# df['Most Distinctive Feature'] = df['Most Distinctive Feature'].fillna(df['Distinctive Feature'])
# df['Most Distinctive Feature'] = df['Most Distinctive Feature'].fillna(df['Special Features'])
# 
# df['Features'] = df['Most Distinctive Feature']
# # Concatenate the strings if both objects have the same features ... A lot of repetition
# # df['Features'] = df[['Most Distinctive Feature', 'Distinctive Feature', 'Special Features']].apply(lambda x: '. '.join(x.dropna().astype(str)), axis=1)
# 
# # Drop the original columns
# df = df.drop(['Distinctive Feature', 'Special Features', 'Most Distinctive Feature'], axis=1)
# 

# print(df['Most Distinctive Feature'].unique())
# 

#if location is Sub-Saharan Africa change to sub-Saharan Africa
#df['Location'] = df['Location'].str.replace('Sub-Saharan Africa', 'sub-Saharan Africa') 

# Urgente FALAR SOBRE VALORES ERRADOS principalmente na location
# chat gpt ajuda a encontrar erros

#df.to_csv('output.csv', index=False)

