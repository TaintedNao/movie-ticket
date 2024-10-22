from flask import request, Blueprint
import sqlite3
import json
from sqlite.variables import *
import sqlite.queries.user as us

user_blueprint = Blueprint('/user/', __name__)


@user_blueprint.route('/user/create_user', methods=['POST'])
def create_user():

    # Request for 
    rq = request.json

    # Connect to the db and create a cursor
    connection = sqlite3.connect(DB_FILE)

    # Create a new user using the create_user func
    result = us.create_new_user(
        rq['email'],
        rq['password'],
        rq['first_name'],
        rq['last_name'],
        connection
    )

    # Close the connection
    connection.close()

    # Handle the result of the create_user func
    if result[0] == True:
        ret_dict = {'TYPE': 'success', 'MESSAGE': "Account created."}
        return json.dumps(ret_dict)
    elif result[1] == 'account_exists':
        ret_dict = {'TYPE': 'error', 'MESSAGE': "Account already exists"}
        return json.dumps(ret_dict)
    else:
        ret_dict = {'TYPE': 'error', 'MESSAGE': "Server error!!"}
        return json.dumps(ret_dict)