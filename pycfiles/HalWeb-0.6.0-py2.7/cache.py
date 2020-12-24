# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/halicea/cache.py
# Compiled at: 2011-12-30 07:30:29
from conf.settings import RUN
if RUN == 'appengine':
    from google.appengine.api import memcache
else:
    from memcache import Client
    memcache = Client('localhost', 1120)
__cache__ = memcache

def get(key, default=None):
    return __cache__.get(key) or default


def set(key, item, time=0, namespace=None):
    return __cache__.set(key, item, time=time, namespace=namespace)


def delete(key):
    return __cache__.delete(key)