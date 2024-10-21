import sqlite3 as sq
import sys
import os
# from user import *

DB_FILE = "database.db"
SCHEMA_FILE = "schema.sql"

print(sys.argv)

def create_db():

    # Create connection and cursor for database file
    conn = sq.connect(DB_FILE)
    curs = conn.cursor()

    # Open the schema file and execute the code
    with open(SCHEMA_FILE, 'r') as file:
        curs.executescript(file.read())
    

    # Close the connection
    conn.close()

# Run if an argument is passed when running the script
if len(sys.argv) > 1:
    if sys.argv[1].lower() == "force":
        if os.path.isfile(DB_FILE):
            in_str = input("WARNING: PROCEEDING WILL DELETE THE DATABASE AND ALL DATA WILL BE LOST! IF YOU ARE SURE, TYPE 'YES' TO CONTINUE AND PRESS ENTER. OTHERWISE THE PROCESS WILL BE ABORTED.")
            if in_str.lower() != 'yes':
                print("Aborting...")
                exit()
        create_db()

# If force switch is not used and db file already exists, exit with error message
elif os.path.isfile(DB_FILE):
    print(f"{DB_FILE} file already exists. Use 'force' switch to force deletion and recreation of the database.")

# If db file does not exist, create it
else:
    create_db()