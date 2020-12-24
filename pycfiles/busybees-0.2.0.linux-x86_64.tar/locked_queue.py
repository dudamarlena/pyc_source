# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/busybees/locked_queue.py
# Compiled at: 2015-07-22 09:29:41
import threading

class LockedQueue(object):

    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()

    def access(self):
        self.lock.acquire()
        return self.queue

    def enum(self):
        return self.queue

    def append(self, obj):
        if type(obj) == list:
            self.queue.extend(obj)
        else:
            self.queue.append(obj)

    def clear(self):
        self.queue = []