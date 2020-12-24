# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/convertish/util.py
# Compiled at: 2010-02-16 12:03:01
"""
General support and utility module.
"""
from datetime import timedelta, tzinfo

class SimpleTZInfo(tzinfo):
    """
    Simple concrete datetime.tzinfo class that handles only
    offset in minutes form UTC.
    """

    def __init__(self, minutes):
        self.minutes = minutes

    def utcoffset(self, dt):
        return timedelta(minutes=self.minutes)

    def dst(self, dt):
        return timedelta()

    def tzname(self, dt):
        if self.minutes < 0:
            sign = '-'
            (hours, minutes) = divmod(-self.minutes, 60)
        else:
            sign = '+'
            (hours, minutes) = divmod(self.minutes, 60)
        return '%s%02d:%02d' % (sign, hours, minutes)