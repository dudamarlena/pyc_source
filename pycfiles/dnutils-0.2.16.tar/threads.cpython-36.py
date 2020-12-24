# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/code/dnutils/python3.5/dnutils/threads.py
# Compiled at: 2019-05-09 07:17:25
# Size of source mod 2**32: 65308 bytes
import random, sys
from dnutils import out, ifnone, signals
import sys as _sys, _thread
from time import monotonic as _time
from traceback import format_exc as _format_exc
from _weakrefset import WeakSet
from itertools import islice as _islice, count as _count
try:
    from _collections import deque as _deque, defaultdict
except ImportError:
    from collections import deque as _deque

__all__ = [
 'active_count', 'Condition', 'current_thread', 'enumerate', 'Event',
 'Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Thread', 'Barrier',
 'Timer', 'ThreadError', 'ThreadInterrupt', 'setprofile', 'settrace', 'local', 'stack_size']
_start_new_thread = _thread.start_new_thread
_allocate_lock = _thread.allocate_lock
_set_sentinel = _thread._set_sentinel
get_ident = _thread.get_ident
ThreadError = _thread.error
TIMEOUT_MAX = _thread.TIMEOUT_MAX
del _thread
_profile_hook = None
_trace_hook = None

def setprofile(func):
    """Set a profile function for all threads started from the threading module.

    The func will be passed to sys.setprofile() for each thread, before its
    run() method is called.

    """
    global _profile_hook
    _profile_hook = func


def settrace(func):
    """Set a trace function for all threads started from the threading module.

    The func will be passed to sys.settrace() for each thread, before its run()
    method is called.

    """
    global _trace_hook
    _trace_hook = func


def sleep(seconds):
    """
    Block the calling thread for the given number of seconds.

    :param seconds:
    :return:
    """
    l = Lock()
    l.acquire()
    l.acquire(timeout=seconds)


def waitabout(sec):
    """
    Sleeps for approximately the given number of seconds.

    :return:    the number of seconds the function was blocking
    """
    t = sec + (random.random() - 0.5) * sec * 0.5
    sleep(t)
    return t


def iteractive():
    """Returns a generator of tuples of thread ids and respective thread objects
    of threads that are currently active."""
    for tid, tobj in _active.items():
        yield (
         tid, tobj)


def active():
    """Returns a dict of active local threads, which maps the thread ID to
    the respective thread object."""
    return dict(list(iteractive()))


class ThreadInterrupt(Exception):
    pass


CLock = _allocate_lock

class Lock:
    __doc__ = 'An implementation of a lock which is interruptable.'

    def __init__(self):
        self._Lock__lock = _allocate_lock()
        self._Lock__blocking = None
        self._Lock__waiters = {}
        self._Lock__owner = None
        self._Lock__nextowner = None
        self._Lock__interrupt = set()

    def locked(self):
        return self._Lock__owner is not None

    def acquire(self, blocking=True, timeout=None):
        """
        Acquire the lock.

        If the lock is acquired by some other thread and ``blocking`` is ``True``, this method blocks until it
        is released. If block is ``False``, :func:`Lock.acquire` immediately returns whether or not it has
        successfully acquired the lock (boolean). If ``blocking`` is ``True`` and a timeout is specified, the method
        blocks until the timeout has expired. The return value then specifies whether the lock was acquired
        successfully or not. When mutliple threads wait for for a release of the lock, an arbitrary thread may
        obtain it finally. This behavior is equivalent to the behavior of the original :class:`threading.Lock`
        implementation.

        :param blocking:    Whether or not this method should block until the lock could be acquired.
        :param timeout:     A positive value causes this method to return after the given time (in seconds)
                            no matter whether the lock was acquired or not.
        :return:
        """
        t = current_thread()
        tid = get_ident()
        self._Lock__lock.acquire()
        try:
            while 1:
                if tid in self._Lock__interrupt:
                    self._Lock__interrupt.remove(tid)
                    raise ThreadInterrupt()
                if not self.locked():
                    if self._Lock__nextowner is None or self._Lock__nextowner == tid:
                        self._Lock__owner = tid
                        self._Lock__nextowner = None
                        return True
                    else:
                        if not blocking:
                            return False
                        waiter = _allocate_lock()
                        waiter.acquire()
                        self._Lock__waiters[tid] = waiter
                        t._blocked_by = self
                        self._Lock__lock.release()
                        gotit = waiter.acquire(True, ifnone(timeout, -1))
                        while True:
                            self._Lock__lock.acquire()
                            if self._Lock__blocking is None or self._Lock__blocking == tid:
                                break
                            self._Lock__lock.release()

                        self._Lock__blocking = None
                        del self._Lock__waiters[tid]
                        t._blocked_by = None
                        if not gotit and timeout is not None:
                            return False

        finally:
            try:
                self._Lock__lock.release()
            except RuntimeError:
                pass

    def interrupt(self, tid):
        """
        Interrupts the thread with the given thread id if it is waiting for
        the acquisition of the lock.

        In case a thread is unresponsive for it blocks in :func:`Lock.acquire`, it may
        be interrupted by this method. A call to this method causes an :class:`ThreadInterrupt`
        error being raised in the respective thread.

        :param tid:     the ID of the thread to be interrupted.
        :return:
        """
        try:
            self._Lock__safe_acquire()
            if tid not in self._Lock__waiters:
                return
            self._Lock__interrupt.add(tid)
            self._Lock__blocking = tid
            self._Lock__waiters[tid].release()
        finally:
            self._Lock__safe_release()

    def release(self):
        """
        Releases the lock.

        This method may or may not be called from the thread holding the lock.

        If ``release()`` is called on an unacquired lock, a runtime error is raised.

        :return:   no return value
        """
        self._Lock__safe_acquire()
        self._Lock__release()
        self._Lock__safe_release()

    def __safe_acquire(self):
        while True:
            self._Lock__lock.acquire()
            if self._Lock__blocking is None:
                return
            self._Lock__lock.release()

    def __safe_release(self):
        self._Lock__lock.release()

    def __release(self):
        """
        non-threadsafe variant of the release method.
        :return:
        """
        t = current_thread()
        if not self.locked():
            raise RuntimeError('cannot release an unacquired lock.')
        self._Lock__owner = None
        waiters = set(self._Lock__waiters.keys())
        if waiters:
            self._Lock__nextowner = waiters.pop()
            self._Lock__blocking = self._Lock__nextowner
            self._Lock__waiters[self._Lock__nextowner].release()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, e, t, tb):
        try:
            self._Lock__safe_acquire()
            if self.locked():
                self._Lock__release()
        finally:
            self._Lock__safe_release()

    def __repr__(self):
        return '<%s.%s %s at 0x%s>' % (self.__class__.__module__,
         self.__class__.__qualname__,
         'locked by thread %s' % self._Lock__owner if self.locked() else 'unlocked',
         hex(id(self)))


