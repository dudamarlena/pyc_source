# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\test\lock_tests.py
# Compiled at: 2017-12-11 20:12:50
"""
Various tests for synchronization primitives.
Taken from lib/test/lock_test.py and adapted for stackless
"""
import sys, time, stackless, unittest
from test import test_support as support
from .. import main
t0 = time.time()
while True:
    t1 = time.time()
    if t1 != t0:
        break

time_gran = t1 - t0

def pumper():
    while True:
        main.mainloop.pump()
        stackless.schedule()


def _wait():
    t = time.time()
    while time.time() - t < 0.01:
        stackless.schedule()


def get_ident():
    return id(stackless.getcurrent())


def start_new_thread(func, args):
    stackless.tasklet(func)(*args)


class Bunch(object):
    """
    A bunch of threads.
    """

    def __init__(self, f, n, wait_before_exit=False):
        """
        Construct a bunch of `n` threads running the same function `f`.
        If `wait_before_exit` is True, the threads won't terminate until
        do_finish() is called.
        """
        self.f = f
        self.n = n
        self.started = []
        self.finished = []
        self._can_exit = not wait_before_exit

        def task():
            tid = get_ident()
            self.started.append(tid)
            try:
                f()
            finally:
                self.finished.append(tid)
                while not self._can_exit:
                    _wait()

        for i in range(n):
            start_new_thread(task, ())

    def wait_for_started(self):
        while len(self.started) < self.n:
            _wait()

    def wait_for_finished(self):
        while len(self.finished) < self.n:
            _wait()

    def do_finish(self):
        self._can_exit = True


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.pumper = stackless.tasklet(pumper)()

    def tearDown(self):
        self.pumper.kill()


class BaseLockTests(BaseTestCase):
    """
    Tests for both recursive and non-recursive locks.
    """

    def test_constructor(self):
        lock = self.locktype()
        del lock

    def test_acquire_destroy(self):
        lock = self.locktype()
        lock.acquire()
        del lock

    def test_acquire_release(self):
        lock = self.locktype()
        lock.acquire()
        lock.release()
        del lock

    def test_try_acquire(self):
        lock = self.locktype()
        self.assertTrue(lock.acquire(False))
        lock.release()

    def test_try_acquire_contended(self):
        lock = self.locktype()
        lock.acquire()
        result = []

        def f():
            result.append(lock.acquire(False))

        Bunch(f, 1).wait_for_finished()
        self.assertFalse(result[0])
        lock.release()

    def test_acquire_contended(self):
        lock = self.locktype()
        lock.acquire()
        N = 5

        def f():
            lock.acquire()
            lock.release()

        b = Bunch(f, N)
        b.wait_for_started()
        _wait()
        self.assertEqual(len(b.finished), 0)
        lock.release()
        b.wait_for_finished()
        self.assertEqual(len(b.finished), N)

    def test_with(self):
        lock = self.locktype()

        def f():
            lock.acquire()
            lock.release()

        def _with(err=None):
            with lock:
                if err is not None:
                    raise err
            return

        _with()
        Bunch(f, 1).wait_for_finished()
        self.assertRaises(TypeError, _with, TypeError)
        Bunch(f, 1).wait_for_finished()
        return

    def _test_thread_leak(self):
        lock = self.locktype()

        def f():
            lock.acquire()
            lock.release()

        n = len(threading.enumerate())
        Bunch(f, 15).wait_for_finished()
        self.assertEqual(n, len(threading.enumerate()))


class LockTests(BaseLockTests):
    """
    Tests for non-recursive, weak locks
    (which can be acquired and released from different threads).
    """

    def test_reacquire(self):
        lock = self.locktype()
        phase = []

        def f():
            lock.acquire()
            phase.append(None)
            lock.acquire()
            phase.append(None)
            return

        start_new_thread(f, ())
        while len(phase) == 0:
            _wait()

        _wait()
        self.assertEqual(len(phase), 1)
        lock.release()
        while len(phase) == 1:
            _wait()

        self.assertEqual(len(phase), 2)

    def test_different_thread(self):
        lock = self.locktype()
        lock.acquire()

        def f():
            lock.release()

        b = Bunch(f, 1)
        b.wait_for_finished()
        lock.acquire()
        lock.release()


