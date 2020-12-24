# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\herokuify\cache.py
# Compiled at: 2013-01-22 21:14:34
from __future__ import unicode_literals
from memcacheify import memcacheify

def get_cache_config():
    """Return a fully configured Django ``CACHES`` setting.

    Scans environment variables for available memcache addon.
    Additionally includes Django's LocMemCache backend under ``"locmem"``
    cache name.
    """
    caches = memcacheify()
    caches[b'locmem'] = {b'BACKEND': b'django.core.cache.backends.locmem.LocMemCache'}
    return caches