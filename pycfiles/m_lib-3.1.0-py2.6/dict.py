# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/lazy/dict.py
# Compiled at: 2016-07-25 10:38:46
"""Lazy dictionaries calculate self content upon first access"""

class LazyDict:
    """Abstract parent of all lazy dictionaries"""

    def _init(self):
        raise NotImplementedError

    def __getattr__(self, attr):
        if self.data is None:
            self._init()
        return getattr(self.data, attr)

    def __getitem__(self, key):
        if self.data is None:
            self._init()
        return self.data[key]

    def __setitem__(self, key, value):
        if self.data is None:
            self._init()
        self.data[key] = value
        return


class LazyDictInitFunc(LazyDict):
    """Lazy dict that initializes itself by calling supplied init function"""

    def __init__(self, init=None, *args, **kw):
        self.init = init
        self.data = None
        self.args = args
        self.kw = kw
        return

    def _init(self):
        init = self.init
        if init is None:
            data = {}
        else:
            data = init(*self.args, **self.kw)
        self.data = data
        return