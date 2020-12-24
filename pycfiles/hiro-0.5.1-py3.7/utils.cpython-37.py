# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/hiro/utils.py
# Compiled at: 2019-10-04 00:47:03
# Size of source mod 2**32: 1091 bytes
"""
random utility functions
"""
import calendar, datetime, functools
from .errors import InvalidTypeError

def timedelta_to_seconds(delta):
    """
    converts a timedelta object to seconds
    """
    seconds = delta.microseconds
    seconds += (delta.seconds + delta.days * 24 * 3600) * 1000000
    return float(seconds) / 1000000


def time_in_seconds(value):
    """
    normalized either a datetime.date, datetime.datetime or float
    to a float
    """
    if isinstance(value, (float, int)):
        return value
    if isinstance(value, (datetime.date, datetime.datetime)):
        return calendar.timegm(value.timetuple())
    raise InvalidTypeError(value)


def chained(method):
    """
    Method decorator to allow chaining.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        if result is None:
            return self
        return result

    return wrapper