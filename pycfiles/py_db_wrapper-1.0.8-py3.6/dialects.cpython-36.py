# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py_db_wrapper/dialects.py
# Compiled at: 2019-04-11 15:43:11
# Size of source mod 2**32: 266 bytes


class Dialect(object):
    TYPES = {}

    def __init__(self):
        pass

    def __str__(self):
        return str(self.TYPES)


class Hive(Dialect):
    GENERIC_TYPES = {}


class Mssql(Dialect):
    TYPES = {}


class Mysql(Dialect):
    TYPES = {}