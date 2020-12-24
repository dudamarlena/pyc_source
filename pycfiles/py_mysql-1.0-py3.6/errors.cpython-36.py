# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\errors.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 10253 bytes
"""Python exceptions
"""
from . import utils
from .locales import get_client_error
from .catch23 import PY2
_CUSTOM_ERROR_EXCEPTIONS = {}

def custom_error_exception(error=None, exception=None):
    """Define custom exceptions for MySQL server errors

    This function defines custom exceptions for MySQL server errors and
    returns the current set customizations.

    If error is a MySQL Server error number, then you have to pass also the
    exception class.

    The error argument can also be a dictionary in which case the key is
    the server error number, and value the exception to be raised.

    If none of the arguments are given, then custom_error_exception() will
    simply return the current set customizations.

    To reset the customizations, simply supply an empty dictionary.

    Examples:
        import mysql.connector
        from mysql.connector import errorcode

        # Server error 1028 should raise a DatabaseError
        mysql.connector.custom_error_exception(
            1028, mysql.connector.DatabaseError)

        # Or using a dictionary:
        mysql.connector.custom_error_exception({
            1028: mysql.connector.DatabaseError,
            1029: mysql.connector.OperationalError,
            })

        # Reset
        mysql.connector.custom_error_exception({})

    Returns a dictionary.
    """
    global _CUSTOM_ERROR_EXCEPTIONS
    if isinstance(error, dict) and not len(error):
        _CUSTOM_ERROR_EXCEPTIONS = {}
        return _CUSTOM_ERROR_EXCEPTIONS
    else:
        if not error:
            if not exception:
                return _CUSTOM_ERROR_EXCEPTIONS
        else:
            if not isinstance(error, (int, dict)):
                raise ValueError('The error argument should be either an integer or dictionary')
            if isinstance(error, int):
                error = {error: exception}
        for errno, exception in error.items():
            if not isinstance(errno, int):
                raise ValueError('error number should be an integer')
            try:
                if not issubclass(exception, Exception):
                    raise TypeError
            except TypeError:
                raise ValueError('exception should be subclass of Exception')

            _CUSTOM_ERROR_EXCEPTIONS[errno] = exception

        return _CUSTOM_ERROR_EXCEPTIONS


def get_mysql_exception(errno, msg=None, sqlstate=None):
    """Get the exception matching the MySQL error

    This function will return an exception based on the SQLState. The given
    message will be passed on in the returned exception.

    The exception returned can be customized using the
    mysql.connector.custom_error_exception() function.

    Returns an Exception
    """
    try:
        return _CUSTOM_ERROR_EXCEPTIONS[errno](msg=msg,
          errno=errno,
          sqlstate=sqlstate)
    except KeyError:
        pass

    try:
        return _ERROR_EXCEPTIONS[errno](msg=msg,
          errno=errno,
          sqlstate=sqlstate)
    except KeyError:
        pass

    if not sqlstate:
        return DatabaseError(msg=msg, errno=errno)
    try:
        return _SQLSTATE_CLASS_EXCEPTION[sqlstate[0:2]](msg=msg,
          errno=errno,
          sqlstate=sqlstate)
    except KeyError:
        return DatabaseError(msg=msg, errno=errno, sqlstate=sqlstate)


def get_exception(packet):
    """Returns an exception object based on the MySQL error

    Returns an exception object based on the MySQL error in the given
    packet.

    Returns an Error-Object.
    """
    errno = errmsg = None
    try:
        if packet[4] != 255:
            raise ValueError('Packet is not an error packet')
    except IndexError as err:
        return InterfaceError('Failed getting Error information (%r)' % err)

    sqlstate = None
    try:
        packet = packet[5:]
        packet, errno = utils.read_int(packet, 2)
        if packet[0] != 35:
            if isinstance(packet, (bytes, bytearray)):
                errmsg = packet.decode('utf8')
            else:
                errmsg = packet
        else:
            packet, sqlstate = utils.read_bytes(packet[1:], 5)
            sqlstate = sqlstate.decode('utf8')
            errmsg = packet.decode('utf8')
    except Exception as err:
        return InterfaceError('Failed getting Error information (%r)' % err)
    else:
        return get_mysql_exception(errno, errmsg, sqlstate)


