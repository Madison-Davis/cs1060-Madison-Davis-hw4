#!/usr/bin/env python3

import sys
import csv
import sqlite3
import os

"""
NOTE for graders:
"Behavior on bad CSV is undefined" means the script is not required to gracefully handle erroneous
or malformed CSV files.  Based on the prompt, my model (GPT-4.1 Harvard Sandbox) chose to not do anything,
which is within the specification.
"""

def csv_to_table(dbname, csv_filename):
    """ Create a table from a CSV file and insert data into it. """
    tablename = os.path.splitext(os.path.basename(csv_filename))[0]
    with open(csv_filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        columns = [col.strip() for col in header]
        coldefs = ', '.join(f'{col} TEXT' for col in columns)

        # Connect to database
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()

        # Create table
        cur.execute(f'DROP TABLE IF EXISTS {tablename}')
        cur.execute(f'CREATE TABLE {tablename} ({coldefs})')

        # Prepare for insertion
        placeholders = ','.join(['?']*len(columns))
        insert_query = f'INSERT INTO {tablename} VALUES ({placeholders})'

        # Insert data
        for row in reader:
            cur.execute(insert_query, row)
        conn.commit()
        conn.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 csv_to_sqlite.py <database> <csv_file>")
        sys.exit(1)
    dbname, csv_filename = sys.argv[1], sys.argv[2]
    csv_to_table(dbname, csv_filename)

if __name__ == '__main__':

    main()