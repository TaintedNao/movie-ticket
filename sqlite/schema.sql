-- Table: User
CREATE TABLE user (
    email TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    password_salt TEXT,
    password_hash TEXT,
    is_admin INTEGER
);

-- Table: Theatre
CREATE TABLE theatre (
    theatre_num INTEGER PRIMARY KEY,
    capacity INTEGER
);

-- Table: Payment
CREATE TABLE payment (
    payment_ID INTEGER PRIMARY KEY,
    total INTEGER,
    method TEXT,
    email TEXT,
    FOREIGN KEY (email) REFERENCES user(email)
);

-- Table: Movie
CREATE TABLE movie (
    movie_ID INTEGER PRIMARY KEY,
    showtime DATETIME,
    description TEXT,
    theatre INTEGER,
    rating TEXT,
    remaining_seats INTEGER,
    FOREIGN KEY (theatre) REFERENCES theatre(theatre_num)
);

-- Table: Ticket
CREATE TABLE ticket (
    ticket_ID INTEGER PRIMARY KEY,
    movie_ID INTEGER,
    price INTEGER,
    seat INTEGER,
    payment_ID INTEGER,
    FOREIGN KEY (movie_ID) REFERENCES movie(movie_ID),
    FOREIGN KEY (payment_ID) REFERENCES payment(payment_ID)
);


-- Indexes for faster lookup on foreign keys (optional but recommended)
CREATE INDEX idx_Movie_Theatre ON movie(theatre);
CREATE INDEX idx_Ticket_Movie_ID ON ticket(movie_ID);
CREATE INDEX idx_Ticket_Payment_ID ON ticket(payment_ID);
CREATE INDEX idx_Payment_Email ON payment(email);

/*
    SQLite does not have a storage class set aside for storing dates and/or times. Instead, the built-in Date And Time Functions of SQLite are capable of storing dates and times as TEXT, REAL, or INTEGER values:

        TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").
        REAL as Julian day numbers, the number of days since noon in Greenwich on November 24, 4714 B.C. according to the proleptic Gregorian calendar.
        INTEGER as Unix Time, the number of seconds since 1970-01-01 00:00:00 UTC.

    Applications can chose to store dates and times in any of these formats and freely convert between formats using the built-in date and time functions.
*/