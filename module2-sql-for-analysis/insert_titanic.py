import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

# Connect to postgres DB
conn = psycopg2.connect(dbname=DB_NAME, 
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST)
cursor = conn.cursor()

# Create titanic table in db
create_sex_type = '''
CREATE TYPE
    sex AS ENUM ('male', 'female');
'''

create_titanic_table = '''
CREATE TABLE titanic (
    passenger_id SERIAL PRIMARY KEY,
    survived INT,
    name VARCHAR(120),
    sex sex,
    age INT,
    siblings_or_spouses_aboard INT,
    parents_or_children_aboard INT,
    fare DECIMAL
)
'''

cursor.execute(create_sex_type)
cursor.execute(create_titanic_table)

# Insert titanic.csv into database
titanic_df = pd.read_csv('titanic.csv')

# convert each row of df into a tuple and add it to a list
passengers = []
for i in range(len(titanic_df)):
    passenger = ()
    for x in titanic_df.iloc[i][1:]:
        if isinstance(x,str) and "'" in x:
            x = x.replace("'", '')
        passenger = passenger + (x,)
    passengers.append(passenger)

# insert passengers into db
for passenger in passengers:
    insert_query = f'''
    INSERT INTO titanic
    (survived, name, sex, age, siblings_or_spouses_aboard, parents_or_children_aboard, fare)
    VALUES {passenger}
    '''

    cursor.execute(insert_query)

conn.commit()