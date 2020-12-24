# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/g-braeunlich/IPyOpt/setup_helpers/lazy_extension_loader.py
# Compiled at: 2019-08-07 10:42:15
# Size of source mod 2**32: 651 bytes
"""Provides a way to define extensions without importing modules
not installed before setup
"""

class LazyList(list):
    __doc__ = 'Evaluates extension list lazyly.\n    pattern taken from http://tinyurl.com/qb8478q'

    def __init__(self, generator):
        super().__init__()
        self._list = None
        self._generator = generator

    def get(self):
        if self._list is None:
            self._list = list(self._generator)
        return self._list

    def __iter__(self):
        for e in self.get():
            yield e

    def __getitem__(self, i):
        return self.get()[i]

    def __len__(self):
        return len(self.get())