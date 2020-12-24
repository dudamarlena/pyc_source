# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.6.0-i686/egg/tvdbapi_client/timeutil.py
# Compiled at: 2015-06-28 01:14:44
"""Time related utilities and helper functions."""
import datetime
ONE_HOUR = datetime.timedelta(minutes=55)

def utcnow():
    """Gets current time.

    :returns: current time from utc
    :rtype: :py:obj:`datetime.datetime`
    """
    return datetime.datetime.utcnow()


def is_older_than(before, delta):
    """Checks if a datetime is older than delta

    :param datetime before: a datetime to check
    :param timedelta delta: period of time to compare against
    :returns: ``True`` if before is older than time period else ``False``
    :rtype: bool
    """
    return utcnow() - before > delta


def is_newer_than(after, delta):
    """Checks if a datetime is newer than delta

    :param datetime after: a datetime to check
    :param timedelta delta: period of time to compare against
    :returns: ``True`` if before is newer than time period else ``False``
    :rtype: bool
    """
    return after - utcnow() > delta