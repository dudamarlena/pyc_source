# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aiothrottle\__init__.py
# Compiled at: 2016-08-30 15:55:55
# Size of source mod 2**32: 261 bytes
"""
Providing classes for limiting data rates of asyncio sockets
"""
from .throttle import Throttle, ThrottledStreamReader, limit_rate, unlimit_rate
__version__ = '0.1.3'
__all__ = ('Throttle', 'ThrottledStreamReader', 'limit_rate', 'unlimit_rate')