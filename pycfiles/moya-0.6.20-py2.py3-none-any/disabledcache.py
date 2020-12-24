# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/cache/disabledcache.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from .base import Cache

class DisabledCache(Cache):
    cache_backend_name = b'disabled'
    enabled = False

    def get(self, key, default=None):
        return default

    def set(self, key, value, time=0):
        pass

    def delete(self, key):
        pass