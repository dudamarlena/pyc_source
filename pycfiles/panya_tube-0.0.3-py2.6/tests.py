# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tube/tests.py
# Compiled at: 2011-01-10 04:27:38
import unittest
from tube.models import ClipBase

class ClipBaseTestCase(unittest.TestCase):

    def test_duration_as_hours_minute_seconds(self):
        clip_base = ClipBase(duration=0)
        result = clip_base.duration_as_hours_minute_seconds
        self.failUnless(result['hours'] == 0, result)
        self.failUnless(result['minutes'] == 0, result)
        self.failUnless(result['seconds'] == 0, result)
        clip_base = ClipBase(duration=3660)
        result = clip_base.duration_as_hours_minute_seconds
        self.failUnless(result['hours'] == 1, result)
        self.failUnless(result['minutes'] == 1, result)
        self.failUnless(result['seconds'] == 0, result)
        clip_base = ClipBase(duration=3665)
        result = clip_base.duration_as_hours_minute_seconds
        self.failUnless(result['hours'] == 1, result)
        self.failUnless(result['minutes'] == 1, result)
        self.failUnless(result['seconds'] == 5, result)
        clip_base = ClipBase(duration=74564376)
        result = clip_base.duration_as_hours_minute_seconds
        self.failUnless(result['hours'] == 20712, result)
        self.failUnless(result['minutes'] == 19, result)
        self.failUnless(result['seconds'] == 36, result)