# Create keyspace

create_keyspace_query = """CREATE KEYSPACE IF NOT EXISTS sparkify WITH 
REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"""

# Create tables

create_table_query1 = """CREATE TABLE IF NOT EXISTS played_songs (session_id 
TEXT, item_in_session TEXT, artist TEXT, song TEXT, length TEXT, PRIMARY KEY (
session_id, item_in_session))"""

create_table_query2 = """CREATE TABLE IF NOT EXISTS user_plays (user_id 
TEXT, session_id TEXT, item_in_session TEXT, artist TEXT, song TEXT, 
first_name TEXT, last_name TEXT, PRIMARY KEY ((user_id, session_id), 
item_in_session))"""

create_table_query3 = """CREATE TABLE IF NOT EXISTS song_listeners (song TEXT, 
user_id TEXT, first_name TEXT, last_name TEXT, PRIMARY KEY (song, user_id))"""

# Drop tables

drop_table_query1 = """DROP TABLE IF EXISTS played_songs"""
drop_table_query2 = """DROP TABLE IF EXISTS user_plays"""
drop_table_query3 = """DROP TABLE IF EXISTS song_listeners"""

# Insert records

insert_table_query1 = """INSERT INTO played_songs (session_id, item_in_session, 
artist, song, length) VALUES (%s, %s, %s, %s, %s)"""

insert_table_query2 = """INSERT INTO user_plays (user_id, session_id, 
item_in_session, artist, song, first_name, last_name) VALUES (%s, %s, %s, 
%s, %s, %s, %s)"""

insert_table_query3 = """INSERT INTO song_listeners (song, user_id, first_name, 
last_name) VALUES (%s, %s, %s, %s)"""

# Select data

select_query1 = """SELECT artist, song, length FROM played_songs WHERE 
session_id = '338' AND item_in_session = '4'"""

select_query2 = """SELECT artist, song, first_name, last_name FROM user_plays 
WHERE user_id = '10' AND session_id = '182'"""

select_query3 = """SELECT first_name, last_name FROM song_listeners WHERE song = 
'All Hands Against His Own'"""


# Query list
create_tables_queries = [create_table_query1, create_table_query2,
                         create_table_query3]
drop_tables_queries = [drop_table_query1, drop_table_query2, drop_table_query3]
table_insert_queries = [insert_table_query1, insert_table_query2,
                        insert_table_query3]
select_queries = [select_query1, select_query2, select_query3]