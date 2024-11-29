import sqlite3 as sq

# Description:
#       Create a payment record with total amount, method, and email attached to it
# Pre:
#       total(int): total payment amount
#       method(string): payment method
#       email(string): email of the user associated with the payment
#       status(string): payment status 
# Post:
#       Inserts a payment record into the database
def create_payment(total, method, email, status, connection):
    
    # Create a cursor
    cursor = connection.cursor()

    # Define the query
    query = '''
        INSERT INTO
            payment(
                total,
                method,
                email,
                status
            )
        VALUES (?, ?, ?, ?)
    '''

    # Execute and commit the query
    cursor.execute(query, (total, method, email, status))
    connection.commit()
    return (True, "payment_created")


# Description:
#       Find a payment record in the database by payment ID
# Pre:
#       payment_id(int)
# Post:
#       Fetch a payment record from the database
def find_payment(payment_id, connection):
    
    # Create a cursor
    cursor = connection.cursor()

    # Define the query
    query = '''
        SELECT
            payment_id,
            total,
            method,
            email,
            status
        FROM payment
        WHERE payment_id = ?
    '''

    # Execute the query
    cursor.execute(query, (payment_id,))

    # Fetch the payment record
    payment = cursor.fetchone()

    return payment


# Description:
#       Update the status of a payment
# Pre:
#       payment_id(int)
#       status(string)
# Post:
#       Updates the status of the payment in the database
def update_payment_status(payment_id, status, connection):
    
    # Create a cursor
    cursor = connection.cursor()

    # Define the query
    query = '''
        UPDATE payment
        SET status = ?
        WHERE payment_id = ?
    '''

    # Execute and commit the query
    cursor.execute(query, (status, payment_id))
    connection.commit()
    return (True, "payment_status_updated")


# Description:
#       Delete a payment record from the database
# Pre:
#       payment_id(int)
# Post:
#       Deletes the payment record from the database
def delete_payment(payment_id, connection):
    
    # Create a cursor
    cursor = connection.cursor()

    # Define the query
    query = '''
        DELETE FROM payment
        WHERE payment_id = ?
    '''

    # Execute and commit the query
    cursor.execute(query, (payment_id,))
    connection.commit()
    return (True, "payment_deleted")


# Description:
#       Retrieve all payments from the database
# Pre:
#       None
# Post:
#       Fetches all payment records from the database
def get_all_payments(connection):
    
    # Create a cursor
    cursor = connection.cursor()

    # Define the query
    query = '''
        SELECT
            payment_id,
            total,
            method,
            email,
            status
        FROM payment
    '''

    # Execute the query
    cursor.execute(query)

    # Fetch all payment records
    payments = cursor.fetchall()

    return(payments, "all_payments_found")


# Description:
#       Find all payments associated with a specific user email
# Pre:
#       email(string)
# Post:
#       Fetch all payment records associated with the given email
def find_payments_by_email(email, connection):
    
    # Create a cursor
    cursor = connection.cursor()

    # Define the query
    query = '''
        SELECT
            payment_id,
            total,
            method,
            email,
            status
        FROM payment
        WHERE email = ?
    '''

    # Execute the query
    cursor.execute(query, (email,))

    # Fetch all payment records for the user
    payments = cursor.fetchall()

    return(payments, "payment_by_email_found")