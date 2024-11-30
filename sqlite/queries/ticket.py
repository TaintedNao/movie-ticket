import sqlite3 as sq
import sqlite.queries.movie as mo


# Description:
#       Create a ticket that will have a movie ID and a payment ID attached to it    
# Pre:
#       movie_id(string)
#       price(int)
#       seat(string)
#       payment_id(string)
# Post:
#       Inserts a ticket with the above info into the db
def create_ticket(movie_id, price, seat, payment_id, connection):
    
    # Create a cursor
    cursor = connection.cursor()

    # Get seats remaining to make sure there is enough seats
    seats_remaining = mo.get_seats_remaining(movie_id, connection)
    if seats_remaining == 0:
        return(False, "no seats remaining!")

    # Make a query
    query = '''
        INSERT INTO
            ticket(
                movie_ID,
                price,
                seat,
                payment_ID
            )
        VALUES (?, ?, ?, ?)
    '''

    # Execute and commit the query
    cursor.execute(
        query,
        (movie_id, price, seat, payment_id)
    )

    connection.commit()

    # Update seats remaining
    mo.update_seats_remaining(movie_id, seats_remaining - 1, connection)


    return(True, "ticket_created")


# Description:
#       Find a ticket in the db
# Pre:
#       ticket_id(int)
# Post:
#       Fetch a ticket from the db
def find_ticket(ticket_id, connection):

    # Create a cursor
    cursor = connection.cursor()

    # Query for fetch
    query = '''
        SELECT
            ticket_id,
            movie_id,
            price,
            seat,
            payment_id
        FROM ticket
        WHERE ticket_id = ?
    '''

    # Execute the query
    cursor.execute(query, (ticket_id,))

    # Fetch one ticket
    ticket = cursor.fetchone()

    return ticket


# Description:
#       Find ticket based by payment
# Pre:
#       payment_id(int)
# Post:
#       Fetch all tickets from a payment_id
def find_ticket_by_payment(payment_id, connection):

    # Create a cursor
    cursor = connection.cursor()

    # Query to fetch
    query = '''
        SELECT
            ticket_id,
            movie_id,
            price,
            seat,
            payment_id
        FROM ticket
        WHERE payment_id = ?
    '''

    # Execute the query
    cursor.execute(query, (payment_id,))

    # Fetch all tickets associated
    tickets = cursor.fetchall()

    return tickets


# Description:
#       Find a ticket from movie_id
# Pre:
#       movie_id(int)
# Post:
#       Fetch all tickets from the movie_id
def find_ticket_by_movie(movie_id, connection):

    # Create the cursor
    cursor = connection.cursor()

    # Qeury for the fetch
    query = '''
        SELECT
            ticket_id,
            movie_id,
            price,
            seat,
            payment_id
        FROM ticket
        WHERE movie_id = ?
    '''

    # Execute the query
    cursor.execute(query, (movie_id,))

    # Fetch all tickets
    tickets = cursor.fetchall()

    return tickets


# Description:
#       
# Pre:
#       
# Post:
#       


# Description:
#       
# Pre:
#       
# Post:
#       


# Description:
#       
# Pre:
#       
# Post:
#       