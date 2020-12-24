# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/time_util.py
# Compiled at: 2019-12-26 15:55:22
# Size of source mod 2**32: 681 bytes
from datetime import datetime, timedelta
epoch = datetime(1970, 1, 1)

def utc_now():
    """
    Get current datetime in UTC, without time zone info.
    """
    return datetime.utcnow()


def x_seconds_before_now(seconds):
    """
    Get the datetime that ``x`` seconds before now.

    :type seconds: int
    :param seconds:

    :rtype: datetime
    :return:
    """
    return utc_now() - timedelta(seconds=seconds)


def x_seconds_after_now(seconds):
    """
    Get the datetime that ``y`` seconds after now.

    :type seconds: int
    :param seconds:

    :rtype: datetime
    :return:
    """
    return utc_now() + timedelta(seconds=seconds)