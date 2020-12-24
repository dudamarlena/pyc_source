# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/packagetrack/tests/test_tracking_info.py
# Compiled at: 2010-06-21 16:23:10
from datetime import datetime, date
from unittest import TestCase
from packagetrack.data import TrackingInfo

class TestTrackingInfo(TestCase):

    def test_repr(self):
        now = datetime.now()
        today = date.today()
        info = TrackingInfo(delivery_date=today, status='IN TRANSIT', last_update=now)
        s = repr(info)
        assert repr(now) in s
        assert repr(today) in s
        assert 'IN TRANSIT' in s