# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/storage/models/storagedict.py
# Compiled at: 2020-01-30 06:21:49
# Size of source mod 2**32: 1784 bytes
from dataclay import DataClayObject, dclayMethod

class StorageDict(DataClayObject):
    __doc__ = 'Demonstration of the StorageDict class.\n\n    This class is prepared for demonstration purposes and is not suitable,\n    as it is right now, for HPC applications and production workflows.\n\n    @ClassField _dict anything\n    '

    @dclayMethod()
    def __init__(self):
        self._dict = dict()

    @dclayMethod(return_='int')
    def __len__(self):
        return len(self._dict)

    @dclayMethod(key='anything', return_='anything')
    def __getitem__(self, key):
        return self._dict[key]

    @dclayMethod(key='anything', value='anything')
    def __setitem__(self, key, value):
        self._dict[key] = value

    @dclayMethod(key='anything')
    def __delitem__(self, key):
        del self._dict[key]

    @dclayMethod(_local=True, return_='anything')
    def __iter__(self):
        return iter(self._dict)

    @dclayMethod(key='anything', return_='bool')
    def __contains__(self, key):
        return key in self._dict

    @dclayMethod(_local=True, return_='anything')
    def keys(self):
        return self._dict.keys()

    @dclayMethod(_local=True, return_='anything')
    def items(self):
        return self._dict.items()

    @dclayMethod(_local=True, return_='anything')
    def values(self):
        return self._dict.values()

    @dclayMethod(return_='anything')
    def split(self):
        from itertools import cycle
        out_a = dict()
        out_b = dict()
        for (key, value), out in zip(self._dict.items(), cycle(out_a, out_b)):
            out[key] = value

        return (out_a, out_b)

    @dclayMethod(return_='str')
    def __str__(self):
        return str(self._dict)