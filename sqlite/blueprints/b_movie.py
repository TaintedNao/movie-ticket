from flask import request, Blueprint
import sqlite3
import json
from variables import *
import queries.movie as mo

movie_blueprint = Blueprint('/movie/', __name__)


@movie_blueprint.route('/movie/create_movie', methods=['POST'])
def create_movie():

    # json request
    rq = request.json

    # Create a new ticket using the create_ticket func
    # Using a with statement because once it exits the statement the connection will automatically close
    with sqlite3.connect(DB_FILE) as connection:
        result = mo.create_movie(
            rq['showtime'],
            rq['description'],
            rq['theatre'],
            rq['rating'],
            rq['remaining_seats'],
            connection
        )

    # Handle the result
    if result[0] == True:
        ret_dict = {'TYPE': 'success', 'MESSAGE': "Movie created."}
        return json.dumps(ret_dict)
    elif result[1] == 'movie_exists':
        ret_dict = {'TYPE': 'error', 'MESSAGE': "Movie already exists"}
        return json.dumps(ret_dict)
    else:
        ret_dict = {'TYPE': 'error', 'MESSAGE': "Server error!!"}
        return json.dumps(ret_dict)