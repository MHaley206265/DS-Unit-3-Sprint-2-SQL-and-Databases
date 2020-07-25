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

# How many are weapons, how many are not
weapon_count = '''
SELECT
	COUNT(ai.item_id) AS Total_Item_Count,
	COUNT(aw.item_ptr_id) AS Weapon_Count,
	(COUNT(ai.item_id) - COUNT(aw.item_ptr_id)) AS Items_Not_Weapon
FROM
	armory_item AS ai
LEFT JOIN
	armory_weapon AS aw
ON
	ai.item_id = aw.item_ptr_id
'''

make_query(weapon_count, cursor)

# How many items does each character have (first 20 results)
inventory_count = '''
SELECT
	cc.name,
	COUNT(cci.item_id) AS Item_Count
FROM
	charactercreator_character_inventory AS cci
LEFT JOIN
	charactercreator_character AS cc
ON
	cci.character_id = cc.character_id
GROUP BY
	cci.character_id
ORDER BY
	Item_Count DESC
LIMIT
    20
'''

make_query(inventory_count, cursor)

# how many weapons does each character have(first 20)
char_weapon_count = '''
SELECT
	cc.name,
	COUNT(aw.item_ptr_id) AS Weapon_Count
FROM
	charactercreator_character_inventory AS cci
LEFT JOIN
	charactercreator_character AS cc
ON
	cci.character_id = cc.character_id
LEFT JOIN
    armory_weapon AS aw
ON
    cci.item_id = aw.item_ptr_id
GROUP BY
	cci.character_id
ORDER BY
	Weapon_Count DESC
LIMIT
    20
'''

make_query(char_weapon_count, cursor)

# Average number of items
average_items = '''
SELECT
    AVG(Item_Count) AS Average_Item_Count
FROM (
    SELECT
        cc.name,
        COUNT(cci.item_id) AS Item_Count
    FROM
        charactercreator_character_inventory AS cci
    LEFT JOIN
        charactercreator_character AS cc
    ON
        cci.character_id = cc.character_id
    GROUP BY
        cci.character_id
    ORDER BY
        Item_Count DESC
);
'''
make_query(average_items, cursor)

# Average number of weapons
average_weapons = '''
SELECT
	AVG(Weapon_Count) as Average_Weapon_Count
FROM (
	SELECT
		cc.name,
		COUNT(aw.item_ptr_id) AS Weapon_Count
	FROM
		charactercreator_character_inventory AS cci
	LEFT JOIN
		charactercreator_character AS cc
	ON
		cci.character_id = cc.character_id
	LEFT JOIN
	    armory_weapon AS aw
	ON
	    cci.item_id = aw.item_ptr_id
	GROUP BY
		cci.character_id
);
'''
make_query(average_weapons, cursor)