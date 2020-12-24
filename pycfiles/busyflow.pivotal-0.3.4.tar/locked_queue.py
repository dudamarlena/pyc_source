# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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