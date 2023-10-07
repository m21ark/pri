import pandas as pd
import numpy as np
import re


df = pd.read_csv('output.csv')


def clean_text():
    global df
    # if NaN, replace with empty string
    df = df.replace(np.nan, '', regex=True)

    # remove all quotes, \n, and trailing spaces
    df = df.replace(r'\"', '', regex=True)
    df = df.replace('"', '', regex=False)
    df = df.replace(r'\n', '', regex=True)
    df = df.replace(r'\s+$', '', regex=True)

    return df



def drop_columns():
    global df
    try:
        df = df.drop(['Group', 'Average Litter Size', 'Litter Size'
                    'Training', 'Number Of Species'], axis=1)
    except:
        # It was already cleaned previously
        print('Columns already dropped')
        pass
    return df



def join_food_cols(df):
    food_columns = ['Diet', 'Diet for this Fish', 'Prey', 'Favorite Food',
                    'Main Prey']
    
    # Check if the columns exist
    for col in food_columns:
        if col not in df.columns:
            print('Column ' + col + ' does not exist')
            return df

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


def clean_ph():
    global df

    # Try to join the 2 collumns together
    try:
        df['Optimum pH Level'] = df['Optimum pH Level'].fillna(df['Optimum PH Level'])
        df = df.drop(['Optimum PH Level'], axis=1)
    except:
        # It was already cleaned previously
        print('Optimum PH Level already cleaned')
        pass
    

def clean_feature():
    global df

    try:
        # Concatenate the features 'Most Distinctive Feature', 'Feature' and 'Special Features'
        df['Most Distinctive Feature'] = df['Most Distinctive Feature'].fillna(df['Distinctive Feature'])
        df['Most Distinctive Feature'] = df['Most Distinctive Feature'].fillna(df['Special Features'])
        
        df['Features'] = df['Most Distinctive Feature']
        # Concatenate the strings if both objects have the same features ... A lot of repetition
        # df['Features'] = df[['Most Distinctive Feature', 'Distinctive Feature', 'Special Features']].apply(lambda x: '. '.join(x.dropna().astype(str)), axis=1)
        
        # Drop the original columns
        df = df.drop(['Distinctive Feature', 'Special Features', 'Most Distinctive Feature'], axis=1)
    except:
        # It was already cleaned previously
        print('Features already cleaned')
        pass

    

def clean_location():
    global df
    #if location is Sub-Saharan Africa change to sub-Saharan Africa
    df['Location'] = df['Location'].str.replace('Sub-Saharan Africa', 'sub-Saharan Africa') 

    # should we do this ???? TODO
    #df['Location'] = df['Location'].fillna(df['Origin'])


def clean_names(): 
    global df

    try:
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
        

        # drop the Common Name column
        df = df.drop(['Common Name'], axis=1)
    except:
        # It was already cleaned previously
        print('Names already cleaned')
        pass



def clean_slogan():
    global df

    try:
        df['Fun Fact'] = df['Fun Fact'].fillna(df['Slogan'].fillna(df['Quote']))

        # drop the slogan column and Quote column
        df = df.drop(['Slogan', 'Quote'], axis=1)
    except:
        # It was already cleaned previously
        print('Slogan already cleaned')
        pass


def clean_migratory():
    global df

    # Replace all nan with 0
    df['Migratory'] = df['Migratory'].fillna(0)


def clean_venomous():
    global df

    # Replace all nan with 0
    df['Venomous'] = df['Venomous'].fillna(0)

    df['Venomous'] = df['Venomous'].replace('Yes', 1)
    df['Venomous'] = df['Venomous'].replace('No', 0)



# ==================================================== Interval Cleaning ====================================================

# For a given dataframe column, clean the intervals using the mapping regexes. It also clears the ones that 
def clean_interval(df_col, mapping, regex_l=[]):
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
                # print(i, 'Not Matched: ', string, flush=True)

                for x in regex_l:
                    #match = re.findall(x, string)
                    if x in string:
                       df_col[i] = ''
                       print(i, 'Matched AS OUTLIER', flush=True)
                       break

                list_of_not_matched.append(string)

    #print(list_of_not_matched)


