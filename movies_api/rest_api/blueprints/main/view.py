from types import NoneType
from flask import Blueprint
from repositories.persistance import get_all_from_table, get_schema_tables
from flask import request
from etl.case import Case
main = Blueprint('main', __name__, template_folder='blueprints/main')


@main.route("/",methods=["GET"])
def index():
    case = Case()
    serialized = case.get_structured_data()
    return serialized


@main.route("/list-table",methods=["GET"])
def list_table():
    possible_tables = get_schema_tables()
    get_type = request.args.get('type', type=str)
    if type(get_type) is NoneType:
        return [{'Message':"Error"},{"Type argument must be provided with one of the following table_name's": possible_tables}]
    get_type = [entry for entry in possible_tables if get_type.upper()
                == entry['table_name']]                
    if (len(get_type) > 0):
        return get_all_from_table(get_type[0]['table_name'])
    else:
        return [{'Message':"Error"},{"Available tables": possible_tables}]
