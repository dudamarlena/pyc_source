# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/threads/producer_consumer.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 819 bytes
import contextlib, queue

class Queues(object):

    def __init__(self, item, *items):
        self.empty = queue.Queue()
        self.full = queue.Queue()
        self.empty.put(item)
        for i in items:
            self.empty.put(i)

    @contextlib.contextmanager
    def produce(self):
        i = self.empty.get()
        yield i
        self.full.put(i)

    @contextlib.contextmanager
    def consume(self):
        i = self.full.get()
        yield i
        self.empty.put(i)