# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/canoe/data.py
# Compiled at: 2013-03-20 10:50:18


class Buffer(object):

    class EmptyValue:
        pass

    def __init__(self, n):
        self.n = n + 1
        self.start = 0
        self.end = 0
        self.els = [ None for n in range(n + 1) ]
        return

    def full(self):
        return (self.end + 1) % self.n == self.start

    def empty(self):
        return self.end == self.start

    def push(self, val):
        self.els[self.end] = val
        self.end = (self.end + 1) % self.n
        if self.end == self.start:
            self.start = (self.start + 1) % self.n

    def alter(self, fn):
        tmp = fn(self.els[self.start])
        if not self.empty():
            self.els[self.start] = tmp
        else:
            self.push(tmp)
        return tmp

    def pop(self):
        if self.empty():
            raise ValueError('queue is empty')
        elem = self.els[self.start]
        self.els[self.start] = None
        self.start = (self.start + 1) % self.n
        return elem

    def copyn(self, n):
        """Copies last n items out of the buffer"""
        out = []
        if n >= self.n:
            n = self.n
        i = 0
        e = (self.end - 1) % self.n
        while e != self.start and i < n:
            out.append(self.els[e])
            e = (e - 1) % self.n
            i += 1

        out.reverse()
        return out