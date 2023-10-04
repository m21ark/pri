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

# print the unique values of the column Lifespan
#print(df['Lifespan'][:40])


def clean_df_column(df_col, mapping):
    # mapping is a tuple of (regex, replacement function)
    # replacement function takes a match object and returns the replacement string
    for i in range(200): # TODO: change to len(df[column_name])
        string = str(df_col[i])
        matched = False
        if string != 'nan':
            for regex, replacement in mapping:
                match = re.match(regex, string)
                if match:
                    print(i, 'Matched: ', df_col[i], ' to: ', replacement(match))
                    df_col[i] = replacement(match)
                    matched = True
                    break
            if not matched:
                print(i, 'Not Matched: ', string)
    
    return df

mapping_lifespan = [
    (r'(\d+)\s*(to|-|–)\s*(\d+)\s*years', lambda match: str(int((int(match.group(1)) + int(match.group(3))) / 2)) + ' years'), # These 4 can simplified, but wait for later decisions
    (r'(\d+)\s*(to|-|–)\s*(\d+)\s*months', lambda match: str(int((int(match.group(1)) + int(match.group(3))) / 2)) + ' months'),
    (r'(\d+)\s*(to|-|–)\s*(\d+)\s*days', lambda match: str(int((int(match.group(1)) + int(match.group(3))) / 2)) + ' days'),
    (r'(\d+)\s*(to|-|–)\s*(\d+)\s*weeks', lambda match: str(int((int(match.group(1)) + int(match.group(3))) / 2)) + ' weeks'),
    (r'(\d+)\s*(years|months|weeks|days)\s*(to|-|–)\s*(\d+)\s*(years|months|weeks|days)', lambda match: str(int((int(match.group(1)) + int(match.group(4))) / 2)) + ' ' + match.group(2)),
    (r'(U|u)p\s*to\s*(\d+)\s*years', lambda match: str(int(match.group(2))) + ' years'),
    (r'(U|u)p\s*to\s*one\s*year', lambda match: '1 years'),
    (r'(As long as|can be|About|Around)\s*(\d+)\s*(\+?)\s*(years|months|weeks|days)', lambda match: str(int(match.group(2))) + ' ' + match.group(4)),
    (r'(\d+)\s*\+\s*(years|months|weeks|days)', lambda match: str(int(match.group(1))) + ' ' + match.group(2)),
    (r'(\d+)\s*(to|-|–)\s*(\d+)', lambda match: str(int((int(match.group(1)) + int(match.group(3))) / 2)) + ' years') # Should be last one
]

clean_df_column(df['Lifespan'], mapping_lifespan)

# Problemas:
# 144. 3 weeks - I year


        
        



#print(df['Lifespan'].unique())

