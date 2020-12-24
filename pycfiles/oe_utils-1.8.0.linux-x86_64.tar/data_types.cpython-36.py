# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/data/data_types.py
# Compiled at: 2020-02-12 07:50:31
# Size of source mod 2**32: 1321 bytes
from sqlalchemy.ext.mutable import Mutable

class MutableList(Mutable, list):

    @classmethod
    def coerce(cls, key, value):
        """Convert plain list to MutableList."""
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def __getstate__(self):
        return list(self)

    def __setstate__(self, state):
        self.extend(state)

    def append(self, value):
        list.append(self, value)
        self.changed()

    def extend(self, iterable):
        list.extend(self, iterable)
        self.changed()

    def insert(self, index, item):
        list.insert(self, index, item)
        self.changed()

    def pop(self, index=None):
        if index:
            list.pop(self, index)
        else:
            list.pop(self)
        self.changed()

    def remove(self, item):
        list.remove(self, item)
        self.changed()

    def reverse(self):
        list.reverse(self)
        self.changed()

    def sort(self, **kwargs):
        (list.sort)(self, **kwargs)
        self.changed()