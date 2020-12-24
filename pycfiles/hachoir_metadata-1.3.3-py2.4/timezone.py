# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_metadata/timezone.py
# Compiled at: 2009-09-07 17:44:28
from datetime import tzinfo, timedelta

class TimezoneUTC(tzinfo):
    """UTC timezone"""
    __module__ = __name__
    ZERO = timedelta(0)

    def utcoffset(self, dt):
        return TimezoneUTC.ZERO

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        return TimezoneUTC.ZERO

    def __repr__(self):
        return "<TimezoneUTC delta=0, name=u'UTC'>"


class Timezone(TimezoneUTC):
    """Fixed offset in hour from UTC."""
    __module__ = __name__

    def __init__(self, offset):
        self._offset = timedelta(minutes=offset * 60)
        self._name = '%+03u00' % offset

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self._name

    def __repr__(self):
        return "<Timezone delta=%s, name='%s'>" % (self._offset, self._name)


UTC = TimezoneUTC()

def createTimezone(offset):
    if offset:
        return Timezone(offset)
    else:
        return UTC