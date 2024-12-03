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
@app.route("/book/<int:movie_id>", methods=["GET", "POST"])
def book(movie_id):
    if "user_id" not in session:
        flash("You need to log in to book tickets.", "error")
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Fetch movie details
    cursor.execute("SELECT * FROM movie WHERE movie_ID = ?", (movie_id,))
    movie = cursor.fetchone()
    
    if not movie:
        flash("Movie not found.", "error")
        return redirect(url_for("index"))
    
    total_seats = movie[5]  # Total seats from the `remaining_seats` column
    cursor.execute("""
        SELECT seat FROM ticket WHERE movie_ID = ?
    """, (movie_id,))
    booked_seats = {row[0] for row in cursor.fetchall()}  # Booked seats set

    # Fetch ticket price (use a fixed price or dynamically fetch per seat if needed)
    ticket_price = 10  # Example fixed price for all tickets; replace with database logic if variable pricing exists

    # Generate all possible seat options based on total seats
    rows = "ABCDE"  # Adjust rows/columns based on your seating arrangement
    seats_per_row = total_seats // len(rows)
    seats = [f"{row}{num}" for row in rows for num in range(1, seats_per_row + 1)]
    
    available_seats = [seat for seat in seats if seat not in booked_seats]
    
    if request.method == "POST":
        selected_seat = request.form.get("seat")
        
        if selected_seat not in available_seats:
            flash("Seat is not available or invalid selection.", "error")
        else:
            user_email = session["user_id"]
            
            # Create payment entry
            cursor.execute("""
                INSERT INTO payment (total, method, email) VALUES (?, ?, ?)
            """, (ticket_price, "Credit Card", user_email))
            payment_id = cursor.lastrowid
            
            # Book the ticket
            cursor.execute("""
                INSERT INTO ticket (movie_ID, price, seat, payment_ID) VALUES (?, ?, ?, ?)
            """, (movie_id, ticket_price, selected_seat, payment_id))
            
            # Update remaining seats
            cursor.execute("""
                UPDATE movie SET remaining_seats = remaining_seats - 1 WHERE movie_ID = ?
            """, (movie_id,))
            
            conn.commit()
            conn.close()
            
            flash(f"Successfully booked seat {selected_seat} for {movie[2]}.", "success")
            return redirect(url_for("index"))
    
    conn.close()
    return render_template("book.html", movie=movie, available_seats=available_seats, ticket_price=ticket_price)

@app.route("/my_tickets")
def my_tickets():
    if "user_id" not in session:
        flash("You need to log in to view your tickets.", "error")
        return redirect(url_for("login"))

    user_email = session["user_id"]
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Fetch tickets for the logged-in user
    cursor.execute("""
        SELECT ticket.ticket_ID, movie.description, movie.showtime, ticket.seat, ticket.price
        FROM ticket
        JOIN payment ON ticket.payment_ID = payment.payment_ID
        JOIN movie ON ticket.movie_ID = movie.movie_ID
        WHERE payment.email = ?
    """, (user_email,))
    tickets = cursor.fetchall()

    conn.close()
    return render_template("my_tickets.html", tickets=tickets)

@app.route("/cancel_ticket/<int:ticket_id>", methods=["POST"])
def cancel_ticket(ticket_id):
    if "user_id" not in session:
        flash("You need to log in to cancel tickets.", "error")
        return redirect(url_for("login"))
    
    user_email = session["user_id"]
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Verify the ticket belongs to the logged-in user
    cursor.execute("""
        SELECT ticket_ID, movie_ID
        FROM ticket
        JOIN payment ON ticket.payment_ID = payment.payment_ID
        WHERE ticket_ID = ? AND payment.email = ?
    """, (ticket_id, user_email))
    ticket = cursor.fetchone()

    if not ticket:
        flash("Ticket not found or you are not authorized to cancel it.", "error")
        conn.close()
        return redirect(url_for("my_tickets"))
    
    ticket_id, movie_id = ticket

    # Remove the ticket from the database
    cursor.execute("DELETE FROM ticket WHERE ticket_ID = ?", (ticket_id,))

    # Increment the remaining seats for the associated movie
    cursor.execute("""
        UPDATE movie SET remaining_seats = remaining_seats + 1 WHERE movie_ID = ?
    """, (movie_id,))
    
    conn.commit()
    conn.close()

    flash(f"Ticket {ticket_id} has been successfully canceled.", "success")
    return redirect(url_for("my_tickets"))


if __name__ == '__main__':
    app.run(debug=True)
