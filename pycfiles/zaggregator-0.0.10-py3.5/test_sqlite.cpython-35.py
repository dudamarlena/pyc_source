# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/tests/test_sqlite.py
# Compiled at: 2018-06-25 06:56:20
# Size of source mod 2**32: 901 bytes
import unittest, logging, inspect, sqlite3, zaggregator.sqlite as sqlite
sqlite.DBPATH = ':memory:'
sqlite.__init__(sqlite.DBPATH)
import zaggregator.tests as tests

class TestSqliteModule(tests.TestCase):
    records = (('test0', 1, 2, 10, 41, 10.0), ('test1', 5, 2, 11, 42, 11.0), ('test2', 6, 8, 13, 43, 12.0),
               ('test3', 7, 9, 12, 44, 13.0))

    def test_db(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        self.assertTrue(type(sqlite.db) == sqlite3.Connection)

    def test_add_get_record(self):
        for r in self.records:
            sqlite.add_record(r)

    def test_get_bundle_names(self):
        names = sqlite.get_bundle_names()
        self.assertTrue(names == [r[0] for r in self.records])


if __name__ == '__main__':
    run_test_module_by_name(__file__)