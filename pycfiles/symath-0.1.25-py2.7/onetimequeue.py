# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/symath/datastructures/onetimequeue.py
# Compiled at: 2015-08-21 11:58:24
from collections import deque

class onetimequeue(object):

    def __init__(self):
        self._q = deque()
        self._seen = set()

    def push(self, obj):
        if obj in self._seen:
            return
        self._seen.add(obj)
        self._q.append(obj)

    def pop(self):
        return self._q.popleft()

    def __len__(self):
        return len(self._q)