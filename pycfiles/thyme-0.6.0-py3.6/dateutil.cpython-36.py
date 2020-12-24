# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thyme/util/dateutil.py
# Compiled at: 2020-04-06 09:21:33
# Size of source mod 2**32: 1394 bytes
"""
Helpful utilities for working with datetime values.
"""
import datetime
from enum import Enum, auto

class DatetimeRounding(Enum):
    __doc__ = 'An enumeration for types of datetime rounding'
    NEAREST_HOUR = auto()
    NEAREST_MINUTE = auto()


def round(dt, rounding=None):
    """Round a datetime value using specified rounding method.

    Args:
        dt: `datetime` value to be rounded.
        rounding: `DatetimeRounding` value representing rounding method.
    """
    if rounding is DatetimeRounding.NEAREST_HOUR:
        return round_to_hour(dt)
    else:
        if rounding is DatetimeRounding.NEAREST_MINUTE:
            return round_to_minute(dt)
        return dt


def round_to_hour(dt):
    """Round `datetime` value to nearest hour.

    Args:
        dt: `datetime` value to be rounded.

    Returns:
        Rounded `datetime` value.
    """
    base_dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0)
    if dt.minute >= 30:
        return base_dt + datetime.timedelta(hours=1)
    else:
        return base_dt


def round_to_minute(dt):
    """Round `datetime` value to nearest minute.

    Args:
        dt: `datetime` value to be rounded.

    Returns:
        Rounded `datetime` value.
    """
    base_dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0)
    if dt.second >= 30:
        return base_dt + datetime.timedelta(minutes=1)
    else:
        return base_dt