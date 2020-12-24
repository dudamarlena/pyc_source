# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/tzinfo.py
# Compiled at: 2018-07-11 18:15:30
"""Implementation of tzinfo classes for use with datetime.datetime."""
from __future__ import unicode_literals
import time
from datetime import timedelta, tzinfo
from django.utils.encoding import force_str, force_text, DEFAULT_LOCALE_ENCODING

class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset):
        if isinstance(offset, timedelta):
            self.__offset = offset
            offset = self.__offset.seconds // 60
        else:
            self.__offset = timedelta(minutes=offset)
        sign = b'-' if offset < 0 else b'+'
        self.__name = b'%s%02d%02d' % (sign, abs(offset) / 60.0, abs(offset) % 60)

    def __repr__(self):
        return self.__name

    def __getinitargs__(self):
        return (
         self.__offset,)

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return timedelta(0)


class LocalTimezone(tzinfo):
    """Proxy timezone information from time module."""

    def __init__(self, dt):
        tzinfo.__init__(self)
        self.__dt = dt
        self._tzname = self.tzname(dt)

    def __repr__(self):
        return force_str(self._tzname)

    def __getinitargs__(self):
        return (
         self.__dt,)

    def utcoffset(self, dt):
        if self._isdst(dt):
            return timedelta(seconds=-time.altzone)
        else:
            return timedelta(seconds=-time.timezone)

    def dst(self, dt):
        if self._isdst(dt):
            return timedelta(seconds=-time.altzone) - timedelta(seconds=-time.timezone)
        else:
            return timedelta(0)

    def tzname(self, dt):
        try:
            return force_text(time.tzname[self._isdst(dt)], DEFAULT_LOCALE_ENCODING)
        except UnicodeDecodeError:
            return

        return

    def _isdst(self, dt):
        tt = (
         dt.year, dt.month, dt.day,
         dt.hour, dt.minute, dt.second,
         dt.weekday(), 0, 0)
        try:
            stamp = time.mktime(tt)
        except (OverflowError, ValueError):
            tt = (2037, ) + tt[1:]
            stamp = time.mktime(tt)

        tt = time.localtime(stamp)
        return tt.tm_isdst > 0