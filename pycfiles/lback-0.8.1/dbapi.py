# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mysql\connector\dbapi.pyc
# Compiled at: 2014-07-26 22:44:23
"""
This module implements some constructors and singletons as required by the
DB API v2.0 (PEP-249).
"""
apilevel = '2.0'
threadsafety = 1
paramstyle = 'pyformat'
import time, datetime
from mysql.connector import constants

class _DBAPITypeObject:

    def __init__(self, *values):
        self.values = values

    def __cmp__(self, other):
        if other in self.values:
            return 0
        else:
            if other < self.values:
                return 1
            return -1


Date = datetime.date
Time = datetime.time
Timestamp = datetime.datetime

def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])


Binary = str
STRING = _DBAPITypeObject(constants.FieldType.get_string_types())
BINARY = _DBAPITypeObject(constants.FieldType.get_binary_types())
NUMBER = _DBAPITypeObject(constants.FieldType.get_number_types())
DATETIME = _DBAPITypeObject(constants.FieldType.get_timestamp_types())
ROWID = _DBAPITypeObject()