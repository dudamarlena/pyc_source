# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/error.py
# Compiled at: 2019-08-18 17:24:05
from pyasn1.error import PyAsn1Error
from pysnmp.error import PySnmpError

class SmiError(PySnmpError, PyAsn1Error):
    __module__ = __name__


class MibLoadError(SmiError):
    __module__ = __name__


class MibNotFoundError(MibLoadError):
    __module__ = __name__


class MibOperationError(SmiError):
    __module__ = __name__

    def __init__(self, **kwargs):
        self.__outArgs = kwargs

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.__outArgs)

    def __getitem__(self, key):
        return self.__outArgs[key]

    def __contains__(self, key):
        return key in self.__outArgs

    def get(self, key, defVal=None):
        return self.__outArgs.get(key, defVal)

    def keys(self):
        return self.__outArgs.keys()

    def update(self, d):
        self.__outArgs.update(d)


class TooBigError(MibOperationError):
    __module__ = __name__


class NoSuchNameError(MibOperationError):
    __module__ = __name__


class BadValueError(MibOperationError):
    __module__ = __name__


class ReadOnlyError(MibOperationError):
    __module__ = __name__


class GenError(MibOperationError):
    __module__ = __name__


class NoAccessError(MibOperationError):
    __module__ = __name__


class WrongTypeError(MibOperationError):
    __module__ = __name__


class WrongLengthError(MibOperationError):
    __module__ = __name__


class WrongEncodingError(MibOperationError):
    __module__ = __name__


class WrongValueError(MibOperationError):
    __module__ = __name__


class NoCreationError(MibOperationError):
    __module__ = __name__


class InconsistentValueError(MibOperationError):
    __module__ = __name__


class ResourceUnavailableError(MibOperationError):
    __module__ = __name__


class CommitFailedError(MibOperationError):
    __module__ = __name__


class UndoFailedError(MibOperationError):
    __module__ = __name__


class AuthorizationError(MibOperationError):
    __module__ = __name__


class NotWritableError(MibOperationError):
    __module__ = __name__


class InconsistentNameError(MibOperationError):
    __module__ = __name__


class NoSuchObjectError(NoSuchNameError):
    __module__ = __name__


class NoSuchInstanceError(NoSuchNameError):
    __module__ = __name__


class EndOfMibViewError(NoSuchNameError):
    __module__ = __name__


class TableRowManagement(MibOperationError):
    __module__ = __name__


class RowCreationWanted(TableRowManagement):
    __module__ = __name__


class RowDestructionWanted(TableRowManagement):
    __module__ = __name__