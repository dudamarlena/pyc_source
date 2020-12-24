# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/exception.py
# Compiled at: 2015-10-11 07:17:06
from difflib import get_close_matches
from dbmanagr.logger import logger
CONNECTION_NOT_FOUND = 'Connection "{0}" was not found ({1})'
TABLE_NOT_FOUND = 'Table "{0}" was not found ({1})'
COLUMN_NOT_FOUND = 'Column "{0}" was not found on table "{1}" ({2})'
CLOSE_MATCHES = 'close matches: {0}'
NO_CLOSE_MATCHES = 'no close matches in: {0}'

def unknown_connection_message(connection, haystack):
    matches = get_close_matches(connection, haystack)
    if not matches:
        return CONNECTION_NOT_FOUND.format(connection, 'no close matches')
    return CONNECTION_NOT_FOUND.format(connection, CLOSE_MATCHES.format((', ').join(matches)))


def unknown_table_message(tablename, haystack):
    if tablename is None:
        tablename = '?'
    matches = get_close_matches(tablename, haystack)
    if not matches:
        return TABLE_NOT_FOUND.format(tablename, NO_CLOSE_MATCHES.format((', ').join(haystack)))
    else:
        return TABLE_NOT_FOUND.format(tablename, CLOSE_MATCHES.format((', ').join(matches)))


def unknown_column_message(table, column, haystack=None):
    if haystack is None:
        haystack = map(lambda c: c.name, table.columns())
    logger.debug('haystack: %s', haystack)
    matches = get_close_matches(column, haystack)
    if not matches:
        return COLUMN_NOT_FOUND.format(column, table.name if table else '?', NO_CLOSE_MATCHES.format((', ').join(haystack)))
    else:
        return COLUMN_NOT_FOUND.format(column, table.name if table else '?', CLOSE_MATCHES.format((', ').join(matches)))


class BusinessException(Exception):
    pass


class UnknownConnectionException(BusinessException):

    def __init__(self, connection, haystack):
        super(UnknownConnectionException, self).__init__(unknown_connection_message(connection, haystack))


class UnknownTableException(BusinessException):

    def __init__(self, tablename, haystack):
        super(UnknownTableException, self).__init__(unknown_table_message(tablename, haystack))


class UnknownColumnException(BusinessException):

    def __init__(self, table, column, haystack=None):
        super(UnknownColumnException, self).__init__(unknown_column_message(table, column, haystack))