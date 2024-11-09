from flask import request, Blueprint
import sqlite3
import json
from variables import *
import queries.ticket as ti

ticket_blueprint = Blueprint('/ticket/', __name__)


@ticket_blueprint.route('/ticket/create_ticket', methods=['POST'])
def create_ticket():

    # json request
    rq = request.json

    # Connect to the db and create a cursor
    connection = sqlite3.connect(DB_FILE)

    # Create a new ticket using the create_ticket func
    result = ti.create_ticket(
        rq['movie_id'],
        rq['price'],
        rq['seat'],
        rq['payment_id'],
        connection
    )

    # Close the connection
    connection.close()

    # Handle the result
    if result[0] == True:
        ret_dict = {'TYPE': 'success', 'MESSAGE': "Ticket created."}
        return json.dumps(ret_dict)
    elif result[1] == 'ticket_exists':
        ret_dict = {'TYPE': 'error', 'MESSAGE': "Ticket already exists"}
        return json.dumps(ret_dict)
    else:
        ret_dict = {'TYPE': 'error', 'MESSAGE': "Server error!!"}
        return json.dumps(ret_dict)