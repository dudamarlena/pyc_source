# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/site-packages/arc_cache/decorator.py
# Compiled at: 2015-11-25 23:58:42
# Size of source mod 2**32: 5591 bytes
"""Memoization decorator that caches a function's return value.

Subsequent calls of the same function with the same arguments will retrieve the
cached value, instead of re-evaluating. Adapted from the Python implementation
of ``lru_cache`` in Python 3.4.
"""
from functools import wraps, partial, _make_key
from collections import namedtuple, OrderedDict as od
_CacheInfo = namedtuple('CacheInfo', ['hits', 'misses', 'max_size',
 't1_size', 't2_size', 'split'])

def _shift(src, dst):
    """Pops the first item in ``src`` and moves it to ``dst``."""
    key, value = src.popitem(last=False)
    dst.append(key)


def _pop(src):
    """Pops the first item in ``src``."""
    src.pop(0)


def _delta(x, y):
    """Computes |y|/|x|."""
    return max(float(len(y)) / float(len(x)), 1.0)


def _adapt_plus(b1, b2, max_size, p):
    return min(p + _delta(b1, b2), float(max_size))


def _adapt_minus(b2, b1, p):
    return max(p - _delta(b2, b1), 0.0)


def arc_cache(max_size=128, typed=False):
    """Decorator to memoize the given callable using an adaptive replacement cache.

    :param max_size: maximum number of elements in the cache
    :type max_size: int

    ``max_size`` must be a positive integer.

    If ``typed`` is True, arguments of different types will be cached separately.
    For example, ``f(3.0)`` and ``f(3)`` will be treated as distinct calls with
    distinct results.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple
    ``(hits, misses, max_size, t1_size, t2_size, split)`` with ``f.cache_info()``.
    Reset the cache using ``f.cache_clear()``.

    TODO worry about thread-safety
    """
    if not isinstance(max_size, int):
        raise TypeError('max_size must be of type int.')
    if max_size is None or 0 >= max_size:
        raise ValueError('max_size must be a positive integer. If you want an unbounded cache, use functools.lru_cache.')

    def decorating_function(func):
        t1, b1, t2, b2 = (
         od(), [], od(), [])
        p = max_size / 2
        hits = misses = 0
        evict_t1 = partial(_shift, t1, b1)
        evict_t2 = partial(_shift, t2, b2)
        evict_b1 = partial(_pop, b1)
        evict_b2 = partial(_pop, b2)
        adapt_plus = partial(_adapt_plus, b1, b2, max_size)
        adapt_minus = partial(_adapt_minus, b2, b1)

        def evict_t1_t2():
            if t1 and len(t1) > p:
                evict_t1()
            else:
                evict_t2()

        def evict_l1():
            if b1:
                evict_b1()
                evict_t1_t2()
            else:
                t1.popitem(last=False)

        def evict_l2():
            total = len(t1) + len(b1) + len(t2) + len(b2)
            if total >= max_size:
                if total == 2 * max_size:
                    evict_b2()
                evict_t1_t2()

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal hits
            nonlocal misses
            nonlocal p
            key = _make_key(args, kwargs, typed)
            if key in t1:
                hits += 1
                result = t1[key]
                del t1[key]
                t2[key] = result
                return result
            if key in t2:
                hits += 1
                t2.move_to_end(key)
                return t2[key]
            misses += 1
            result = func(*args, **kwargs)
            if key in b1:
                p = adapt_plus(p)
                evict_t1_t2()
                t2[key] = result
            else:
                if key in b2:
                    p = adapt_minus(p)
                    evict_t1_t2()
                    t2[key] = result
                else:
                    len_l1 = len(t1) + len(b1)
            if len_l1 == max_size:
                evict_l1()
            else:
                if len_l1 < max_size:
                    evict_l2()
                t1[key] = result
            return result

        def cache_info():
            return _CacheInfo(hits, misses, max_size, len(t1), len(t2), p)

        def cache_clear():
            nonlocal b1
            nonlocal b2
            nonlocal hits
            nonlocal misses
            nonlocal p
            nonlocal t1
            nonlocal t2
            t1, b1, t2, b2 = (
             od(), [], od(), [])
            p = max_size / 2
            hits = misses = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper

    return decorating_function