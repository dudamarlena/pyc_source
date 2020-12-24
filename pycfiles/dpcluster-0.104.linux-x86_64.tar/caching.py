# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/dpcluster/caching.py
# Compiled at: 2013-05-29 16:52:07
import numpy as np, hashlib
enabled = True
cache = {}

def h(a):
    try:
        return hash(a)
    except:
        if isinstance(a, np.ndarray):
            rt = hashlib.sha1(a).hexdigest()
            return rt


def all_read_only(rt):
    try:
        for a in rt:
            if isinstance(a, np.ndarray):
                a.setflags(write=False)

    except TypeError:
        if isinstance(rt, np.ndarray):
            rt.setflags(write=False)

    return rt


hsh = lambda x: hash(tuple(h(a) for a in x))

def cached(f):

    def new_f(*args):
        fh = hsh((f,))
        key = hsh(args)
        if fh not in cache:
            cache[fh] = [
             None, None]
        if cache[fh][0] != key:
            rt = all_read_only(f(*args))
            cache[fh] = (key, rt)
        return cache[fh][1]

    if enabled:
        return new_f
    else:
        return f