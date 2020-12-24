# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/synch.py
# Compiled at: 2019-02-14 00:35:17
"""
Synchronization primitives:

    - reader-writer lock (preference to writers)

(Contributed to Django by eugene@lazutkin.com)
"""
import contextlib, threading

class RWLock(object):
    """
    Classic implementation of reader-writer lock with preference to writers.

    Readers can access a resource simultaneously.
    Writers get an exclusive access.

    API is self-descriptive:
        reader_enters()
        reader_leaves()
        writer_enters()
        writer_leaves()
    """

    def __init__(self):
        self.mutex = threading.RLock()
        self.can_read = threading.Semaphore(0)
        self.can_write = threading.Semaphore(0)
        self.active_readers = 0
        self.active_writers = 0
        self.waiting_readers = 0
        self.waiting_writers = 0

    def reader_enters(self):
        with self.mutex:
            if self.active_writers == 0 and self.waiting_writers == 0:
                self.active_readers += 1
                self.can_read.release()
            else:
                self.waiting_readers += 1
        self.can_read.acquire()

    def reader_leaves(self):
        with self.mutex:
            self.active_readers -= 1
            if self.active_readers == 0 and self.waiting_writers != 0:
                self.active_writers += 1
                self.waiting_writers -= 1
                self.can_write.release()

    @contextlib.contextmanager
    def reader(self):
        self.reader_enters()
        try:
            yield
        finally:
            self.reader_leaves()

    def writer_enters(self):
        with self.mutex:
            if self.active_writers == 0 and self.waiting_writers == 0 and self.active_readers == 0:
                self.active_writers += 1
                self.can_write.release()
            else:
                self.waiting_writers += 1
        self.can_write.acquire()

    def writer_leaves(self):
        with self.mutex:
            self.active_writers -= 1
            if self.waiting_writers != 0:
                self.active_writers += 1
                self.waiting_writers -= 1
                self.can_write.release()
            elif self.waiting_readers != 0:
                t = self.waiting_readers
                self.waiting_readers = 0
                self.active_readers += t
                while t > 0:
                    self.can_read.release()
                    t -= 1

    @contextlib.contextmanager
    def writer(self):
        self.writer_enters()
        try:
            yield
        finally:
            self.writer_leaves()