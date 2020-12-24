# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/squidnet/combomethods.py
# Compiled at: 2010-04-07 08:54:00
import functools
__all__ = ('combomethod', )

class combomethod(object):

    def __init__(self, method):
        self.method = method

    def __get__(self, obj=None, objtype=None):

        @functools.wraps(self.method)
        def _wrapper(*args, **kwargs):
            if obj is not None:
                return self.method(obj, *args, **kwargs)
            else:
                return self.method(objtype, *args, **kwargs)
            return

        return _wrapper