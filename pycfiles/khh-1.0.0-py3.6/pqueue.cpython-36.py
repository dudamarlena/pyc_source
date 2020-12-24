# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/khh/pqueue.py
# Compiled at: 2017-11-27 17:45:48
# Size of source mod 2**32: 1038 bytes
import itertools
from heapq import heappush, heappop, nlargest, heapify

class PriorityQueue(object):
    __doc__ = 'Vanilla pq implementation using python libraries.'

    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def push(self, hash_code, priority=0):
        self.remove(hash_code)
        count = next(self.counter)
        entry = [priority, count, hash_code]
        self.entry_finder[hash_code] = entry
        heappush(self.pq, entry)

    def remove(self, hash_code):
        if hash_code in self.entry_finder:
            entry = self.entry_finder.pop(hash_code)
            self.pq.remove(entry)
            heapify(self.pq)
            return entry

    def pop(self):
        while self.pq:
            priority, count, hash_code = heappop(self.pq)
            del self.entry_finder[hash_code]
            return hash_code

        raise KeyError('pop from an empty priority queue')

    def nlargest(self, n):
        return [entry[2] for entry in nlargest(n, self.pq)]

    def __len__(self):
        return len(self.pq)