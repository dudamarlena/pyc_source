# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/cache.py
# Compiled at: 2018-08-17 21:53:27
from __future__ import print_function

class SnapPyCache(dict):
    """
    Implementation of a simple cache used by the Manifold and Triangulation
    to save the results of methods which require a significant amount of
    computation.
    
    This cache uses the tuple (method.__name, args, kwargs) as its key.
    """
    debug = False
    _clear = dict.clear

    def save(self, answer, method_name, *args, **kwargs):
        self[(method_name, args, tuple(kwargs.items()))] = answer
        return answer

    def lookup(self, method_name, *args, **kwargs):
        return self[(method_name, args, tuple(kwargs.items()))]

    def clear(self, key=None, message=''):
        if self.debug:
            print('_clear_cache: %s' % message)
        if key is None:
            self._clear()
        else:
            self.pop(key)
        return