class Error(Exception):
    __doc__ = 'Exception that is base class for all other error exceptions'

    def __init__(self, msg=None, errno=None, values=None, sqlstate=None):
        super(Error, self).__init__()
        self.msg = msg
        self._full_msg = self.msg
        self.errno = errno or -1
        self.sqlstate = sqlstate
        if not self.msg and 2000 <= self.errno < 3000:
            self.msg = get_client_error(self.errno)
            if values is not None:
                try:
                    self.msg = self.msg % values
                except TypeError as err:
                    self.msg = '{0} (Warning: {1})'.format(self.msg, str(err))

        else:
            if not self.msg:
                self._full_msg = self.msg = 'Unknown error'
        if self.msg and self.errno != -1:
            fields = {'errno':self.errno,  'msg':self.msg.encode('utf8') if PY2 else self.msg}
            if self.sqlstate:
                fmt = '{errno} ({state}): {msg}'
                fields['state'] = self.sqlstate
            else:
                fmt = '{errno}: {msg}'
            self._full_msg = (fmt.format)(**fields)
        self.args = (self.errno, self._full_msg, self.sqlstate)

    def __str__(self):
        return self._full_msg


class Warning(Exception):
    __doc__ = 'Exception for important warnings'


class InterfaceError(Error):
    __doc__ = 'Exception for errors related to the interface'


class DatabaseError(Error):
    __doc__ = 'Exception for errors related to the database'


class InternalError(DatabaseError):
    __doc__ = 'Exception for errors internal database errors'


class OperationalError(DatabaseError):
    __doc__ = "Exception for errors related to the database's operation"


class ProgrammingError(DatabaseError):
    __doc__ = 'Exception for errors programming errors'


class IntegrityError(DatabaseError):
    __doc__ = 'Exception for errors regarding relational integrity'


class DataError(DatabaseError):
    __doc__ = 'Exception for errors reporting problems with processed data'


class NotSupportedError(DatabaseError):
    __doc__ = 'Exception for errors when an unsupported database feature was used'


class PoolError(Error):
    __doc__ = 'Exception for errors relating to connection pooling'


class MySQLFabricError(Error):
    __doc__ = 'Exception for errors relating to MySQL Fabric'


_SQLSTATE_CLASS_EXCEPTION = {'02':DataError, 
 '07':DatabaseError, 
 '08':OperationalError, 
 '0A':NotSupportedError, 
 '21':DataError, 
 '22':DataError, 
 '23':IntegrityError, 
 '24':ProgrammingError, 
 '25':ProgrammingError, 
 '26':ProgrammingError, 
 '27':ProgrammingError, 
 '28':ProgrammingError, 
 '2A':ProgrammingError, 
 '2B':DatabaseError, 
 '2C':ProgrammingError, 
 '2D':DatabaseError, 
 '2E':DatabaseError, 
 '33':DatabaseError, 
 '34':ProgrammingError, 
 '35':ProgrammingError, 
 '37':ProgrammingError, 
 '3C':ProgrammingError, 
 '3D':ProgrammingError, 
 '3F':ProgrammingError, 
 '40':InternalError, 
 '42':ProgrammingError, 
 '44':InternalError, 
 'HZ':OperationalError, 
 'XA':IntegrityError, 
 '0K':OperationalError, 
 'HY':DatabaseError}
_ERROR_EXCEPTIONS = {1243:ProgrammingError, 
 1210:ProgrammingError, 
 2002:InterfaceError, 
 2013:OperationalError, 
 2049:NotSupportedError, 
 2055:OperationalError, 
 2061:InterfaceError, 
 2026:InterfaceError}