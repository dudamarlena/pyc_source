# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/contrib/pymysql/err.py
# Compiled at: 2013-10-14 11:16:24
import struct
try:
    (StandardError, Warning)
except ImportError:
    try:
        from exceptions import StandardError, Warning
    except ImportError:
        import sys
        e = sys.modules['exceptions']
        StandardError = e.StandardError
        Warning = e.Warning

from constants import ER
import sys

class MySQLError(StandardError):
    """Exception related to operation with MySQL."""
    pass


class Warning(Warning, MySQLError):
    """Exception raised for important warnings like data truncations
    while inserting, etc."""
    pass


class Error(MySQLError):
    """Exception that is the base class of all other error exceptions
    (not Warning)."""
    pass


class InterfaceError(Error):
    """Exception raised for errors that are related to the database
    interface rather than the database itself."""
    pass


class DatabaseError(Error):
    """Exception raised for errors that are related to the
    database."""
    pass


class DataError(DatabaseError):
    """Exception raised for errors that are due to problems with the
    processed data like division by zero, numeric value out of range,
    etc."""
    pass


class OperationalError(DatabaseError):
    """Exception raised for errors that are related to the database's
    operation and not necessarily under the control of the programmer,
    e.g. an unexpected disconnect occurs, the data source name is not
    found, a transaction could not be processed, a memory allocation
    error occurred during processing, etc."""
    pass


class IntegrityError(DatabaseError):
    """Exception raised when the relational integrity of the database
    is affected, e.g. a foreign key check fails, duplicate key,
    etc."""
    pass


class InternalError(DatabaseError):
    """Exception raised when the database encounters an internal
    error, e.g. the cursor is not valid anymore, the transaction is
    out of sync, etc."""
    pass


class ProgrammingError(DatabaseError):
    """Exception raised for programming errors, e.g. table not found
    or already exists, syntax error in the SQL statement, wrong number
    of parameters specified, etc."""
    pass


class NotSupportedError(DatabaseError):
    """Exception raised in case a method or database API was used
    which is not supported by the database, e.g. requesting a
    .rollback() on a connection that does not support transaction or
    has transactions turned off."""
    pass


error_map = {}

def _map_error(exc, *errors):
    for error in errors:
        error_map[error] = exc


_map_error(ProgrammingError, ER.DB_CREATE_EXISTS, ER.SYNTAX_ERROR, ER.PARSE_ERROR, ER.NO_SUCH_TABLE, ER.WRONG_DB_NAME, ER.WRONG_TABLE_NAME, ER.FIELD_SPECIFIED_TWICE, ER.INVALID_GROUP_FUNC_USE, ER.UNSUPPORTED_EXTENSION, ER.TABLE_MUST_HAVE_COLUMNS, ER.CANT_DO_THIS_DURING_AN_TRANSACTION)
_map_error(DataError, ER.WARN_DATA_TRUNCATED, ER.WARN_NULL_TO_NOTNULL, ER.WARN_DATA_OUT_OF_RANGE, ER.NO_DEFAULT, ER.PRIMARY_CANT_HAVE_NULL, ER.DATA_TOO_LONG, ER.DATETIME_FUNCTION_OVERFLOW)
_map_error(IntegrityError, ER.DUP_ENTRY, ER.NO_REFERENCED_ROW, ER.NO_REFERENCED_ROW_2, ER.ROW_IS_REFERENCED, ER.ROW_IS_REFERENCED_2, ER.CANNOT_ADD_FOREIGN)
_map_error(NotSupportedError, ER.WARNING_NOT_COMPLETE_ROLLBACK, ER.NOT_SUPPORTED_YET, ER.FEATURE_DISABLED, ER.UNKNOWN_STORAGE_ENGINE)
_map_error(OperationalError, ER.DBACCESS_DENIED_ERROR, ER.ACCESS_DENIED_ERROR, ER.TABLEACCESS_DENIED_ERROR, ER.COLUMNACCESS_DENIED_ERROR)
del _map_error
del ER

def _get_error_info(data):
    errno = struct.unpack('<h', data[1:3])[0]
    if sys.version_info[0] == 3:
        is_41 = data[3] == ord('#')
    else:
        is_41 = data[3] == '#'
    if is_41:
        sqlstate = data[4:9].decode('utf8')
        errorvalue = data[9:].decode('utf8')
        return (
         errno, sqlstate, errorvalue)
    else:
        return (
         errno, None, data[3:].decode('utf8'))
        return


def _check_mysql_exception(errinfo):
    errno, sqlstate, errorvalue = errinfo
    errorclass = error_map.get(errno, None)
    if errorclass:
        raise errorclass, (errno, errorvalue)
    raise InternalError, (errno, errorvalue)
    return


def raise_mysql_exception(data):
    errinfo = _get_error_info(data)
    _check_mysql_exception(errinfo)