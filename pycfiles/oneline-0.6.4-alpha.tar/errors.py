# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bson/errors.py
# Compiled at: 2014-03-05 17:52:04
"""Exceptions raised by the BSON package."""

class BSONError(Exception):
    """Base class for all BSON exceptions.
    """
    pass


class InvalidBSON(BSONError):
    """Raised when trying to create a BSON object from invalid data.
    """
    pass


class InvalidStringData(BSONError):
    """Raised when trying to encode a string containing non-UTF8 data.
    """
    pass


class InvalidDocument(BSONError):
    """Raised when trying to create a BSON object from an invalid document.
    """
    pass


class InvalidId(BSONError):
    """Raised when trying to create an ObjectId from invalid data.
    """
    pass