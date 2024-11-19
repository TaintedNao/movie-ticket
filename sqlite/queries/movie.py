import sqlite3 as sq


# Description:
#       Add a new movie
# Pre:
#       movie_id(int) 
#       showtime(str) 
#       description(str) 
#       theatre(int) 
#       rating(str) 
#       remaining_seats(int)
# Post:
#       Inserts a new movie with the above info into the db
def add_movie(showtime, description, theatre, rating, remaining_seats, connection):
    
    # Create a cursor
    cursor = connection.cursor()

    # Make a query
    query = '''
        INSERT INTO
            movie(
                showtime,
                description,
                theatre,
                rating,
                remaining_seats
            )
        VALUES (?, ?, ?, ?, ?)
    '''

    # Execute and commit the query
    cursor.execute(
        query,
        (showtime, description, theatre, rating, remaining_seats)
    )

    connection.commit()
    return(True, "movie_added")


# Description:
#       Gets the number of remaining seats for a specific movie
# Pre:
#       movie_id(int) 
# Post:
#       Returns the number of remaining seats for the specified movie
def get_seats_remaining(movie_id, connection):

    # Create a cursor
    cursor = connection.cursor()

    # Query to fetch remaining seats
    query = '''
        SELECT
            remaining_seats
        FROM movie
        WHERE movie_ID = ?
    '''

    # Execute the query
    cursor.execute(query, (movie_id,))

    # Fetch remaining seats
    seats_remaining = cursor.fetchone()

    return seats_remaining[0] if seats_remaining else None


# Description:
#       Updates the number of remaining seats for a movie
# Pre:
#       movie_id(int) 
#       remaining_seats(int)
# Post:
#       Updates the remaining seats for the specified movie in the db
def update_seats_remaining(movie_id, remaining_seats, connection):

    # Create a cursor
    cursor = connection.cursor()

    # Query to update remaining seats
    query = '''
        UPDATE movie
        SET remaining_seats = ?
        WHERE movie_ID = ?
    '''

    # Execute and commit the query
    cursor.execute(query, (remaining_seats, movie_id))
    connection.commit()

    return True, "seats_updated"


# Description:
#       deletes a movie from the db
# Pre:
#       movie_id(int) 
# Post:
#       Deletes the specified movie from the db
def remove_movie(movie_id, connection):

    # Create a cursor
    cursor = connection.cursor()

    # Query to delete movie
    query = '''
        DELETE FROM movie
        WHERE movie_ID = ?
    '''

    # Execute and commit the query
    cursor.execute(query, (movie_id,))
    connection.commit()

    return True, "movie_removed"