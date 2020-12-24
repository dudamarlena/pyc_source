# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sven/0/_sdks/python/sven-2.7/lib/python2.7/site-packages/knewt/store.py
# Compiled at: 2018-02-12 16:52:50
import hashlib

def object_store(density=3):
    store = {}
    hasher = lambda k: k
    hasher = lambda v: hashlib.md5(str(v)).hexdigest()[:density]
    update = lambda k, v: store.update({hasher(k): v})
    let = lambda k, v: update(hasher(k), v)
    get = lambda k: store[hasher(k)]
    return (let, get, hasher)


def primitive_store():
    store = {}
    hasher = lambda k: k
    update = lambda k, v: store.update({hasher(k): v})
    let = lambda k, v: update(hasher(k), v)
    get = lambda k: store[hasher(k)]
    return (let, get, hasher)