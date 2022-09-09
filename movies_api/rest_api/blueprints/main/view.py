from pickle import GET
from flask import Blueprint
from repositories.persistance import get_all_from_table, get_schema_tables
from flask import request
from etl.case import Case
main = Blueprint('main', __name__, template_folder='blueprints/main')


@main.route("/")
def index():
    case = Case()
    serialized = case.get_structured_data()
    return serialized


@main.route("/list-table")
def list_table():
    possible_tables = get_schema_tables()
    get_type = request.args.get('type', default='movie', type=str)
    get_type = [entry for entry in possible_tables if get_type.upper()
                == entry['table_name']]                
    if (len(get_type) > 0):
        return get_all_from_table(get_type[0]['table_name'])
