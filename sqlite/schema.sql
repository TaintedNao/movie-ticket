-- Table: Movie
CREATE TABLE Movie (
    Movie_ID INTEGER PRIMARY KEY,
    Showtime DATETIME,
    Description VARCHAR,
    Theatre INTEGER,
    Rating VARCHAR,
    Remaining_Seats INTEGER,
    FOREIGN KEY (Theatre) REFERENCES Theatre(Theatre_num)
);

-- Table: Theatre
CREATE TABLE Theatre (
    Theatre_num INTEGER PRIMARY KEY,
    Capacity INTEGER
);

-- Table: Ticket
CREATE TABLE Ticket (
    Ticket_ID INTEGER PRIMARY KEY,
    Movie_ID INTEGER,
    Price INTEGER,
    Seat INTEGER,
    Payment_ID INTEGER,
    FOREIGN KEY (Movie_ID) REFERENCES Movie(Movie_ID),
    FOREIGN KEY (Payment_ID) REFERENCES Payment(Payment_ID)
);

-- Table: Payment
CREATE TABLE Payment (
    Payment_ID INTEGER PRIMARY KEY,
    Total INTEGER,
    Method VARCHAR,
    Email VARCHAR,
    FOREIGN KEY (Email) REFERENCES User(Email)
);

-- Table: User
CREATE TABLE User (
    Email VARCHAR PRIMARY KEY,
    Name VARCHAR,
    Password VARCHAR,
    Is_Admin BOOLEAN
);

-- Indexes for faster lookup on foreign keys (optional but recommended)
CREATE INDEX idx_Movie_Theatre ON Movie(Theatre);
CREATE INDEX idx_Ticket_Movie_ID ON Ticket(Movie_ID);
CREATE INDEX idx_Ticket_Payment_ID ON Ticket(Payment_ID);
CREATE INDEX idx_Payment_Email ON Payment(Email);

/*
    SQLite does not have a storage class set aside for storing dates and/or times. Instead, the built-in Date And Time Functions of SQLite are capable of storing dates and times as TEXT, REAL, or INTEGER values:

        TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").
        REAL as Julian day numbers, the number of days since noon in Greenwich on November 24, 4714 B.C. according to the proleptic Gregorian calendar.
        INTEGER as Unix Time, the number of seconds since 1970-01-01 00:00:00 UTC.

    Applications can chose to store dates and times in any of these formats and freely convert between formats using the built-in date and time functions.
*/
