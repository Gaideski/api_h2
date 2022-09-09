import unittest
from unittest import TestCase
import sys
import os
sys.path.insert(0,os.path.abspath('movies_api/rest_api'))
from repositories.persistance import *
from repositories.persistance_insertion import insert_database_data
from etl.csv_extractor import initialize_data

class TestDatabase(TestCase):
    def test_initialize_database(self):
        initialize()
        conn = get_conn()
        status = conn._closed
        self.assertFalse(status)
        close_conection()

    def test_close_connection(self):
        initialize()
        conn = get_conn()
        close_conection()
        status = conn._closed
        self.assertTrue(status)

    def test_database_creation(self):
        initialize()
        schema = get_schema_tables()
        close_conection()
        self.assertGreater(len(schema),0)

    def test_insert_producers(self):
        initialize()
        ids = insert_get_producer_or_studio_id([{'name':'test1'},{'name':'test2'}])
        close_conection()

    def test_load_dataset(self):
        initialize()
        df = initialize_data()
        movies_added = insert_database_data(df)
        close_conection()
        self.assertEqual(movies_added,df.shape[0])

if __name__ == '__main__':
    unittest.main()