import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite.queries.user as us
import sqlite.queries.payment as pa
import sqlite.queries.ticket as ti
import sqlite3
from sqlite.variables import *

def main():
    
    # User variables
    email = "test@gmail.com"
    first_name = "John"
    last_name = "Doe"
    password = "password"

    connection = sqlite3.connect(DB_FILE)
    
    check = input("Delete user(y/n)? :")
    if(check == 'y'):
        results = us.remove_user(email, connection)
        print(results)

    results = us.create_new_user(email, first_name, last_name, password, connection)
    print(results)

    check = input("Continue(y/n)? :")
    if(check == 'n'):
        return

    if(results):
        
        # Payment variables
        total = 19.99
        method = "debit"
        status = "open"
        
        # Add payment
        results = pa.create_payment(total, method, email, status, connection)
        print(results)
        check = input("Continue(y/n)? :")
        if(check == 'n'):
            return


        check = input("Delete user(y/n)? :")
        if(check == 'y'):
            results = us.remove_user(email, connection)
            print(results)
    else:
        print("Didn't create user")


    connection.close()



if __name__ == "__main__":
    main()