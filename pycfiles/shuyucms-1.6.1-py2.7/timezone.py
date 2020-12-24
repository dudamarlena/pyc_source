# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/utils/timezone.py
# Compiled at: 2016-05-20 23:26:47
from __future__ import unicode_literals
import datetime, time, pytz, tzlocal

def get_best_local_timezone():
    """
    Compares local timezone offset to pytz's timezone db, to determine
    a matching timezone name to use when TIME_ZONE is not set.
    """
    zone_name = tzlocal.get_localzone().zone
    if zone_name in pytz.all_timezones:
        return zone_name
    if time.daylight:
        local_offset = time.altzone
        localtz = time.tzname[1]
    else:
        local_offset = time.timezone
        localtz = time.tzname[0]
    local_offset = datetime.timedelta(seconds=-local_offset)
    for zone_name in pytz.all_timezones:
        timezone = pytz.timezone(zone_name)
        if not hasattr(timezone, b'_tzinfos'):
            continue
        for utcoffset, daylight, tzname in timezone._tzinfos:
            if utcoffset == local_offset and tzname == localtz:
                return zone_name