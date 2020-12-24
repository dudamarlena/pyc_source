# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mpcabd/Projects/pyentist/env/lib/python3.5/site-packages/pyentist/freezable.py
# Compiled at: 2016-02-23 16:52:33
# Size of source mod 2**32: 806 bytes


class Freezable(object):

    def __init__(self):
        self._is_frozen = False

    def freeze(self):
        self._is_frozen = True
        for prop in dir(self.__class__):
            p = getattr(self.__class__, prop)
            if isinstance(p, property) and p.fset:

                def setter(self, *args, **kwargs):
                    raise AttributeError('Cannot set property {} of object {} because it is frozen.'.format(prop, self))

                setattr(self.__class__, prop, property(p.fget, setter, p.fdel))

    @property
    def is_frozen(self):
        if not hasattr(self, '_is_frozen'):
            self._is_frozen = False
        return self._is_frozen