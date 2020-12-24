# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/util/frozen.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 876 bytes


class Frozen(object):
    _Frozen__isfrozen = False

    def __setattr__(self, key, value):
        if self._Frozen__isfrozen:
            if not hasattr(self, key):
                raise AttributeError('%r is not an attribute of class %s. Call "unfreeze()" to allow addition of new attributes' % (
                 key, self))
        object.__setattr__(self, key, value)

    def freeze(self):
        """Freeze the object so that only existing properties can be set"""
        self._Frozen__isfrozen = True

    def unfreeze(self):
        """Unfreeze the object so that additional properties can be added"""
        self._Frozen__isfrozen = False