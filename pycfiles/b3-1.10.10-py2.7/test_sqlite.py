# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\storage\test_sqlite.py
# Compiled at: 2016-03-08 18:42:10
import nose
from b3.functions import splitDSN
from b3.storage.sqlite import SqliteStorage
from tests import B3TestCase
from tests.core.storage.common import StorageAPITest
SQLITE_DB = ':memory:'

class Test_sqlite(B3TestCase, StorageAPITest):

    def setUp(self):
        """this method is called before each test"""
        B3TestCase.setUp(self)
        self.storage = self.console.storage = SqliteStorage('sqlite://' + SQLITE_DB, splitDSN('sqlite://' + SQLITE_DB), self.console)
        self.storage.connect()

    def tearDown(self):
        """this method is called after each test"""
        B3TestCase.tearDown(self)
        self.storage.shutdown()

    def test_getTables(self):
        self.assertSetEqual(set([
         'sqlite_sequence',
         'aliases',
         'ipaliases',
         'clients',
         'groups',
         'penalties',
         'data']), set(self.storage.getTables()))


if __name__ == '__main__':
    nose.main()