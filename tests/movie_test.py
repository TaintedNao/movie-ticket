import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite.queries.movie as mo
import sqlite3
from sqlite.variables import *
import datetime




def main():

    showtime = datetime.datetime.now().isoformat()
    description = "Comedy movie"
    theatre = 2
    rating = "M"
    remaining_seats = 20

    # Connect to the db and create a cursor
    connection = sqlite3.connect(DB_FILE)

    results = mo.add_movie(showtime, description, theatre, rating, remaining_seats, connection)

    # Close the connection
    connection.close()

    print(results)

if __name__ == "__main__":
    main()