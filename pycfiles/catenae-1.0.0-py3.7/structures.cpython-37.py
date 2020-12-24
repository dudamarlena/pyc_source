# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/structures.py
# Compiled at: 2019-08-07 08:55:15
# Size of source mod 2**32: 839 bytes
from collections import OrderedDict
from orderedset import OrderedSet

class CircularOrderedDict(OrderedDict):

    def __init__(self, size=0):
        super(CircularOrderedDict, self).__init__()
        self.size = size

    def __setitem__(self, key, value):
        super(CircularOrderedDict, self).__setitem__(key, value)
        self._truncate()

    def _truncate(self):
        if len(self) > self.size:
            self.popitem(last=False)


class CircularOrderedSet(OrderedSet):

    def __init__(self, size=0):
        super(CircularOrderedSet, self).__init__()
        self.size = size

    def add(self, value):
        super(CircularOrderedSet, self).add(value)
        self._truncate()

    def _truncate(self):
        if len(self) > self.size:
            self.pop(last=False)