# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/util/frozen.py
# Compiled at: 2016-11-03 01:40:19


class Frozen(object):
    __isfrozen = False

    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise AttributeError('%r is not an attribute of class %s. Call "unfreeze()" to allow addition of new attributes' % (
             key, self))
        object.__setattr__(self, key, value)

    def freeze(self):
        """Freeze the object so that only existing properties can be set"""
        self.__isfrozen = True

    def unfreeze(self):
        """Unfreeze the object so that additional properties can be added"""
        self.__isfrozen = False