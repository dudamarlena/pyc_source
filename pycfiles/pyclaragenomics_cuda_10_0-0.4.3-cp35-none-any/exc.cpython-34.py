# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyclamdplus/exc.py
# Compiled at: 2015-11-10 07:07:03
# Size of source mod 2**32: 1570 bytes
__doc__ = '\nExceptions raised by :mod:`pyclamdplus`.\n\n'
__all__ = ('PyclamdplusException', 'ConnectionError', 'RequestError', 'BadTargetError')

class PyclamdplusException(Exception):
    """PyclamdplusException"""
    pass


class ConnectionError(PyclamdplusException):
    """ConnectionError"""
    pass


class RequestError(PyclamdplusException):
    """RequestError"""
    pass


class BadTargetError(RequestError):
    """BadTargetError"""
    pass