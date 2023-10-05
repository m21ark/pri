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
    for i in range(1,200): # TODO: change to len(df[column_name])
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
    if avg:
        return ((float(int1) + float(dec1)) + (float(int2) + float(dec2))) / 2
    else:
        return float(int1) + float(dec1)

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

#clean_df_column(df['Weight'], mapping_weight)
        
# Problemas:
# 108. longer for humans
# 123. 1.16mph


# print(df['Length'][:40])

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

# clean_df_column(df['Length'], mapping_length)

# Problemas:
# 87. 25kg - 48kg
# 108. Varies
# 115. Fish
# 120. Nose to tail length
# 123. 20+ Years

# clean_df_column(df['Height'], mapping_length)

# Problemas:
# 123. Sea Otters, Humans, Larger Fish (Including Larger Char)

# clean_df_column(df['Wingspan'], mapping_length)

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
    (r'\s*\D*(\d+)?(,\d+)?\s*(millions?|thousands?)?\s*(to|-|–)\s*(\d+)?(,\d+)?\s*(millions?|thousands?)?', lambda match: convert_to_unit(match.group(3), match.group(7), match.group(1), match.group(2), match.group(5), match.group(6))),
    (r'\s*([Uu]p to|About|Around|As much as|can be|[Ll]ess than|[Aa]pproximately)\s*(\d+)(,\d+)?\s*(millions?|thousands?)?', lambda match: convert_to_unit(match.group(4), '', match.group(2), match.group(3), 0, 0, False)),
    (r'\s*(\d+)(,\d+)?\s*\+?\s*(millions?|thousands?)?', lambda match: convert_to_unit(match.group(3), '', match.group(1), match.group(2), 0, 0, False)),
]

clean_df_column(df['Average Spawn Size'], mapping_count)

# Problemas:
# 139. Several thousand
# 156. bristly hairs that contain venom
# 172. No
