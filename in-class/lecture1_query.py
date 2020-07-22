import sqlite3
import pandas as pd

DB_FILEPATH = 'database\chinook.db'

conn = sqlite3.connect(DB_FILEPATH)

cursor = conn.cursor()

query = '''
SELECT
	artists.ArtistId,
	artists.Name AS "ArtistName",
	COUNT(albums.ArtistId) AS "AlbumCount"
FROM
	albums
JOIN
	artists
ON
	albums.ArtistId = artists.ArtistId
GROUP BY 
	albums.ArtistId
ORDER BY 
	AlbumCount DESC;
'''

result = cursor.execute(query).fetchall()

# get columns from cursor object
columns = list(map(lambda x: x[0], cursor.description))

# assign to dataframe
df = pd.DataFrame(data=result, columns=columns)

print(df.shape)
df.head()