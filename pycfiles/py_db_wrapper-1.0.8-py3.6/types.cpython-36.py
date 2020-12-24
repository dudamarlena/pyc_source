# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py_db_wrapper/types.py
# Compiled at: 2019-04-11 15:43:11
# Size of source mod 2**32: 830 bytes
from .exceptions import TYPE_NOT_DEFINED
from .dialects import *

class SQL_TYPE(object):
    __doc__ = '\n    '
    TYPES = {}

    @classmethod
    def get_type_string(cls, dialect):
        return cls.TYPES[dialect]


class BIGINT(SQL_TYPE):
    __doc__ = '\n    '
    TYPES = {Mssql: 'bigint', 
     Mysql: 'BIGINT'}


class TINYINT(SQL_TYPE):
    __doc__ = '\n    '
    TYPES = {Mssql: 'tinyint', 
     Mysql: 'TINYINT'}


TYPE_REGISTER = [
 BIGINT,
 TINYINT]

def get_base_type_from_string(dialect, type_string):
    for type in TYPE_REGISTER:
        if type_string == type.TYPES[dialect]:
            return type

    raise TYPE_NOT_DEFINED


def convert_type_string(type_string, from_d, to_d):
    base_type = get_base_type_from_string(from_d, type_string)
    return base_type.get_type_string(to_d)