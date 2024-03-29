from cassandra.cluster import Cluster
import os
import glob
import csv
from cql_queries import *


def get_datafile_paths():
    """
    Creates a list of filepaths to process original event csv data files.
    :return: list of file paths
    """

    # checking your current working directory
    print(os.getcwd())

    # Get your current folder and subfolder event data
    filepath = os.getcwd() + '/event_data'

    # Create a for loop to create a list of files and collect each filepath
    for root, dirs, files in os.walk(filepath):
        # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root, '*'))

    return file_path_list


def create_aggregate_datafile(file_path_list, file):
    """
    Creates one aggregate data file in csv format to be used for Apache
    Cassandra tables.
    :param: file_path_list: a list of individual data file file paths
    :param: file: file path of the aggregate datafile created
    """

    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = []

    # for every filepath in the file path list
    for f in file_path_list:

        # reading csv file
        with open(f, 'r', encoding='utf8', newline='') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            next(csvreader)  # skip header

            # extracting each data row one by one and append it
            for line in csvreader:
                # print(line)
                full_data_rows_list.append(line)

    # get total number of rows from aggregate csv
    print("Number of rows in raw data: {}".format(len(full_data_rows_list)))
    # show first entry of event data rows
    # print(full_data_rows_list[0])

    # creating a smaller event data csv file called event_datafile_new that
    # will be used to insert data into the Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL,
                         skipinitialspace=True)

    with open(file, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(
            ['artist', 'firstName', 'gender', 'itemInSession', 'lastName',
             'length', 'level', 'location', 'sessionId', 'song', 'userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue  # skips entries with missing artist
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6],
                             row[7], row[8], row[12], row[13], row[16]))

    # check the number of rows in your csv file
    with open(file, 'r', encoding = 'utf8') as f:
        print("Number of rows in denormalized data: {}\n".format(sum(1 for line
                                                                   in f)))


def create_database_connection(host):
    """
    Creates a connection to the cassandra database.
    :param: host: database host IP
    :return: cluster: database connection
             session: database session
    """

    try:
        cluster = Cluster([host])  # using 9042 native client port
        session = cluster.connect()
    except Exception as e:
        print(e)

    return cluster, session


def create_tables(session):
    """Creates database tables"""

    for query in create_tables_queries:
        session.execute(query)


def drop_tables(session):
    """Drops database tables"""

    for query in drop_tables_queries:
        session.execute(query)


def insert_into_tables(file, session):
    """
    Inserts selected data from the aggregate data file into the database
    tables.
    :param: file: file path of the aggregate data file
    :param: session: database session
    """

    # insert data into query 1 table
    with open(file, encoding='utf8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip header
        for line in csv_reader:
            session.execute(table_insert_queries[0], (line[8], line[3], line[0],
                                                  line[9], line[5]))
        print("played_songs table written")

    # insert data into query 2 table
    with open(file, encoding='utf8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip header
        for line in csv_reader:
            session.execute(table_insert_queries[1], (line[10], line[8],
                                                      line[3], line[0],
                                                      line[9], line[1],
                                                      line[4]))
        print("user_plays table written")

    # insert data into query 3 table
    with open(file, encoding='utf8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip header
        for line in csv_reader:
            session.execute(table_insert_queries[2], (line[9], line[10],
                                                      line[1], line[4]))
        print("song_listeners table written")


def execute_select_statements(session):
    """Prints outcome of select queries to validate the data model."""

    # print query 1 output
    try:
        rows = session.execute(select_queries[0])
    except Exception as e:
        print(e)

    print("\nQuery 1 output:")
    for row in rows:
        print(row.artist, row.song, row.length)

    # print query 2 output
    try:
        rows = session.execute(select_queries[1])
    except Exception as e:
        print(e)

    print("\nQuery 2 output:")
    for row in rows:
        print(row.artist, row.song, row.first_name, row.last_name)

    # print query 3 output
    try:
        rows = session.execute(select_queries[2])
    except Exception as e:
        print(e)

    print("\nQuery 3 output:")
    for row in rows:
        print(row.first_name, row.last_name)

def main():
    # create csv files
    file_path_list = get_datafile_paths()

    # write aggregate data to csv file
    file = 'event_datafile_new.csv'
    create_aggregate_datafile(file_path_list, file)

    # create a connection to the local cassandra database
    host_ip = '127.0.0.1'
    cluster, session = create_database_connection(host_ip)

    session.execute(create_keyspace_query)  # create keyspace
    session.set_keyspace('sparkify')  # connect to the keyspace

    drop_tables(session)  # drop tables
    create_tables(session)  # create tables

    # insert data into the query tables
    insert_into_tables(file, session)

    # print query data to validate data model
    execute_select_statements(session)

    session.shutdown()  # close session
    cluster.shutdown()  # close cluster connection

if __name__ == "__main__":
    main()

