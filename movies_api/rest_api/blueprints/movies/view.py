from flask import Blueprint
from repositories.persistance import get_all_from_table
from flask import request

movies = Blueprint('movies', __name__)


@movies.route("/movies")
def index():    
    return get_all_from_table('MOVIE')
