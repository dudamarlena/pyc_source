# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\core\timezone.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
from datetime import timedelta, tzinfo

class OffsetTzInfo(tzinfo):
    """Fixed offset in minutes east from UTC"""

    def __init__(self, offset, name):
        self.offset = offset
        self.name = name
        self._offset = timedelta(minutes=offset)

    def __str__(self):
        return self.name

    def __repr__(self):
        return ('OffsetTzInfo(offset={0.offset!r}, name={0.name!r})').format(self)

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self.name

    def dst(self, dt):
        return timedelta(0)

    def __getinitargs__(self):
        return (
         self.offset, self.name)