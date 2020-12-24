# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gmsdk/exceptions.py
# Compiled at: 2015-04-04 04:52:46


class Error(Exception):
    """
    Base class for exceptions in this module.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidVersionError(Error):
    """
    Raised exception in case invalid version supplied
    """
    pass


class InvalidStatusError(Error):
    """
    Raised exception in case invalid version supplied
    """
    pass


class MissingDataError(Error):
    """
    Raised exception in case invalid version supplied
    """
    pass