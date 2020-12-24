# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/shared/tests/test_time.py
# Compiled at: 2016-11-12 07:38:04
import unittest
from datetime import datetime
from beeswarm.shared.misc.time import isoformatToDatetime

class TimeTests(unittest.TestCase):

    def test_isoFormatToDateTime(self):
        no_microseconds = datetime(2016, 11, 12, 11, 47, 20, 0)
        no_microseconds_isoformat = no_microseconds.isoformat()
        self.assertEquals(isoformatToDatetime(no_microseconds_isoformat), no_microseconds)
        has_microseconds = datetime(2016, 11, 12, 11, 47, 20, 4242)
        has_microseconds_isoformat = has_microseconds.isoformat()
        self.assertEquals(isoformatToDatetime(has_microseconds_isoformat), has_microseconds)