# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/luqum/exceptions.py
# Compiled at: 2018-06-12 11:31:53
# Size of source mod 2**32: 655 bytes


class InconsistentQueryException(Exception):
    __doc__ = 'Raised when a query have a problem in its structure\n    '


class OrAndAndOnSameLevel(InconsistentQueryException):
    __doc__ = "\n    Raised when a OR and a AND are on the same level as we don't know how to\n    handle this case\n    "


class NestedSearchFieldException(InconsistentQueryException):
    __doc__ = "\n    Raised when a SearchField is nested in an other SearchField as it doesn't\n    make sense. For Instance field1:(spam AND field2:eggs)\n    "


class ObjectSearchFieldException(InconsistentQueryException):
    __doc__ = '\n    Raised when a doted field name is queried which is not an object field\n    '