# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ivan/release/sqlitedict/tests/test_named_db.py
# Compiled at: 2017-10-18 05:34:28
import tempfile, unittest, sqlitedict
from test_temp_db import TempSqliteDictTest
from test_core import TestCaseBackport
from accessories import norm_file

class InMemorySqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        self.d = sqlitedict.SqliteDict(filename=':memory:', autocommit=True)

    def tearDown(self):
        self.d.terminate()


class NamedSqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        db = norm_file('tests/db/sqlitedict-with-def.sqlite')
        self.d = sqlitedict.SqliteDict(filename=db)


class CreateNewSqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        db = norm_file('tests/db/sqlitedict-with-n-flag.sqlite')
        self.d = sqlitedict.SqliteDict(filename=db, flag='n')

    def tearDown(self):
        self.d.terminate()


class StartsWithEmptySqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        db = norm_file('tests/db/sqlitedict-with-w-flag.sqlite')
        self.d = sqlitedict.SqliteDict(filename=db, flag='w')

    def tearDown(self):
        self.d.terminate()


class SqliteDictAutocommitTest(TempSqliteDictTest):

    def setUp(self):
        db = norm_file('tests/db/sqlitedict-autocommit.sqlite')
        self.d = sqlitedict.SqliteDict(filename=db, autocommit=True)

    def tearDown(self):
        self.d.terminate()