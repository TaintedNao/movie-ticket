import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

DATABASE = 'database.db'

# Function to connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        is_admin = 0

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        if cursor.fetchone():
            flash('Email is already registered.', 'error')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO user (email, first_name, last_name, password_salt, password_hash, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email, first_name, last_name, '', password_hash, is_admin))
        db.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['email']
            session['is_admin'] = bool(user['is_admin'])
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Homepage with Movie Listings
@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM movie ORDER BY showtime ASC")
    movies = cursor.fetchall()
    return render_template("index.html", movies=movies)

# Book Tickets
@app.route('/book/<int:movie_id>', methods=['GET', 'POST'])
def book(movie_id):
    if 'user_id' not in session:
        flash('You must be logged in to book tickets.', 'error')
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        seat = request.form['seat']
        price = request.form['price']

        # Check if the seat is already booked
        cursor.execute("SELECT * FROM ticket WHERE movie_ID = ? AND seat = ?", (movie_id, seat))
        if cursor.fetchone():
            flash('Seat already booked. Please choose a different seat.', 'error')
            return redirect(url_for('book', movie_id=movie_id))

        # Add ticket to the database
        cursor.execute("""
            INSERT INTO ticket (movie_ID, price, seat, payment_ID)
            VALUES (?, ?, ?, NULL)
        """, (movie_id, price, seat))

        # Update remaining seats in the movie table
        cursor.execute("""
            UPDATE movie
            SET remaining_seats = remaining_seats - 1
            WHERE movie_ID = ?
        """, (movie_id,))
        db.commit()

        flash('Ticket booked successfully!', 'success')
        return redirect(url_for('index'))

    # Fetch movie details
    cursor.execute("SELECT * FROM movie WHERE movie_ID = ?", (movie_id,))
    movie = cursor.fetchone()

    return render_template("book.html", movie=movie)

if __name__ == '__main__':
    app.run(debug=True)
