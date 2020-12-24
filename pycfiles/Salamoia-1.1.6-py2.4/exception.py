# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/exception.py
# Compiled at: 2007-12-02 16:26:58
"""
This module contains salamoia specific exception classes
"""
from salamoia.utility.reflection import ClassNamed
import sys

class SalamoiaException(Exception):
    """
    This is the base class for all salamoia exceptions.
    It is useful because it can unwrap xmlrpc wrapped faults.
    """
    __module__ = __name__

    @classmethod
    def matches(cls):
        return cls.matchesName(ClassNamed.className(cls))

    @staticmethod
    def matchesName(name):
        try:
            return name in str(sys.exc_type) or name in sys.exc_value.faultString
        except:
            return False

    @staticmethod
    def message():
        exc = sys.exc_value
        try:
            return exc.faultString
        except:
            return str(exc)


class ObsoleteException(SalamoiaException):
    """
    Raised when callilng an obsolete function
    """
    __module__ = __name__


class ReadOnlyError(SalamoiaException):
    """
    Raised when an attribute is read only and was written
    """
    __module__ = __name__


class SearchError(SalamoiaException):
    """
    Raised when an error occoured while searching
    """
    __module__ = __name__


class FetchError(SalamoiaException):
    """
    Raised while fetching an object
    """
    __module__ = __name__


class StoreError(SalamoiaException):
    """
    Raised while storing an object
    """
    __module__ = __name__


class StoreCreateError(StoreError):
    """
    Raised while creating a new object
    """
    __module__ = __name__


class StoreAlreadyExistsError(StoreCreateError):
    """
    Riased when storing an object in 'create' mode and the object altready exists
    """
    __module__ = __name__


class StoreModifyError(StoreError):
    """
    Riased when storing an object in 'modify' mode and the object don't exists
    """
    __module__ = __name__


class ConnectionError(SalamoiaException):
    """
    Connection error
    """
    __module__ = __name__


class AuthenticationError(ConnectionError):
    """
    Raised when the authentication credentials are incorrect
    """
    __module__ = __name__


class EmptyPasswordError(ConnectionError):
    __module__ = __name__


class VFSError(SalamoiaException):
    __module__ = __name__


class InvalidPathError(VFSError):
    __module__ = __name__


class ProtocolError(SalamoiaException):
    __module__ = __name__


class FormatError(SalamoiaException):
    __module__ = __name__


class LimitExceededError(SalamoiaException):
    """
    Raised when an object is created over the limits specified in the db
    """
    __module__ = __name__


class JunkError(SalamoiaException):
    """
    Raised when an attribute doesn't match the type
    """
    __module__ = __name__


class JunkInMailStringError(JunkError):
    """
    Raised when a email attribute doesn't match a email format

    REFACTOR
    """
    __module__ = __name__


class EncodingError(SalamoiaException):
    __module__ = __name__


class TransactionError(SalamoiaException):
    __module__ = __name__


class TransactionDoesNotExistError(TransactionError):
    __module__ = __name__


class ScriptError(SalamoiaException):
    """
    Raised when a script terminates with an error
    """
    __module__ = __name__


class HandledError(SalamoiaException):
    """
    error which is already catched and handled
    but can be rethrown for exiting nested constructs
    """
    __module__ = __name__


class ServiceException(SalamoiaException):
    """
    Exception caused while executing service related routines
    """
    __module__ = __name__


class ServiceNotFoundException(ServiceException):
    """
    The given uri doesn't match a registered service
    """
    __module__ = __name__


class ServiceDoesNotImplementException(ServiceException):
    """
    The given method is not implemented
    """
    __module__ = __name__


class XMLException(SalamoiaException):
    """
    Exception during parsing of xml
    """
    __module__ = __name__


class UnknownXMLChildException(XMLException):
    """
    xmlparser based parser elements found a child element that is not implemented
    """
    __module__ = __name__


class TransformationError(SalamoiaException):
    """
    Raised when the xmlserver fails to transform complex objects in primitive types
    """
    __module__ = __name__


class TransactionDoesNotExistException(SalamoiaException):
    """
    Obsolete
    """
    __module__ = __name__


class SecurityException(SalamoiaException):
    """
    Base for security exceptions
    """
    __module__ = __name__


class BadAceFormatException(SecurityException):
    """
    Raised when the ace string format is wrong
    """
    __module__ = __name__


class PermissionDeniedException(SecurityException):
    """
    Raised when the ACL doesn't permit something
    """
    __module__ = __name__


class ReadPermissionDeniedException(PermissionDeniedException, FetchError):
    """
    Raised when the ACL doesn't permit writing
    """
    __module__ = __name__


class WritePermissionDeniedException(PermissionDeniedException, StoreError):
    """
    Raised when the ACL doesn't permit writing
    """
    __module__ = __name__


from salamoia.tests import *
runDocTests()