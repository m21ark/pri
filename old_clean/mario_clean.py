import pandas as pd
import numpy as np
import re

df = pd.read_csv('output.csv')


def clean_aggression_groupbehavior_temperament(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function parses the `Agression`, `Group Behavior` and `Temperament` columns
    combining them into a new column `Behavior`, dropping the previous three columns

    Parameters:
    arg1 (pd.DataFrame): dataframe to be processed

    Returns;
    pd.DataFrame: processed dataframe
    """

    if('Aggression' not in df.columns):
        return 'Aggression column not in the df'
    
    if('Temperament' not in df.columns):
        return 'Temperament column not in the df'
    
    if('Group Behavior' not in df.columns):
        return 'Group Behavior column not in the df'

    df_aux = pd.DataFrame()

    df['Aggression'] = df['Aggression'].fillna('')
    df['Group Behavior'] = df['Group Behavior'].fillna('')
    df['Temperament'] = df['Temperament'].fillna('')

    # Aggression
    def parse_aggression(elem):
        if(not elem): return elem

        return f"Their aggression level is {elem.lower()}."

    df['Aggression'] = df['Aggression'].apply(parse_aggression)
    
    # Group Behavior
    def parse_group_behavior(elem):
        if(not elem): return elem

        return '/'.join([sentence.strip().lower() for sentence in elem.split('\n') if sentence.strip()])

    df['Group Behavior'] = df['Group Behavior'].apply(parse_group_behavior)

    are_group = ['social', 'sociable', 'territorial', 'gregarious', 'solitary', 'community-minded', 'subsocial']

    def split_group_behaviors(sentence):
        if(not sentence): return '', ''
        fragments = sentence.split('/')

        are_sentences = []
        other_sentences = []

        for f in fragments:
            if(any(keyword in f for keyword in are_group)):
                are_sentences.append(f)
            else:
                other_sentences.append(f)
        
        return '/'.join(are_sentences) if len(are_sentences) > 0 else '', '/'.join(other_sentences) if len(other_sentences) > 0 else ''

    df_aux[['Group_are', 'Group_live']] = df['Group Behavior'].apply(split_group_behaviors).apply(pd.Series)

    def remove_similar_behaviors(elem):
        if(not elem): return elem

        unique = set([x for x in elem.split('/')])

        if(any(behavior in ['largely solitary', 'mainly solitary'] for behavior in unique)):
            unique.discard('solitary')

        if('solitary except during mating season' in unique):
            unique.discard('solitary')

            if('largely solitary' in unique):
                unique.discard('largely solitary')
                unique = {'largely solitary except during mating season' if x == 'solitary except during mating season' else x for x in unique}
            elif('mainly solitary' in unique):
                unique.discard('mainly solitary')
                unique = {'mainly solitary except during mating season' if x == 'solitary except during mating season' else x for x in unique}

        return '/'.join(unique)

    df_aux['Group_are'] = df_aux['Group_are'].apply(remove_similar_behaviors)

    to_pluralize = [
        "band", "gang", "bloom", "breeding pair", "cluster", "flock", 
        "group", "pair", "legion", "swarm", "shoal", "herd", "smack", 
        "school", "infestation", "pack", "skulk", "sounder", "troop", "pod"]

    to_transform = {
        'colonial nesting': 'colonial nests',
        'colony': 'colonies'
    }
        
    def transform_live_behaviors(elem):
        if(not elem): return ''
        
        transformed = []
        for u in [x for x in elem.split('/')]:
            if u in to_pluralize:
                transformed.append(f'{u}s')
            elif u in to_transform:
                transformed.append(f'{to_transform[u]}')
            else:
                transformed.append(u)
        
        unique = set([x for x in transformed])

        return '/'.join(unique)

    df_aux['Group_live'] = df_aux['Group_live'].apply(transform_live_behaviors)


    def build_sentence_live(elem):
        if(not elem): return elem

        fragments = elem.split('/')

        result = fragments[0]
        for index, fragment in enumerate(fragments[1:]):
            fragment = fragment.strip()
            if(index == len(fragments) - 2):
                result += f' or {fragment}'
            else:
                result += f', {fragment}'

        return f"They usually live in {result}"

    def build_sentence_are(elem):
        if(not elem): return elem

        fragments = elem.split('/')

        result = fragments[0]
        for index, fragment in enumerate(fragments[1:]):
            fragment = fragment.strip()
            if(index == len(fragments) - 2):
                result += f' and {fragment}'
            else:
                result += f', {fragment}'
        
        return f" and can be characterized as {result}."

    def format_sentence(elem):
        if(not elem): return elem
        
        if(elem.split(' ')[1] == "and"):
            return f"They {' '.join(elem.split(' ')[2:])}"
        
        if(elem[-1] != '.'):
            elem += '.'
        return elem

    df_aux['Group_are'] = df_aux['Group_are'].apply(build_sentence_are) 
    df_aux['Group_live'] = df_aux['Group_live'].apply(build_sentence_live)

    df['Group Behavior'] = df_aux['Group_live']  + df_aux['Group_are'] 
    df['Group Behavior'] = df['Group Behavior'].apply(format_sentence)

    # Temperament

    def custom_split(text):
        if (not text): return ''

        sentences = text.split('.')
        result = []
        for sentence in sentences:
            fragments = [fragment.strip() for fragment in re.split(r'[.;,]|and ', sentence)]
            result.extend(fragments)
        return '/'.join(result)

    df['Temperament'] = df['Temperament'].apply(custom_split)
    df['Temperament'] = df['Temperament'].str.lower()
    df['Temperament'] = df['Temperament'].str.replace(r'/+', '/', regex=True).str.strip('/')
    df['Temperament'] = df['Temperament'].str\
        .replace(r'\bthey are \b|\bcan be \b|\b hens\b|\b roosters\b|\bswedish elkhounds are \b|\bwelsh black cattle are \b|\bthey \b'\
                , '', regex=True)

    def custom_join(text):
        if(not text): return ''
        fragments = text.split('/')

        result = fragments[0]
        for index, fragment in enumerate(fragments[1:]):
            fragment = fragment.strip()
            if fragment.startswith(('but ', 'except ', 'yet ')):
                result += f' {fragment}'
            else:
                if(index == len(fragments) - 2):
                    result += f' and {fragment}'
                else:
                    result += f', {fragment}'
                

        return f' Their temperament can be characterized as {result}.'

    df['Temperament'] = df['Temperament'].apply(custom_join)


    # Joinning
    df['Behavior'] = df['Group Behavior'] + df['Temperament'] + df['Aggression']
    df['Behavior'] = df['Behavior'].str.strip()

    df = df.drop(columns=['Group Behavior', 'Temperament', 'Aggression'], axis=1)

    return df

def clean_topspeed(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function parses the `Top Speed` column, converting the values from `mp/h` to `km/h`
    and negative values to positives. The result is present in the same column `Top Speed`

    Parameters:
    arg1 (pd.DataFrame): dataframe to be processed

    Returns;
    pd.DataFrame: processed dataframe
    """
    df['Top Speed'] = df['Top Speed'].fillna('0 mph')

    def convert_mph_to_kmh(mph_value):
        # Extract the numerical value (x) from the mph string
        mph = float(mph_value.split(" ")[0])
        # Convert mph to km/h (1 mph = 1.60934 km/h)
        kmh = mph * 1.60934
        return abs(kmh)

    df['Top Speed'] = df['Top Speed'].apply(convert_mph_to_kmh)
    return df

def clean_color_skintype(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function parses the `Color` and `Skin Type` columns
    combining them into a new column `Body`, dropping the previous two columns

    Parameters:
    arg1 (pd.DataFrame): dataframe to be processed

    Returns;
    pd.DataFrame: processed dataframe
    """

    df['Skin Type'] = df['Skin Type'].fillna('')
    df['Color'] = df['Color'].fillna('')

    df['Skin Type'] = df['Skin Type'].str.lower()

    skin_type_is = ['permeable', 'leather', 'smooth', 'rough', 'tough', 'porous', 'spiky']

    skin_type_has = {
        'exoskeleton': 'an exoskeleton',
        'shell': 'a shell',
        'hard outer shell': 'a hard outer shell',
        'hard shell': 'a hard shell',
    }

    def transform_skin_type(elem):
        if(not elem): return elem

        if elem in skin_type_is:
            return f"This animal's skin is {elem}."
        
        if elem in skin_type_has:
            return f"This animal has {skin_type_has[elem]}."
        
        return f"This animal has {elem}."
        

    df['Skin Type'] = df['Skin Type'].apply(transform_skin_type)


    df['Color'] = df['Color'].str.replace(r'\s+', '/', regex=True)

    def remove_duplicates_colours(elem):
        if(not elem): return elem

        return '/'.join([x for x in set(elem.split('/')) if pd.notna(elem)])

    df['Color'] = df['Color'].apply(remove_duplicates_colours)

    df['Color'] = df['Color'].str.replace(r'.*Multi-colored.*', 'Multi-colored', regex=True).str.lower()

    def build_sentence_body_color(elem):
        if(not elem): return elem

        fragments = elem.split('/')

        result = fragments[0]
        for index, fragment in enumerate(fragments[1:]):
            fragment = fragment.strip()

            if(index == len(fragments) - 2):
                result += f' and {fragment}'
            else:
                result += f', {fragment}'
                

        return f"Its body can be {result}."

    df['Color'] = df['Color'].apply(build_sentence_body_color)

    df['Body'] = df['Skin Type'] + df['Color']
    df['Body'] = df['Body'].apply(lambda x: None if pd.isna(x) else (f"This animal's{x[3:]}" if x.split(' ')[0] == 'Its' else x))

    df = df.drop(columns=['Color', 'Skin Type'], axis=1)

    return df

def clean_habitat_nestingplace(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function parses the `Habitat` and `Nesting Location` columns
    combining them into a new column `Natural Habitat`, dropping the previous two columns

    Parameters:
    arg1 (pd.DataFrame): dataframe to be processed

    Returns;
    pd.DataFrame: processed dataframe
    """
    df['Nesting Location'] = df['Nesting Location'].fillna('')
    df['Natural Habitat'] = df['Habitat'].fillna(df['Nesting Location']).str.lower()


    def format_habitat(elem):
        if(not elem): return elem

        items = re.split(r', | and ', elem)
        result = items[0]

        for index, item in enumerate(items[1:]):
            if(index == len(items) - 2):
                result += f' and {item}'
            else:
                result += f', {item}'

        return f"This animal's natural habitat is {result}."

    df['Natural Habitat'] = df['Natural Habitat'].apply(format_habitat)

    df = df.drop(columns=['Habitat', 'Nesting Location'], axis=1)

    return df

def clean_lifestyle(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function parses the `Lifestyle` column

    Parameters:
    arg1 (pd.DataFrame): dataframe to be processed

    Returns;
    pd.DataFrame: processed dataframe
    """
    df['Lifestyle'] = df['Lifestyle'].fillna('')
    
    df['Lifestyle'] = df['Lifestyle'].str.replace(r'\s+', '/', regex=True).str.lower()

    lifestyle_keywords = ["region", "animal", "constant", "or", "and", "on", "day", "night", "region", "depending"]

    def remove_lifestyle_keywords(row):
        if(not row): return row
        words = row.split('/')

        filtered_words = [word for word in words if word not in lifestyle_keywords]
        return '/'.join(set(filtered_words))

    # Apply the custom function to the DataFrame column
    df['Lifestyle'] = df['Lifestyle'].apply(remove_lifestyle_keywords)

    def build_sentence_lifestyle(elem):
        if(not elem): return elem

        items = elem.split('/')
        result = items[0]

        for index, item in enumerate(items[1:]):
            if(index == len(items)-2):
                result += " and " + item
            else:
                result += ", " + item

        return f"It has a {result} lifestyle."

    df['Lifestyle'] = df['Lifestyle'].apply(build_sentence_lifestyle)

    return df

df = clean_aggression_groupbehavior_temperament(df)

df = clean_topspeed(df)

df = clean_color_skintype(df)

df = clean_habitat_nestingplace(df)

df = clean_lifestyle(df)

save_columns = ['Name', 'Behavior', 'Top Speed', 'Body', 'Natural Habitat', 'Lifestyle']

df[save_columns].to_csv('output_mario.csv', index=False)
