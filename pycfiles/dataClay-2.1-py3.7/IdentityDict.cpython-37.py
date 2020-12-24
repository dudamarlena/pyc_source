# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/IdentityDict.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 976 bytes
""" Class description goes here. """
import collections
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2016 Barcelona Supercomputing Center (BSC-CNS)'

class IdentityDict(collections.MutableMapping):
    __slots__ = ('internal_dict', )

    def __init__(self):
        self.internal_dict = dict()

    def __setitem__(self, key, value):
        self.internal_dict[id(key)] = (
         key, value)

    def __getitem__(self, item):
        return self.internal_dict[id(item)][1]

    def items(self):
        return self.internal_dict.values()

    def __delitem__(self, key):
        del self.internal_dict[id(key)]

    def __len__(self):
        return len(self.internal_dict)

    def __iter__(self):
        return self.internal_dict.values()

    def __contains__(self, item):
        return id(item) in self.internal_dict