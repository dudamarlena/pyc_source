# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/custom_queue.py
# Compiled at: 2019-08-07 08:55:31
# Size of source mod 2**32: 2224 bytes
import threading, multiprocessing, time
from .utils import get_timestamp

class CustomQueue:
    BLOCKING_SECONDS = 0.1

    def __init__(self, size=0, circular=False):
        self._size = size
        self._circular = circular

    def put(self):
        pass

    def get(self):
        pass

    class EmptyError(Exception):

        def __init__(self, message=None):
            if message is None:
                message = 'The queue is empty'
            super().__init__(message)


class ThreadingQueue(CustomQueue):

    def __init__(self, size=0, circular=False):
        super().__init__(size, circular)
        self._queue = list()
        self._lock = threading.Lock()

    def _truncate(self):
        if self._size > 0:
            if len(self._queue) > self._size:
                self._queue.pop(0)

    def put(self, item, block=True, timeout=None):
        if self._circular:
            self._lock.acquire()
            self._queue.append(item)
            self._truncate()
            self._lock.release()
            return
        start_timestamp = get_timestamp()
        while timeout is None or get_timestamp() - start_timestamp < timeout:
            self._lock.acquire()
            if not self._size <= 0:
                if len(self._queue) < self._size:
                    self._queue.append(item)
                    self._lock.release()
                    return
            self._lock.release()
            if not block:
                raise ThreadingQueue.EmptyError
            time.sleep(ThreadingQueue.BLOCKING_SECONDS)

    def get(self, block=True, timeout=None):
        if timeout is not None:
            block = False
        start_timestamp = get_timestamp()
        while timeout is None or get_timestamp() - start_timestamp < timeout:
            self._lock.acquire()
            if len(self._queue) > 0:
                item = self._queue.pop(0)
                self._lock.release()
                return item
            self._lock.release()
            if timeout is None:
                if not block:
                    raise ThreadingQueue.EmptyError
            time.sleep(ThreadingQueue.BLOCKING_SECONDS)

        if not block:
            raise ThreadingQueue.EmptyError