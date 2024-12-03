import sqlite3
from datetime import datetime, timedelta

# Database connection
DATABASE = "database.db"

def create_theaters_and_movies():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Clear previous data (optional, use with caution)
    cursor.execute("DELETE FROM theatre")
    cursor.execute("DELETE FROM movie")
    cursor.execute("DELETE FROM seat")
    
    # Define theaters
    theaters = [
        {"theatre_num": 1, "capacity": 100},
        {"theatre_num": 2, "capacity": 50},
        {"theatre_num": 3, "capacity": 150}
    ]
    
    # Insert theaters
    for theater in theaters:
        cursor.execute("INSERT INTO theatre (theatre_num, capacity) VALUES (?, ?)", 
                       (theater["theatre_num"], theater["capacity"]))
    
    # Define movies and showtimes
    start_time = datetime.now()
    movies = [
        {
            "description": "Adventure",
            "showtimes": [start_time + timedelta(hours=i*3) for i in range(3)],
            "rating": "PG",
            "theatre_num": 1
        },
        {
            "description": "Comedy Night",
            "showtimes": [start_time + timedelta(hours=i*3) for i in range(2)],
            "rating": "R",
            "theatre_num": 2
        },
        {
            "description": "Horror Tales",
            "showtimes": [start_time + timedelta(hours=i*4) for i in range(4)],
            "rating": "PG-13",
            "theatre_num": 3
        }
    ]
    
    # Insert movies and initialize seats
    for movie in movies:
        for showtime in movie["showtimes"]:
            cursor.execute("""
                INSERT INTO movie (showtime, description, theatre, rating, remaining_seats)
                VALUES (?, ?, ?, ?, ?)
            """, (showtime.strftime("%Y-%m-%d %H:%M:%S"), movie["description"], movie["theatre_num"], 
                  movie["rating"], theaters[movie["theatre_num"]-1]["capacity"]))
            
            # Get the movie ID of the last inserted movie
            movie_id = cursor.lastrowid
            
            # Add seats for the movie
            initialize_seats(cursor, movie_id, theaters[movie["theatre_num"]-1]["capacity"])
    
    conn.commit()
    conn.close()
    print("Database populated with theaters, movies, and seats.")

def initialize_seats(cursor, movie_id, capacity):
    """
    Initialize seats for a movie based on the theater's capacity.
    """
    rows = "ABCDE"  # Adjust as needed
    seats_per_row = capacity // len(rows)

    # Generate seats with proper numerical sorting
    seats = [f"{row}{num}" for row in rows for num in range(1, seats_per_row + 1)]
    seats.sort(key=lambda x: (x[0], int(x[1:])))  # Sort by row, then numerically by number

    for seat in seats:
        cursor.execute("INSERT INTO seat (movie_ID, seat_number) VALUES (?, ?)", (movie_id, seat))



# Run the script
if __name__ == "__main__":
    create_theaters_and_movies()
