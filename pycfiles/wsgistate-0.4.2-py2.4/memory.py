# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wsgistate/memory.py
# Compiled at: 2007-10-22 20:29:02
"""Thread-safe in-memory cache backend."""
import copy, time
try:
    import threading
except ImportError:
    import dummy_threading as threading

from wsgistate import synchronized
from wsgistate.simple import SimpleCache
from wsgistate.cache import WsgiMemoize
from wsgistate.session import CookieSession, URLSession, SessionCache
__all__ = [
 'MemoryCache', 'memoize', 'session', 'urlsession']

def memorymemo_deploy(global_conf, **kw):
    """Paste Deploy loader for caching."""

    def decorator(application):
        _memory_memo_cache = MemoryCache(kw.get('cache'), **kw)
        return WsgiMemoize(application, _memory_memo_cache, **kw)

    return decorator


def memorysess_deploy(global_conf, **kw):
    """Paste Deploy loader for sessions."""

    def decorator(application):
        _memory_base_cache = MemoryCache(kw.get('cache'), **kw)
        _memory_session_cache = SessionCache(_memory_base_cache, **kw)
        return CookieSession(application, _memory_session_cache, **kw)

    return decorator


def memoryurlsess_deploy(global_conf, **kw):
    """Paste Deploy loader for URL encoded sessions.

    @param initstr Database initialization string
    """

    def decorator(application):
        _memory_ubase_cache = MemoryCache(kw.get('cache'), **kw)
        _memory_url_cache = SessionCache(_memory_ubase_cache, **kw)
        return URLSession(application, _memory_url_cache, **kw)

    return decorator


def memoize(**kw):
    """Decorator for caching."""

    def decorator(application):
        _mem_memo_cache = MemoryCache(**kw)
        return WsgiMemoize(application, _mem_memo_cache, **kw)

    return decorator


def session(**kw):
    """Decorator for sessions."""

    def decorator(application):
        _mem_base_cache = MemoryCache(**kw)
        _mem_session_cache = SessionCache(_mem_base_cache, **kw)
        return CookieSession(application, _mem_session_cache, **kw)

    return decorator


def urlsession(**kw):
    """Decorator for URL encoded sessions."""

    def decorator(application):
        _mem_ubase_cache = MemoryCache(**kw)
        _mem_url_cache = SessionCache(_mem_ubase_cache, **kw)
        return URLSession(application, _mem_url_cache, **kw)

    return decorator


class MemoryCache(SimpleCache):
    """Thread-safe in-memory cache backend."""
    __module__ = __name__

    def __init__(self, *a, **kw):
        super(MemoryCache, self).__init__(*a, **kw)
        self._lock = threading.Condition()

    @synchronized
    def get(self, key, default=None):
        """Fetch a given key from the cache. If the key does not exist, return
        default, which itself defaults to None.

        @param key Keyword of item in cache.
        @param default Default value (default: None)
        """
        return copy.deepcopy(super(MemoryCache, self).get(key))

    @synchronized
    def set(self, key, value):
        """Set a value in the cache.

        @param key Keyword of item in cache.
        @param value Value to be inserted in cache.
        """
        super(MemoryCache, self).set(key, value)

    @synchronized
    def delete(self, key):
        """Delete a key from the cache, failing silently.

        @param key Keyword of item in cache.
        """
        super(MemoryCache, self).delete(key)