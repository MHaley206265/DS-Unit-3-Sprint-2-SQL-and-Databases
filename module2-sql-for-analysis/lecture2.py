import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

# Create character table in postgres
# create_character_table_query = '''
# CREATE TABLE rpg_characters (
#     character_id SERIAL PRIMARY KEY,
# 	name VARCHAR(30),
# 	level INT,
# 	exp INT,
# 	hp INT,
# 	strength INT,
# 	intelligence INT,
# 	dexterity INT,
# 	wisdom INT
# )
# '''

import sqlite3

sl_conn = sqlite3.connect('rpg_db.sqlite3')
sl_cursor = sl_conn.cursor()

characters = sl_cursor.execute('SELECT * FROM charactercreator_character').fetchall()

conn = psycopg2.connect(dbname=DB_NAME, 
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST)
cursor = conn.cursor()
# cursor.execute(create_character_table_query)
# conn.commit()

### insert data into characters table ###



for character in characters:
    insert_query = f'''
    INSERT INTO rpg_characters
        (character_id, name, level, exp, hp, strength, intelligence, dexterity, wisdom) VALUES
        {character}
    '''
    cursor.execute(insert_query)

conn.commit()