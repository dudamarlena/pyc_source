# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/lib/timehelpers.py
# Compiled at: 2011-02-18 19:15:09
from datetime import tzinfo, datetime, timedelta

class GMT2(tzinfo):

    def __init__(self):
        dt = datetime.now()
        d = datetime(dt.year, 4, 1)
        self.dston = d - timedelta(days=d.weekday() + 1)
        d = datetime(dt.year, 11, 1)
        self.dstoff = d - timedelta(days=d.weekday() + 1)

    def utcoffset(self, dt):
        return timedelta(hours=1) + self.dst(dt)

    def dst(self, dt):
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=2)
        else:
            return timedelta(0)
            return

    def tzname(self, dt):
        return 'GMT +2'


def now():
    tz = GMT2()
    now = datetime.now(tz)
    return now