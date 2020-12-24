# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drizzle/errors.py
# Compiled at: 2010-03-22 02:56:07
import exceptions, types

class Error(exceptions.StandardError):
    """Base class of all other error exceptions"""
    pass


class CodedError(Error):
    """Base class of all other error exceptions"""

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return ('{msg} (#{code})').format(msg=self.msg, code=self.code)


class Warning(exceptions.StandardError):
    """Exception raised for important warnings."""
    pass


class InterfaceError(Error):
    """Exception raised for errors that are related to the database interface 
    rather than the database itself.
    
    """
    pass


class DatabaseError(CodedError):
    """Exception raised for errors that are related to the database."""
    pass


class InternalError(DatabaseError):
    """Exception raised when the database encounters an internal error."""
    pass


class OperationalError(DatabaseError):
    """Exception raised for errors that are related to the database's operation
    and not necessarily under the control of the programmer.
    
    """
    pass


class ProgrammingError(DatabaseError):
    """Exception raised for programming errors."""
    pass


class IntegrityError(DatabaseError):
    """Exception raised when the database encounters an internal error."""
    pass


class DataError(DatabaseError):
    """Exception raised for errors that are due to problems with the processed
    data.
    
    """
    pass


class NotSupportedError(DatabaseError):
    """Exception raised in case a method or database API was used which is not 
    supported by the database.
    
    """
    pass


class LibDrizzleError(InterfaceError, CodedError):
    """Exception raised for coded errors raised by libdrizzle."""
    pass


class AddressError(LibDrizzleError):
    """Exception raised when a hostname or IP is invalid or cannot be resolved."""
    pass


class AuthFailedError(LibDrizzleError):
    """Exception raised when authentication with the server failed."""
    pass


class LostConnectionError(LibDrizzleError):
    """Exception raised when the connection to a database is lost."""
    pass


class CouldNotConnectError(LibDrizzleError):
    """Exception raised when a connection could not be established."""
    pass