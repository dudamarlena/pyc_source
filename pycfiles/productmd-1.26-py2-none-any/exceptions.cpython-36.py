# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/exceptions/exceptions.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 2614 bytes
__doc__ = '\nproducti_gestio.exceptions.exceptions\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nIt contains all the producti-gestio exceptions.\n'

class NotAFunction(Exception):
    """NotAFunction"""

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The given parameter is not a callable function.'


class NotABoolean(Exception):
    """NotABoolean"""

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The given parameter is not boolean.'


class NotAString(Exception):
    """NotAString"""

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The given parameter is not a string.'


class NotAnInteger(Exception):
    """NotAnInteger"""

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The given parameter is not an integer.'


class NotDefinedFunction(Exception):
    """NotDefinedFunction"""

    def __init__(self):
        """
        It throws the exception.
        """
        self.message = 'The handler function is not defined.'