def getValue(int1, dec1, int2, dec2, avg = True):
    if int1 == None:
        int1 = 0
    if int2 == None:
        int2 = 0
    if dec1 == None:
        dec1 = 0
    if dec2 == None:
        dec2 = 0
    if str(dec1).startswith(','):
        int1 = str(int1) + str(dec1)[1:]
        dec1 = 0
    if str(dec2).startswith(','):
        int2 = str(int2) + str(dec2)[1:]
        dec2 = 0
    if str(dec1).startswith('/'):
        int1 = float(int1) / float(str(dec1)[1:])
        dec1 = 0
    if str(dec2).startswith('/'):
        print('Print: ', int2, '/', dec2)
        int2 = float(int2) / float(str(dec2)[1:])
        dec2 = 0
    if avg:
        return ((float(int1) + float(dec1)) + (float(int2) + float(dec2))) / 2
    else:
        return float(int1) + float(dec1)
    

regex_l = [
    'lbs', 'mph', ' ft ', 'cm', 'kg', 'inches', 'feet', 'pounds', 'miles per hour', 'centimeters', 'ounces'
]

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


def convert_to_kg(unit, int1, dec1, int2, dec2, avg=True):
    if unit == 'kg' or unit == 'kilograms' or unit == 'kilogram':
        return str(round(getValue(int1, dec1, int2, dec2, avg), 3)) + ' kg'
    elif unit == 'g':
        return str(round(getValue(int1, dec1, int2, dec2, avg) * 0.001, 6)) + ' kg'
    elif unit == 'mg':
        return str(round(getValue(int1, dec1, int2, dec2, avg) * 0.000001, 6)) + ' kg'
    elif unit == 'pounds' or unit == 'lbs' or unit == 'pound' or unit == 'lb':
        return str(round(getValue(int1, dec1, int2, dec2, avg) * 0.453592, 3)) + ' kg'
    elif unit == 'ounces' or unit == 'ounce' or unit == 'oz':
        return str(round(getValue(int1, dec1, int2, dec2, avg) * 0.0283495, 6)) + ' kg'
    return '0 kg'


mapping_weight = [
    (r'\s*(\d+)?(.\d+|,\d+)?\s*(kg|kilograms?|g|oz|mg|pounds|lbs|ounces)?\s*(to|-|–)\s*(\d+)?(.\d+|,\d+)?\s*(kg|kilograms?|g|oz|mg|pounds?|lbs?|ounces?)', lambda match: convert_to_kg(match.group(7), match.group(1), match.group(2), match.group(5), match.group(6))),
    (r'\s*([Uu]p to|About|Around|As much as|can be|[Ll]ess than|[Aa]pproximately)\s*(\d+)(.\d+|,\d+)?\s*(kg|kilograms?|g|oz|mg|pounds?|lbs?|ounces?)', lambda match: convert_to_kg(match.group(4), match.group(2), match.group(3), 0, 0, False)),
    (r'\s*(\d+)(.\d+|,\d+)?\s*\+?\s*(kg|kilograms?|g|oz|mg|pounds?|lbs?|ounces?)', lambda match: convert_to_kg(match.group(3), match.group(1), match.group(2), 0, 0, False)),
]



def convert_to_m(unit, int1, dec1, int2, dec2, avg=True):
    if unit == 'm' or unit == 'meters' or unit == 'meter':
        return str(round(getValue(int1, dec1, int2, dec2, avg), 3)) + ' m'
    elif unit == 'cm' or unit == 'centimeters' or unit == 'centimeter':
        return str(round(getValue(int1, dec1, int2, dec2, avg) * 0.01, 6)) + ' m'
    elif unit == 'ft' or unit == 'feet' or unit == 'foot':
        return str(round(getValue(int1, dec1, int2, dec2, avg) * 0.3048, 3)) + ' m'
    elif unit == 'in' or unit == 'inches' or unit == 'inch':
        return str(round(getValue(int1, dec1, int2, dec2, avg) * 0.0254, 6)) + ' m'
    return '0 m'

mapping_length = [
    (r'\s*\D*(\d+)?(.\d+|,\d+)?\s*(m|meters?|cm|centimeters?|ft|foot|feet|in|inch|inches)?\s*(to|-|–)\s*(\d+)?(.\d+|,\d+)?\s*(m|meters?|cm|centimeters?|ft|foot|feet|in|inch|inches)', lambda match: convert_to_m(match.group(7), match.group(1), match.group(2), match.group(5), match.group(6))),
    (r'\s*([Uu]p to|About|Around|As much as|can be|[Ll]ess than|[Aa]pproximately)\s*(\d+)(.\d+|,\d+)?\s*(m|meters?|cm|centimeters?|ft|foot|feet|in|inch|inches)', lambda match: convert_to_m(match.group(4), match.group(2), match.group(3), 0, 0, False)),
    (r'\s*(\d+)(.\d+|,\d+)?\s*\+?\s*(m|meters?|cm|centimeters?|ft|foot|feet|in|inch|inches)', lambda match: convert_to_m(match.group(3), match.group(1), match.group(2), 0, 0, False)),
]