class RLock:
    __doc__ = 'This class implements reentrant lock objects.\n\n    A reentrant lock must be released by the thread that acquired it. Once a\n    thread has acquired a reentrant lock, the same thread may acquire it\n    again without blocking; the thread must release it once for each time it\n    has acquired it.\n\n    '

    def __init__(self):
        self._block = Lock()
        self._owner = None
        self._count = 0

    def __repr__(self):
        owner = self._owner
        try:
            owner = _active[owner].name
        except KeyError:
            pass

        return '<%s %s.%s object owner=%r count=%d at %s>' % (
         'locked' if self._block.locked() else 'unlocked',
         self.__class__.__module__,
         self.__class__.__qualname__,
         owner,
         self._count,
         hex(id(self)))

    def acquire(self, blocking=True, timeout=-1):
        """Acquire a lock, blocking or non-blocking.

        When invoked without arguments: if this thread already owns the lock,
        increment the recursion level by one, and return immediately. Otherwise,
        if another thread owns the lock, block until the lock is unlocked. Once
        the lock is unlocked (not owned by any thread), then grab ownership, set
        the recursion level to one, and return. If more than one thread is
        blocked waiting until the lock is unlocked, only one at a time will be
        able to grab ownership of the lock. There is no return value in this
        case.

        When invoked with the blocking argument set to true, do the same thing
        as when called without arguments, and return true.

        When invoked with the blocking argument set to false, do not block. If a
        call without an argument would block, return false immediately;
        otherwise, do the same thing as when called without arguments, and
        return true.

        When invoked with the floating-point timeout argument set to a positive
        value, block for at most the number of seconds specified by timeout
        and as long as the lock cannot be acquired.  Return true if the lock has
        been acquired, false if the timeout has elapsed.

        """
        me = get_ident()
        if self._owner == me:
            self._count += 1
            return 1
        else:
            rc = self._block.acquire(blocking, timeout)
            if rc:
                self._owner = me
                self._count = 1
            return rc

    __enter__ = acquire

    def release(self):
        """Release a lock, decrementing the recursion level.

        If after the decrement it is zero, reset the lock to unlocked (not owned
        by any thread), and if any other threads are blocked waiting for the
        lock to become unlocked, allow exactly one of them to proceed. If after
        the decrement the recursion level is still nonzero, the lock remains
        locked and owned by the calling thread.

        Only call this method when the calling thread owns the lock. A
        RuntimeError is raised if this method is called when the lock is
        unlocked.

        There is no return value.

        """
        if self._owner != get_ident():
            raise RuntimeError('cannot release un-acquired lock')
        self._count = count = self._count - 1
        if not count:
            self._owner = None
            self._block.release()

    def __exit__(self, t, v, tb):
        self.release()

    def _acquire_restore(self, state):
        self._block.acquire()
        self._count, self._owner = state

    def _release_save(self):
        if self._count == 0:
            raise RuntimeError('cannot release un-acquired lock')
        count = self._count
        self._count = 0
        owner = self._owner
        self._owner = None
        self._block.release()
        return (count, owner)

    def _is_owned(self):
        return self._owner == get_ident()

    def interrupt(self, tid):
        self._RLock__block.interrupt(tid)


