import sqlite3
import pandas as pd


DB_FILEPATH = 'rpg_db.sqlite3'

conn = sqlite3.connect(DB_FILEPATH)

cursor = conn.cursor()

total_characters = '''
SELECT
    COUNT(character_id) as Character_Count
FROM
    charactercreator_character
'''

def make_query(query, cursor):

    result = cursor.execute(query).fetchall()

    # get columns from cursor object
    columns = list(map(lambda x: x[0], cursor.description))

    # assign to dataframe
    df = pd.DataFrame(data=result, columns=columns)

    print(df)

# How many total characters
make_query(total_characters, cursor)

# How many of each class
class_tables = [
    'cleric',
    'fighter',
    'mage',
    'necromancer',
    'thief'
]

for character_class in class_tables:

    total_classes = f'''
    SELECT
        COUNT(*) as {character_class.capitalize()}_Count
    FROM
        charactercreator_{character_class}
    '''

    make_query(total_classes, cursor)

# How many total Items
item_count = '''
SELECT
    COUNT(item_id) as Item_Count
FROM
    armory_item
'''

make_query(item_count, cursor)