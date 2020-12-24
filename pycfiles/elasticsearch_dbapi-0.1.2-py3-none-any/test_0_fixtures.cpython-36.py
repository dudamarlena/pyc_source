# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpgaspar/workarea/preset/elasticsearch-dbapi/es/tests/test_0_fixtures.py
# Compiled at: 2019-11-05 12:13:17
# Size of source mod 2**32: 486 bytes
import os, unittest
from .fixtures.fixtures import delete_index, import_data1, import_flights
BASE_URL = 'http://localhost:9200'

class TestData(unittest.TestCase):

    def setUp(self):
        self.base_url = os.environ.get('ES_URI', BASE_URL)

    def test_data_flights(self):
        delete_index(self.base_url, 'flights')
        import_flights(self.base_url)

    def test_data_data1(self):
        delete_index(self.base_url, 'data1')
        import_data1(self.base_url)