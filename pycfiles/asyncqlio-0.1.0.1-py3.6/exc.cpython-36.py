# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/exc.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 695 bytes
"""
Exceptions for asyncqlio.
"""

class DatabaseException(Exception):
    __doc__ = '\n    The base class for ALL exceptions.\n\n    Catch this if you wish to catch any custom exception raised inside the lib.\n    '


class SchemaError(DatabaseException):
    __doc__ = '\n    Raised when there is an error in the database schema.\n    '


class IntegrityError(DatabaseException):
    __doc__ = "\n    Raised when a column's integrity is not preserved (e.g. null or unique violations).\n    "


class OperationalError(DatabaseException):
    __doc__ = '\n    Raised when an operational error has occurred.\n    '


class NoSuchColumnError(DatabaseException):
    __doc__ = '\n    Raised when a non-existing column is requested.\n    '