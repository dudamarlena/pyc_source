# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/test/db/test_creator.py
# Compiled at: 2020-03-29 20:59:07
# Size of source mod 2**32: 1674 bytes
import unittest
from ComunioScore.db.fetcher import DBFetcher
from ComunioScore.db.inserter import DBInserter
from ComunioScore.db.creator import DBCreator, Table, Column
from ComunioScore.db.connector import DBConnector

class TestDBCreator(unittest.TestCase):

    def setUp(self) -> None:
        DBConnector().connect_psycopg(host='127.0.0.1', port=5432, username='postgres', password='postgres', dbname='postgres')
        self.fetcher = DBFetcher()
        self.inserter = DBInserter()
        self.creator = DBCreator()
        self.creator.build(obj=(Table('test', Column(name='id', type='bigint'), Column(name='username', type='text'))))

    def test_database(self):
        pass

    def test_schema(self):
        pass

    def test_table(self):
        self.table_str = Table('test', Column(name='id', type='bigint'), Column(name='id2', type='text')).__repr__()
        self.assertIsInstance((self.table_str), str, msg='table creation must be type of string')
        self.assertEqual((self.table_str), 'create table if not exists test (id bigint , id2 text )', msg='table creation string is faulty')

    def test_column(self):
        self.colum_str = Column(name='id', type='bigint').__repr__()
        self.assertIsInstance((self.colum_str), str, msg='colum creation must be type of string')
        self.assertEqual((self.colum_str), 'id bigint ', msg='colum creation string is faulty')

    def tearDown(self) -> None:
        sql = 'delete from test'
        self.inserter.sql(sql=sql)


if __name__ == '__main__':
    unittest.main()