# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\simplru\simplru.py
# Compiled at: 2017-08-01 10:09:06
"""lru_cahce.py - A backport of Python 3 LRU Cache functionality for Python 2
"""
__all__ = [
 'lru_cache']
from collections import namedtuple
from functools import update_wrapper
try:
    from _thread import RLock
except ImportError:

    class RLock:
        """Dummy reentrant lock for builds without threads"""

        def __enter__(self):
            pass

        def __exit__(self, exctype, excinst, exctb):
            pass


_CacheInfo = namedtuple('CacheInfo', ['hits', 'misses', 'maxsize', 'currsize'])

class _HashedSeq(list):
    """ This class guarantees that hash() will be called no more than once
        per element.  This is important because the lru_cache() will hash
        the key multiple times on a cache miss.
    """
    __slots__ = 'hashvalue'

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue


def _make_key(args, kwds, typed, kwd_mark=(
 object(),), fasttypes={
 int, str, frozenset, type(None)}, tuple=tuple, type=type, len=len):
    """Make a cache key from optionally typed positional and keyword arguments
    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.
    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.
    """
    key = args
    if kwds:
        key += kwd_mark
        for item in kwds.items():
            key += item

    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for v in kwds.values())
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedSeq(key)


def lru_cache(maxsize=128, typed=False):
    """Least-recently-used cache decorator.
    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.
    If *typed* is True, arguments of different types will be cached separately.
    For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.
    Arguments to the cached function must be hashable.
    View the cache statistics named tuple (hits, misses, maxsize, currsize)
    with f.cache_info().  Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.
    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used
    """
    if maxsize is not None and not isinstance(maxsize, int):
        raise TypeError('Expected maxsize to be an integer or None')

    def decorating_function(user_function):
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
        return update_wrapper(wrapper, user_function)

    return decorating_function


def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    sentinel = object()
    make_key = _make_key
    PREV, NEXT, KEY, RESULT = (0, 1, 2, 3)
    cache = {}
    cache_get = cache.get
    cache_len = cache.__len__
    lock = RLock()

    class nonlocal:
        hits = 0
        misses = 0
        full = False
        root = []
        root[:] = [root, root, None, None]

    if maxsize == 0:

        def wrapper(*args, **kwds):
            result = user_function(*args, **kwds)
            nonlocal.misses += 1
            return result

    elif maxsize is None:

        def wrapper(*args, **kwds):
            key = make_key(args, kwds, typed)
            result = cache_get(key, sentinel)
            if result is not sentinel:
                nonlocal.hits += 1
                return result
            result = user_function(*args, **kwds)
            cache[key] = result
            nonlocal.misses += 1
            return result

    else:

        def wrapper(*args, **kwds):
            key = make_key(args, kwds, typed)
            with lock:
                link = cache_get(key)
                if link is not None:
                    link_prev, link_next, _key, result = link
                    link_prev[NEXT] = link_next
                    link_next[PREV] = link_prev
                    last = nonlocal.root[PREV]
                    last[NEXT] = nonlocal.root[PREV] = link
                    link[PREV] = last
                    link[NEXT] = nonlocal.root
                    nonlocal.hits += 1
                    return result
            result = user_function(*args, **kwds)
            with lock:
                if key in cache:
                    pass
                elif nonlocal.full:
                    oldroot = nonlocal.root
                    oldroot[KEY] = key
                    oldroot[RESULT] = result
                    nonlocal.root = oldroot[NEXT]
                    oldkey = nonlocal.root[KEY]
                    oldresult = nonlocal.root[RESULT]
                    nonlocal.root[KEY] = nonlocal.root[RESULT] = None
                    del cache[oldkey]
                    cache[key] = oldroot
                else:
                    last = nonlocal.root[PREV]
                    link = [last, nonlocal.root, key, result]
                    last[NEXT] = nonlocal.root[PREV] = cache[key] = link
                    nonlocal.full = cache_len() >= maxsize
                nonlocal.misses += 1
            return result

    def cache_info():
        """Report cache statistics"""
        with lock:
            return _CacheInfo(nonlocal.hits, nonlocal.misses, maxsize, cache_len())

    def cache_clear():
        """Clear the cache and cache statistics"""
        with lock:
            cache.clear()
            nonlocal.root[:] = [nonlocal.root, nonlocal.root, None, None]
            nonlocal.hits = nonlocal.misses = 0
            nonlocal.full = False
        return

    wrapper.cache_info = cache_info
    wrapper.cache_clear = cache_clear
    return wrapper