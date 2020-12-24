# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\errors.py
# Compiled at: 2017-12-11 20:12:50


class TimeoutError(RuntimeError):
    """Stackless operation timed out"""
    pass


class CancelledError(RuntimeError):
    """The operation was cancelled"""
    pass


class AsyncCallFailed(RuntimeError):
    """Exception raised when an on_failure callback is made"""
    pass