class RLockTests(BaseLockTests):
    """
    Tests for recursive locks.
    """

    def test_reacquire(self):
        lock = self.locktype()
        lock.acquire()
        lock.acquire()
        lock.release()
        lock.acquire()
        lock.release()
        lock.release()

    def test_release_unacquired(self):
        lock = self.locktype()
        self.assertRaises(RuntimeError, lock.release)
        lock.acquire()
        lock.acquire()
        lock.release()
        lock.acquire()
        lock.release()
        lock.release()
        self.assertRaises(RuntimeError, lock.release)

    def test_different_thread(self):
        lock = self.locktype()

        def f():
            lock.acquire()

        b = Bunch(f, 1, True)
        try:
            self.assertRaises(RuntimeError, lock.release)
        finally:
            b.do_finish()

    def test__is_owned(self):
        lock = self.locktype()
        self.assertFalse(lock._is_owned())
        lock.acquire()
        self.assertTrue(lock._is_owned())
        lock.acquire()
        self.assertTrue(lock._is_owned())
        result = []

        def f():
            result.append(lock._is_owned())

        Bunch(f, 1).wait_for_finished()
        self.assertFalse(result[0])
        lock.release()
        self.assertTrue(lock._is_owned())
        lock.release()
        self.assertFalse(lock._is_owned())


class EventTests(BaseTestCase):
    """
    Tests for Event objects.
    """

    def test_is_set(self):
        evt = self.eventtype()
        self.assertFalse(evt.is_set())
        evt.set()
        self.assertTrue(evt.is_set())
        evt.set()
        self.assertTrue(evt.is_set())
        evt.clear()
        self.assertFalse(evt.is_set())
        evt.clear()
        self.assertFalse(evt.is_set())

    def _check_notify(self, evt):
        N = 5
        results1 = []
        results2 = []

        def f():
            results1.append(evt.wait())
            results2.append(evt.wait())

        b = Bunch(f, N)
        b.wait_for_started()
        _wait()
        self.assertEqual(len(results1), 0)
        evt.set()
        b.wait_for_finished()
        self.assertEqual(results1, [True] * N)
        self.assertEqual(results2, [True] * N)

    def test_notify(self):
        evt = self.eventtype()
        self._check_notify(evt)
        evt.set()
        evt.clear()
        self._check_notify(evt)

    def test_timeout(self):
        evt = self.eventtype()
        results1 = []
        results2 = []
        N = 5

        def f():
            results1.append(evt.wait(0.0))
            t1 = time.time()
            r = evt.wait(0.2)
            t2 = time.time()
            results2.append((r, t2 - t1))

        Bunch(f, N).wait_for_finished()
        self.assertEqual(results1, [False] * N)
        for r, dt in results2:
            self.assertFalse(r)
            self.assertTrue(dt >= 0.2 - time_gran, dt)

        results1 = []
        results2 = []
        evt.set()
        Bunch(f, N).wait_for_finished()
        self.assertEqual(results1, [True] * N)
        for r, dt in results2:
            self.assertTrue(r)


