# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\multiprocessing\synchronize.py
# Compiled at: 2009-07-30 09:32:54
__all__ = [
 'Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Condition', 'Event']
import threading, os, sys
from time import time as _time, sleep as _sleep
import _multiprocessing
from multiprocessing.process import current_process
from multiprocessing.util import Finalize, register_after_fork, debug
from multiprocessing.forking import assert_spawning, Popen
try:
    from _multiprocessing import SemLock
except ImportError:
    raise ImportError('This platform lacks a functioning sem_open' + ' implementation, therefore, the required' + ' synchronization primitives needed will not' + ' function, see issue 3770.')

(RECURSIVE_MUTEX, SEMAPHORE) = range(2)
SEM_VALUE_MAX = _multiprocessing.SemLock.SEM_VALUE_MAX

class SemLock(object):
    __module__ = __name__

    def __init__(self, kind, value, maxvalue):
        sl = self._semlock = _multiprocessing.SemLock(kind, value, maxvalue)
        debug('created semlock with handle %s' % sl.handle)
        self._make_methods()
        if sys.platform != 'win32':

            def _after_fork(obj):
                obj._semlock._after_fork()

            register_after_fork(self, _after_fork)

    def _make_methods(self):
        self.acquire = self._semlock.acquire
        self.release = self._semlock.release
        self.__enter__ = self._semlock.__enter__
        self.__exit__ = self._semlock.__exit__

    def __getstate__(self):
        assert_spawning(self)
        sl = self._semlock
        return (Popen.duplicate_for_child(sl.handle), sl.kind, sl.maxvalue)

    def __setstate__(self, state):
        self._semlock = _multiprocessing.SemLock._rebuild(*state)
        debug('recreated blocker with handle %r' % state[0])
        self._make_methods()


class Semaphore(SemLock):
    __module__ = __name__

    def __init__(self, value=1):
        SemLock.__init__(self, SEMAPHORE, value, SEM_VALUE_MAX)

    def get_value(self):
        return self._semlock._get_value()

    def __repr__(self):
        try:
            value = self._semlock._get_value()
        except Exception:
            value = 'unknown'

        return '<Semaphore(value=%s)>' % value


class BoundedSemaphore(Semaphore):
    __module__ = __name__

    def __init__(self, value=1):
        SemLock.__init__(self, SEMAPHORE, value, value)

    def __repr__(self):
        try:
            value = self._semlock._get_value()
        except Exception:
            value = 'unknown'

        return '<BoundedSemaphore(value=%s, maxvalue=%s)>' % (value, self._semlock.maxvalue)


class Lock(SemLock):
    __module__ = __name__

    def __init__(self):
        SemLock.__init__(self, SEMAPHORE, 1, 1)

    def __repr__(self):
        try:
            if self._semlock._is_mine():
                name = current_process().name
                if threading.current_thread().name != 'MainThread':
                    name += '|' + threading.current_thread().name
            elif self._semlock._get_value() == 1:
                name = 'None'
            elif self._semlock._count() > 0:
                name = 'SomeOtherThread'
            else:
                name = 'SomeOtherProcess'
        except Exception:
            name = 'unknown'

        return '<Lock(owner=%s)>' % name


class RLock(SemLock):
    __module__ = __name__

    def __init__(self):
        SemLock.__init__(self, RECURSIVE_MUTEX, 1, 1)

    def __repr__(self):
        try:
            if self._semlock._is_mine():
                name = current_process().name
                if threading.current_thread().name != 'MainThread':
                    name += '|' + threading.current_thread().name
                count = self._semlock._count()
            elif self._semlock._get_value() == 1:
                (name, count) = ('None', 0)
            elif self._semlock._count() > 0:
                (name, count) = ('SomeOtherThread', 'nonzero')
            else:
                (name, count) = ('SomeOtherProcess', 'nonzero')
        except Exception:
            (name, count) = ('unknown', 'unknown')

        return '<RLock(%s, %s)>' % (name, count)


class Condition(object):
    __module__ = __name__

    def __init__(self, lock=None):
        self._lock = lock or RLock()
        self._sleeping_count = Semaphore(0)
        self._woken_count = Semaphore(0)
        self._wait_semaphore = Semaphore(0)
        self._make_methods()

    def __getstate__(self):
        assert_spawning(self)
        return (self._lock, self._sleeping_count, self._woken_count, self._wait_semaphore)

    def __setstate__(self, state):
        (self._lock, self._sleeping_count, self._woken_count, self._wait_semaphore) = state
        self._make_methods()

    def _make_methods(self):
        self.acquire = self._lock.acquire
        self.release = self._lock.release
        self.__enter__ = self._lock.__enter__
        self.__exit__ = self._lock.__exit__

    def __repr__(self):
        try:
            num_waiters = self._sleeping_count._semlock._get_value() - self._woken_count._semlock._get_value()
        except Exception:
            num_waiters = 'unkown'

        return '<Condition(%s, %s)>' % (self._lock, num_waiters)

    def wait(self, timeout=None):
        assert self._lock._semlock._is_mine(), 'must acquire() condition before using wait()'
        self._sleeping_count.release()
        count = self._lock._semlock._count()
        for i in xrange(count):
            self._lock.release()

        try:
            self._wait_semaphore.acquire(True, timeout)
        finally:
            self._woken_count.release()
            for i in xrange(count):
                self._lock.acquire()

    def notify(self):
        assert self._lock._semlock._is_mine(), 'lock is not owned'
        assert not self._wait_semaphore.acquire(False)
        while self._woken_count.acquire(False):
            res = self._sleeping_count.acquire(False)
            assert res

        if self._sleeping_count.acquire(False):
            self._wait_semaphore.release()
            self._woken_count.acquire()
            self._wait_semaphore.acquire(False)

    def notify_all(self):
        assert self._lock._semlock._is_mine(), 'lock is not owned'
        assert not self._wait_semaphore.acquire(False)
        while self._woken_count.acquire(False):
            res = self._sleeping_count.acquire(False)
            assert res

        sleepers = 0
        while self._sleeping_count.acquire(False):
            self._wait_semaphore.release()
            sleepers += 1

        if sleepers:
            for i in xrange(sleepers):
                self._woken_count.acquire()

            while self._wait_semaphore.acquire(False):
                pass


class Event(object):
    __module__ = __name__

    def __init__(self):
        self._cond = Condition(Lock())
        self._flag = Semaphore(0)

    def is_set(self):
        self._cond.acquire()
        try:
            if self._flag.acquire(False):
                self._flag.release()
                return True
            return False
        finally:
            self._cond.release()

    def set(self):
        self._cond.acquire()
        try:
            self._flag.acquire(False)
            self._flag.release()
            self._cond.notify_all()
        finally:
            self._cond.release()

    def clear(self):
        self._cond.acquire()
        try:
            self._flag.acquire(False)
        finally:
            self._cond.release()

    def wait(self, timeout=None):
        self._cond.acquire()
        try:
            if self._flag.acquire(False):
                self._flag.release()
            else:
                self._cond.wait(timeout)
        finally:
            self._cond.release()