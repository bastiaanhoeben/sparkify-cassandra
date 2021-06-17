## Sparkify data modeling with Apache Cassandra

### About the project
In this project, data from a fictive streaming music company "Sparkify" is 
processed and written to an Apache Cassandra database. The Cassandra 
database hereby enables easy querying of the data for analysis purposes. This project is part of the Udacity nanodegree 
Data Engineering.

### Overview

The project contains two python scripts, being:

- **main.py**, containing all functions for performing the necessary ETL's 
  and querying the data, including functions for creating a new database schema 
  and tables and functions for selectively extracting song play data and 
  writing said data to the database tables; and
- **cql_queries.py**, containing all the CQL queries performed on the 
  database engine.
  
Moreover, the project contains a Jupyter Notebook - **project_notebook.
ipynb** - which in the basis has the same functionality as the *main.py* and 
*cql_queries.py* files. For running instructions, please see below under 
"Making use of the Jupyter notebook".

### Description of the dataset

The repo provides a sample dataset for interaction with the scripts. This 
dataset can be found in the *event_data* directory.

The dataset consists of songplay event data, wherein the data for each day 
is contained in a separate file in CSV format. To get a feel for the data 
format, a sample of the data is given below.

![Data sample](support_files/data_sample.png)

### Queries and data model

The type of queries run against the database are:

1. Give me the artist, song title and song's length in the music app 
   history that was heard during sessionId = #, and itemInSession = #.
   
2. Give me only the following: name of artist, song (sorted by itemInSession)
   and user (first and last name) for userid = #, sessionid = #.
   
3. Give me every user name (first and last) in my music app history who 
   listened to the song #.

The data in the Apache Cassandra database is modelled to fit the type of 
queries that are run against the database. For this reason, each query type 
needs its own table to perform the queries on. To be descriptive of the type of 
queries performed, the tables are named as follows:

1.  played_songs
2.  user_plays
3.  song_listeners

Now, the corresponding select CQL queries can be formulated. An example 
query against each of the tables is given below:

1.  Query 1:
    ```
    SELECT artist, song, length 
    FROM played_songs 
    WHERE session_id = '338' AND item_in_session = '4';
    ```

2.  Query 2:
    ```
    SELECT artist, song, first_name, last_name 
    FROM user_play
    WHERE user_id = '10' AND session_id = '182';
    ```
    
3.  Query 3:
    ```
    SELECT first_name, last_name
    FROM song_listeners
    WHERE song = 'All Hands Against His Own';
    ```

To successfully run the first query, a table must be created that can filer 
based on *session_id* and *item_in_session*. As such, both *session_id* and 
*item_in_session* must be contained in one, compound primary key. This primary 
key also meets the requirement of uniqueness. Moreover, the columns *artist*, 
*song* and *length* that are in the select statement must be included as well.

Running the second query requires a table that can filter based on *user_id* 
and *session_id*. Moreover, the results should be ordered based on 
*item_in_session*. To make this possible, and make the primary key unique as 
well, the primary key must comprise *user_id*, *session_id* and 
*item_in_session*. The columns *user_id* and *session_id* may hereby act as 
compound partition key, where *item_in_session* then constitutes a clustering 
column. The columns *artist*, *song*, *first_name* and *last_name* must be 
included as well, as they are in the select statement.

Finally, the third query requires a table that can filter based on *song*
(song title). To make the primary key unique, an efficient choice would be to 
include *song* together with *user_id* in the primary key. For the partition 
key, *song* is chosen. Finally, the columns *first_name* and *last_name* are 
included as they are included in the select statement.
   
Consequently, the data model for the database looks as follows:

![Data model](support_files/data_model.png)

### Running instructions

To get a local environment running in which to create the ETL pipelines and 
query the database, go through the following steps:

1. Clone the repository into the working directory and move into the project
   directory:
   ```
   git clone https://github.com/bastiaanhoeben/sparkify-cassandra.git
   ```
   ```
   cd sparkify
   ```   
   
2. Start up the Cassandra database service in the background:
   ```
   docker-compose up -d
   ```
   
3. Create a virtual environment and activate it:
   ```
   python3 -m venv .venv
   ```
   ```
   source .venv/bin/activate
   ```
   
4. Install the necessary packages from requirements.txt:
   ```
   python -m pip install -r requirements.txt
   ```

5. Run the piplines and query the database with the *main.py* script:
   ```
   python main.py
   ```


### Making use of the Jupyter notebook

The database can be populated without the use of the notebook. For a proper 
functioning of the notebook, Jupyter Notebook must run *inside* the virtual 
environment. An easy way to achieve this is by installing Jupyter Notebook 
within the activate venv like so:
```
pip install notebook
```

The notebook can then be started easily through:
```
jupyter notebook project_template.ipynb
```