class NLConditionTests(BaseTestCase):
    """
    Tests for condition variables.
    """

    def test_acquire(self):
        cond = self.condtype()
        cond.acquire()
        cond.acquire()
        cond.release()
        cond.release()
        cond = self.condtype()
        cond.acquire()
        cond.release()

    def _test_unacquired_wait(self):
        cond = self.condtype()
        self.assertRaises(RuntimeError, cond.wait)

    def _test_unacquired_notify(self):
        cond = self.condtype()
        self.assertRaises(RuntimeError, cond.notify)

    def _check_notify(self, cond):
        N = 5
        results1 = []
        results2 = []
        phase_num = 0

        def f():
            cond.acquire()
            cond.wait()
            cond.release()
            results1.append(phase_num)
            cond.acquire()
            cond.wait()
            cond.release()
            results2.append(phase_num)

        b = Bunch(f, N)
        b.wait_for_started()
        _wait()
        self.assertEqual(results1, [])
        cond.acquire()
        cond.notify(3)
        phase_num = 1
        _wait()
        cond.release()
        while len(results1) < 3:
            _wait()

        self.assertEqual(results1, [1] * 3)
        self.assertEqual(results2, [])
        cond.acquire()
        cond.notify(5)
        phase_num = 2
        _wait()
        cond.release()
        while len(results1) + len(results2) < 8:
            _wait()

        self.assertEqual(results1, [1] * 3 + [2] * 2)
        self.assertEqual(results2, [2] * 3)
        cond.acquire()
        cond.notify_all()
        phase_num = 3
        cond.release()
        _wait()
        while len(results2) < 5:
            _wait()

        self.assertEqual(results1, [1] * 3 + [2] * 2)
        self.assertEqual(results2, [2] * 3 + [3] * 2)
        b.wait_for_finished()

    def test_notify(self):
        cond = self.condtype()
        self._check_notify(cond)
        self._check_notify(cond)

    def test_timeout(self):
        cond = self.condtype()
        results = []
        N = 5

        def f():
            cond.acquire()
            t1 = time.time()
            cond.wait(0.2)
            t2 = time.time()
            cond.release()
            results.append(t2 - t1)

        Bunch(f, N).wait_for_finished()
        self.assertEqual(len(results), 5)
        for dt in results:
            self.assertTrue(dt >= 0.2 - time_gran, dt)


class ConditionTests(BaseTestCase):
    """
    Tests for condition variables.
    """

    def test_acquire(self):
        cond = self.condtype()
        cond.acquire()
        cond.acquire()
        cond.release()
        cond.release()
        lock = self.locktype()
        cond = self.condtype(lock)
        cond.acquire()
        self.assertFalse(lock.acquire(False))
        cond.release()
        self.assertTrue(lock.acquire(False))
        self.assertFalse(cond.acquire(False))
        lock.release()
        with cond:
            self.assertFalse(lock.acquire(False))

    def test_unacquired_wait(self):
        cond = self.condtype()
        self.assertRaises(RuntimeError, cond.wait)

    def test_unacquired_notify(self):
        cond = self.condtype()
        self.assertRaises(RuntimeError, cond.notify)

    def _check_notify(self, cond):
        N = 5
        results1 = []
        results2 = []
        phase_num = 0

        def f():
            cond.acquire()
            cond.wait()
            cond.release()
            results1.append(phase_num)
            cond.acquire()
            cond.wait()
            cond.release()
            results2.append(phase_num)

        b = Bunch(f, N)
        b.wait_for_started()
        _wait()
        self.assertEqual(results1, [])
        cond.acquire()
        cond.notify(3)
        _wait()
        phase_num = 1
        cond.release()
        while len(results1) < 3:
            _wait()

        self.assertEqual(results1, [1] * 3)
        self.assertEqual(results2, [])
        cond.acquire()
        cond.notify(5)
        _wait()
        phase_num = 2
        cond.release()
        while len(results1) + len(results2) < 8:
            _wait()

        self.assertEqual(results1, [1] * 3 + [2] * 2)
        self.assertEqual(results2, [2] * 3)
        cond.acquire()
        cond.notify_all()
        _wait()
        phase_num = 3
        cond.release()
        while len(results2) < 5:
            _wait()

        self.assertEqual(results1, [1] * 3 + [2] * 2)
        self.assertEqual(results2, [2] * 3 + [3] * 2)
        b.wait_for_finished()

    def test_notify(self):
        cond = self.condtype()
        self._check_notify(cond)
        self._check_notify(cond)

    def test_timeout(self):
        cond = self.condtype()
        results = []
        N = 5

        def f():
            cond.acquire()
            t1 = time.time()
            cond.wait(0.2)
            t2 = time.time()
            cond.release()
            results.append(t2 - t1)

        Bunch(f, N).wait_for_finished()
        self.assertEqual(len(results), 5)
        for dt in results:
            self.assertTrue(dt >= 0.2 - time_gran, dt)


