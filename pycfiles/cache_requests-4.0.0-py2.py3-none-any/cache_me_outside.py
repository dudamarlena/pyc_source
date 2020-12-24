# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cache_me_outside.py
# Compiled at: 2017-04-02 02:08:13
try:
    from functools import lru_cache as cache_me_outside
except ImportError:
    from backports.functools_lru_cache import lru_cache as cache_me_outside