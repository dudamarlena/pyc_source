# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/storage/models/storagelist.py
# Compiled at: 2020-01-30 06:21:49
# Size of source mod 2**32: 1573 bytes
from dataclay import DataClayObject, dclayMethod

class StorageList(DataClayObject):
    __doc__ = 'Demonstration of the StorageList class.\n\n    This class is prepared for demonstration purposes and is not suitable,\n    as it is right now, for HPC applications and production workflows.\n\n    @ClassField _list anything\n    '

    @dclayMethod()
    def __init__(self):
        self._list = list()

    @dclayMethod(return_='int')
    def __len__(self):
        return len(self._list)

    @dclayMethod(item='anything', return_='bool')
    def __contains__(self, item):
        return item in self._list

    @dclayMethod(item='anything')
    def append(self, item):
        self._list.append(item)

    @dclayMethod(_local=True, return_='anything')
    def __iter__(self):
        return iter(self._list)

    @dclayMethod(_local=True, return_='anything')
    def split(self):
        from itertools import cycle
        out_a = list()
        out_b = list()
        for elem, out in zip(self._list, cycle(out_a, out_b)):
            out.append(elem)

        return (out_a, out_b)

    @dclayMethod(item='anything', return_='anything')
    def __getitem__(self, item):
        return self._list[item]

    @dclayMethod(item='anything', value='anything')
    def __setitem__(self, item, value):
        self._list[item] = value

    @dclayMethod(item='anything')
    def __delitem__(self, item):
        del self._list[item]

    @dclayMethod(return_='str')
    def __str__(self):
        return str(self._list)