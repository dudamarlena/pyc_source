# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/dal/conversions.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 3530 bytes
"""
Created on Sep 23, 2013

@author: Nicklas Boerjesson
"""
from datetime import datetime
from qal.dal.types import DB_MYSQL
MySQL_DECIMAL = 0
MySQL_TINY = 1
MySQL_SHORT = 2
MySQL_LONG = 3
MySQL_FLOAT = 4
MySQL_DOUBLE = 5
MySQL_NULL = 6
MySQL_TIMESTAMP = 7
MySQL_LONGLONG = 8
MySQL_INT24 = 9
MySQL_DATE = 10
MySQL_TIME = 11
MySQL_DATETIME = 12
MySQL_YEAR = 13
MySQL_NEWDATE = 14
MySQL_VARCHAR = 15
MySQL_BIT = 16
MySQL_NEWDECIMAL = 246
MySQL_ENUM = 247
MySQL_SET = 248
MySQL_TINY_BLOB = 249
MySQL_MEDIUM_BLOB = 250
MySQL_LONG_BLOB = 251
MySQL_BLOB = 252
MySQL_VAR_STRING = 253
MySQL_STRING = 254
MySQL_GEOMETRY = 255

def mysql_type_to_sql_type(_type_code):
    """
    Convert the internal MySQL type to the SQL type

    :param _type_code: A MySQL field constant
    """
    if _type_code in (
     MySQL_VARCHAR,
     MySQL_VAR_STRING,
     MySQL_STRING):
        return 'string'
    if _type_code in (
     MySQL_TINY_BLOB,
     MySQL_MEDIUM_BLOB,
     MySQL_LONG_BLOB):
        return 'blob'
    if _type_code in (
     MySQL_BLOB,):
        return 'string'
    if _type_code in (
     MySQL_DECIMAL,
     MySQL_FLOAT,
     MySQL_DOUBLE,
     MySQL_NEWDECIMAL):
        return 'float'
    if _type_code in (
     MySQL_TINY,
     MySQL_SHORT,
     MySQL_LONG,
     MySQL_LONGLONG,
     MySQL_INT24,
     MySQL_BIT):
        return 'integer'
    if _type_code in (
     MySQL_DATE,
     MySQL_TIME,
     MySQL_DATETIME,
     MySQL_YEAR,
     MySQL_NEWDATE,
     MySQL_TIMESTAMP):
        return 'timestamp'
    raise Exception('mysql_type_to_sql_type: _type_code "' + str(_type_code) + '"not supported')


def python_type_to_sql_type(_python_type):
    """
    Convert a python data type to ab SQL type.

    :param _python_type: A Python internal type
    """
    if _python_type == str:
        return 'string'
    if _python_type == bytes:
        return 'blob'
    if _python_type == float:
        return 'float'
    if _python_type == int:
        return 'integer'
    if _python_type == datetime:
        return 'datetime'
    if _python_type == bool:
        return 'boolean'
    raise Exception('python_type_to_sql_type: _type_code "' + str(_python_type) + '"not supported')


def parse_description(_descriptions, _db_type):
    """Convert field descriptions to field name- and field type-lists.

    :param _descriptions: A list of descriptions
    :param _db_type: The database type
    """
    _field_names = []
    _field_types = []
    for _column in _descriptions:
        _field_names.append(_column[0])
        if _db_type == DB_MYSQL:
            _field_types.append(mysql_type_to_sql_type(_column[1]))
        else:
            _field_types.append(_column[1])

    return (
     _field_names, _field_types)