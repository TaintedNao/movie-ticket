import sqlite3
from flask import Flask, render_template, g

app = Flask(__name__)
app.secret_key = "123"

DATABASE = 'database.db'

# Route for the homepage
@app.route("/")
def index():
    # Fetch movie data
    movies = fetch_movies()
    return render_template("index.html", movies=movies)

# Function to fetch movie data from the database
def fetch_movies():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT movie_ID, description, showtime, rating, remaining_seats, theatre
        FROM movie
        ORDER BY showtime ASC
    """)
    movies = cursor.fetchall()
    return movies

# Function to connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Function to close the database connection after request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
