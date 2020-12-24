# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/apljungquist/docs/2020/nopy/public/src/nopy/fib_py.py
# Compiled at: 2020-01-25 12:40:15
# Size of source mod 2**32: 252 bytes
import functools

def fib_naive(n):
    if n >= 2:
        return fib_naive(n - 1) + fib_naive(n - 2)
    return 1


@functools.lru_cache(maxsize=100)
def fib_cached(n):
    if n >= 2:
        return fib_cached(n - 1) + fib_cached(n - 2)
    return 1