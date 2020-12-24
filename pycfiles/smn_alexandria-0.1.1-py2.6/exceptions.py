# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/dsl/exceptions.py
# Compiled at: 2010-04-19 04:42:57


class BaseException(Exception):
    """
    All exceptions should subclass this so we can trap all our applications
    errors if needed with one `except BaseException` statment
    """
    pass


class InvalidInputException(BaseException):
    """
    Raised when a value is received that doesn't match one of the given
    options. I.E. Menu has options 1-4 and the user requests option 5.
    """
    pass