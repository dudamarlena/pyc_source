# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgalan/projects/redongo/redongo/queue_utils.py
# Compiled at: 2016-08-11 11:38:11
from queuelib.queue import FifoDiskQueue

class Queue(object):

    class PushInClosedQueue(Exception):
        pass

    class PopInClosedQueue(Exception):
        pass

    def __init__(self, queue_name, size=0):
        self._size_queue = size
        self._disk_queue_name = queue_name
        self._disk_queue = FifoDiskQueue(queue_name)
        self._is_open = True
        if self._disk_queue.__len__() > 0:
            self._length = self._disk_queue.__len__()
            self._empty_disk = False
            self._is_open_dq = True
        else:
            self._length = 0
            self._empty_disk = True
            self._disk_queue.close()
            self._is_open_dq = False

    def push(self, obj):
        if not self._is_open:
            raise self.PushInClosedQueue()
        else:
            if not self._is_open_dq:
                self._disk_queue = FifoDiskQueue(self._disk_queue_name)
                self._is_open_dq = True
            self._disk_queue.push(obj)
            self._empty_disk = False
            self._length += 1

    def pop(self):
        if not self._is_open:
            raise self.PopInClosedQueue()
        elif self._is_open and self._length > 0:
            self._length -= 1
            obj = self._disk_queue.pop()
            if self._disk_queue.__len__() == 0:
                self._disk_queue.close()
                self._is_open_dq = False
                self._empty_disk = True
            return obj

    def close(self):
        if self._is_open_dq:
            self._disk_queue.close()
        self._is_open = False