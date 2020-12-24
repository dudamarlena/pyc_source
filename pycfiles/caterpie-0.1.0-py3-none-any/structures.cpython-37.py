# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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