# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/convertish/tests/test_util.py
# Compiled at: 2010-02-16 12:03:01
from datetime import time, timedelta
import unittest
from convertish.util import SimpleTZInfo

class TestSimpleTZInfo(unittest.TestCase):

    def test_utcoffset(self):
        self.assertEquals(SimpleTZInfo(60).utcoffset(None), timedelta(minutes=60))
        self.assertEquals(SimpleTZInfo(-60).utcoffset(None), timedelta(minutes=-60))
        return

    def test_dst(self):
        tz = SimpleTZInfo(60)
        self.assertEquals(tz.dst(None), timedelta())
        return

    def test_tzname(self):
        self.assertEquals(SimpleTZInfo(0).tzname(None), '+00:00')
        self.assertEquals(SimpleTZInfo(60).tzname(None), '+01:00')
        self.assertEquals(SimpleTZInfo(90).tzname(None), '+01:30')
        self.assertEquals(SimpleTZInfo(-60).tzname(None), '-01:00')
        self.assertEquals(SimpleTZInfo(-90).tzname(None), '-01:30')
        return

    def test_affect(self):
        self.assertEquals(time(1, 2, 3, 0, SimpleTZInfo(0)).isoformat(), '01:02:03+00:00')
        self.assertEquals(time(1, 2, 3, 0, SimpleTZInfo(90)).isoformat(), '01:02:03+01:30')
        self.assertEquals(time(1, 2, 3, 0, SimpleTZInfo(-90)).isoformat(), '01:02:03-01:30')