class Condition:
    __doc__ = 'Class that implements a condition variable.\n\n    A condition variable allows one or more threads to wait until they are\n    notified by another thread.\n\n    If the lock argument is given and not None, it must be a Lock or RLock\n    object, and it is used as the underlying lock. Otherwise, a new RLock object\n    is created and used as the underlying lock.\n\n    '

    def __init__(self, lock=None):
        if lock is None:
            lock = RLock()
        self._lock = lock
        self.acquire = lock.acquire
        self.release = lock.release
        try:
            self._is_owned = lock._is_owned
        except AttributeError:
            pass

        self._waiters = _deque()

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return (self._lock.__exit__)(*args)

    def __repr__(self):
        return '<Condition(%s, %d)>' % (self._lock, len(self._waiters))

    def _release_save(self):
        self._lock.release()

    def _acquire_restore(self, x):
        self._lock.acquire()

    def _is_owned(self):
        if self._lock.acquire(0):
            self._lock.release()
            return False
        else:
            return True

    def wait(self, timeout=None):
        """Wait until notified or until a timeout occurs.

        If the calling thread has not acquired the lock when this method is
        called, a RuntimeError is raised.

        This method releases the underlying lock, and then blocks until it is
        awakened by a notify() or notify_all() call for the same condition
        variable in another thread, or until the optional timeout occurs. Once
        awakened or timed out, it re-acquires the lock and returns.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof).

        When the underlying lock is an RLock, it is not released using its
        release() method, since this may not actually unlock the lock when it
        was acquired multiple times recursively. Instead, an internal interface
        of the RLock class is used, which really unlocks it even when it has
        been recursively acquired several times. Another internal interface is
        then used to restore the recursion level when the lock is reacquired.

        """
        if not self._is_owned():
            raise RuntimeError('cannot wait on un-acquired lock')
        waiter = Lock()
        waiter.acquire()
        self._waiters.append(waiter)
        saved_state = self._release_save()
        gotit = False
        try:
            if timeout is None:
                waiter.acquire()
                gotit = True
            else:
                if timeout > 0:
                    gotit = waiter.acquire(True, timeout)
                else:
                    gotit = waiter.acquire(False)
            return gotit
        finally:
            self._acquire_restore(saved_state)
            if not gotit:
                try:
                    self._waiters.remove(waiter)
                except ValueError:
                    pass

    def wait_for(self, predicate, timeout=None):
        """Wait until a condition evaluates to True.

        predicate should be a callable which result will be interpreted as a
        boolean value.  A timeout may be provided giving the maximum time to
        wait.

        """
        endtime = None
        waittime = timeout
        result = predicate()
        while not result:
            if waittime is not None:
                if endtime is None:
                    endtime = _time() + waittime
                else:
                    waittime = endtime - _time()
                    if waittime <= 0:
                        break
            self.wait(waittime)
            result = predicate()

        return result

    def notify(self, n=1):
        """Wake up one or more threads waiting on this condition, if any.

        If the calling thread has not acquired the lock when this method is
        called, a RuntimeError is raised.

        This method wakes up at most n of the threads waiting for the condition
        variable; it is a no-op if no threads are waiting.

        """
        if not self._is_owned():
            raise RuntimeError('cannot notify on un-acquired lock')
        all_waiters = self._waiters
        waiters_to_notify = _deque(_islice(all_waiters, n))
        if not waiters_to_notify:
            return
        for waiter in waiters_to_notify:
            waiter.release()
            try:
                all_waiters.remove(waiter)
            except ValueError:
                pass

    def notify_thread(self, tid):
        """
        Wake up only the thread with the given thread id.
        :param tid:
        :return:
        """
        if not self._is_owned():
            raise RuntimeError('cannot notify on un-acquired lock')
        else:
            waiter = self._Condition__waiters.get(tid)
            if waiter is None:
                self._note('%s.notify(): no thread with id %s waiting on condition', self, tid)
                return
            self._note('%s.notify(): notifying waiter of thread %s', self, tid)
            t = active().get(tid)
            waiter.release()
            try:
                del self._Condition__waiters[tid]
            except KeyError:
                pass

    def notify_all(self):
        """Wake up all threads waiting on this condition.

        If the calling thread has not acquired the lock when this method
        is called, a RuntimeError is raised.

        """
        self.notify(len(self._waiters))

    notifyAll = notify_all


