import pandas as pd
from cassandra.cluster import Cluster
import re
import os
import glob
import numpy as np
import json
import csv


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


def create_aggregate_datafile(file_path_list):
    """
    Creates one aggregate data file in csv format to be used for Apache
    Cassandra tables.
    :param file_path_list: a list of individual data file file paths
    """

    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = []

    # for every filepath in the file path list
    for f in file_path_list:

        # reading csv file
        with open(f, 'r', encoding='utf8', newline='') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            next(csvreader) # skip header

            # extracting each data row one by one and append it
            for line in csvreader:
                # print(line)
                full_data_rows_list.append(line)

    # get total number of rows from aggregate csv
    print(f"Number of rows in raw data: {len(full_data_rows_list)}")
    # show first entry of event data rows
    # print(full_data_rows_list[0])

    # creating a smaller event data csv file called event_datafile_new that
    # will be used to insert data into the Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL,
                         skipinitialspace=True)

    with open('event_datafile_new.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(
            ['artist', 'firstName', 'gender', 'itemInSession', 'lastName',
             'length', 'level', 'location', 'sessionId', 'song', 'userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6],
                             row[7], row[8], row[12], row[13], row[16]))

    # check the number of rows in your csv file
    with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
        print(f"Number of rows in denormalized data: {sum(1 for line in f)}")


def connect_to_database():
    """
    Connect to a local Cassandra database instance, and create and connect to
    keyspace.
    """

    # Create a connection to the cassandra database
    try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect()
    except Exception as e:
        print(e)

    # Create a keyspace
    try:
        session.execute("""CREATE KEYSPACE IF NOT EXISTS sparkify WITH 
        REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
        """)
    except Exception as e:
        print(e)

    # Connect to the keyspace
    try:
        session.set_keyspace('sparkify')
    except Exception as e:
        print(e)

        



def main():
    file_path_list = get_datafile_paths()
    create_aggregate_datafile(file_path_list)
    connect_to_database()


if __name__ == "__main__":
    main()
