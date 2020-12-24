# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/db/test_sqlite.py
# Compiled at: 2011-03-19 21:05:04
import unittest
from chula.error import *
from chula.db import datastore
from chula.db.engines import sqlite

class Test_sqlite(unittest.TestCase):
    doctest = sqlite

    def setUp(self):
        self.db = datastore.DataStoreFactory('sqlite:memory')
        self.cursor = self.db.cursor()

    def tearDown(self):
        self.cursor.close()
        self.db.close()

    def test_default_isolation_level(self):
        self.assertEquals(None, self.db.conn.isolation_level)
        return

    def test_invalid_isolation_level(self):
        self.assertEquals(3, 3)
        self.assertRaises(InvalidAttributeError, self.db.set_isolation, 'awesome')

    def test_specified_isolation_level(self):
        isolation = 'DEFERRED'
        db = datastore.DataStoreFactory('sqlite:memory', isolation=isolation)
        self.assertEquals(isolation, db.conn.isolation_level)