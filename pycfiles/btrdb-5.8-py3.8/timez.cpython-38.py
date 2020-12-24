# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/utils/timez.py
# Compiled at: 2019-09-30 18:27:35
# Size of source mod 2**32: 7233 bytes
"""
Time related utilities
"""
from datetime import datetime
from operator import mul
from decimal import Decimal
import pytz
DATETIME_FORMATS = ('%Y-%m-%d %H:%M:%S.%f%z', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S.%fZ',
                    '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S.%f',
                    '%Y-%m-%d %H:%M:%S%z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d')

def currently_as_ns():
    """
    Returns the current UTC time as nanoseconds since epoch
    """
    dt = datetime.utcnow()
    return int(dt.replace(tzinfo=(pytz.utc)).timestamp() * 1000000000.0)


def ns_to_datetime(ns):
    """
    Converts nanoseconds to a datetime object (UTC)

    Parameters
    ----------
    ns : int
        nanoseconds since epoch

    Returns
    -------
    nanoseconds since epoch as a datetime object : datetime

    """
    dt = datetime.utcfromtimestamp(ns / 1000000000.0)
    return dt.replace(tzinfo=(pytz.utc))


def datetime_to_ns(dt):
    """
    Converts a datetime object to nanoseconds since epoch.  If a timezone aware
    object is received then it will be converted to UTC.

    Parameters
    ----------
    dt : datetime

    Returns
    -------
    nanoseconds : int

    """
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        aware = pytz.utc.localize(dt)
    else:
        aware = dt
    dt_utc = aware.astimezone(pytz.utc)
    return int(dt_utc.timestamp() * 1000000000.0)


def to_nanoseconds(val):
    """
    Converts datetime, datetime64, float, str (RFC 2822) to nanoseconds.  If a
    datetime-like object is received then nanoseconds since epoch is returned.

    Parameters
    ----------
    val : datetime, datetime64, float, str
        an object to convert to nanoseconds

    Returns
    -------
    object converted to nanoseconds : int

    Notes
    ----
    The following string formats are supported for conversion.

    +--------------------------------+------------------------------------------+
    | Format String                  | Description                              |
    +================================+==========================================+
    | %Y-%m-%d %H:%M:%S.%f%z         | RFC3339 format                           |
    +--------------------------------+------------------------------------------+
    | %Y-%m-%d %H:%M:%S.%f           | RFC3339 with UTC default timezone        |
    +--------------------------------+------------------------------------------+
    | %Y-%m-%dT%H:%M:%S.%fZ          | JSON encoding, UTC timezone              |
    +--------------------------------+------------------------------------------+
    | %Y-%m-%dT%H:%M:%SZ             | JSON encoding, UTC timezone, without μs  |
    +--------------------------------+------------------------------------------+
    | %Y-%m-%dT%H:%M:%S.%f%z         | JSON-like encoding                       |
    +--------------------------------+------------------------------------------+
    | %Y-%m-%dT%H:%M:%S.%f           | JSON-like encoding, UTC default timezone |
    +--------------------------------+------------------------------------------+
    | %Y-%m-%d %H:%M:%S%z            | human readable date time with TZ         |
    +--------------------------------+------------------------------------------+
    | %Y-%m-%d %H:%M:%S              | human readable date time UTC default     |
    +--------------------------------+------------------------------------------+
    | %Y-%m-%d                       | midnight at a particular date            |
    +--------------------------------+------------------------------------------+

    """
    if val is None or isinstance(val, int):
        return val
    try:
        import numpy as np
        if isinstance(val, np.datetime64):
            val = val.astype(datetime)
    except ImportError:
        pass
    else:
        if isinstance(val, str):
            if val.isdigit():
                return int(val)
            for format in DATETIME_FORMATS:
                try:
                    val = datetime.strptime(val, format)
                    break
                except ValueError:
                    pass

            else:
                if isinstance(val, str):
                    raise ValueError('unsupported string format, please use RFC3339')

        if isinstance(val, datetime):
            return datetime_to_ns(val)
        if isinstance(val, float):
            if val.is_integer():
                return int(val)
            raise ValueError('can only convert whole numbers to nanoseconds')
        raise TypeError('only int, float, str, datetime, and datetime64 are allowed')


def ns_delta(days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0, nanoseconds=0):
    """
    Similar to `timedelta`, ns_delta represents a span of time but as
    the total number of nanoseconds.

    Parameters
    ----------
    days : int, float, decimal.Decimal
        days (as 24 hours) to convert to nanoseconds
    hours : int, float, decimal.Decimal
        hours to convert to nanoseconds
    minutes : int, float, decimal.Decimal
        minutes to convert to nanoseconds
    seconds : int, float, decimal.Decimal
        seconds to convert to nanoseconds
    milliseconds : int, float, decimal.Decimal
        milliseconds to convert to nanoseconds
    microseconds : int, float, decimal.Decimal
        microseconds to convert to nanoseconds
    nanoseconds : int
        nanoseconds to add to the time span

    Returns
    -------
    amount of time in nanoseconds : int

    """
    MICROSECOND = 1000
    MILLISECOND = MICROSECOND * 1000
    SECOND = MILLISECOND * 1000
    MINUTE = SECOND * 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24
    if not isinstance(nanoseconds, int):
        raise TypeError('nanoseconds argument must be an integer')
    units = []
    for unit in (days, hours, minutes, seconds, milliseconds, microseconds):
        if isinstance(unit, float):
            unit = Decimal(unit)
        units.append(unit)
    else:
        factors = [
         DAY, HOUR, MINUTE, SECOND, MILLISECOND, MICROSECOND]
        nanoseconds += sum(map(mul, units, factors))
        return int(nanoseconds)