class Semaphore:
    __doc__ = 'This class implements semaphore objects.\n\n    Semaphores manage a counter representing the number of release() calls minus\n    the number of acquire() calls, plus an initial value. The acquire() method\n    blocks if necessary until it can return without making the counter\n    negative. If not given, value defaults to 1.\n\n    '

    def __init__(self, value=1):
        if value < 0:
            raise ValueError('semaphore initial value must be >= 0')
        self._cond = Condition(Lock())
        self._value = value

    def acquire(self, blocking=True, timeout=None):
        """Acquire a semaphore, decrementing the internal counter by one.

        When invoked without arguments: if the internal counter is larger than
        zero on entry, decrement it by one and return immediately. If it is zero
        on entry, block, waiting until some other thread has called release() to
        make it larger than zero. This is done with proper interlocking so that
        if multiple acquire() calls are blocked, release() will wake exactly one
        of them up. The implementation may pick one at random, so the order in
        which blocked threads are awakened should not be relied on. There is no
        return value in this case.

        When invoked with blocking set to true, do the same thing as when called
        without arguments, and return true.

        When invoked with blocking set to false, do not block. If a call without
        an argument would block, return false immediately; otherwise, do the
        same thing as when called without arguments, and return true.

        When invoked with a timeout other than None, it will block for at
        most timeout seconds.  If acquire does not complete successfully in
        that interval, return false.  Return true otherwise.

        """
        if not blocking:
            if timeout is not None:
                raise ValueError("can't specify timeout for non-blocking acquire")
        rc = False
        endtime = None
        with self._cond:
            while self._value == 0:
                if not blocking:
                    break
                if timeout is not None:
                    if endtime is None:
                        endtime = _time() + timeout
                    else:
                        timeout = endtime - _time()
                        if timeout <= 0:
                            break
                self._cond.wait(timeout)
            else:
                self._value -= 1
                rc = True

        return rc

    __enter__ = acquire

    def release(self):
        """Release a semaphore, incrementing the internal counter by one.

        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.

        """
        with self._cond:
            self._value += 1
            self._cond.notify()

    def __exit__(self, t, v, tb):
        self.release()


class BoundedSemaphore(Semaphore):
    __doc__ = "Implements a bounded semaphore.\n\n    A bounded semaphore checks to make sure its current value doesn't exceed its\n    initial value. If it does, ValueError is raised. In most situations\n    semaphores are used to guard resources with limited capacity.\n\n    If the semaphore is released too many times it's a sign of a bug. If not\n    given, value defaults to 1.\n\n    Like regular semaphores, bounded semaphores manage a counter representing\n    the number of release() calls minus the number of acquire() calls, plus an\n    initial value. The acquire() method blocks if necessary until it can return\n    without making the counter negative. If not given, value defaults to 1.\n\n    "

    def __init__(self, value=1):
        Semaphore.__init__(self, value)
        self._initial_value = value

    def release(self):
        """Release a semaphore, incrementing the internal counter by one.

        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.

        If the number of releases exceeds the number of acquires,
        raise a ValueError.

        """
        with self._cond:
            if self._value >= self._initial_value:
                raise ValueError('Semaphore released too many times')
            self._value += 1
            self._cond.notify()


class Event:
    __doc__ = 'Class implementing event objects.\n\n    Events manage a flag that can be set to true with the set() method and reset\n    to false with the clear() method. The wait() method blocks until the flag is\n    true.  The flag is initially false.\n\n    '

    def __init__(self):
        self._cond = Condition(Lock())
        self._flag = False

    def _reset_internal_locks(self):
        self._cond.__init__(Lock())

    def is_set(self):
        """Return true if and only if the internal flag is true."""
        return self._flag

    isSet = is_set

    def set(self):
        """Set the internal flag to true.

        All threads waiting for it to become true are awakened. Threads
        that call wait() once the flag is true will not block at all.

        """
        with self._cond:
            self._flag = True
            self._cond.notify_all()

    def clear(self):
        """Reset the internal flag to false.

        Subsequently, threads calling wait() will block until set() is called to
        set the internal flag to true again.

        """
        with self._cond:
            self._flag = False

    def wait(self, timeout=None):
        """Block until the internal flag is true.

        If the internal flag is true on entry, return immediately. Otherwise,
        block until another thread calls set() to set the flag to true, or until
        the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof).

        This method returns the internal flag on exit, so it will always return
        True except if a timeout is given and the operation times out.

        """
        with self._cond:
            signaled = self._flag
            if not signaled:
                signaled = self._cond.wait(timeout)
            return signaled


