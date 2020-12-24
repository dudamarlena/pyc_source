# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/test/db/test_connector.py
# Compiled at: 2020-03-29 20:59:07
# Size of source mod 2**32: 880 bytes
import unittest, psycopg2
from ComunioScore.db.connector import DBConnector

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