import os
import psycopg2

conn = psycopg2.connect(
        host="LOCALHOST",
        database="PI UNIVESP 2022",
        user='admin',
        password=os.environ['123'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS posts')
cur.execute('CREATE TABLE posts (id INTEGER PRIMARY KEY,'
                                 'created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
                                 'title TEXT NOT NULL,'
                                 'content TEXT NOT NULL);'
                                 )
cur.execute('drop view if exists Resultados')
cur.execute(
    'CREATE VIEW Resultados as SELECT bairro AS Bairros, count(*) AS Ocorrências FROM posts group by (bairro) ORDER BY Ocorrências DESC;');

conn.commit()

cur.close()
conn.close()