class Barrier:
    __doc__ = "Implements a Barrier.\n\n    Useful for synchronizing a fixed number of threads at known synchronization\n    points.  Threads block on 'wait()' and are simultaneously once they have all\n    made that call.\n\n    "

    def __init__(self, parties, action=None, timeout=None):
        """Create a barrier, initialised to 'parties' threads.

        'action' is a callable which, when supplied, will be called by one of
        the threads after they have all entered the barrier and just prior to
        releasing them all. If a 'timeout' is provided, it is uses as the
        default for all subsequent 'wait()' calls.

        """
        self._cond = Condition(Lock())
        self._action = action
        self._timeout = timeout
        self._parties = parties
        self._state = 0
        self._count = 0

    def wait(self, timeout=None):
        """Wait for the barrier.

        When the specified number of threads have started waiting, they are all
        simultaneously awoken. If an 'action' was provided for the barrier, one
        of the threads will have executed that callback prior to returning.
        Returns an individual index number from 0 to 'parties-1'.

        """
        if timeout is None:
            timeout = self._timeout
        with self._cond:
            self._enter()
            index = self._count
            self._count += 1
            try:
                if index + 1 == self._parties:
                    self._release()
                else:
                    self._wait(timeout)
                return index
            finally:
                self._count -= 1
                self._exit()

    def _enter(self):
        while self._state in (-1, 1):
            self._cond.wait()

        if self._state < 0:
            raise BrokenBarrierError
        elif not self._state == 0:
            raise AssertionError

    def _release(self):
        try:
            if self._action:
                self._action()
            self._state = 1
            self._cond.notify_all()
        except:
            self._break()
            raise

    def _wait(self, timeout):
        if not self._cond.wait_for(lambda : self._state != 0, timeout):
            self._break()
            raise BrokenBarrierError
        else:
            if self._state < 0:
                raise BrokenBarrierError
            assert self._state == 1

    def _exit(self):
        if self._count == 0:
            if self._state in (-1, 1):
                self._state = 0
                self._cond.notify_all()

    def reset(self):
        """Reset the barrier to the initial state.

        Any threads currently waiting will get the BrokenBarrier exception
        raised.

        """
        with self._cond:
            if self._count > 0:
                if self._state == 0:
                    self._state = -1
                elif self._state == -2:
                    self._state = -1
            else:
                self._state = 0
            self._cond.notify_all()

    def abort(self):
        """Place the barrier into a 'broken' state.

        Useful in case of error.  Any currently waiting threads and threads
        attempting to 'wait()' will have BrokenBarrierError raised.

        """
        with self._cond:
            self._break()

    def _break(self):
        self._state = -2
        self._cond.notify_all()

    @property
    def parties(self):
        """Return the number of threads required to trip the barrier."""
        return self._parties

    @property
    def n_waiting(self):
        """Return the number of threads currently waiting at the barrier."""
        if self._state == 0:
            return self._count
        else:
            return 0

    @property
    def broken(self):
        """Return True if the barrier is in a broken state."""
        return self._state == -2


class BrokenBarrierError(RuntimeError):
    pass


class Relay:
    __doc__ = '\n    A :class:`dnutils.threads.Relay` can be used in a thread to wait until a set of tasks\n    has been accomplished. The thread holding the relay, however, does not work any of the\n    tasks itself, but it just waits until all tasks have been done by other threads.\n    Only one thread can hold the relay at a time.\n\n    Technically, a relay is thread-safe counter that can be increased and decrased by any\n    thread and the owning thread blocks until the counter has reached 0. For any increase or\n    decrease operation, however, there must be at least one thread waiting on the relay.\n    '

    def __init__(self):
        self._waiter = Condition(RLock())
        self._lock = RLock()
        self._occupied = None
        self._relay = Lock()
        self._flag = False
        self._counter = 0
        self.__enter__ = self._waiter.__enter__
        self.__exit__ = self._waiter.__exit__

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, exc, exct, tb):
        self.unlock()

    def _checkowner(self):
        if self._occupied is None:
            raise RuntimeError('relay must be owned by a thread.')

    def acquire(self):
        with self._relay:
            self._occupied = get_ident()

    def release(self):
        with self._relay:
            if self._occupied != get_ident():
                raise RuntimeError('cannot release an unacquired relay.')
            self._occupied = None

    def reset(self):
        with self._lock:
            self._counter = 0

    def wait(self):
        with self._waiter:
            self._checkowner()
            if self._flag:
                return
            self._waiter.wait()

    def inc(self):
        """Increments the relay counter."""
        with self._lock:
            self._checkowner()
            self._counter += 1

    def dec(self):
        """Decrements the relay counter.

        Notifies the thread holding the relay and waiting for the completio tasks
        when the counter reaches 0.
        """
        with self._lock:
            self._checkowner()
            self._counter -= 1
            if self._counter == 0:
                self._flag = True
                with self._waiter:
                    self._waiter.notify_all()


_counter = _count().__next__
_counter()

def _newname(template='Thread-%d'):
    return template % _counter()


_active_limbo_lock = _allocate_lock()
_active = {}
_limbo = {}
_dangling = WeakSet()
START = 1
TERM = 2
SUSPEND = 3
RESUME = 4

