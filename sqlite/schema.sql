CREATE TABLE user
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_salt TEXT,
    password_hash TEXT,
    firt_name TEXT,
    last_name TEXT,
    is_admin INT NOT NULL
);

CREATE TABLE payment
(
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_type TEXT NOT NULL,
    payment_total SMALLMONEY NOT NULL
);

CREATE TABLE ticket
(
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    price SMALLMONEY NOT NULL,
    seat CHAR(2),
    FOREIGN KEY(movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE movie
(
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    showtime TEXT NOT NULL,
    movie_description TEXT NOT NULL,
    room_no INTEGER NOT NULL,
    rating TEXT NOT NULL,
    seats_remaining INTEGER NOT NULL

);

/*
    SQLite does not have a storage class set aside for storing dates and/or times. Instead, the built-in Date And Time Functions of SQLite are capable of storing dates and times as TEXT, REAL, or INTEGER values:

        TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").
        REAL as Julian day numbers, the number of days since noon in Greenwich on November 24, 4714 B.C. according to the proleptic Gregorian calendar.
        INTEGER as Unix Time, the number of seconds since 1970-01-01 00:00:00 UTC.

    Applications can chose to store dates and times in any of these formats and freely convert between formats using the built-in date and time functions.
*/