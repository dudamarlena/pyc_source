# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/exceptions/exceptions.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 2614 bytes
"""
producti_gestio.exceptions.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It contains all the producti-gestio exceptions.
"""

class NotAFunction(Exception):
    __doc__ = '\n    Exceptions thrown if the given parameter is not\n    a callable function.\n    '

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The given parameter is not a callable function.'


class NotABoolean(Exception):
    __doc__ = '\n    Exceptions thrown if the given parameter is not\n    a boolean.\n    '

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The given parameter is not boolean.'


class NotAString(Exception):
    __doc__ = '\n    Exceptions thrown if the given parameter is not\n    a string.\n    '

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The given parameter is not a string.'


class NotAnInteger(Exception):
    __doc__ = '\n    Exceptions thrown if the given parameter is not\n    an integer.\n    '

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The given parameter is not an integer.'


class NotDefinedFunction(Exception):
    __doc__ = '\n    Exceptions thrown if the function is not\n    defined.\n    '

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The handler function is not defined.'