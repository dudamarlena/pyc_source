# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/mt/mrow.py
# Compiled at: 2007-03-21 14:34:39
"""Multiple-reader-one-writer resource locking.

For copyright, license, and warranty, see bottom of file.
"""
__svn__ = '$Id: mrow.py 1877 2006-03-19 14:37:54Z pobrien $'
__rev__ = '$Rev: 1877 $'[6:-2]
from thread import get_ident
import threading

def acquire_locked(fn):

    def _acquire_locked_wrapper(self, *args, **kw):
        L = self.acquire_lock
        try:
            L.acquire()
            result = fn(self, *args, **kw)
        finally:
            L.release()
        return result

    return _acquire_locked_wrapper


def release_locked(fn):

    def _release_locked_wrapper(self, *args, **kw):
        L = self.release_lock
        try:
            L.acquire()
            result = fn(self, *args, **kw)
        finally:
            L.release()
        return result

    return _release_locked_wrapper


class RWLock(object):
    """MROW resource lock."""
    __module__ = __name__

    def __init__(self):
        self.acquire_lock = threading.Lock()
        self.release_lock = threading.Lock()
        self.sublocks = []
        self.waiting = []
        self.readers = 0
        self.writing = False
        self.thread_readers = {}
        self.thread_writers = {}

    @acquire_locked
    def reader(self):
        """Return an acquired read lock."""
        thread_readers, thread_writers = self.thread_readers, self.thread_writers
        ident = get_ident()
        if ident in thread_readers:
            (sublock, count) = thread_readers[ident]
            thread_readers[ident] = (sublock, count + 1)
            return sublock
        elif ident in thread_writers:
            (sublock, count) = thread_writers[ident]
            thread_writers[ident] = (sublock, count + 1)
            return sublock
        sublock = RLock(self)
        if self.writing:
            self.waiting.append(sublock)
            sublock.acquire()
        sublock.acquire()
        self.readers += 1
        self.sublocks.append(sublock)
        thread_readers[ident] = (sublock, 1)
        return sublock

    @acquire_locked
    def writer(self):
        """Return an acquired write lock."""
        thread_readers, thread_writers = self.thread_readers, self.thread_writers
        ident = get_ident()
        wasReader = None
        if ident in thread_writers:
            (sublock, count) = thread_writers[ident]
            thread_writers[ident] = (sublock, count + 1)
            return sublock
        elif ident in thread_readers:
            (sublock, count) = thread_readers[ident]
            del thread_readers[ident]
            self.readers -= 1
            self.sublocks.remove(sublock)
            sublock._release()
            wasReader = sublock
        sublock = WLock(self)
        if self.readers or self.writing:
            self.waiting.append(sublock)
            sublock.acquire()
        sublock.acquire()
        self.writing = True
        self.sublocks.append(sublock)
        if wasReader is None:
            count = 0
        else:
            wasReader.becameWriter = sublock
        thread_writers[ident] = (
         sublock, count + 1)
        return sublock

    @release_locked
    def _release_r(self, sublock):
        sublocks = self.sublocks
        if sublock in sublocks:
            thread_readers = self.thread_readers
            ident = get_ident()
            count = thread_readers[ident][1] - 1
            if count:
                thread_readers[ident] = (
                 sublock, count)
            else:
                del thread_readers[ident]
                self.readers -= 1
                sublocks.remove(sublock)
                sublock._release()
                waiting = self.waiting
                if waiting and not self.readers:
                    waiting.pop(0)._release()

    @release_locked
    def _release_w(self, sublock):
        sublocks = self.sublocks
        if sublock in sublocks:
            thread_writers = self.thread_writers
            ident = get_ident()
            count = thread_writers[ident][1] - 1
            if count:
                thread_writers[ident] = (
                 sublock, count)
            else:
                del thread_writers[ident]
                self.writing = False
                sublocks.remove(sublock)
                sublock._release()
                waiting = self.waiting
                while waiting and isinstance(waiting[0], RLock):
                    waiting.pop(0)._release()


class SubLock(object):
    __module__ = __name__

    def __init__(self, rwlock):
        self.lock = threading.Lock()
        self.rwlock = rwlock

    def _release(self):
        self.lock.release()

    def acquire(self):
        self.lock.acquire()


class RLock(SubLock):
    __module__ = __name__

    def __init__(self, rwlock):
        SubLock.__init__(self, rwlock)
        self.becameWriter = None
        return

    def release(self):
        if self.becameWriter is not None:
            self.becameWriter.release()
        else:
            self.rwlock._release_r(self)
        return


class WLock(SubLock):
    __module__ = __name__

    def release(self):
        self.rwlock._release_w(self)