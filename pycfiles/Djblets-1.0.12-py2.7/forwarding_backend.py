# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/cache/forwarding_backend.py
# Compiled at: 2019-06-12 01:17:17
"""A cache backend that forwards to other dynamically-configured backends."""
from __future__ import unicode_literals
import threading
from django.core.signals import request_finished
DEFAULT_FORWARD_CACHE_ALIAS = b'forwarded_backend'

class ForwardingCacheBackend(object):
    """Forwards requests to another cache backend.

    This is used to allow for dynamic configuration of caches that can be
    swapped in and out. By setting this cache backend as the default backend,
    the consumer can easily switch between other cache backends without
    modifying :file:`settings.py` and restarting the app.

    This by default looks for another cache backend in
    ``settings.CACHES['forwarded_backend']``. This can be changed with the
    ``LOCATION`` setting for this cache backend. All requests and attribute
    lookups will be forwarded there.

    If a consumer switches the real cache backend, it can call
    :py:meth:`reset_backend`, and all future cache requests will go to the
    newly computed backend.
    """

    def __init__(self, cache_name=DEFAULT_FORWARD_CACHE_ALIAS, *args, **kwargs):
        self._cache_name = cache_name
        self._backend = None
        self._load_lock = threading.Lock()
        self._load_gen = 0
        return

    @property
    def backend(self):
        """Return the forwarded cache backend."""
        if not self._backend:
            self._load_backend()
        return self._backend

    def reset_backend(self):
        """Reset the forwarded cache backend.

        This must be called after modifying
        ``settings.CACHES['forwarded_backend']`` in order for the new
        backend to be picked up.
        """
        if self._backend:
            try:
                self._backend.close()
            except:
                pass

            self._load_backend()

    def close(self, *args, **kwargs):
        """Close the cache backend."""
        if self._backend:
            self._backend.close(*args, **kwargs)

    def _load_backend(self):
        """Load the caching backend.

        This will replace the current caching backend with a newly loaded
        one, based on the stored cache name.

        Only one thread at a time can load the cache backend. A counter
        is kept that keeps the load generation number. If several threads
        try to reload the backend at once, only one will succeed in doing
        so for that generation.
        """
        cur_load_gen = self._load_gen
        with self._load_lock:
            if self._load_gen == cur_load_gen:
                from django.core.cache import get_cache
                self._backend = get_cache(self._cache_name)
                request_finished.disconnect(self._backend.close)
                self._load_gen = cur_load_gen + 1

    def __contains__(self, key):
        return key in self.backend

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return self.backend.__getattribute__(name)