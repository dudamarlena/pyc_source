# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/collection/test_ubound.py
# Compiled at: 2011-03-19 21:05:04
import unittest
from chula import collection
from chula.collection import ubound
from chula.error import *

class Test_ubound_collection(unittest.TestCase):
    doctest = ubound

    def _fetch_by_key(self, key):
        return self.collection[key]

    def setUp(self):
        self.collection = collection.UboundCollection(5)
        self.collection.a = 1
        self.collection.b = 2
        self.collection.c = 3
        self.collection.d = 4
        self.collection.e = 5

    def tearDown(self):
        pass

    def test_initial_length(self):
        self.collection = collection.UboundCollection(5)
        self.assertEquals(0, len(self.collection))

    def test_allows_specified_max_records(self):
        self.assertEquals(5, len(self.collection))
        self.assertEquals(1, self.collection.a)

    def test_purging_does_purge_FIFO_by_attr(self):
        self.collection.f = 6
        self.assertEquals(5, len(self.collection))
        self.assertRaises(KeyError, self._fetch_by_key, 'a')

    def test_purging_does_purge_FIFO_by_key(self):
        self.collection['f'] = 6
        self.assertEquals(5, len(self.collection))
        self.assertRaises(KeyError, self._fetch_by_key, 'a')