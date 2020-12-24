# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/memojito/__init__.py
# Compiled at: 2007-05-01 00:35:45
"""
see README.txt
"""
_marker = object()

class Memojito(object):
    __module__ = __name__
    propname = '_memojito_'

    def clear(self, inst):
        if hasattr(inst, self.propname):
            delattr(inst, self.propname)

    def clearbefore(self, func):

        def clear(*args, **kwargs):
            inst = args[0]
            self.clear(inst)
            return func(*args, **kwargs)

        return clear

    def clearafter(self, func):

        def clear(*args, **kwargs):
            inst = args[0]
            val = func(*args, **kwargs)
            self.clear(inst)
            return val

        return clear

    def memoizedproperty(self, func):
        return property(self.memoize(func))

    def memoize(self, func):

        def memogetter(*args, **kwargs):
            inst = args[0]
            cache = getattr(inst, self.propname, dict())
            key = (
             func.__name__, args, frozenset(kwargs.items()))
            key = hash(key)
            val = cache.get(key, _marker)
            if val is _marker:
                val = func(*args, **kwargs)
                cache[key] = val
                setattr(inst, self.propname, cache)
            return val

        return memogetter


_m = Memojito()
memoize = _m.memoize
memoizedproperty = _m.memoizedproperty
clearbefore = _m.clearbefore
clearafter = _m.clearafter