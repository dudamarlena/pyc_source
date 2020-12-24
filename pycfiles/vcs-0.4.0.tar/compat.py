# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/.pythonpath/vcs/utils/compat.py
# Compiled at: 2013-04-27 15:11:11
"""
Various utilities to work with Python < 2.7.

Those utilities may be deleted once ``vcs`` stops support for older Python
versions.
"""
import sys, array
if sys.version_info >= (2, 7):
    unittest = __import__('unittest')
else:
    unittest = __import__('unittest2')
if sys.version_info >= (2, 6):
    _bytes = bytes
else:
    _bytes = str
if sys.version_info >= (2, 6):
    _bytearray = bytearray
else:
    _bytearray = array
if sys.version_info >= (2, 6):
    from collections import deque
else:

    class deque(object):

        def __init__(self, iterable=(), maxlen=-1):
            if not hasattr(self, 'data'):
                self.left = self.right = 0
                self.data = {}
            self.maxlen = maxlen or -1
            self.extend(iterable)

        def append(self, x):
            self.data[self.right] = x
            self.right += 1
            if self.maxlen != -1 and len(self) > self.maxlen:
                self.popleft()

        def appendleft(self, x):
            self.left -= 1
            self.data[self.left] = x
            if self.maxlen != -1 and len(self) > self.maxlen:
                self.pop()

        def pop(self):
            if self.left == self.right:
                raise IndexError('cannot pop from empty deque')
            self.right -= 1
            elem = self.data[self.right]
            del self.data[self.right]
            return elem

        def popleft(self):
            if self.left == self.right:
                raise IndexError('cannot pop from empty deque')
            elem = self.data[self.left]
            del self.data[self.left]
            self.left += 1
            return elem

        def clear(self):
            self.data.clear()
            self.left = self.right = 0

        def extend(self, iterable):
            for elem in iterable:
                self.append(elem)

        def extendleft(self, iterable):
            for elem in iterable:
                self.appendleft(elem)

        def rotate(self, n=1):
            if self:
                n %= len(self)
                for i in xrange(n):
                    self.appendleft(self.pop())

        def __getitem__(self, i):
            if i < 0:
                i += len(self)
            try:
                return self.data[(i + self.left)]
            except KeyError:
                raise IndexError

        def __setitem__(self, i, value):
            if i < 0:
                i += len(self)
            try:
                self.data[i + self.left] = value
            except KeyError:
                raise IndexError

        def __delitem__(self, i):
            size = len(self)
            if not -size <= i < size:
                raise IndexError
            data = self.data
            if i < 0:
                i += size
            for j in xrange(self.left + i, self.right - 1):
                data[j] = data[(j + 1)]

            self.pop()

        def __len__(self):
            return self.right - self.left

        def __cmp__(self, other):
            if type(self) != type(other):
                return cmp(type(self), type(other))
            return cmp(list(self), list(other))

        def __repr__(self, _track=[]):
            if id(self) in _track:
                return '...'
            _track.append(id(self))
            r = 'deque(%r, maxlen=%s)' % (list(self), self.maxlen)
            _track.remove(id(self))
            return r

        def __getstate__(self):
            return (
             tuple(self),)

        def __setstate__(self, s):
            self.__init__(s[0])

        def __hash__(self):
            raise TypeError

        def __copy__(self):
            return self.__class__(self)

        def __deepcopy__(self, memo={}):
            from copy import deepcopy
            result = self.__class__()
            memo[id(self)] = result
            result.__init__(deepcopy(tuple(self), memo))
            return result


if sys.version_info >= (2, 6):
    from threading import Event, Thread
else:
    from threading import _Verbose, Lock, Thread, _time, _allocate_lock, RLock, _sleep

    def Condition(*args, **kwargs):
        return _Condition(*args, **kwargs)


    class _Condition(_Verbose):

        def __init__(self, lock=None, verbose=None):
            _Verbose.__init__(self, verbose)
            if lock is None:
                lock = RLock()
            self.__lock = lock
            self.acquire = lock.acquire
            self.release = lock.release
            try:
                self._release_save = lock._release_save
            except AttributeError:
                pass

            try:
                self._acquire_restore = lock._acquire_restore
            except AttributeError:
                pass

            try:
                self._is_owned = lock._is_owned
            except AttributeError:
                pass

            self.__waiters = []
            return

        def __enter__(self):
            return self.__lock.__enter__()

        def __exit__(self, *args):
            return self.__lock.__exit__(*args)

        def __repr__(self):
            return '<Condition(%s, %d)>' % (self.__lock, len(self.__waiters))

        def _release_save(self):
            self.__lock.release()

        def _acquire_restore(self, x):
            self.__lock.acquire()

        def _is_owned(self):
            if self.__lock.acquire(0):
                self.__lock.release()
                return False
            else:
                return True

        def wait(self, timeout=None):
            if not self._is_owned():
                raise RuntimeError('cannot wait on un-acquired lock')
            waiter = _allocate_lock()
            waiter.acquire()
            self.__waiters.append(waiter)
            saved_state = self._release_save()
            try:
                if timeout is None:
                    waiter.acquire()
                    self._note('%s.wait(): got it', self)
                else:
                    endtime = _time() + timeout
                    delay = 0.0005
                    while True:
                        gotit = waiter.acquire(0)
                        if gotit:
                            break
                        remaining = endtime - _time()
                        if remaining <= 0:
                            break
                        delay = min(delay * 2, remaining, 0.05)
                        _sleep(delay)

                    if not gotit:
                        self._note('%s.wait(%s): timed out', self, timeout)
                        try:
                            self.__waiters.remove(waiter)
                        except ValueError:
                            pass

                    else:
                        self._note('%s.wait(%s): got it', self, timeout)
            finally:
                self._acquire_restore(saved_state)

            return

        def notify(self, n=1):
            if not self._is_owned():
                raise RuntimeError('cannot notify on un-acquired lock')
            __waiters = self.__waiters
            waiters = __waiters[:n]
            if not waiters:
                self._note('%s.notify(): no waiters', self)
                return
            self._note('%s.notify(): notifying %d waiter%s', self, n, n != 1 and 's' or '')
            for waiter in waiters:
                waiter.release()
                try:
                    __waiters.remove(waiter)
                except ValueError:
                    pass

        def notifyAll(self):
            self.notify(len(self.__waiters))

        notify_all = notifyAll


    def Event(*args, **kwargs):
        return _Event(*args, **kwargs)


    class _Event(_Verbose):

        def __init__(self, verbose=None):
            _Verbose.__init__(self, verbose)
            self.__cond = Condition(Lock())
            self.__flag = False

        def isSet(self):
            return self.__flag

        is_set = isSet

        def set(self):
            self.__cond.acquire()
            try:
                self.__flag = True
                self.__cond.notify_all()
            finally:
                self.__cond.release()

        def clear(self):
            self.__cond.acquire()
            try:
                self.__flag = False
            finally:
                self.__cond.release()

        def wait(self, timeout=None):
            self.__cond.acquire()
            try:
                if not self.__flag:
                    self.__cond.wait(timeout)
            finally:
                self.__cond.release()