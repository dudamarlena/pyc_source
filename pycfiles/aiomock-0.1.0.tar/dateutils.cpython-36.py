# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/dateutils.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 379 bytes
import datetime, pytz
FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def now(timezone='UTC'):
    return pytz.timezone(timezone).localize(datetime.datetime.utcnow())


def to_iso(dt, tz_name='UTC'):
    result = dt + pytz.timezone(tz_name).utcoffset(dt)
    return result.strftime(FORMAT)


def from_iso_to_datetime(dt, tz_name='UTC'):
    return datetime.datetime.strptime(dt, FORMAT)