import pandas as pd
from models.movies_schema import *
from repositories.persistance import insert_get_producer_or_studio_id, initialize
from repositories.persistance import insert_get_movie_id, insert_get_movie_producer_id
from repositories.persistance import insert_get_movie_studio_id


def insert_database_data(df):
    initialize()
    movies_added=0
    df = df.reset_index()
    for index, row in df.iterrows():
        producers_id = insert_producers_or_studio(
            row['producers'].replace("'", "''"))
        studios_id = insert_producers_or_studio(
            row['studios'].replace("'", "''"), is_studio=True)
        movie_id = insert_movie({'release': row['year'],
                                 'title': row['title'].replace("'", "''"),
                                 'winner': row['winner'] if not pd.isna(row['winner']) else False
                                 })
        movieproducer_id = insert_movie_producer(producers_id, movie_id)
        moviestudio_id = insert_movie_studio(studios_id, movie_id)
        movies_added+=1
        print('one row!')
    return movies_added

def insert_movie_studio(list_studio_id, movie_id):
    movieproducer_id = []
    for studio_id in list_studio_id:
        moviestudio = {'idstudio': studio_id, 'idmovie': movie_id}
        schema = movieStudioSchema().dump(moviestudio)
        movieproducer_id.append(insert_get_movie_studio_id(schema))
    return movieproducer_id


def insert_movie_producer(list_producers_id, movie_id):
    moviestudio_id = []
    for producer_id in list_producers_id:
        movieproducer = {'idproducer': producer_id, 'idmovie': movie_id}
        schema = movieProducerSchema().dump(movieproducer)
        moviestudio_id.append(insert_get_movie_producer_id(schema))
    return movie_id


def insert_movie(movie):
    ms = moviesSchema().dump(movie)
    return insert_get_movie_id(ms)


def insert_producers_or_studio(value, is_studio=None):
    data = [s.strip() for s in value.replace(' and ', ',').split(',')]
    data_id = []
    for name in data:
        if not name:
            continue
        prod = dict(name=name)
        if is_studio:
            ps = studioSchema().dump(prod)
        else:
            ps = producerSchema().dump(prod)
        data_id.append(insert_get_producer_or_studio_id(ps, is_studio))
    return data_id
