# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cltwit/utils.py
# Compiled at: 2013-02-02 15:46:21
__doc__ = "\nClasses utilisées par cltwit\nLocalTimezone : pour convertir une heure en fonction de l'heure locale\n"
import time as _time
from datetime import tzinfo, timedelta
ZERO = timedelta(0)
HOUR = timedelta(hours=1)
STDOFFSET = timedelta(seconds=-_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds=-_time.altzone)
else:
    DSTOFFSET = STDOFFSET
DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(tzinfo):
    u""" Utilisée pour convertir un datetime en fonction de l'heure locale """

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (
         dt.year, dt.month, dt.day,
         dt.hour, dt.minute, dt.second,
         dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0