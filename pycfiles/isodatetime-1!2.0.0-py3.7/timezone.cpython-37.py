# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/isodatetime/timezone.py
# Compiled at: 2019-01-30 07:03:09
# Size of source mod 2**32: 2450 bytes
"""This provides utilities for extracting the local time zone."""
import time, math

class TimeZoneFormatMode(object):
    normal = 'normal'
    reduced = 'reduced'
    extended = 'extended'


def get_local_time_zone():
    """Return the current local UTC offset in hours and minutes."""
    utc_offset_seconds = -time.timezone
    if time.localtime().tm_isdst == 1:
        if time.daylight:
            utc_offset_seconds = -time.altzone
    utc_offset_minutes = utc_offset_seconds // 60 % 60
    utc_offset_hours = math.floor(utc_offset_seconds / float(3600)) if utc_offset_seconds > 0 else math.ceil(utc_offset_seconds / float(3600))
    return (int(utc_offset_hours), utc_offset_minutes)


def get_local_time_zone_format(tz_fmt_mode=TimeZoneFormatMode.normal):
    """Return a string denoting the current local UTC offset.

    :param tz_fmt_mode:
    :type tz_fmt_mode: TimeZoneFormat:
    """
    utc_offset_hours, utc_offset_minutes = get_local_time_zone()
    if utc_offset_hours == 0:
        if utc_offset_minutes == 0:
            return 'Z'
    reduced_timezone_template = '%s%02d'
    timezone_template = '%s%02d%02d'
    if tz_fmt_mode == TimeZoneFormatMode.extended:
        timezone_template = '%s%02d:%02d'
    sign = '-' if (utc_offset_hours < 0 or utc_offset_minutes < 0) else '+'
    if tz_fmt_mode == TimeZoneFormatMode.reduced:
        if utc_offset_minutes == 0:
            return reduced_timezone_template % (sign, abs(utc_offset_hours))
    return timezone_template % (
     sign, abs(utc_offset_hours), abs(utc_offset_minutes))