def convert_to_unit(unit1, unit2, int1, dec1, int2, dec2, avg=True):
    value1 = 0
    value2 = 0
    if unit1 == 'million' or unit1 == 'millions':
        value1 = getValue(int1, dec1, 0, 0, False) * 1000000
    elif unit1 == 'thousand' or unit1 == 'thousands':
        value1 = getValue(int1, dec1, 0, 0, False) * 1000
    else:
        value1 = getValue(int1, dec1, 0, 0, False)

    if avg:
        if unit2 == 'million' or unit2 == 'millions':
            value2 = getValue(int2, dec2, 0, 0, False) * 1000000
        elif unit2 == 'thousand' or unit2 == 'thousands':
            value2 = getValue(int2, dec2, 0, 0, False) * 1000
        else:
            value2 = getValue(int2, dec2,0 ,0 ,False)
        return str(round((value1 + value2) / 2, 0))
    
    else:
        return str(round(value1, 0))


mapping_count = [
    (r'\s*(\d+)?(.\d+|,\d+)?\s*(millions?|thousands?)?\s*(to|-|–)\s*(\d+)?(.\d+|,\d+)?\s*(millions?|thousands?)?', lambda match: convert_to_unit(match.group(3), match.group(7), match.group(1), match.group(2), match.group(5), match.group(6))),
    (r'\s*([Uu]p to|About|Around|As much as|can be|[Ll]ess than|[Mm]ore than|[Aa]pproximately)\s*(\d+)(.\d+|,\d+)?\s*(millions?|thousands?)?', lambda match: convert_to_unit(match.group(4), '', match.group(2), match.group(3), 0, 0, False)),
    (r'\s*(\d+)(.\d+|,\d+)?\s*\+?\s*(millions?|thousands?)?', lambda match: convert_to_unit(match.group(3), '', match.group(1), match.group(2), 0, 0, False)),
]


clean_text()
drop_columns()

join_food_cols(df)

clean_ph()
clean_feature()
clean_location()
clean_names()
clean_slogan()
clean_migratory()
clean_venomous()

clean_interval(df['Age of Sexual Maturity'], mapping_lifespan)

clean_interval(df['Age of Weaning'], mapping_lifespan, regex_l)
clean_interval(df['Age Of Independence'], mapping_lifespan, regex_l)
clean_interval(df['Age of Molting'], mapping_lifespan, regex_l)
clean_interval(df['Age Of Fledgling'], mapping_lifespan, regex_l)
clean_interval(df['Gestation Period'], mapping_lifespan, regex_l)
clean_interval(df['Incubation Period'], mapping_lifespan, regex_l)

clean_interval(df['Lifespan'], mapping_lifespan)
clean_interval(df['Weight'], mapping_weight)
clean_interval(df['Length'], mapping_length)
clean_interval(df['Height'], mapping_length)
clean_interval(df['Wingspan'], mapping_length)
clean_interval(df['Average Spawn Size'], mapping_count)
clean_interval(df['Estimated Population Size'], mapping_count)

# When you want to save it all to the file
# df.to_csv('output_clean.csv', index=False)



# Problemas Average Lifespan:
# 5. Several Months
# 20. 23 years in the wild, up to 60 years in captivity
# 24. 6 weeks - 1 year and 144. 3 weeks - I year
# 27. Varies
# 282. Hair
# 298. Unknown
# 349. 0.6 mph
# 382. A few weeks

# Problemas Weight:
# 108. longer for humans
# 123. 1.16mph

# Problemas Length:
# 87. 25kg - 48kg
# 108. Varies
# 115. Fish
# 120. Nose to tail length
# 123. 20+ Years

# Problemas Height:
# 123. Sea Otters, Humans, Larger Fish (Including Larger Char)

# Problemas Average Spawn Size:
# 139. Several thousand
# 156. bristly hairs that contain venom
# 172. No

# Problemas Estimated population size:
# 15. and 16. Abundant
# 90. 20,700 metric tons
# 123. Artic char is the northern-most fish
# 174. Millions. Conservation status of many of these geckos is least concern
