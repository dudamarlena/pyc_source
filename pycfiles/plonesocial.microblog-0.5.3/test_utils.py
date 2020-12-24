# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/tests/test_utils.py
# Compiled at: 2013-04-12 05:54:49
import time, unittest2 as unittest
from BTrees.LLBTree import LLTreeSet
from plonesocial.microblog.utils import longkeysortreverse

class TestLongkeysortreverse(unittest.TestCase):

    def setUp(self):
        self.treeset = LLTreeSet()
        self.k0 = long(1)
        self.treeset.insert(self.k0)
        self.k1 = long((time.time() - 3700) * 1000000.0)
        self.treeset.insert(self.k1)
        self.k2 = self.k1 + 1
        self.treeset.insert(self.k2)
        self.k3 = self.k2 + 1
        self.treeset.insert(self.k3)
        self.k10 = long(time.time() * 1000000.0 - 10)
        self.treeset.insert(self.k10)
        self.k11 = self.k10 + 1
        self.treeset.insert(self.k11)

    def test_all(self):
        values = list(longkeysortreverse(self.treeset))
        expect = [self.k11, self.k10, self.k3, self.k2, self.k1, self.k0]
        self.assertEquals(values, expect)

    def test_min_hour(self):
        minv = long((time.time() - 3600) * 1000000.0)
        values = list(longkeysortreverse(self.treeset, minv=minv))
        expect = [self.k11, self.k10]
        self.assertEquals(values, expect)

    def test_max_hour(self):
        maxv = long((time.time() - 3600) * 1000000.0)
        values = list(longkeysortreverse(self.treeset, maxv=maxv))
        expect = [self.k3, self.k2, self.k1, self.k0]
        self.assertEquals(values, expect)

    def test_min_day(self):
        minv = long((time.time() - 86400) * 1000000.0)
        values = list(longkeysortreverse(self.treeset, minv=minv))
        expect = [self.k11, self.k10, self.k3, self.k2, self.k1]
        self.assertEquals(values, expect)

    def test_max_day(self):
        maxv = long((time.time() - 86400) * 1000000.0)
        values = list(longkeysortreverse(self.treeset, maxv=maxv))
        expect = [self.k0]
        self.assertEquals(values, expect)

    def test_min_day_max_hour(self):
        maxv = long((time.time() - 3600) * 1000000.0)
        minv = long((time.time() - 86400) * 1000000.0)
        values = list(longkeysortreverse(self.treeset, minv=minv, maxv=maxv))
        expect = [self.k3, self.k2, self.k1]
        self.assertEquals(values, expect)

    def test_all_limit(self):
        values = list(longkeysortreverse(self.treeset, limit=3))
        expect = [self.k11, self.k10, self.k3]
        self.assertEquals(values, expect)

    def test_min_day_max_hour_limit(self):
        maxv = long((time.time() - 3600) * 1000000.0)
        minv = long((time.time() - 86400) * 1000000.0)
        values = list(longkeysortreverse(self.treeset, minv=minv, maxv=maxv, limit=1))
        expect = [self.k3]
        self.assertEquals(values, expect)