class Thread:
    __doc__ = 'A class that represents a thread of control.\n\n    This class can be safely subclassed in a limited fashion. There are two ways\n    to specify the activity: by passing a callable object to the constructor, or\n    by overriding the run() method in a subclass.\n\n    '
    _initialized = False
    _exc_info = _sys.exc_info
    _signals = {
     START, TERM}

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is the argument tuple for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        if not group is None:
            raise AssertionError('group argument must be None for now')
        else:
            if kwargs is None:
                kwargs = {}
            self._target = target
            self._name = str(name or _newname())
            self._args = args
            self._kwargs = kwargs
            if daemon is not None:
                self._daemonic = daemon
            else:
                self._daemonic = current_thread().daemon
        self._ident = None
        self._tstate_lock = None
        self._started = Event()
        self._finished = Event()
        self._initialized = True
        self._blocked_by = None
        self._blocklock = Lock()
        self._handlerlock = Lock()
        self._stderr = _sys.stderr
        _dangling.add(self)
        self._handlers = defaultdict(list)
        self._interrupt = False

    def interrupt(self):
        """
        Sets a flag that this thread is supposed to interrupt.

        Once this method has been invoked, any call to ``dnutils.threads.interrupted()`` will raise
        a :class:`dnutils.thread.ThreadInterrupt` exception.
        """
        self._interrupt = True
        self._interrupt_if_blocking()

    def add_handler(self, signal, handler):
        """
        Add the signal handler to the thread's signal handlers
        :param signal:
        :param handler:
        :return:
        """
        assert signal in self._signals
        with self._handlerlock:
            if handler not in self._handlers[signal]:
                self._handlers[signal].append(handler)

    def rm_handler(self, signal, handler):
        """
        Remove the given signal handler from the thread's signal handlers.
        :param signal:
        :param handler:
        :return:
        """
        assert signal in self._signals
        with self._handlerlock:
            if handler in self._handlers[signal]:
                self._handlers[signal].remove(handler)

    def _interrupt_if_blocking(self):
        with self._blocklock:
            if self._blocked_by is not None:
                self._blocked_by.interrupt(self.ident)

    def _reset_internal_locks(self, is_alive):
        self._started._reset_internal_locks()
        if is_alive:
            self._set_tstate_lock()
        else:
            self._finished.clear()
            self._tstate_lock = None

    def __repr__(self):
        if not self._initialized:
            raise AssertionError('Thread.__init__() was not called')
        else:
            status = 'initial'
            if self._started.is_set():
                status = 'started'
            self.is_alive()
            if self._finished.is_set():
                status = 'finished'
            if self._daemonic:
                status += ' daemon'
            if self._ident is not None:
                status += ' %s' % self._ident
        return '<%s(%s, %s)>' % (self.__class__.__name__, self._name, status)

    def start(self):
        """Start the thread's activity.

        It must be called at most once per thread object. It arranges for the
        object's run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        """
        global _active_limbo_lock
        if not self._initialized:
            raise RuntimeError('thread.__init__() not called')
        else:
            if self._started.is_set():
                raise RuntimeError('threads can only be started once')
            with _active_limbo_lock:
                _limbo[self] = self
            try:
                _start_new_thread(self._bootstrap, ())
            except Exception:
                with _active_limbo_lock:
                    del _limbo[self]
                raise

        self._started.wait()
        return self

    def run(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            if self._target:
                (self._target)(*self._args, **self._kwargs)
        finally:
            del self._target
            del self._args
            del self._kwargs

    def _bootstrap(self):
        try:
            self._bootstrap_inner()
        except:
            if self._daemonic:
                if _sys is None:
                    return
            raise

    def _set_ident(self):
        self._ident = get_ident()

    def _set_tstate_lock(self):
        """
        Set a lock object which will be released by the interpreter when
        the underlying thread state (see pystate.h) gets deleted.
        """
        self._tstate_lock = _set_sentinel()
        self._tstate_lock.acquire()

    def _bootstrap_inner(self):
        try:
            self._set_ident()
            self._set_tstate_lock()
            self._started.set()
            with _active_limbo_lock:
                _active[self._ident] = self
                del _limbo[self]
            if _trace_hook:
                _sys.settrace(_trace_hook)
            if _profile_hook:
                _sys.setprofile(_profile_hook)
            for h in self._handlers[START]:
                h()

            try:
                try:
                    if hasattr(self, '_run'):
                        self._run()
                    else:
                        self.run()
                except SystemExit:
                    pass
                except:
                    if _sys:
                        if _sys.stderr is not None:
                            print(('Exception in thread %s:\n%s' % (self.name, _format_exc())), file=(_sys.stderr))
                    if self._stderr is not None:
                        exc_type, exc_value, exc_tb = self._exc_info()
                        try:
                            print(('Exception in thread %s (most likely raised during interpreter shutdown):' % self.name), file=(self._stderr))
                            print('Traceback (most recent call last):', file=(self._stderr))
                            while exc_tb:
                                print(('  File "%s", line %s, in %s' % (exc_tb.tb_frame.f_code.co_filename,
                                 exc_tb.tb_lineno,
                                 exc_tb.tb_frame.f_code.co_name)),
                                  file=(self._stderr))
                                exc_tb = exc_tb.tb_next

                            print(('%s: %s' % (exc_type, exc_value)), file=(self._stderr))
                        finally:
                            del exc_type
                            del exc_value
                            del exc_tb

            finally:
                pass

        finally:
            for h in self._handlers[TERM]:
                h()

            with _active_limbo_lock:
                try:
                    del _active[get_ident()]
                except:
                    pass

    def _stop(self):
        lock = self._tstate_lock
        if lock is not None:
            if not not lock.locked():
                raise AssertionError
        self._finished.set()
        self._tstate_lock = None

    def _delete(self):
        """Remove current thread from the dict of currently running threads."""
        try:
            with _active_limbo_lock:
                del _active[get_ident()]
        except KeyError:
            if 'dummy_threading' not in _sys.modules:
                raise

    def join(self, timeout=None):
        """Wait until the thread terminates.

        This blocks the calling thread until the thread whose join() method is
        called terminates -- either normally or through an unhandled exception
        or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof). As join() always returns None, you must call
        isAlive() after join() to decide whether a timeout happened -- if the
        thread is still alive, the join() call timed out.

        When the timeout argument is not present or None, the operation will
        block until the thread terminates.

        A thread can be join()ed many times.

        join() raises a RuntimeError if an attempt is made to join the current
        thread as that would cause a deadlock. It is also an error to join() a
        thread before it has been started and attempts to do so raises the same
        exception.

        """
        if not self._initialized:
            raise RuntimeError('Thread.__init__() not called')
        else:
            if not self._started.is_set():
                raise RuntimeError('cannot join thread before it is started')
            if self is current_thread():
                raise RuntimeError('cannot join current thread')
            if timeout is None:
                self._wait_for_tstate_lock()
            else:
                self._wait_for_tstate_lock(timeout=(max(timeout, 0)))

    def _wait_for_tstate_lock(self, block=True, timeout=-1):
        lock = self._tstate_lock
        if lock is None:
            assert self._finished.is_set()
        elif lock.acquire(block, timeout):
            lock.release()
            self._stop()

    @property
    def name(self):
        """A string used for identification purposes only.

        It has no semantics. Multiple threads may be given the same name. The
        initial name is set by the constructor.

        """
        assert self._initialized, 'Thread.__init__() not called'
        return self._name

    @name.setter
    def name(self, name):
        assert self._initialized, 'Thread.__init__() not called'
        self._name = str(name)

    @property
    def ident(self):
        """Thread identifier of this thread or None if it has not been started.

        This is a nonzero integer. See the thread.get_ident() function. Thread
        identifiers may be recycled when a thread exits and another thread is
        created. The identifier is available even after the thread has exited.

        """
        assert self._initialized, 'Thread.__init__() not called'
        return self._ident

    def is_alive(self):
        """Return whether the thread is alive.

        This method returns True just before the run() method starts until just
        after the run() method terminates. The module function enumerate()
        returns a list of all alive threads.

        """
        assert self._initialized, 'Thread.__init__() not called'
        if self._finished.is_set() or not self._started.is_set():
            return False
        else:
            self._wait_for_tstate_lock(False)
            return not self._finished.is_set()

    isAlive = is_alive

    @property
    def daemon(self):
        """A boolean value indicating whether this thread is a daemon thread.

        This must be set before start() is called, otherwise RuntimeError is
        raised. Its initial value is inherited from the creating thread; the
        main thread is not a daemon thread and therefore all threads created in
        the main thread default to daemon = False.

        The entire Python program exits when no alive non-daemon threads are
        left.

        """
        assert self._initialized, 'Thread.__init__() not called'
        return self._daemonic

    @daemon.setter
    def daemon(self, daemonic):
        if not self._initialized:
            raise RuntimeError('Thread.__init__() not called')
        if self._started.is_set():
            raise RuntimeError('cannot set daemon status of active thread')
        self._daemonic = daemonic

    def isDaemon(self):
        return self.daemon

    def setDaemon(self, daemonic):
        self.daemon = daemonic

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name


class Timer(Thread):
    __doc__ = "Call a function after a specified number of seconds:\n\n            t = Timer(30.0, f, args=None, kwargs=None)\n            t.start()\n            t.cancel()     # stop the timer's action if it's still waiting\n\n    "

    def __init__(self, interval, func, repeat=None, args=None, kwargs=None):
        Thread.__init__(self)
        self.interval = interval
        self.function = func
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = Event()
        self.repeat = repeat
        self.runs = 0

    def cancel(self):
        """Stop the timer if it hasn't finished yet."""
        self.finished.set()

    def _checkrepeat(self):
        if self.repeat is None:
            return False
        else:
            if callable(self.repeat):
                return self.repeat()
            if self.repeat == 'inf':
                return True
            return self.repeat > self.runs

    def _autocancel(self, *_):
        self.cancel()

    def run(self):
        try:
            signals.add_handler(signals.SIGINT, self._autocancel)
            self.finished.wait(self.interval)
            if not self.finished.is_set():
                while True:
                    (self.function)(*self.args, **self.kwargs)
                    self.runs += 1
                    if self._checkrepeat() and not self.finished.is_set():
                        self.finished.wait(self.interval)
                    else:
                        break

        finally:
            signals.rm_handler(signals.SIGINT, self._autocancel)
            self.finished.set()


class SuspendableThread(Thread):
    __doc__ = '\n    This class implements a thread variant that is able to suspend itself until\n    it is being resumed by some other thread. There are :attr:`dnutils.threads.suspended`\n    and :attr:`dnutils.threads.resumed` Events that can be used to wait on the\n    respective events.\n    '
    _signals = Thread._signals | {SUSPEND, RESUME}

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._sleeper = Condition(RLock())

    def suspend(self):
        """
        Causes the calling thread to sleep until it gets resumed. Should only be called
        from within the thread class.
        :return:
        """
        if get_ident() != self.ident:
            raise RuntimeError('a thread can only suspend itself.')
        with self._sleeper:
            for h in self._handlers[SUSPEND]:
                h()

            self._sleeper.wait()
            for h in self._handlers[RESUME]:
                h()

    def resume(self):
        """
        Wakes up a :class:`dnutils.threads.SuspendableThread` if it is currently
        suspended.
        :return:
        """
        with self._sleeper:
            self._sleeper.notify_all()


class _MainThread(Thread):

    def __init__(self):
        Thread.__init__(self, name='MainThread', daemon=False)
        self._set_tstate_lock()
        self._started = _DummyEvent()
        self._set_ident()
        with _active_limbo_lock:
            _active[self._ident] = self


class _DummyEvent:

    def set(self):
        pass

    def is_set(self):
        return True

    def clear(self):
        pass

    def wait(self):
        pass


class _DummyThread(Thread):

    def __init__(self):
        Thread.__init__(self, name=(_newname('Dummy-%d')), daemon=True)
        self._started = _DummyEvent()
        self._set_ident()
        with _active_limbo_lock:
            _active[self._ident] = self

    def _stop(self):
        pass

    def join(self, timeout=None):
        assert False, 'cannot join a dummy thread'


def current_thread():
    """Return the current Thread object, corresponding to the caller's thread of control.

    If the caller's thread of control was not created through the threading
    module, a dummy thread object with limited functionality is returned.

    """
    try:
        return _active[get_ident()]
    except KeyError:
        return _DummyThread()


currentThread = current_thread

def active_count():
    """Return the number of Thread objects currently alive.

    The returned count is equal to the length of the list returned by
    enumerate().

    """
    with _active_limbo_lock:
        return len(_active) + len(_limbo)


activeCount = active_count

def _enumerate():
    return list(_active.values()) + list(_limbo.values())


def enumerate():
    """Return a list of all Thread objects currently alive.

    The list includes daemonic threads, dummy thread objects created by
    current_thread(), and the main thread. It excludes terminated threads and
    threads that have not yet been started.

    """
    with _active_limbo_lock:
        return list(_active.values()) + list(_limbo.values())


from _thread import stack_size
_main_thread = _MainThread()

def _shutdown():
    global _main_thread
    tlock = _main_thread._tstate_lock
    if not tlock is not None:
        raise AssertionError
    elif not tlock.locked():
        raise AssertionError
    tlock.release()
    _main_thread._stop()
    t = _pickSomeNonDaemonThread()
    while t:
        t.join()
        t = _pickSomeNonDaemonThread()

    _main_thread._delete()


def _pickSomeNonDaemonThread():
    for t in enumerate():
        if not t.daemon:
            if t.is_alive():
                return t


def main_thread():
    """Return the main thread object.

    In normal conditions, the main thread is the thread from which the
    Python interpreter was started.
    """
    return _main_thread


try:
    from _thread import _local as local
except ImportError:
    from _threading_local import local

def interrupted():
    if current_thread()._interrupt:
        raise ThreadInterrupt()


def _after_fork():
    global _active_limbo_lock
    global _main_thread
    _active_limbo_lock = _allocate_lock()
    new_active = {}
    current = current_thread()
    _main_thread = current
    with _active_limbo_lock:
        threads = set(_enumerate())
        threads.update(_dangling)
        for thread in threads:
            if thread is current:
                thread._reset_internal_locks(True)
                ident = get_ident()
                thread._ident = ident
                new_active[ident] = thread
            else:
                thread._reset_internal_locks(False)
                thread._stop()

        _limbo.clear()
        _active.clear()
        _active.update(new_active)
        assert len(_active) == 1


l = Lock()
r = Relay()
threadnum = 200

class MyThread(SuspendableThread):

    def run(self):
        out('starting thread and sleeping', self.ident)
        try:
            r.inc()
            t = 5
            out(self.name, 'was working for', waitabout(t))
            r.dec()
            self.suspend()
        except ThreadInterrupt as e:
            out('caught', repr(e), 'straightening up...')

        out('exiting thread.')


def _interrupt_blocking_threads(*args):
    for t in enumerate():
        if type(t) is _MainThread:
            pass
        else:
            t.interrupt()

    main_thread().interrupt()


signals.add_handler(signals.SIGINT, _interrupt_blocking_threads)
threads = [MyThread(name=(str(i))) for i in range(threadnum)]

def hello():
    out('hello')


if __name__ == '__main__':
    r.acquire()
    for t in threads:
        t.start()

    out('all threads should sleep now...')
    sleep(1)
    out('waking up the first...')
    sleep(1)
    r.wait()
    r.release()
    out('main thread exiting.')