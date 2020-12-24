# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/automata/util.py
# Compiled at: 2012-12-20 01:24:56
from collections import deque
from sys import stderr

class OneTimeQueue(deque):

    def __init__(self):
        self._seen = set()
        return super(OneTimeQueue, self).__init__()

    def append(self, val):
        if val in self._seen:
            return None
        else:
            self._seen.add(val)
            return super(OneTimeQueue, self).append(val)

    def appendleft(self, val):
        if val in self._seen:
            if val in self:
                self.remove(val)
                return super(OneTimeQueue, self).appendleft(val)
            else:
                return

        else:
            self._seen.add(val)
            return super(OneTimeQueue, self).appendleft(val)
        return

    def seen(self):
        return self._seen


class Associations(object):

    def __init__(self):
        self.forward = {}
        self.backward = {}
        self.last_id = 1

    def associate(self, obj, assval=None):
        if obj in self.forward:
            return self.forward[obj]
        else:
            if assval != None:
                self.forward[obj] = assval
                return assval
            self.forward[obj] = self.last_id
            self.backward[self.last_id] = obj
            self.last_id += 1
            return self.last_id - 1

    def retrieve(self, i):
        return self.backward[i]

    def __contains__(self, obj):
        return obj in self.forward

    def __len__(self):
        return len(self.forward)


def warn(msg):
    print >> stderr, msg