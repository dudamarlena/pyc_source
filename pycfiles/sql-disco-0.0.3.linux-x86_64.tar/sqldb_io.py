# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/sqldisco/sqldb_io.py
# Compiled at: 2013-03-19 09:04:15
"""
File: sql_io.py
Author: Jon Eisen
Description: Input and output routines for sql-disco
"""
sql_packages = {'mssql': 'pymssql'}

def _import(sqltype):
    """ Import the sql package in question """
    return __import__(sql_packages[sqltype])


def _input(query, sqltype, connargs, **kwargs):
    package = _import(sqltype)
    conn = package.connect(**connargs)
    cursor = conn.cursor()
    cursor.execute(query)
    return InputWrapper(cursor)


class InputWrapper(object):
    """Want to wrap the cursor in an object that
    supports the following operations: """

    def __init__(self, cursor):
        self.cursor = cursor

    def __iter__(self):
        if hasattr(self.cursor, '__iter__'):
            return self.cursor.__iter__()
        else:
            return self.cursor_iter()

    def cursor_iter(self):
        row = self.cursor.fetchone()
        while row:
            yield row
            row = self.cursor.fetchone()

    def __len__(self):
        return self.cursor.rowcount

    def close(self):
        self.cursor.close()

    def read(self, size=-1):
        raise Exception('read is not implemented- investigate why this was called')


def sql_input(stream, size, url, params):
    from sqldisco.sqldb_io import _input
    import json
    return _input(**json.loads(url))


sql_input_stream = (
 sql_input,)