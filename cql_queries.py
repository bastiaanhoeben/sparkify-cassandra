# Create keyspace

create_keyspace_query = """CREATE KEYSPACE IF NOT EXISTS sparkify WITH 
REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"""

# Create tables

create_table_query1 = """CREATE TABLE IF NOT EXISTS query1 (session_id INT, 
item_in_session INT, artist TEXT, song TEXT, length TEXT, PRIMARY KEY (
session_id, item_in_session))"""

create_table_query2 = """CREATE TABLE IF NOT EXISTS query2 (user_id INT, 
session_id INT, artist TEXT, song TEXT, first_name TEXT, last_name TEXT, 
PRIMARY KEY (user_id, session_id))"""

# Drop tables

drop_table_query1 = """DROP TABLE IF EXISTS query1"""
drop_table_query2 = """DROP TABLE IF EXISTS query2"""
drop_table_query3 = """DROP TABLE IF EXISTS query3"""

# Insert records

insert_table_query1 = """INSERT INTO query1 (session_id, item_in_session, 
artist, song, length) VALUES (%s, %s, %s, %s, %s)"""

# Select data

select_query1 = """SELECT artist, song, length FROM query1 WHERE session_id 
= 338 AND item_in_session = 4"""

select_query2 = """SELECT artist, song, first_name, last_name FROM query2 WHERE 
user_id = 10 AND session_id = 182"""


# Query list
create_tables_queries = [create_table_query1, create_table_query2]
drop_tables_queries = [drop_table_query1, drop_table_query2, drop_table_query3]