import pandas as pd
import numpy as np
import re


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

    # should we do this ????
    #df['Location'] = df['Location'].fillna(df['Origin'])

    print(len(df['Location'].unique()))

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

#clean_names()

def clean_slogan():
    global df
    # print all the slogans that also have a fun fact
    # print(df[df['Slogan'].notnull() & df['Fun Fact'].notnull()]['Slogan'].unique())
    # print(df[df['Slogan'].notnull() & df['Fun Fact'].notnull()]['Fun Fact'].unique())

    # print len of slogan
    df['Fun Fact'] = df['Fun Fact'].fillna(df['Slogan'].fillna(df['Quote']))

    #print(df['Quote'].unique())
    #print(len(df['Fun Fact'].unique()))
    #print(len(df['Fun Fact'].fillna(df['Slogan'].fillna(df['Quote'])).unique()))


    # drop the slogan column and Quote column
    df = df.drop(['Slogan', 'Quote'], axis=1)


def clean_interval(df_col, mapping):
    # mapping is a tuple of (regex, replacement function)
    # replacement function takes a match object and returns the replacement string
    list_of_not_matched = []
    # r'(\d+)\s*(lbs|mph|ft|in|cm|kg)s?',
    # r'(\d+)\s*(to|-|–)\s*(\d+)\s*(lbs|mph|ft|in|cm|kg)s?',
    # r'(\d+)\s*(to|-|–)\s*(\d+)\s*(to|-|–)\s*(\d+)\s*(lbs|mph|ft|in|cm|kg)s?',
    # r'(\d+)\s*(to|-|–)\s*(\d+)\s*(to|-|–)\s*(\d+)\s*(to|-|–)\s*(\d+)\s*(lbs|mph|ft|in|cm|kg)s?',
    # r'(\d+)\s*(to|-|–)\s*(\d+)\s*(to|-|–)\s*(\d+)\s*(to|-|–)\s*(\d+)\s*(to|-|–)\s*(\d+)\s*(lbs|mph|ft|in|cm|kg)s?',
    # r'\b(?:inches)\b',
    # r'\b(?:feet)\b',
    # r'\b(?:pounds)\b',
    # r'\b(?:miles per hour)\b',
    # r'\b(?:centimeters)\b',
    #regex that identifies lbs mph and ft etc
    regex_l = [
        'lbs', 'mph', ' ft ', 'cm', 'kg', 'inches', 'feet', 'pounds', 'miles per hour', 'centimeters', 'ounces'

        ]

    for i in range(0, len(df_col)): # TODO: change to len(df[column_name])
        string = str(df_col[i])
        matched = False
        if string != 'nan':
            for regex, replacement in mapping:
                match = re.match(regex, string)
                if match:
                    # print(i, 'Matched: ', df_col[i], ' to: ', replacement(match), flush=True)
                    df_col[i] = replacement(match)
                    matched = True
                    break
            if not matched:
                print(i, 'Not Matched: ', string, flush=True)

                for x in regex_l:
                   #match = re.findall(x, string)
                   if x in string:
                       df_col[i] = ''
                       print(i, 'Matched AS OUTLIER', flush=True)
                       break

                

                list_of_not_matched.append(string)

    #print(list_of_not_matched)
    
    return df

mapping_lifespan = [
    (r'\D*(\d+)(.\d+)?\s*(to|-|–)\s*(\d+)(.\d+)?\s*years?', lambda match: str(int((int(match.group(1)) + int(match.group(4))) / 2)) + ' years'), # These 4 can simplified, but wait for later decisions
    (r'\D*(\d+)(.\d+)?\s*(to|-|–)\s*(\d+)(.\d+)?\s*months?', lambda match: str(int((int(match.group(1)) + int(match.group(4))) / 2)) + ' months'),
    (r'\D*(\d+)(.\d+)?\s*(to|-|–)\s*(\d+)(.\d+)?\s*days?', lambda match: str(int((int(match.group(1)) + int(match.group(4))) / 2)) + ' days'),
    (r'\D*(\d+)(.\d+)?\s*(to|-|–)\s*(\d+)(.\d+)?\s*weeks?', lambda match: str(int((int(match.group(1)) + int(match.group(4))) / 2)) + ' weeks'),
    (r'(\d+)\s*(year|month|week|day)s?\s*(to|-|–)\s*(\d+)\s*(year|month|week|day)s?', lambda match: str(int((int(match.group(1)) + int(match.group(4))) / 2)) + ' ' + match.group(2) + 's'),
    (r'(U|u)p\s*to\s*(\d+)\s*years?', lambda match: str(int(match.group(2))) + ' years'),
    (r'(U|u)p\s*to\s*one\s*year', lambda match: '1 years'),
    (r'(About|Around) one year', lambda match: '1 years'),
    (r'(Females|Males)\s*:?\s*(\d+)\s*(year|month|week|day)s?\s*\|\s*(Females|Males)\s*:?\s*(\d+)\s*(year|month|week|day)s?', lambda match: str(int((int(match.group(2)) + int(match.group(5))) / 2)) + ' ' + match.group(3) + 's'),
    (r'(More than|As long as|can be|About|Around)\s*(\d+)\s*(\+?)\s*(year|month|week|day)s?', lambda match: str(int(match.group(2))) + ' ' + match.group(4)+ 's'),
    (r'One (year|month|week|day|Year)s?', lambda match: '1 years'),
    (r'(one|two|five) (year|month|week|day)s?', lambda match: '1 years'),
    (r'(\d+)\s*\+\s*(year|month|week|day)s?', lambda match: str(int(match.group(1))) + ' ' + match.group(2) + 's'),
    (r'\D*(\d+)\s*(year|month|week|day)s?\D*', lambda match: str(int(match.group(1))) + ' ' + match.group(2) + 's'),  # Watch out with these last ones, since they accept a lot
    (r'(\d+)\s*(to|-|–)\s*(\d+)', lambda match: str(int((int(match.group(1)) + int(match.group(3))) / 2)) + ' years') # Should be the last one

]

#clean_location()
#clean_slogan()

print(len(df['Age of Sexual Maturity'].unique()))

#clean_interval(df['Age of Sexual Maturity'], mapping_lifespan)

clean_interval(df['Age of Weaning'], mapping_lifespan)
clean_interval(df['Age Of Independence'], mapping_lifespan)
clean_interval(df['Age of Molting'], mapping_lifespan)
clean_interval(df['Age Of Fledgling'], mapping_lifespan)
clean_interval(df['Gestation Period'], mapping_lifespan)
clean_interval(df['Incubation Period'], mapping_lifespan)


#df.to_csv('output.csv', index=False)

