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
    payment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    total INTEGER,
    method TEXT,
    email TEXT,
    FOREIGN KEY (email) REFERENCES user(email)
);

-- Table: Movie
CREATE TABLE movie (
    movie_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    showtime TEXT,
    description TEXT,
    theatre INTEGER,
    rating TEXT,
    remaining_seats INTEGER,
    FOREIGN KEY (theatre) REFERENCES theatre(theatre_num)
);

-- Table: Ticket
CREATE TABLE ticket (
    ticket_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_ID INTEGER,
    price INTEGER,
    seat VARCHAR(2),
    payment_ID INTEGER,
    FOREIGN KEY (movie_ID) REFERENCES movie(movie_ID),
    FOREIGN KEY (payment_ID) REFERENCES payment(payment_ID)
);

-- Indexes for faster lookup on foreign keys (optional but recommended)
CREATE INDEX idx_Movie_Theatre ON movie(theatre);
CREATE INDEX idx_Ticket_Movie_ID ON ticket(movie_ID);
CREATE INDEX idx_Ticket_Payment_ID ON ticket(payment_ID);
CREATE INDEX idx_Payment_Email ON payment(email);