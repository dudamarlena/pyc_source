# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/test/snapshot_test.py
# Compiled at: 2011-05-31 11:44:21
import unittest
from linseed import Snapshot

class Test(unittest.TestCase):

    def setUp(self):
        self.s = Snapshot()

    def test_api(self):
        self.s.keys()
        self.s.items()
        self.s.values()
        len(self.s)
        for k in self.s:
            self.s[k]