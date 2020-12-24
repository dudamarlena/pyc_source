# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\R and L\Dropbox\Coding Notes and Programming\gcapi-python\gcapi\gcapi_tools.py
# Compiled at: 2020-01-28 12:07:13
# Size of source mod 2**32: 1478 bytes
import re
from datetime import datetime
SPAN_M = [
 1, 2, 3, 5, 10, 15, 30]
SPAN_H = [1, 2, 4, 8]
INTERVAL = ['HOUR', 'MINUTE', 'DAY', 'WEEK', 'MONTH']

def format_date(row):
    """ Extracts the unix timestamp from the string and converts it to a datetime object, best if used with map
    :param row: row from a dataframe """
    row = str(row)
    unix = [int(s) for s in re.findall('-?\\d+\\.?\\d*', row)]
    dt_object = datetime.fromtimestamp(unix[0] / 1000)
    return dt_object


def check_span(interval, span):
    """ Checks if the span is correct for the specific interval
    :param interval: time interval, can be min, hour, day, week, month
    :param span: span of time, it can be 1, 2, 3, 5, etc,,"""
    if interval == 'HOUR':
        if span not in [SPAN_H, str(SPAN_H)]:
            span = 1
            return span
        else:
            return span
    else:
        if interval == 'MINUTE':
            if span not in [SPAN_M, str(SPAN_M)]:
                span = 1
                return span
            else:
                return span
        else:
            span = 1
            return span


def check_interval(interval):
    """ Checks if the interval is one of the correct intervals
    :param interval: time interval, can be min, hour, day, week, month"""
    if interval not in INTERVAL:
        interval = 'HOUR'
        return interval
    else:
        return interval