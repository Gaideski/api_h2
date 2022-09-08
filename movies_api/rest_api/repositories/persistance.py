
import jaydebeapi
from models.movies_schema import moviesSchema, movieProducerSchema, producerSchema, studioSchema
import os
from marshmallow.decorators import post_load


def initialize():
    _execute(
        ("CREATE TABLE IF NOT EXISTS exoplanets ("
         "  id INT PRIMARY KEY AUTO_INCREMENT,"
         "  name VARCHAR NOT NULL,"
         "  year_discovered SIGNED,"
         "  light_years FLOAT,"
         "  mass FLOAT,"
         "  link VARCHAR)"))


def _execute(query, returnResult=None):
    embedded_path = os.path.abspath('database\embedded')
    exec_jar = os.path.abspath('database\h2\\bin\h2-2.1.214.jar')
    connection = jaydebeapi.connect(
        "org.h2.Driver",
        "jdbc:h2:"+embedded_path,
        ["SA", ""],
        exec_jar)
    cursor = connection.cursor()
    cursor.execute('use awards;')
    cursor.execute(query)
    if returnResult:
        returnResult = _convert_to_schema(cursor)
    cursor.close()
    connection.close()

    return returnResult


def _convert_to_schema(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record))
                         for record in cursor.fetchall()]

    return moviesSchema().load(column_and_values, many=True)


def get_all():
    return _execute("SELECT * FROM movies", returnResult=True)


def get(Id):
    return _execute("SELECT * FROM exoplanets WHERE id = {}".format(Id), returnResult=True)


def create(exoplanet):
    count = _execute("SELECT count(*) AS count FROM exoplanets WHERE name LIKE '{}'".format(
        exoplanet.get("name")), returnResult=True)
    if count[0]["count"] > 0:
        return

    columns = ", ".join(exoplanet.keys())
    values = ", ".join("'{}'".format(value) for value in exoplanet.values())
    _execute("INSERT INTO exoplanets ({}) VALUES({})".format(columns, values))

    return {}


def update(exoplanet, Id):
    count = _execute(
        "SELECT count(*) AS count FROM exoplanets WHERE id = {}".format(Id), returnResult=True)
    if count[0]["count"] == 0:
        return

    values = ["'{}'".format(value) for value in exoplanet.values()]
    update_values = ", ".join("{} = {}".format(key, value)
                              for key, value in zip(exoplanet.keys(), values))
    _execute("UPDATE exoplanets SET {} WHERE id = {}".format(update_values, Id))

    return {}


@post_load
def insert_get_producer_or_studio_id(producer, is_studio=None):
    table = 'STUDIO' if is_studio else 'PRODUCER'
    count = _execute("SELECT id FROM {} WHERE name LIKE '{}'".format(
        table,producer["name"]), returnResult=True)
    if (len(count) > 0 and count[0]["id"] > 0):
        return count[0]["id"]

    columns = ", ".join(producer.keys())
    values = ", ".join("'{}'".format(value) for value in producer.values())
    count = _execute(
        "INSERT INTO {} ({}) VALUES({})".format(table,columns, values))
    return insert_get_producer_or_studio_id(producer,is_studio)


def get_producer_id(producer):
    count = _execute(
        f"SELECT ID FROM PRODUCER WHERE NAME = {producer}", returnResult=True)
    if count[0]["count"] == 0:
        return


def delete(Id):
    count = _execute(
        "SELECT count(*) AS count FROM exoplanets WHERE id = {}".format(Id), returnResult=True)
    if count[0]["count"] == 0:
        return

    _execute("DELETE FROM exoplanets WHERE id = {}".format(Id))
    return {}
