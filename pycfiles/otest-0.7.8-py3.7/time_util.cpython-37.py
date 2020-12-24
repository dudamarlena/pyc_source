# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/time_util.py
# Compiled at: 2016-10-24 10:04:08
# Size of source mod 2**32: 1075 bytes
from datetime import datetime
from datetime import timedelta
__author__ = 'roland'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def time_in_a_while(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    """
    format of timedelta:
        timedelta([days[, seconds[, microseconds[, milliseconds[,
                    minutes[, hours[, weeks]]]]]]])
    :return: UTC time
    """
    delta = timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)
    return datetime.utcnow() + delta


def in_a_while(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, time_format=TIME_FORMAT):
    """
    format of timedelta:
        timedelta([days[, seconds[, microseconds[, milliseconds[,
                    minutes[, hours[, weeks]]]]]]])
    """
    if time_format is None:
        time_format = TIME_FORMAT
    return time_in_a_while(days, seconds, microseconds, milliseconds, minutes, hours, weeks).strftime(time_format)