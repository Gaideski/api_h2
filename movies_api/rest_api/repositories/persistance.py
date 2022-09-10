import jaydebeapi
from models.movies_schema import moviesSchema
import os
from marshmallow.decorators import post_load
from etl.csv_extractor import get_case_query, get_database_creation_query

class SingletonConnection(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonConnection, cls).__new__(cls)
        return cls.instance

# Thanks to https://stackabuse.com/integrating-h2-with-python-and-flask/
# for the connection string and cursor load

def initialize():
    # Initialize db connecion
    conn = SingletonConnection()
    embedded_path = os.path.abspath('movies_api/database/embedded')
    exec_jar = os.path.abspath('movies_api/database/h2/bin/h2-2.1.214.jar')
    conn.connection = jaydebeapi.connect(
        "org.h2.Driver",
        "jdbc:h2:mem:test_mem",
        ["SA", ""],
        exec_jar)
    # conn.connection = jaydebeapi.connect(
    #     "org.h2.Driver",
    #     "jdbc:h2:"+embedded_path,
    #     ["SA", ""],
    #     exec_jar)
    sql = get_database_creation_query()
    sql = sql.split(";")
    for entry in sql:
        _execute(entry.strip()+';')
  
def get_conn():
    return SingletonConnection().connection

def _execute(query, returnResult=None):
    conn = SingletonConnection()
    cursor = conn.connection.cursor()
    cursor.execute(query)
    if returnResult:
        returnResult = _convert_to_schema(cursor)
    cursor.close()
    return returnResult


def close_conection():
    conn = SingletonConnection()
    conn.connection.close()

def _convert_to_schema(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record))
                         for record in cursor.fetchall()]

    return moviesSchema().load(column_and_values, many=True)


def get_all():
    return _execute("SELECT * FROM movies", returnResult=True)


def get(Id):
    return _execute("SELECT * FROM exoplanets WHERE id = {}".format(Id), returnResult=True)


def _insert_get_id(query, data, table):
    count = _execute(query, returnResult=True)
    if (len(count) > 0 and count[0]["id"] > 0):
        return count[0]["id"]

    columns = ", ".join(data.keys())
    values = ", ".join("'{}'".format(value) for value in data.values())
    count = _execute(
        "INSERT INTO {} ({}) VALUES({})".format(table, columns, values))
    print(f"New entry added to table {table}")
    return _insert_get_id(query, data, table)


@post_load
def insert_get_movie_id(movie):
    query = f"SELECT id FROM MOVIE WHERE title = '{movie['title']}' and release = {movie['release']}"
    table = 'Movie'
    return _insert_get_id(query, movie, table)


@post_load
def insert_get_movie_producer_id(movieproducer):
    query = f"""SELECT id FROM MOVIEPRODUCER WHERE idproducer={movieproducer['idproducer']}
     and idmovie={movieproducer['idmovie']}"""
    table = 'MOVIEPRODUCER'
    return _insert_get_id(query, movieproducer, table)

@post_load
def insert_get_movie_studio_id(moviestudio):
    query = f"""SELECT id FROM MOVIESTUDIO WHERE idstudio={moviestudio['idstudio']}
     and idmovie={moviestudio['idmovie']}"""
    table = 'MOVIESTUDIO'
    return _insert_get_id(query, moviestudio, table)

@post_load
def insert_get_producer_or_studio_id(producer, is_studio=None):
    table = 'STUDIO' if is_studio else 'PRODUCER'
    query = "SELECT id FROM {} WHERE name LIKE '{}'".format(
        table, producer["name"])  
    return _insert_get_id(query,producer,table)


def get_all_movies():
    count = _execute(
        f"SELECT * FROM MOVIE;", returnResult=True)
    return count


def get_all_from_table(table):
    count = _execute(
        "SELECT * FROM {};".format(table), returnResult=True)
    return count


def get_producer_id(producer):
    count = _execute(
        f"SELECT ID FROM PRODUCER WHERE NAME = {producer}", returnResult=True)
    if count[0]["count"] == 0:
        return

def get_movies_count():
    count = _execute("SELECT COUNT(*) FROM MOVIE", returnResult=True)
    return count[0]['count']

def get_case():
    count = _execute(get_case_query(),returnResult=True)
    return count
    
def get_schema_tables():
    count = _execute(
        "SHOW TABLES FROM AWARDS;", returnResult=True)
    return count
