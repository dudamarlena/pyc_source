# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/cfs.py
# Compiled at: 2013-10-14 11:16:23
"""
This file is part of the web2py Web Framework
Copyrighted by Massimo Di Pierro <mdipierro@cs.depaul.edu>
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)

Functions required to execute app components
============================================

FOR INTERNAL USE ONLY
"""
from os import stat
import thread, logging
from gluon.fileutils import read_file
cfs = {}
cfs_lock = thread.allocate_lock()

def getcfs(key, filename, filter=None):
    """
    Caches the *filtered* file `filename` with `key` until the file is
    modified.

    :param key: the cache key
    :param filename: the file to cache
    :param filter: is the function used for filtering. Normally `filename` is a
        .py file and `filter` is a function that bytecode compiles the file.
        In this way the bytecode compiled file is cached. (Default = None)

    This is used on Google App Engine since pyc files cannot be saved.
    """
    try:
        t = stat(filename).st_mtime
    except OSError:
        if callable(filter):
            return filter()
        return ''

    cfs_lock.acquire()
    item = cfs.get(key, None)
    cfs_lock.release()
    if item and item[0] == t:
        return item[1]
    else:
        if not callable(filter):
            data = read_file(filename)
        else:
            data = filter()
        cfs_lock.acquire()
        cfs[key] = (t, data)
        cfs_lock.release()
        return data