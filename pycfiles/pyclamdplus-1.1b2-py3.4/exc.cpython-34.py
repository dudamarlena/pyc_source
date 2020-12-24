# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyclamdplus/exc.py
# Compiled at: 2015-11-10 07:07:03
# Size of source mod 2**32: 1570 bytes
"""
Exceptions raised by :mod:`pyclamdplus`.

"""
__all__ = ('PyclamdplusException', 'ConnectionError', 'RequestError', 'BadTargetError')

class PyclamdplusException(Exception):
    __doc__ = '\n    Base exception for Pyclamdplus.\n    \n    '


class ConnectionError(PyclamdplusException):
    __doc__ = '\n    Exception raised when there was a problem trying to connect to the daemon.\n    \n    '


class RequestError(PyclamdplusException):
    __doc__ = "\n    Exception raised when Clamd did not execute a request we've made.\n    \n    "


class BadTargetError(RequestError):
    __doc__ = '\n    Exception raised when a bad target (file or directory) was requested to be\n    scanned.\n    \n    '