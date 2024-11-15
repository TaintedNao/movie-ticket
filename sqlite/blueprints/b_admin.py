from flask import request, Blueprint
import sqlite3
import json
from variables import *
import queries.user as us

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin/get_users', methods=['GET'])
def get_users():

    # json request
    rq = request.json

    # Connect to the db and create a cursor
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Query for the email
    query = '''
        SELECT email, first_name, last_name
        FROM user
    '''

    cursor.execute(query)
    users = cursor.fetchall()

    # Put users in a list
    user_list = []
    for user in users:
        user_data = {
            "email": user[0],
            "first_name": user[1],
            "last_name": user[2]
        }
        user_list.append(user_data)
    
    # Close the connection
    connection.close()
