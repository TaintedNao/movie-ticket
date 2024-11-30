import sqlite.queries.ticket as ti
import sqlite3
from sqlite.variables import *



def main():

    movie_ID = 1
    price = 15.99
    seat = "A4"
    payment_ID = 1

    # Connect to the db and create a cursor
    connection = sqlite3.connect(DB_FILE)

    results = ti.create_ticket(movie_ID, price, seat, payment_ID, connection)

    # Close the connection
    connection.close()

    print(results)

if __name__ == "__main__":
    main()