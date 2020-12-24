# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/cache.py
# Compiled at: 2016-05-04 07:56:27
import time
_max_cache_age = 600
_stamp = time.time()
_lists = {}

def _clear():
    global _lists
    global _stamp
    _stamp = time.time()
    _lists = {}


def is_cached(name):
    if time.time() - _stamp > _max_cache_age:
        _clear()
    return name in _lists


def store(name, lst):
    _lists[name] = lst
    return lst


def retrieve(name):
    if is_cached(name):
        return _lists[name]
    else:
        return