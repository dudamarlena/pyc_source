# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/test/db/test_fetcher.py
# Compiled at: 2020-03-29 20:59:07
# Size of source mod 2**32: 1900 bytes
import unittest
from ComunioScore.db.fetcher import DBFetcher
from ComunioScore.db.inserter import DBInserter
from ComunioScore.db.creator import DBCreator, Table, Column
from ComunioScore.db.connector import DBConnector

class TestDBFetcher(unittest.TestCase):

    def setUp(self) -> None:
        DBConnector().connect_psycopg(host='127.0.0.1', port=5432, username='postgres', password='postgres', dbname='postgres')
        self.fetcher = DBFetcher()
        self.inserter = DBInserter()
        self.creator = DBCreator()
        self.creator.build(obj=(Table('test', Column(name='id', type='bigint'), Column(name='username', type='text'))))
        sql = 'insert into test (id, username) values (%s, %s)'
        self.inserter.many_rows(sql=sql, datas=[(0, 'abc'), (1, 'def'), (2, 'ghi')])

    def test_one(self):
        sql = 'select * from test'
        one_row = self.fetcher.one(sql=sql)
        self.assertIsInstance(one_row, tuple, msg='one row must be of type tuple')
        self.assertEqual((one_row[0]), 0, msg='first element in one_row must be 0')
        self.assertEqual((one_row[1]), 'abc', msg="second element in one_row must be 'abc'")

    def test_many(self):
        sql = 'select * from test'
        rows = self.fetcher.many(sql=sql, size=2)
        self.assertIsInstance(rows, list, msg='rows must be of type tuple')
        self.assertEqual((len(rows)), 2, msg='rows must be of length 2')

    def test_all(self):
        sql = 'select * from test'
        all = self.fetcher.all(sql=sql)
        self.assertIsInstance(all, list, msg='rows must be of type tuple')
        self.assertEqual((len(all)), 3, msg='rows must be of length 2')

    def tearDown(self) -> None:
        sql = 'delete from test'
        self.inserter.sql(sql=sql)


if __name__ == '__main__':
    unittest.main()