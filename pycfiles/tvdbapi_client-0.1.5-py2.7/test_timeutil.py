# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.6.0-i686/egg/tvdbapi_client/tests/test_timeutil.py
# Compiled at: 2015-06-28 01:13:41
from __future__ import print_function
import datetime
from tvdbapi_client.tests import base
from tvdbapi_client import timeutil
MINS_15 = datetime.timedelta(minutes=15)
MINS_30 = datetime.timedelta(minutes=30)
MINS_45 = datetime.timedelta(minutes=45)
ONE_HOUR = datetime.timedelta(minutes=60)

class TimeutilTest(base.BaseTest):

    def test_is_older_than(self):
        now = timeutil.utcnow()
        before = now - MINS_15
        self.assertFalse(timeutil.is_older_than(before, timeutil.ONE_HOUR))
        before = now - MINS_30
        self.assertFalse(timeutil.is_older_than(before, timeutil.ONE_HOUR))
        before = now - MINS_45
        self.assertFalse(timeutil.is_older_than(before, timeutil.ONE_HOUR))
        before = now - ONE_HOUR
        self.assertTrue(timeutil.is_older_than(before, timeutil.ONE_HOUR))

    def test_is_newer_than(self):
        now = timeutil.utcnow()
        after = now + MINS_15
        self.assertFalse(timeutil.is_newer_than(after, timeutil.ONE_HOUR))
        after = now + MINS_30
        self.assertFalse(timeutil.is_newer_than(after, timeutil.ONE_HOUR))
        after = now + MINS_45
        self.assertFalse(timeutil.is_newer_than(after, timeutil.ONE_HOUR))
        after = now + ONE_HOUR
        self.assertTrue(timeutil.is_newer_than(after, timeutil.ONE_HOUR))