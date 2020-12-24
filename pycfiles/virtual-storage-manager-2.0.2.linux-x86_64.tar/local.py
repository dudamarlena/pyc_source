# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/local.py
# Compiled at: 2016-06-13 14:11:03
"""Greenthread local storage of variables using weak references"""
import weakref
from eventlet import corolocal

class WeakLocal(corolocal.local):

    def __getattribute__(self, attr):
        rval = corolocal.local.__getattribute__(self, attr)
        if rval:
            rval = rval()
        return rval

    def __setattr__(self, attr, value):
        value = weakref.ref(value)
        return corolocal.local.__setattr__(self, attr, value)


store = WeakLocal()
weak_store = WeakLocal()
strong_store = corolocal.local