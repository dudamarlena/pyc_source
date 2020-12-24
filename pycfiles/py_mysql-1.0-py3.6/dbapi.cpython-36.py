# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\dbapi.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 2330 bytes
"""
This module implements some constructors and singletons as required by the
DB API v2.0 (PEP-249).
"""
apilevel = '2.0'
threadsafety = 1
paramstyle = 'pyformat'
import time, datetime
from . import constants

class _DBAPITypeObject(object):

    def __init__(self, *values):
        self.values = values

    def __eq__(self, other):
        if other in self.values:
            return True
        else:
            return False

    def __ne__(self, other):
        if other in self.values:
            return False
        else:
            return True


Date = datetime.date
Time = datetime.time
Timestamp = datetime.datetime

def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])


Binary = bytes
STRING = _DBAPITypeObject(*constants.FieldType.get_string_types())
BINARY = _DBAPITypeObject(*constants.FieldType.get_binary_types())
NUMBER = _DBAPITypeObject(*constants.FieldType.get_number_types())
DATETIME = _DBAPITypeObject(*constants.FieldType.get_timestamp_types())
ROWID = _DBAPITypeObject()