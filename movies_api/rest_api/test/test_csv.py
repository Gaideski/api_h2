import unittest
from unittest import TestCase
import sys
import os
sys.path.insert(0, os.path.abspath('movies_api/rest_api'))
from etl.csv_extractor import *


class TestCSV(TestCase):
    def test_locate_csv(self):
        csv_list = list_csv()
        self.assertGreater(len(csv_list), 0)

    def test_load_csv(self):
        csv_list = list_csv()
        df = load_csv(csv_list[0])
        self.assertFalse(df.empty)

    
if __name__ == '__main__':
    unittest.main()
