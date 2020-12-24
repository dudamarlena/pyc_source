# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kutana/storages/naive_memory.py
# Compiled at: 2020-05-02 08:54:53
# Size of source mod 2**32: 784 bytes
from ..storage import Storage

class NaiveMemory(Storage):
    __doc__ = "\n    Storage for storing data with naive approach. It uses only memory\n    and will wipe some portion of stored data when number of keys\n    will react certain amount.\n\n    It's not persistent and not safe. It's here for tiny projects\n    and debugging.\n    "

    def __init__(self, max_size=2000000):
        self._storage = {}
        self.max_size = max_size

    async def save(self, name, value):
        if len(self._storage) >= self.max_size:
            keys = list(self._storage.keys())
            for k in keys[:self.max_size // 2]:
                self._storage.pop(k)

        self._storage[name] = value

    async def load(self, name, default=None):
        return self._storage.get(name, default)