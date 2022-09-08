import pandas as pd
import re
from models.movies_schema import *
from repositories.persistance import insert_get_producer_or_studio_id


def insert_database_data(df):
    df = df.reset_index()
    for index, row in df.iterrows():
        producers_id = insert_producers_or_studio(row['producers'])
        studios_id = insert_producers_or_studio(row['studios'], is_studio=True)
        print('one row!')


def insert_studio(studios):
    producers = [s.strip() for s in studios.replace('and', ',').split(',')]
    producers_id = []
    for producer in producers:
        prod = dict(name=producer)
        ps = producerSchema().dump(prod)
        producers_id.append(insert_get_producer_or_studio_id(ps))
    print(producers_id)
    return producers_id


def insert_producers_or_studio(value, is_studio=None):
    data = [s.strip() for s in value.replace('and', ',').split(',')]
    data_id = []
    for name in data:
        prod = dict(name=name)
        if is_studio:
            ps = studioSchema().dump(prod)
        else:
            ps = producerSchema().dump(prod)
        data_id.append(insert_get_producer_or_studio_id(ps, is_studio))
    print(data_id)
    return data_id
