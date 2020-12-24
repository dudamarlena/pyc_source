# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\simplru\test.py
# Compiled at: 2017-08-01 09:44:55
from simplru import lru_cache

@lru_cache(maxsize=2)
def f(x):
    return x ** 2


for i in [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6]:
    print f(i)
    print f.cache_info()