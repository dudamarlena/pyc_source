# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/persistent_dict.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1378 bytes
import os
from . import data_file

class PersistentDict(dict):
    __doc__ = 'A dictionary that persists as a data_file on the filesystem.\n\n    PersistentDict is constructed with a filename, which either does not exist,\n    or contains YAML representing a previously stored value.\n\n    Each time a PersistentDict is mutated, the file is rewritten with the new\n    stored YAML data.\n    '

    def __init__(self, filename):
        self._PersistentDict__filename = filename
        data = data_file.load(filename) if os.path.exists(filename) else {}
        super().__init__(data)

    def clear(self):
        super().clear()
        self._PersistentDict__write()

    def pop(self, *args):
        (super().pop)(*args)
        self._PersistentDict__write()

    def popitem(self):
        super().popitem()
        self._PersistentDict__write()

    def update(self, *args, **kwds):
        (super().update)(*args, **kwds)
        self._PersistentDict__write()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError('Keys for PersistentDict must be strings')
        super().__setitem__(key, value)
        self._PersistentDict__write()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._PersistentDict__write()

    def __write(self):
        ordered = dict(sorted(self.items()))
        data_file.dump(ordered, self._PersistentDict__filename)