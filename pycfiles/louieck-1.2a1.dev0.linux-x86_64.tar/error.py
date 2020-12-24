# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/louieck/error.py
# Compiled at: 2018-05-31 10:36:55
"""Error types for Louie."""

class LouieError(Exception):
    """Base class for all Louie errors"""
    pass


class DispatcherError(LouieError):
    """Base class for all Dispatcher errors"""
    pass


class DispatcherKeyError(KeyError, DispatcherError):
    """Error raised when unknown (sender, signal) specified"""
    pass


class DispatcherTypeError(TypeError, DispatcherError):
    """Error raised when inappropriate signal-type specified (None)"""
    pass


class PluginTypeError(TypeError, LouieError):
    """Error raise when trying to install more than one plugin of a
    certain type."""
    pass