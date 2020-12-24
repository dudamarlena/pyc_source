# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/time.py
# Compiled at: 2020-01-13 02:47:00
# Size of source mod 2**32: 2107 bytes
from datetime import datetime
from dateutil.tz import gettz, tzlocal

def default_timezone():
    """ Get the default timezone

    default system value

    Returns:
        (datetime.tzinfo): Definition of the default timezone
    """
    return tzlocal()


def now_utc():
    """ Retrieve the current time in UTC

    Returns:
        (datetime): The current time in Universal Time, aka GMT
    """
    return to_utc(datetime.utcnow())


def now_local(tz=None):
    """ Retrieve the current time

    Args:
        tz (datetime.tzinfo, optional): Timezone, default to user's settings

    Returns:
        (datetime): The current time
    """
    if not tz:
        tz = default_timezone()
    return datetime.now(tz)


def to_utc(dt):
    """ Convert a datetime with timezone info to a UTC datetime

    Args:
        dt (datetime): A datetime (presumably in some local zone)
    Returns:
        (datetime): time converted to UTC
    """
    tzUTC = gettz('UTC')
    if dt.tzinfo:
        return dt.astimezone(tzUTC)
    return dt.replace(tzinfo=(gettz('UTC'))).astimezone(tzUTC)


def to_local(dt):
    """ Convert a datetime to the user's local timezone

    Args:
        dt (datetime): A datetime (if no timezone, defaults to UTC)
    Returns:
        (datetime): time converted to the local timezone
    """
    tz = default_timezone()
    if dt.tzinfo:
        return dt.astimezone(tz)
    return dt.replace(tzinfo=(gettz('UTC'))).astimezone(tz)