class BaseSemaphoreTests(BaseTestCase):
    """
    Common tests for {bounded, unbounded} semaphore objects.
    """

    def test_constructor(self):
        self.assertRaises(ValueError, self.semtype, value=-1)
        self.assertRaises(ValueError, self.semtype, value=-sys.maxint)

    def test_acquire(self):
        sem = self.semtype(1)
        sem.acquire()
        sem.release()
        sem = self.semtype(2)
        sem.acquire()
        sem.acquire()
        sem.release()
        sem.release()

    def test_acquire_destroy(self):
        sem = self.semtype()
        sem.acquire()
        del sem

    def test_acquire_contended(self):
        sem = self.semtype(7)
        sem.acquire()
        N = 10
        results1 = []
        results2 = []
        phase_num = 0

        def f():
            sem.acquire()
            results1.append(phase_num)
            sem.acquire()
            results2.append(phase_num)

        b = Bunch(f, 10)
        b.wait_for_started()
        while len(results1) + len(results2) < 6:
            _wait()

        self.assertEqual(results1 + results2, [0] * 6)
        phase_num = 1
        for i in range(7):
            sem.release()

        while len(results1) + len(results2) < 13:
            _wait()

        self.assertEqual(sorted(results1 + results2), [0] * 6 + [1] * 7)
        phase_num = 2
        for i in range(6):
            sem.release()

        while len(results1) + len(results2) < 19:
            _wait()

        self.assertEqual(sorted(results1 + results2), [0] * 6 + [1] * 7 + [2] * 6)
        self.assertFalse(sem.acquire(False))
        sem.release()
        b.wait_for_finished()

    def test_try_acquire(self):
        sem = self.semtype(2)
        self.assertTrue(sem.acquire(False))
        self.assertTrue(sem.acquire(False))
        self.assertFalse(sem.acquire(False))
        sem.release()
        self.assertTrue(sem.acquire(False))

    def test_try_acquire_contended(self):
        sem = self.semtype(4)
        sem.acquire()
        results = []

        def f():
            results.append(sem.acquire(False))
            results.append(sem.acquire(False))

        Bunch(f, 5).wait_for_finished()
        self.assertEqual(sorted(results), [False] * 7 + [True] * 3)

    def test_default_value(self):
        sem = self.semtype()
        sem.acquire()

        def f():
            sem.acquire()
            sem.release()

        b = Bunch(f, 1)
        b.wait_for_started()
        _wait()
        self.assertFalse(b.finished)
        sem.release()
        b.wait_for_finished()

    def test_with(self):
        sem = self.semtype(2)

        def _with(err=None):
            with sem:
                self.assertTrue(sem.acquire(False))
                sem.release()
                with sem:
                    self.assertFalse(sem.acquire(False))
                    if err:
                        raise err

        _with()
        self.assertTrue(sem.acquire(False))
        sem.release()
        self.assertRaises(TypeError, _with, TypeError)
        self.assertTrue(sem.acquire(False))
        sem.release()
        return


class SemaphoreTests(BaseSemaphoreTests):
    """
    Tests for unbounded semaphores.
    """

    def test_release_unacquired(self):
        sem = self.semtype(1)
        sem.release()
        sem.acquire()
        sem.acquire()
        sem.release()


class BoundedSemaphoreTests(BaseSemaphoreTests):
    """
    Tests for bounded semaphores.
    """

    def test_release_unacquired(self):
        sem = self.semtype()
        self.assertRaises(ValueError, sem.release)
        sem.acquire()
        sem.release()
        self.assertRaises(ValueError, sem.release)