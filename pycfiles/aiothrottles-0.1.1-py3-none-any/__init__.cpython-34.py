# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aiothrottle\__init__.py
# Compiled at: 2016-08-30 15:55:55
# Size of source mod 2**32: 261 bytes
__doc__ = '\nProviding classes for limiting data rates of asyncio sockets\n'
from .throttle import Throttle, ThrottledStreamReader, limit_rate, unlimit_rate
__version__ = '0.1.3'
__all__ = ('Throttle', 'ThrottledStreamReader', 'limit_rate', 'unlimit_rate')