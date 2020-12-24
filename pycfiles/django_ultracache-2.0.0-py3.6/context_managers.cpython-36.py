# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/context_managers.py
# Compiled at: 2019-06-02 16:42:08
# Size of source mod 2**32: 1051 bytes
import hashlib
from django.core.cache import cache
from ultracache import _thread_locals
from ultracache.utils import cache_meta

class EmptyMarker:
    pass


empty_marker_1 = EmptyMarker()
empty_marker_2 = EmptyMarker()

class Ultracache:

    def __init__(self, timeout, *params, request=None):
        self.timeout = timeout
        self.params = params
        self.request = request
        self._cached = empty_marker_1
        s = ':'.join([str(p) for p in self.params])
        hashed = hashlib.md5(s.encode('utf-8')).hexdigest()
        self.cache_key = 'ucache-get-%s' % hashed

    @property
    def cached(self):
        if self._cached is empty_marker_1:
            self._cached = cache.get(self.cache_key, empty_marker_2)
        return self._cached

    def __bool__(self):
        return self.cached is not empty_marker_2

    def cache(self, value):
        cache.set(self.cache_key, value)
        cache_meta((_thread_locals.ultracache_recorder),
          (self.cache_key),
          request=(self.request))