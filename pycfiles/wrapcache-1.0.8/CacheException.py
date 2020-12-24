# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\dev_ws\wrapcache\wrapcache\adapter\CacheException.py
# Compiled at: 2016-01-10 20:19:35
"""
Cache Exceptions
"""

class CacheExpiredException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DBNotSetException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)