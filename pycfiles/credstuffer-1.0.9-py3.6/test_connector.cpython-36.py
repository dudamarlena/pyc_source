# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/test/db/test_connector.py
# Compiled at: 2019-12-19 17:10:46
# Size of source mod 2**32: 879 bytes
import unittest, psycopg2
from credstuffer.db.connector import DBConnector

class TestDBConnector(unittest.TestCase):

    def setUp(self) -> None:
        self.connector = DBConnector()
        self.connector.connect_psycopg(host='127.0.0.1', port=5432, username='postgres', password='postgres', dbname='postgres')

    def test_get_cursor(self):
        with self.connector.get_cursor() as (cursor):
            self.assertIsInstance(cursor, (psycopg2.extensions.cursor), msg='cursor must be type of psycopg2.extensions.cursor')

    def test_get_conn(self):
        with self.connector.get_conn() as (conn):
            self.assertIsInstance(conn, (psycopg2.extensions.connection), msg='conn must be type of psycopg2.extensions.connection')

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()