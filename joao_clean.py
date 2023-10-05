import pandas as pd
import re

# Tarefas: 

# 2 Intervalos
# Lifespan: 2147    ---> Provavelmente fazer parsing de intervalos para valor médio ou converter tudo para uma só unidade
# Weight: 1843
# Length: 1582 
# Height: 617
# Wingspan: 407
# Average Spawn Size: 170
# Estimated Population Size: 946 ----> Soome are in interval, some are numbers, other are just stable. 



# read the output.csv file
df = pd.read_csv('output.csv')


#print(df['Lifespan'][:40])


def clean_df_column(df_col, mapping):
    # mapping is a tuple of (regex, replacement function)
    # replacement function takes a match object and returns the replacement string
    for i in range(50): # TODO: change to len(df[column_name])
        string = str(df_col[i])
        matched = False
        if string != 'nan':
            for regex, replacement in mapping:
                match = re.match(regex, string)
                if match:
                    print(i, 'Matched: ', df_col[i], ' to: ', replacement(match), flush=True)
                    df_col[i] = replacement(match)
                    matched = True
                    break
            if not matched:
                print(i, 'Not Matched: ', string, flush=True)
    
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
    (r'(\d+)\s*\+\s*(year|month|week|day)s?', lambda match: str(int(match.group(1))) + ' ' + match.group(2) + 's'),
    (r'\D*(\d+)\s*(year|month|week|day)s?\D*', lambda match: str(int(match.group(1))) + ' ' + match.group(2) + 's'),  # Watch out with these last ones, since they accept a lot
    (r'(\d+)\s*(to|-|–)\s*(\d+)', lambda match: str(int((int(match.group(1)) + int(match.group(3))) / 2)) + ' years') # Should be the last one
]

# clean_df_column(df['Lifespan'], mapping_lifespan)

# Problemas:
# 5. Several Months
# 20. 23 years in the wild, up to 60 years in captivity
# 24. 6 weeks - 1 year and 144. 3 weeks - I year
# 27. Varies
# 282. Hair
# 298. Unknown
# 349. 0.6 mph
# 382. A few weeks

#print(df['Lifespan'].unique())


# print(df['Weight'][:40])

def getWeight(int1, dec1, int2, dec2, avg = True):
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
    if avg:
        return ((float(int1) + float(dec1)) + (float(int2) + float(dec2))) / 2
    else:
        return float(int1) + float(dec1)

def convert_to_kg(unit, int1, dec1, int2, dec2, avg=True):
    if unit == 'kg' or unit == 'kilograms' or unit == 'kilogram':
        return str(round(getWeight(int1, dec1, int2, dec2, avg), 3)) + ' kg'
    elif unit == 'g':
        return str(round(getWeight(int1, dec1, int2, dec2, avg) * 0.001, 6)) + ' kg'
    elif unit == 'mg':
        return str(round(getWeight(int1, dec1, int2, dec2, avg) * 0.000001, 6)) + ' kg'
    elif unit == 'pounds' or unit == 'lbs' or unit == 'pound' or unit == 'lb':
        return str(round(getWeight(int1, dec1, int2, dec2, avg) * 0.453592, 3)) + ' kg'
    elif unit == 'ounces' or unit == 'ounce' or unit == 'oz':
        return str(round(getWeight(int1, dec1, int2, dec2, avg) * 0.0283495, 6)) + ' kg'
    return '0 kg'


mapping_weight = [
    (r'\s*(\d+)?(.\d+|,\d+)?\s*(kg|kilograms?|g|oz|mg|pounds|lbs|ounces)?\s*(to|-|–)\s*(\d+)?(.\d+|,\d+)?\s*(kg|kilograms?|g|oz|mg|pounds?|lbs?|ounces?)', lambda match: convert_to_kg(match.group(7), match.group(1), match.group(2), match.group(5), match.group(6))),
    (r'\s*([Uu]p to|About|Around|As much as|can be|[Ll]ess than)\s*(\d+)(.\d+|,\d+)?\s*(kg|kilograms?|g|oz|mg|pounds?|lbs?|ounces?)', lambda match: convert_to_kg(match.group(4), match.group(2), match.group(3), 0, 0, False)),
    (r'\s*(\d+)(.\d+|,\d+)?\s*\+?\s*(kg|kilograms?|g|oz|mg|pounds?|lbs?|ounces?)', lambda match: convert_to_kg(match.group(3), match.group(1), match.group(2), 0, 0, False)),

]

#clean_df_column(df['Weight'], mapping_weight)
        
# Problemas:
# 108. longer for humans
# 123. 1.16mph


# print(df['Length'][:40])

mapping_length = [

]

clean_df_column(df['Length'], mapping_length)




