import sqlite3 as sq
import hashlib
import secrets

# Description:
#         Uses BLAKE2 to generate a hash
# Pre:
#         password(string)
# Post:
#         Hash and Salt
def get_secure_hash(password):

    # Generate a salt using a secure number generator
    salt = secrets.token_hex(16)

    # Use the BLAKE2 hashing algorithm as it is collision resistant.
    hasher = hashlib.blake2s()

    # Get the hash for the salted password. Note that we append the salt on the end.
    hasher.update((password + salt).encode())
    hash = hasher.hexdigest()

    return {'hash': hash, 'salt': salt}


# Description:
#       Takes in a password and a salt and returns a hash
#       using the BLAKE2 Algorithm
# Pre:
#       password(string)
#       salt(string) -- Add to the end of the password
# Post:
#       Hash generated from the salted password.
def get_password_hash(password, salt):
    
    # Create a hasher and pass in salted password
    hasher = hashlib.blake2s()
    hasher.update((password + salt).encode())

    return hasher.hexdigest()

# Description:
#         Check to see if the user is an is_admin
# Pre:
#         email(string)
# Post:
#         Returns true or false if the user is an admin
def is_admin(email, connection):

    cursor = connection.cursor()

    query = '''
        SELECT is_admin
        FROM user
        WHERE email = ?
    '''

    cursor.execute(query, (email,))
    results = cursor.fetchall()

    # If results is not empty and the first result is 1 (admin)
    if results and results[0][0] == 1:
        return True
    else:
        return False


# Description:
#       Checks to see if the user exists and checks if the password is correct
# Pre:
#       user_name(string)
#       password(string)
# Post:
#       returns a success if the user exists and the password is correct
def authenticate_user(user_name, password, connection):

    cursor = connection.cursor()

    # Query to get the hash and salt
    query = '''
        SELECT password_hash, password_salt
        FROM user
        WHERE email == ?
    '''
    cursor.execute(query, (user_name,))
    hash_details = cursor.fetchall()[0]

    if len(hash_details) == 0:
        return (False, "user_not_found")
    
    password_hash = get_password_hash(password, hash_details[1])

    if password_hash == hash_details[0]:
        return (True, "auth_success")
    else:
        return (False, "incorrect_pass")


# Description: 
#       Creates a new user
# Pre:
#       email(string)
#       password(string)
#       first_name(string)
#       last_name(string)
# Post:
#       Inserts a new user into the database
def create_new_user(email, password, first_name, last_name, connection):

    cursor = connection.cursor()

    # Checks to see if the email is in use
    if is_user(email, connection) == True:
        return(False, "account_exists")

    # SQL to call
    query = '''
        INSERT INTO
            user(
                email,
                password_salt,
                password_hash,
                first_name,
                last_name
            )
        VALUES (?, ?, ?, ?, ?)
    '''

    # Get salt and hash generated by the password
    hashing = get_secure_hash(password)

    # Insert the user and commit
    cursor.execute(
        query, 
        (email, hashing['salt'], hashing['hash'], first_name, last_name)
    )

    # Commit to the database
    connection.commit()

    return(True, "account_created")


# Description: 
#       Update the password for an existing user
# Pre:
#       email(string)
#       first_name(string)
#       last_name(string)
# Post:
#       update the users password
def update_user_password(email, new_pass, connection):

    cursor = connection.cursor()
    
    # Get a salt and the corresponding hash for the new password
    sh = get_secure_hash(new_pass)

    # Query to update user's password
    query = '''
        UPDATE user
        SET password_salt = ?, password_hash = ?
        WHERE email == ?
    '''

    # Update and commit
    cursor.execute(query, (sh['salt'], sh['hash'], email))
    connection.commit()


# Description:
#       Removes a user from the system and handles related data (payments, tickets).
# Pre:
#       email (string) - The email of the user to be removed.
# Post:
#       Removes the user and all related data from the database.
def remove_user(email, connection):
    
    cursor = connection.cursor()

    # Check if the user exists in the database
    if is_user(email, connection) == False:
        return(False, "user_not_found")

    # Delete the user from the user table
    query = '''
        DELETE FROM user
        WHERE email == ?
    '''
    cursor.execute(query, (email,))

    # Commit changes
    connection.commit()

    return (True, "user_removed")


# Description:
#       Checks to see if a user is in the db
# Pre:
#       email (string) - The email of the user to be removed.
# Post:
#       True or False depeneding on if a user in in the db
def is_user(email, connection):
    
    cursor = connection.cursor()

    # Check if the user exists in the database
    query = '''
        SELECT email
        FROM user
        WHERE email == ?
    '''
    cursor.execute(query, (email,))
    user = cursor.fetchall()

    if len(user) == 0:
        return(False)
    else:
        return(True)