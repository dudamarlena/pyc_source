# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/parser/helpers.py
# Compiled at: 2017-09-13 03:09:29
# Size of source mod 2**32: 708 bytes
from collections import namedtuple
from heapq_max import *
Record = namedtuple('Record', ['value', 'uuid'])

class rHeap(object):
    __doc__ = "\n    This wrapper class holds Record namedtuples in a heap.\n    r = Record(uuid, value)\n\n    h = rHeap()\n    h.push(Record('1426828011', 9)\n    h.pop_x(1)\n    "

    def __init__(self):
        self._data = []

    def push(self, record):
        heappush_max(self._data, record)

    def pop_x(self, x):
        x_largest = []
        for i in range(x):
            x_largest.append(heappop_max(self._data).uuid)

        return x_largest

    def size(self):
        return len(self._data)