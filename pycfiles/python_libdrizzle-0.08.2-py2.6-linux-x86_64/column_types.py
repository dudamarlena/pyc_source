# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drizzle/column_types.py
# Compiled at: 2010-03-21 15:04:44
import types, time, datetime
from decimal import Decimal
from drizzle import libdrizzle as libd
__all__ = [
 'from_db', 'to_db', 'STRING', 'BINARY', 'NUMBER', 'DATETIME',
 'ROWID', 'DateFromTicks', 'TimeFromTicks', 'TimestampFromTicks',
 'Timestamp', 'Date', 'Time', 'Binary']

class DBAPIColumnType(frozenset):

    def __eq__(self, val):
        if isinstance(val, DBAPIColumnType):
            return not self.difference(val)
        return val in self


class ConversionSet(object):

    def __init__(self, converters={}):
        self.converters = converters

    def register(self, valuetype, converter, force=False):
        """Register a converter for a given type. 
        
        If a converter already exists, ValueError will be raised unless 
        the optional force parameter is set to True.
        
        """
        if converter in self.converters and force == false:
            raise ValueError
        else:
            self.converters[valuetype] = converter

    def convert(self, value, valuetype=None):
        """Convert a value using the set of converters.
        
        If an appropriate converter cannot be found, KeyError will be 
        raised with the type of the value.
        
        """
        if valuetype is None:
            valuetype = type(value)
        if valuetype in self.converters:
            if value is None:
                return
            else:
                return self.converters[valuetype](value)
        else:
            raise KeyError(valuetype)
        return


STRING = DBAPIColumnType([
 libd.DRIZZLE_COLUMN_TYPE_VARCHAR,
 libd.DRIZZLE_COLUMN_TYPE_ENUM])
BINARY = DBAPIColumnType([
 libd.DRIZZLE_COLUMN_TYPE_BLOB])
NUMBER = DBAPIColumnType([
 libd.DRIZZLE_COLUMN_TYPE_DOUBLE,
 libd.DRIZZLE_COLUMN_TYPE_LONG,
 libd.DRIZZLE_COLUMN_TYPE_LONGLONG,
 libd.DRIZZLE_COLUMN_TYPE_NEWDECIMAL,
 libd.DRIZZLE_COLUMN_TYPE_TINY])
DATETIME = DBAPIColumnType([
 libd.DRIZZLE_COLUMN_TYPE_DATE,
 libd.DRIZZLE_COLUMN_TYPE_DATETIME,
 libd.DRIZZLE_COLUMN_TYPE_TIMESTAMP])
ROWID = DBAPIColumnType([])

def _datetime_from_string(s):
    tt = time.strptime(s, '%Y-%m-%d %H:%M:%S')
    return datetime.datetime(*tt[:6])


def _date_from_string(s):
    tt = time.strptime(s, '%Y-%m-%d')
    return datetime.date(*tt[:3])


def _time_from_string(s):
    tt = time.strptime(s, '%H:%M:%S')
    return datetime.time(*tt[3:6])


def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])


Timestamp = datetime.datetime
Date = datetime.date
Time = datetime.time
Binary = buffer
from_db = ConversionSet({libd.DRIZZLE_COLUMN_TYPE_VARCHAR: str, 
   libd.DRIZZLE_COLUMN_TYPE_ENUM: str, 
   libd.DRIZZLE_COLUMN_TYPE_BLOB: buffer, 
   libd.DRIZZLE_COLUMN_TYPE_LONG: int, 
   libd.DRIZZLE_COLUMN_TYPE_LONGLONG: int, 
   libd.DRIZZLE_COLUMN_TYPE_TINY: int, 
   libd.DRIZZLE_COLUMN_TYPE_DOUBLE: float, 
   libd.DRIZZLE_COLUMN_TYPE_NEWDECIMAL: Decimal, 
   libd.DRIZZLE_COLUMN_TYPE_DATE: _date_from_string, 
   libd.DRIZZLE_COLUMN_TYPE_DATETIME: _datetime_from_string, 
   libd.DRIZZLE_COLUMN_TYPE_TIMESTAMP: _time_from_string})
to_db = ConversionSet({})