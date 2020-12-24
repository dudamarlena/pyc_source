# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\multiprocessing\tests.py
# Compiled at: 2009-07-30 09:32:54
import unittest, threading, Queue, time, sys, os, gc, signal, array, copy, socket, random, logging
try:
    import multiprocessing.synchronize
except ImportError, e:
    from test.test_support import TestSkipped
    raise TestSkipped(e)

import multiprocessing.dummy, multiprocessing.connection, multiprocessing.managers, multiprocessing.heap, multiprocessing.pool, _multiprocessing
from multiprocessing import util
latin = str
bytes = str
LOG_LEVEL = util.SUBWARNING
DELTA = 0.1
CHECK_TIMINGS = False
if CHECK_TIMINGS:
    (TIMEOUT1, TIMEOUT2, TIMEOUT3) = (0.82, 0.35, 1.4)
else:
    (TIMEOUT1, TIMEOUT2, TIMEOUT3) = (0.1, 0.1, 0.1)
HAVE_GETVALUE = not getattr(_multiprocessing, 'HAVE_BROKEN_SEM_GETVALUE', False)
WIN32 = sys.platform == 'win32'

class TimingWrapper(object):
    __module__ = __name__

    def __init__(self, func):
        self.func = func
        self.elapsed = None
        return

    def __call__(self, *args, **kwds):
        t = time.time()
        try:
            return self.func(*args, **kwds)
        finally:
            self.elapsed = time.time() - t


class BaseTestCase(object):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', 'manager', 'threads')

    def assertTimingAlmostEqual(self, a, b):
        if CHECK_TIMINGS:
            self.assertAlmostEqual(a, b, 1)

    def assertReturnsIfImplemented(self, value, func, *args):
        try:
            res = func(*args)
        except NotImplementedError:
            pass
        else:
            return self.assertEqual(value, res)


def get_value(self):
    try:
        return self.get_value()
    except AttributeError:
        try:
            return self._Semaphore__value
        except AttributeError:
            try:
                return self._value
            except AttributeError:
                raise NotImplementedError


class _TestProcess(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', 'threads')

    def test_current(self):
        if self.TYPE == 'threads':
            return
        current = self.current_process()
        authkey = current.authkey
        self.assertTrue(current.is_alive())
        self.assertTrue(not current.daemon)
        self.assertTrue(isinstance(authkey, bytes))
        self.assertTrue(len(authkey) > 0)
        self.assertEqual(current.ident, os.getpid())
        self.assertEqual(current.exitcode, None)
        return

    def _test(self, q, *args, **kwds):
        current = self.current_process()
        q.put(args)
        q.put(kwds)
        q.put(current.name)
        if self.TYPE != 'threads':
            q.put(bytes(current.authkey))
            q.put(current.pid)

    def test_process(self):
        q = self.Queue(1)
        e = self.Event()
        args = (q, 1, 2)
        kwargs = {'hello': 23, 'bye': 2.54}
        name = 'SomeProcess'
        p = self.Process(target=self._test, args=args, kwargs=kwargs, name=name)
        p.daemon = True
        current = self.current_process()
        if self.TYPE != 'threads':
            self.assertEquals(p.authkey, current.authkey)
        self.assertEquals(p.is_alive(), False)
        self.assertEquals(p.daemon, True)
        self.assertTrue(p not in self.active_children())
        self.assertTrue(type(self.active_children()) is list)
        self.assertEqual(p.exitcode, None)
        p.start()
        self.assertEquals(p.exitcode, None)
        self.assertEquals(p.is_alive(), True)
        self.assertTrue(p in self.active_children())
        self.assertEquals(q.get(), args[1:])
        self.assertEquals(q.get(), kwargs)
        self.assertEquals(q.get(), p.name)
        if self.TYPE != 'threads':
            self.assertEquals(q.get(), current.authkey)
            self.assertEquals(q.get(), p.pid)
        p.join()
        self.assertEquals(p.exitcode, 0)
        self.assertEquals(p.is_alive(), False)
        self.assertTrue(p not in self.active_children())
        return

    def _test_terminate(self):
        time.sleep(1000)

    def test_terminate(self):
        if self.TYPE == 'threads':
            return
        p = self.Process(target=self._test_terminate)
        p.daemon = True
        p.start()
        self.assertEqual(p.is_alive(), True)
        self.assertTrue(p in self.active_children())
        self.assertEqual(p.exitcode, None)
        p.terminate()
        join = TimingWrapper(p.join)
        self.assertEqual(join(), None)
        self.assertTimingAlmostEqual(join.elapsed, 0.0)
        self.assertEqual(p.is_alive(), False)
        self.assertTrue(p not in self.active_children())
        p.join()
        return

    def test_cpu_count(self):
        try:
            cpus = multiprocessing.cpu_count()
        except NotImplementedError:
            cpus = 1

        self.assertTrue(type(cpus) is int)
        self.assertTrue(cpus >= 1)

    def test_active_children(self):
        self.assertEqual(type(self.active_children()), list)
        p = self.Process(target=time.sleep, args=(DELTA,))
        self.assertTrue(p not in self.active_children())
        p.start()
        self.assertTrue(p in self.active_children())
        p.join()
        self.assertTrue(p not in self.active_children())

    def _test_recursion(self, wconn, id):
        from multiprocessing import forking
        wconn.send(id)
        if len(id) < 2:
            for i in range(2):
                p = self.Process(target=self._test_recursion, args=(wconn, id + [i]))
                p.start()
                p.join()

    def test_recursion(self):
        (rconn, wconn) = self.Pipe(duplex=False)
        self._test_recursion(wconn, [])
        time.sleep(DELTA)
        result = []
        while rconn.poll():
            result.append(rconn.recv())

        expected = [[], [0], [0, 0], [0, 1], [1], [1, 0], [1, 1]]
        self.assertEqual(result, expected)


class _UpperCaser(multiprocessing.Process):
    __module__ = __name__

    def __init__(self):
        multiprocessing.Process.__init__(self)
        (self.child_conn, self.parent_conn) = multiprocessing.Pipe()

    def run(self):
        self.parent_conn.close()
        for s in iter(self.child_conn.recv, None):
            self.child_conn.send(s.upper())

        self.child_conn.close()
        return

    def submit(self, s):
        assert type(s) is str
        self.parent_conn.send(s)
        return self.parent_conn.recv()

    def stop(self):
        self.parent_conn.send(None)
        self.parent_conn.close()
        self.child_conn.close()
        return


class _TestSubclassingProcess(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', )

    def test_subclassing(self):
        uppercaser = _UpperCaser()
        uppercaser.start()
        self.assertEqual(uppercaser.submit('hello'), 'HELLO')
        self.assertEqual(uppercaser.submit('world'), 'WORLD')
        uppercaser.stop()
        uppercaser.join()


def queue_empty(q):
    if hasattr(q, 'empty'):
        return q.empty()
    else:
        return q.qsize() == 0


def queue_full(q, maxsize):
    if hasattr(q, 'full'):
        return q.full()
    else:
        return q.qsize() == maxsize


class _TestQueue(BaseTestCase):
    __module__ = __name__

    def _test_put(self, queue, child_can_start, parent_can_continue):
        child_can_start.wait()
        for i in range(6):
            queue.get()

        parent_can_continue.set()

    def test_put(self):
        MAXSIZE = 6
        queue = self.Queue(maxsize=MAXSIZE)
        child_can_start = self.Event()
        parent_can_continue = self.Event()
        proc = self.Process(target=self._test_put, args=(queue, child_can_start, parent_can_continue))
        proc.daemon = True
        proc.start()
        self.assertEqual(queue_empty(queue), True)
        self.assertEqual(queue_full(queue, MAXSIZE), False)
        queue.put(1)
        queue.put(2, True)
        queue.put(3, True, None)
        queue.put(4, False)
        queue.put(5, False, None)
        queue.put_nowait(6)
        time.sleep(DELTA)
        self.assertEqual(queue_empty(queue), False)
        self.assertEqual(queue_full(queue, MAXSIZE), True)
        put = TimingWrapper(queue.put)
        put_nowait = TimingWrapper(queue.put_nowait)
        self.assertRaises(Queue.Full, put, 7, False)
        self.assertTimingAlmostEqual(put.elapsed, 0)
        self.assertRaises(Queue.Full, put, 7, False, None)
        self.assertTimingAlmostEqual(put.elapsed, 0)
        self.assertRaises(Queue.Full, put_nowait, 7)
        self.assertTimingAlmostEqual(put_nowait.elapsed, 0)
        self.assertRaises(Queue.Full, put, 7, True, TIMEOUT1)
        self.assertTimingAlmostEqual(put.elapsed, TIMEOUT1)
        self.assertRaises(Queue.Full, put, 7, False, TIMEOUT2)
        self.assertTimingAlmostEqual(put.elapsed, 0)
        self.assertRaises(Queue.Full, put, 7, True, timeout=TIMEOUT3)
        self.assertTimingAlmostEqual(put.elapsed, TIMEOUT3)
        child_can_start.set()
        parent_can_continue.wait()
        self.assertEqual(queue_empty(queue), True)
        self.assertEqual(queue_full(queue, MAXSIZE), False)
        proc.join()
        return

    def _test_get(self, queue, child_can_start, parent_can_continue):
        child_can_start.wait()
        queue.put(2)
        queue.put(3)
        queue.put(4)
        queue.put(5)
        parent_can_continue.set()

    def test_get(self):
        queue = self.Queue()
        child_can_start = self.Event()
        parent_can_continue = self.Event()
        proc = self.Process(target=self._test_get, args=(queue, child_can_start, parent_can_continue))
        proc.daemon = True
        proc.start()
        self.assertEqual(queue_empty(queue), True)
        child_can_start.set()
        parent_can_continue.wait()
        time.sleep(DELTA)
        self.assertEqual(queue_empty(queue), False)
        self.assertEqual(queue.get(True, None), 2)
        self.assertEqual(queue.get(True), 3)
        self.assertEqual(queue.get(timeout=1), 4)
        self.assertEqual(queue.get_nowait(), 5)
        self.assertEqual(queue_empty(queue), True)
        get = TimingWrapper(queue.get)
        get_nowait = TimingWrapper(queue.get_nowait)
        self.assertRaises(Queue.Empty, get, False)
        self.assertTimingAlmostEqual(get.elapsed, 0)
        self.assertRaises(Queue.Empty, get, False, None)
        self.assertTimingAlmostEqual(get.elapsed, 0)
        self.assertRaises(Queue.Empty, get_nowait)
        self.assertTimingAlmostEqual(get_nowait.elapsed, 0)
        self.assertRaises(Queue.Empty, get, True, TIMEOUT1)
        self.assertTimingAlmostEqual(get.elapsed, TIMEOUT1)
        self.assertRaises(Queue.Empty, get, False, TIMEOUT2)
        self.assertTimingAlmostEqual(get.elapsed, 0)
        self.assertRaises(Queue.Empty, get, timeout=TIMEOUT3)
        self.assertTimingAlmostEqual(get.elapsed, TIMEOUT3)
        proc.join()
        return

    def _test_fork(self, queue):
        for i in range(10, 20):
            queue.put(i)

    def test_fork(self):
        queue = self.Queue()
        for i in range(10):
            queue.put(i)

        time.sleep(DELTA)
        p = self.Process(target=self._test_fork, args=(queue,))
        p.start()
        for i in range(20):
            self.assertEqual(queue.get(), i)

        self.assertRaises(Queue.Empty, queue.get, False)
        p.join()

    def test_qsize(self):
        q = self.Queue()
        try:
            self.assertEqual(q.qsize(), 0)
        except NotImplementedError:
            return

        q.put(1)
        self.assertEqual(q.qsize(), 1)
        q.put(5)
        self.assertEqual(q.qsize(), 2)
        q.get()
        self.assertEqual(q.qsize(), 1)
        q.get()
        self.assertEqual(q.qsize(), 0)

    def _test_task_done(self, q):
        for obj in iter(q.get, None):
            time.sleep(DELTA)
            q.task_done()

        return

    def test_task_done(self):
        queue = self.JoinableQueue()
        if sys.version_info < (2, 5) and not hasattr(queue, 'task_done'):
            return
        workers = [ self.Process(target=self._test_task_done, args=(queue,)) for i in xrange(4) ]
        for p in workers:
            p.start()

        for i in xrange(10):
            queue.put(i)

        queue.join()
        for p in workers:
            queue.put(None)

        for p in workers:
            p.join()

        return


class _TestLock(BaseTestCase):
    __module__ = __name__

    def test_lock(self):
        lock = self.Lock()
        self.assertEqual(lock.acquire(), True)
        self.assertEqual(lock.acquire(False), False)
        self.assertEqual(lock.release(), None)
        self.assertRaises((ValueError, threading.ThreadError), lock.release)
        return

    def test_rlock(self):
        lock = self.RLock()
        self.assertEqual(lock.acquire(), True)
        self.assertEqual(lock.acquire(), True)
        self.assertEqual(lock.acquire(), True)
        self.assertEqual(lock.release(), None)
        self.assertEqual(lock.release(), None)
        self.assertEqual(lock.release(), None)
        self.assertRaises((AssertionError, RuntimeError), lock.release)
        return


class _TestSemaphore(BaseTestCase):
    __module__ = __name__

    def _test_semaphore(self, sem):
        self.assertReturnsIfImplemented(2, get_value, sem)
        self.assertEqual(sem.acquire(), True)
        self.assertReturnsIfImplemented(1, get_value, sem)
        self.assertEqual(sem.acquire(), True)
        self.assertReturnsIfImplemented(0, get_value, sem)
        self.assertEqual(sem.acquire(False), False)
        self.assertReturnsIfImplemented(0, get_value, sem)
        self.assertEqual(sem.release(), None)
        self.assertReturnsIfImplemented(1, get_value, sem)
        self.assertEqual(sem.release(), None)
        self.assertReturnsIfImplemented(2, get_value, sem)
        return

    def test_semaphore(self):
        sem = self.Semaphore(2)
        self._test_semaphore(sem)
        self.assertEqual(sem.release(), None)
        self.assertReturnsIfImplemented(3, get_value, sem)
        self.assertEqual(sem.release(), None)
        self.assertReturnsIfImplemented(4, get_value, sem)
        return

    def test_bounded_semaphore(self):
        sem = self.BoundedSemaphore(2)
        self._test_semaphore(sem)

    def test_timeout(self):
        if self.TYPE != 'processes':
            return
        sem = self.Semaphore(0)
        acquire = TimingWrapper(sem.acquire)
        self.assertEqual(acquire(False), False)
        self.assertTimingAlmostEqual(acquire.elapsed, 0.0)
        self.assertEqual(acquire(False, None), False)
        self.assertTimingAlmostEqual(acquire.elapsed, 0.0)
        self.assertEqual(acquire(False, TIMEOUT1), False)
        self.assertTimingAlmostEqual(acquire.elapsed, 0)
        self.assertEqual(acquire(True, TIMEOUT2), False)
        self.assertTimingAlmostEqual(acquire.elapsed, TIMEOUT2)
        self.assertEqual(acquire(timeout=TIMEOUT3), False)
        self.assertTimingAlmostEqual(acquire.elapsed, TIMEOUT3)
        return


class _TestCondition(BaseTestCase):
    __module__ = __name__

    def f(self, cond, sleeping, woken, timeout=None):
        cond.acquire()
        sleeping.release()
        cond.wait(timeout)
        woken.release()
        cond.release()

    def check_invariant(self, cond):
        if self.TYPE == 'processes':
            try:
                sleepers = cond._sleeping_count.get_value() - cond._woken_count.get_value()
                self.assertEqual(sleepers, 0)
                self.assertEqual(cond._wait_semaphore.get_value(), 0)
            except NotImplementedError:
                pass

    def test_notify(self):
        cond = self.Condition()
        sleeping = self.Semaphore(0)
        woken = self.Semaphore(0)
        p = self.Process(target=self.f, args=(cond, sleeping, woken))
        p.daemon = True
        p.start()
        p = threading.Thread(target=self.f, args=(cond, sleeping, woken))
        p.daemon = True
        p.start()
        sleeping.acquire()
        sleeping.acquire()
        time.sleep(DELTA)
        self.assertReturnsIfImplemented(0, get_value, woken)
        cond.acquire()
        cond.notify()
        cond.release()
        time.sleep(DELTA)
        self.assertReturnsIfImplemented(1, get_value, woken)
        cond.acquire()
        cond.notify()
        cond.release()
        time.sleep(DELTA)
        self.assertReturnsIfImplemented(2, get_value, woken)
        self.check_invariant(cond)
        p.join()

    def test_notify_all(self):
        cond = self.Condition()
        sleeping = self.Semaphore(0)
        woken = self.Semaphore(0)
        for i in range(3):
            p = self.Process(target=self.f, args=(cond, sleeping, woken, TIMEOUT1))
            p.daemon = True
            p.start()
            t = threading.Thread(target=self.f, args=(cond, sleeping, woken, TIMEOUT1))
            t.daemon = True
            t.start()

        for i in xrange(6):
            sleeping.acquire()

        for i in xrange(6):
            woken.acquire()

        self.assertReturnsIfImplemented(0, get_value, woken)
        self.check_invariant(cond)
        for i in range(3):
            p = self.Process(target=self.f, args=(cond, sleeping, woken))
            p.daemon = True
            p.start()
            t = threading.Thread(target=self.f, args=(cond, sleeping, woken))
            t.daemon = True
            t.start()

        for i in xrange(6):
            sleeping.acquire()

        time.sleep(DELTA)
        self.assertReturnsIfImplemented(0, get_value, woken)
        cond.acquire()
        cond.notify_all()
        cond.release()
        time.sleep(DELTA)
        self.assertReturnsIfImplemented(6, get_value, woken)
        self.check_invariant(cond)

    def test_timeout(self):
        cond = self.Condition()
        wait = TimingWrapper(cond.wait)
        cond.acquire()
        res = wait(TIMEOUT1)
        cond.release()
        self.assertEqual(res, None)
        self.assertTimingAlmostEqual(wait.elapsed, TIMEOUT1)
        return


class _TestEvent(BaseTestCase):
    __module__ = __name__

    def _test_event(self, event):
        time.sleep(TIMEOUT2)
        event.set()

    def test_event(self):
        event = self.Event()
        wait = TimingWrapper(event.wait)
        self.assertEqual(wait(0.0), None)
        self.assertTimingAlmostEqual(wait.elapsed, 0.0)
        self.assertEqual(wait(TIMEOUT1), None)
        self.assertTimingAlmostEqual(wait.elapsed, TIMEOUT1)
        event.set()
        self.assertEqual(wait(), None)
        self.assertTimingAlmostEqual(wait.elapsed, 0.0)
        self.assertEqual(wait(TIMEOUT1), None)
        self.assertTimingAlmostEqual(wait.elapsed, 0.0)
        event.clear()
        self.Process(target=self._test_event, args=(event,)).start()
        self.assertEqual(wait(), None)
        return


class _TestValue(BaseTestCase):
    __module__ = __name__
    codes_values = [
     ('i', 4343, 24234), ('d', 3.625, -4.25), ('h', -232, 234), ('c', latin('x'), latin('y'))]

    def _test(self, values):
        for (sv, cv) in zip(values, self.codes_values):
            sv.value = cv[2]

    def test_value(self, raw=False):
        if self.TYPE != 'processes':
            return
        if raw:
            values = [ self.RawValue(code, value) for (code, value, _) in self.codes_values ]
        else:
            values = [ self.Value(code, value) for (code, value, _) in self.codes_values ]
        for (sv, cv) in zip(values, self.codes_values):
            self.assertEqual(sv.value, cv[1])

        proc = self.Process(target=self._test, args=(values,))
        proc.start()
        proc.join()
        for (sv, cv) in zip(values, self.codes_values):
            self.assertEqual(sv.value, cv[2])

    def test_rawvalue(self):
        self.test_value(raw=True)

    def test_getobj_getlock(self):
        if self.TYPE != 'processes':
            return
        val1 = self.Value('i', 5)
        lock1 = val1.get_lock()
        obj1 = val1.get_obj()
        val2 = self.Value('i', 5, lock=None)
        lock2 = val2.get_lock()
        obj2 = val2.get_obj()
        lock = self.Lock()
        val3 = self.Value('i', 5, lock=lock)
        lock3 = val3.get_lock()
        obj3 = val3.get_obj()
        self.assertEqual(lock, lock3)
        arr4 = self.Value('i', 5, lock=False)
        self.assertFalse(hasattr(arr4, 'get_lock'))
        self.assertFalse(hasattr(arr4, 'get_obj'))
        self.assertRaises(AttributeError, self.Value, 'i', 5, lock='navalue')
        arr5 = self.RawValue('i', 5)
        self.assertFalse(hasattr(arr5, 'get_lock'))
        self.assertFalse(hasattr(arr5, 'get_obj'))
        return


class _TestArray(BaseTestCase):
    __module__ = __name__

    def f(self, seq):
        for i in range(1, len(seq)):
            seq[i] += seq[(i - 1)]

    def test_array(self, raw=False):
        if self.TYPE != 'processes':
            return
        seq = [
         680, 626, 934, 821, 150, 233, 548, 982, 714, 831]
        if raw:
            arr = self.RawArray('i', seq)
        else:
            arr = self.Array('i', seq)
        self.assertEqual(len(arr), len(seq))
        self.assertEqual(arr[3], seq[3])
        self.assertEqual(list(arr[2:7]), list(seq[2:7]))
        arr[4:8] = seq[4:8] = array.array('i', [1, 2, 3, 4])
        self.assertEqual(list(arr[:]), seq)
        self.f(seq)
        p = self.Process(target=self.f, args=(arr,))
        p.start()
        p.join()
        self.assertEqual(list(arr[:]), seq)

    def test_rawarray(self):
        self.test_array(raw=True)

    def test_getobj_getlock_obj(self):
        if self.TYPE != 'processes':
            return
        arr1 = self.Array('i', range(10))
        lock1 = arr1.get_lock()
        obj1 = arr1.get_obj()
        arr2 = self.Array('i', range(10), lock=None)
        lock2 = arr2.get_lock()
        obj2 = arr2.get_obj()
        lock = self.Lock()
        arr3 = self.Array('i', range(10), lock=lock)
        lock3 = arr3.get_lock()
        obj3 = arr3.get_obj()
        self.assertEqual(lock, lock3)
        arr4 = self.Array('i', range(10), lock=False)
        self.assertFalse(hasattr(arr4, 'get_lock'))
        self.assertFalse(hasattr(arr4, 'get_obj'))
        self.assertRaises(AttributeError, self.Array, 'i', range(10), lock='notalock')
        arr5 = self.RawArray('i', range(10))
        self.assertFalse(hasattr(arr5, 'get_lock'))
        self.assertFalse(hasattr(arr5, 'get_obj'))
        return


class _TestContainers(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('manager', )

    def test_list(self):
        a = self.list(range(10))
        self.assertEqual(a[:], range(10))
        b = self.list()
        self.assertEqual(b[:], [])
        b.extend(range(5))
        self.assertEqual(b[:], range(5))
        self.assertEqual(b[2], 2)
        self.assertEqual(b[2:10], [2, 3, 4])
        b *= 2
        self.assertEqual(b[:], [0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
        self.assertEqual(b + [5, 6], [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6])
        self.assertEqual(a[:], range(10))
        d = [
         a, b]
        e = self.list(d)
        self.assertEqual(e[:], [
         [
          0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]])
        f = self.list([a])
        a.append('hello')
        self.assertEqual(f[:], [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'hello']])

    def test_dict(self):
        d = self.dict()
        indices = range(65, 70)
        for i in indices:
            d[i] = chr(i)

        self.assertEqual(d.copy(), dict(((i, chr(i)) for i in indices)))
        self.assertEqual(sorted(d.keys()), indices)
        self.assertEqual(sorted(d.values()), [ chr(i) for i in indices ])
        self.assertEqual(sorted(d.items()), [ (i, chr(i)) for i in indices ])

    def test_namespace(self):
        n = self.Namespace()
        n.name = 'Bob'
        n.job = 'Builder'
        n._hidden = 'hidden'
        self.assertEqual((n.name, n.job), ('Bob', 'Builder'))
        del n.job
        self.assertEqual(str(n), "Namespace(name='Bob')")
        self.assertTrue(hasattr(n, 'name'))
        self.assertTrue(not hasattr(n, 'job'))


def sqr(x, wait=0.0):
    time.sleep(wait)
    return x * x


class _TestPool(BaseTestCase):
    __module__ = __name__

    def test_apply(self):
        papply = self.pool.apply
        self.assertEqual(papply(sqr, (5, )), sqr(5))
        self.assertEqual(papply(sqr, (), {'x': 3}), sqr(x=3))

    def test_map(self):
        pmap = self.pool.map
        self.assertEqual(pmap(sqr, range(10)), map(sqr, range(10)))
        self.assertEqual(pmap(sqr, range(100), chunksize=20), map(sqr, range(100)))

    def test_async(self):
        res = self.pool.apply_async(sqr, (7, TIMEOUT1))
        get = TimingWrapper(res.get)
        self.assertEqual(get(), 49)
        self.assertTimingAlmostEqual(get.elapsed, TIMEOUT1)

    def test_async_timeout(self):
        res = self.pool.apply_async(sqr, (6, TIMEOUT2 + 0.2))
        get = TimingWrapper(res.get)
        self.assertRaises(multiprocessing.TimeoutError, get, timeout=TIMEOUT2)
        self.assertTimingAlmostEqual(get.elapsed, TIMEOUT2)

    def test_imap(self):
        it = self.pool.imap(sqr, range(10))
        self.assertEqual(list(it), map(sqr, range(10)))
        it = self.pool.imap(sqr, range(10))
        for i in range(10):
            self.assertEqual(it.next(), i * i)

        self.assertRaises(StopIteration, it.next)
        it = self.pool.imap(sqr, range(1000), chunksize=100)
        for i in range(1000):
            self.assertEqual(it.next(), i * i)

        self.assertRaises(StopIteration, it.next)

    def test_imap_unordered(self):
        it = self.pool.imap_unordered(sqr, range(1000))
        self.assertEqual(sorted(it), map(sqr, range(1000)))
        it = self.pool.imap_unordered(sqr, range(1000), chunksize=53)
        self.assertEqual(sorted(it), map(sqr, range(1000)))

    def test_make_pool(self):
        p = multiprocessing.Pool(3)
        self.assertEqual(3, len(p._pool))
        p.close()
        p.join()

    def test_terminate(self):
        if self.TYPE == 'manager':
            return
        result = self.pool.map_async(time.sleep, [ 0.1 for i in range(10000) ], chunksize=1)
        self.pool.terminate()
        join = TimingWrapper(self.pool.join)
        join()
        self.assertTrue(join.elapsed < 0.2)


class _TestZZZNumberOfObjects(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('manager', )

    def test_number_of_objects(self):
        EXPECTED_NUMBER = 1
        multiprocessing.active_children()
        gc.collect()
        refs = self.manager._number_of_objects()
        debug_info = self.manager._debug_info()
        if refs != EXPECTED_NUMBER:
            print self.manager._debug_info()
            print debug_info
        self.assertEqual(refs, EXPECTED_NUMBER)


from multiprocessing.managers import BaseManager, BaseProxy, RemoteError

class FooBar(object):
    __module__ = __name__

    def f(self):
        return 'f()'

    def g(self):
        raise ValueError

    def _h(self):
        return '_h()'


def baz():
    for i in xrange(10):
        yield i * i


class IteratorProxy(BaseProxy):
    __module__ = __name__
    _exposed_ = ('next', '__next__')

    def __iter__(self):
        return self

    def next(self):
        return self._callmethod('next')

    def __next__(self):
        return self._callmethod('__next__')


class MyManager(BaseManager):
    __module__ = __name__


MyManager.register('Foo', callable=FooBar)
MyManager.register('Bar', callable=FooBar, exposed=('f', '_h'))
MyManager.register('baz', callable=baz, proxytype=IteratorProxy)

class _TestMyManager(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('manager', )

    def test_mymanager(self):
        manager = MyManager()
        manager.start()
        foo = manager.Foo()
        bar = manager.Bar()
        baz = manager.baz()
        foo_methods = [ name for name in ('f', 'g', '_h') if hasattr(foo, name) ]
        bar_methods = [ name for name in ('f', 'g', '_h') if hasattr(bar, name) ]
        self.assertEqual(foo_methods, ['f', 'g'])
        self.assertEqual(bar_methods, ['f', '_h'])
        self.assertEqual(foo.f(), 'f()')
        self.assertRaises(ValueError, foo.g)
        self.assertEqual(foo._callmethod('f'), 'f()')
        self.assertRaises(RemoteError, foo._callmethod, '_h')
        self.assertEqual(bar.f(), 'f()')
        self.assertEqual(bar._h(), '_h()')
        self.assertEqual(bar._callmethod('f'), 'f()')
        self.assertEqual(bar._callmethod('_h'), '_h()')
        self.assertEqual(list(baz), [ i * i for i in range(10) ])
        manager.shutdown()


_queue = Queue.Queue()

def get_queue():
    return _queue


class QueueManager(BaseManager):
    """manager class used by server process"""
    __module__ = __name__


QueueManager.register('get_queue', callable=get_queue)

class QueueManager2(BaseManager):
    """manager class which specifies the same interface as QueueManager"""
    __module__ = __name__


QueueManager2.register('get_queue')
SERIALIZER = 'xmlrpclib'

class _TestRemoteManager(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('manager', )

    def _putter(self, address, authkey):
        manager = QueueManager2(address=address, authkey=authkey, serializer=SERIALIZER)
        manager.connect()
        queue = manager.get_queue()
        queue.put(('hello world', None, True, 2.25))
        return

    def test_remote(self):
        authkey = os.urandom(32)
        manager = QueueManager(address=('localhost', 0), authkey=authkey, serializer=SERIALIZER)
        manager.start()
        p = self.Process(target=self._putter, args=(manager.address, authkey))
        p.start()
        manager2 = QueueManager2(address=manager.address, authkey=authkey, serializer=SERIALIZER)
        manager2.connect()
        queue = manager2.get_queue()
        self.assertEqual(queue.get(), ['hello world', None, True, 2.25])
        self.assertRaises(Exception, queue.put, time.sleep)
        del queue
        manager.shutdown()
        return


SENTINEL = latin('')

class _TestConnection(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', 'threads')

    def _echo(self, conn):
        for msg in iter(conn.recv_bytes, SENTINEL):
            conn.send_bytes(msg)

        conn.close()

    def test_connection(self):
        (conn, child_conn) = self.Pipe()
        p = self.Process(target=self._echo, args=(child_conn,))
        p.daemon = True
        p.start()
        seq = [
         1, 2.25, None]
        msg = latin('hello world')
        longmsg = msg * 10
        arr = array.array('i', range(4))
        if self.TYPE == 'processes':
            self.assertEqual(type(conn.fileno()), int)
        self.assertEqual(conn.send(seq), None)
        self.assertEqual(conn.recv(), seq)
        self.assertEqual(conn.send_bytes(msg), None)
        self.assertEqual(conn.recv_bytes(), msg)
        if self.TYPE == 'processes':
            buffer = array.array('i', [0] * 10)
            expected = list(arr) + [0] * (10 - len(arr))
            self.assertEqual(conn.send_bytes(arr), None)
            self.assertEqual(conn.recv_bytes_into(buffer), len(arr) * buffer.itemsize)
            self.assertEqual(list(buffer), expected)
            buffer = array.array('i', [0] * 10)
            expected = [0] * 3 + list(arr) + [0] * (10 - 3 - len(arr))
            self.assertEqual(conn.send_bytes(arr), None)
            self.assertEqual(conn.recv_bytes_into(buffer, 3 * buffer.itemsize), len(arr) * buffer.itemsize)
            self.assertEqual(list(buffer), expected)
            buffer = array.array('i', [0] * 10)
            self.assertEqual(conn.send_bytes(longmsg), None)
            try:
                res = conn.recv_bytes_into(buffer)
            except multiprocessing.BufferTooShort, e:
                self.assertEqual(e.args, (longmsg,))
            else:
                self.fail('expected BufferTooShort, got %s' % res)
        poll = TimingWrapper(conn.poll)
        self.assertEqual(poll(), False)
        self.assertTimingAlmostEqual(poll.elapsed, 0)
        self.assertEqual(poll(TIMEOUT1), False)
        self.assertTimingAlmostEqual(poll.elapsed, TIMEOUT1)
        conn.send(None)
        self.assertEqual(poll(TIMEOUT1), True)
        self.assertTimingAlmostEqual(poll.elapsed, 0)
        self.assertEqual(conn.recv(), None)
        really_big_msg = latin('X') * (1024 * 1024 * 16)
        conn.send_bytes(really_big_msg)
        self.assertEqual(conn.recv_bytes(), really_big_msg)
        conn.send_bytes(SENTINEL)
        child_conn.close()
        if self.TYPE == 'processes':
            self.assertEqual(conn.readable, True)
            self.assertEqual(conn.writable, True)
            self.assertRaises(EOFError, conn.recv)
            self.assertRaises(EOFError, conn.recv_bytes)
        p.join()
        return

    def test_duplex_false(self):
        (reader, writer) = self.Pipe(duplex=False)
        self.assertEqual(writer.send(1), None)
        self.assertEqual(reader.recv(), 1)
        if self.TYPE == 'processes':
            self.assertEqual(reader.readable, True)
            self.assertEqual(reader.writable, False)
            self.assertEqual(writer.readable, False)
            self.assertEqual(writer.writable, True)
            self.assertRaises(IOError, reader.send, 2)
            self.assertRaises(IOError, writer.recv)
            self.assertRaises(IOError, writer.poll)
        return

    def test_spawn_close(self):
        (conn, child_conn) = self.Pipe()
        p = self.Process(target=self._echo, args=(child_conn,))
        p.start()
        child_conn.close()
        msg = latin('hello')
        conn.send_bytes(msg)
        self.assertEqual(conn.recv_bytes(), msg)
        conn.send_bytes(SENTINEL)
        conn.close()
        p.join()

    def test_sendbytes(self):
        if self.TYPE != 'processes':
            return
        msg = latin('abcdefghijklmnopqrstuvwxyz')
        (a, b) = self.Pipe()
        a.send_bytes(msg)
        self.assertEqual(b.recv_bytes(), msg)
        a.send_bytes(msg, 5)
        self.assertEqual(b.recv_bytes(), msg[5:])
        a.send_bytes(msg, 7, 8)
        self.assertEqual(b.recv_bytes(), msg[7:7 + 8])
        a.send_bytes(msg, 26)
        self.assertEqual(b.recv_bytes(), latin(''))
        a.send_bytes(msg, 26, 0)
        self.assertEqual(b.recv_bytes(), latin(''))
        self.assertRaises(ValueError, a.send_bytes, msg, 27)
        self.assertRaises(ValueError, a.send_bytes, msg, 22, 5)
        self.assertRaises(ValueError, a.send_bytes, msg, 26, 1)
        self.assertRaises(ValueError, a.send_bytes, msg, -1)
        self.assertRaises(ValueError, a.send_bytes, msg, 4, -1)


class _TestListenerClient(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', 'threads')

    def _test(self, address):
        conn = self.connection.Client(address)
        conn.send('hello')
        conn.close()

    def test_listener_client(self):
        for family in self.connection.families:
            l = self.connection.Listener(family=family)
            p = self.Process(target=self._test, args=(l.address,))
            p.daemon = True
            p.start()
            conn = l.accept()
            self.assertEqual(conn.recv(), 'hello')
            p.join()
            l.close()


class _TestHeap(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', )

    def test_heap(self):
        iterations = 5000
        maxblocks = 50
        blocks = []
        for i in xrange(iterations):
            size = int(random.lognormvariate(0, 1) * 1000)
            b = multiprocessing.heap.BufferWrapper(size)
            blocks.append(b)
            if len(blocks) > maxblocks:
                i = random.randrange(maxblocks)
                del blocks[i]

        heap = multiprocessing.heap.BufferWrapper._heap
        all = []
        occupied = 0
        for L in heap._len_to_seq.values():
            for (arena, start, stop) in L:
                all.append((heap._arenas.index(arena), start, stop, stop - start, 'free'))

        for (arena, start, stop) in heap._allocated_blocks:
            all.append((heap._arenas.index(arena), start, stop, stop - start, 'occupied'))
            occupied += stop - start

        all.sort()
        for i in range(len(all) - 1):
            (arena, start, stop) = all[i][:3]
            (narena, nstart, nstop) = all[(i + 1)][:3]
            self.assertTrue(arena != narena and nstart == 0 or stop == nstart)


try:
    from ctypes import Structure, Value, copy, c_int, c_double
except ImportError:
    Structure = object
    c_int = c_double = None

class _Foo(Structure):
    __module__ = __name__
    _fields_ = [('x', c_int), ('y', c_double)]


class _TestSharedCTypes(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', )

    def _double(self, x, y, foo, arr, string):
        x.value *= 2
        y.value *= 2
        foo.x *= 2
        foo.y *= 2
        string.value *= 2
        for i in range(len(arr)):
            arr[i] *= 2

    def test_sharedctypes(self, lock=False):
        if c_int is None:
            return
        x = Value('i', 7, lock=lock)
        y = Value(ctypes.c_double, 1.0 / 3.0, lock=lock)
        foo = Value(_Foo, 3, 2, lock=lock)
        arr = Array('d', range(10), lock=lock)
        string = Array('c', 20, lock=lock)
        string.value = 'hello'
        p = self.Process(target=self._double, args=(x, y, foo, arr, string))
        p.start()
        p.join()
        self.assertEqual(x.value, 14)
        self.assertAlmostEqual(y.value, 2.0 / 3.0)
        self.assertEqual(foo.x, 6)
        self.assertAlmostEqual(foo.y, 4.0)
        for i in range(10):
            self.assertAlmostEqual(arr[i], i * 2)

        self.assertEqual(string.value, latin('hellohello'))
        return

    def test_synchronize(self):
        self.test_sharedctypes(lock=True)

    def test_copy(self):
        if c_int is None:
            return
        foo = _Foo(2, 5.0)
        bar = copy(foo)
        foo.x = 0
        foo.y = 0
        self.assertEqual(bar.x, 2)
        self.assertAlmostEqual(bar.y, 5.0)
        return


class _TestFinalize(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', )

    def _test_finalize(self, conn):

        class Foo(object):
            __module__ = __name__

        a = Foo()
        util.Finalize(a, conn.send, args=('a', ))
        del a
        b = Foo()
        close_b = util.Finalize(b, conn.send, args=('b', ))
        close_b()
        close_b()
        del b
        c = Foo()
        util.Finalize(c, conn.send, args=('c', ))
        d10 = Foo()
        util.Finalize(d10, conn.send, args=('d10', ), exitpriority=1)
        d01 = Foo()
        util.Finalize(d01, conn.send, args=('d01', ), exitpriority=0)
        d02 = Foo()
        util.Finalize(d02, conn.send, args=('d02', ), exitpriority=0)
        d03 = Foo()
        util.Finalize(d03, conn.send, args=('d03', ), exitpriority=0)
        util.Finalize(None, conn.send, args=('e', ), exitpriority=-10)
        util.Finalize(None, conn.send, args=('STOP', ), exitpriority=-100)
        util._exit_function()
        conn.close()
        os._exit(0)
        return

    def test_finalize(self):
        (conn, child_conn) = self.Pipe()
        p = self.Process(target=self._test_finalize, args=(child_conn,))
        p.start()
        p.join()
        result = [ obj for obj in iter(conn.recv, 'STOP') ]
        self.assertEqual(result, ['a', 'b', 'd10', 'd03', 'd02', 'd01', 'e'])


class _TestImportStar(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', )

    def test_import(self):
        modules = ('multiprocessing', 'multiprocessing.connection', 'multiprocessing.heap',
                   'multiprocessing.managers', 'multiprocessing.pool', 'multiprocessing.process',
                   'multiprocessing.reduction', 'multiprocessing.sharedctypes', 'multiprocessing.synchronize',
                   'multiprocessing.util')
        for name in modules:
            __import__(name)
            mod = sys.modules[name]
            for attr in getattr(mod, '__all__', ()):
                self.assertTrue(hasattr(mod, attr), '%r does not have attribute %r' % (mod, attr))


class _TestLogging(BaseTestCase):
    __module__ = __name__
    ALLOWED_TYPES = ('processes', )

    def test_enable_logging(self):
        logger = multiprocessing.get_logger()
        logger.setLevel(util.SUBWARNING)
        self.assertTrue(logger is not None)
        logger.debug('this will not be printed')
        logger.info('nor will this')
        logger.setLevel(LOG_LEVEL)
        return

    def _test_level(self, conn):
        logger = multiprocessing.get_logger()
        conn.send(logger.getEffectiveLevel())

    def test_level(self):
        LEVEL1 = 32
        LEVEL2 = 37
        logger = multiprocessing.get_logger()
        root_logger = logging.getLogger()
        root_level = root_logger.level
        (reader, writer) = multiprocessing.Pipe(duplex=False)
        logger.setLevel(LEVEL1)
        self.Process(target=self._test_level, args=(writer,)).start()
        self.assertEqual(LEVEL1, reader.recv())
        logger.setLevel(logging.NOTSET)
        root_logger.setLevel(LEVEL2)
        self.Process(target=self._test_level, args=(writer,)).start()
        self.assertEqual(LEVEL2, reader.recv())
        root_logger.setLevel(root_level)
        logger.setLevel(level=LOG_LEVEL)


class TestInvalidHandle(unittest.TestCase):
    __module__ = __name__

    def test_invalid_handles(self):
        if WIN32:
            return
        conn = _multiprocessing.Connection(44977608)
        self.assertRaises(IOError, conn.poll)
        self.assertRaises(IOError, _multiprocessing.Connection, -1)


def get_attributes(Source, names):
    d = {}
    for name in names:
        obj = getattr(Source, name)
        if type(obj) == type(get_attributes):
            obj = staticmethod(obj)
        d[name] = obj

    return d


def create_test_cases(Mixin, type):
    result = {}
    glob = globals()
    Type = type[0].upper() + type[1:]
    for name in glob.keys():
        if name.startswith('_Test'):
            base = glob[name]
            if type in base.ALLOWED_TYPES:
                newname = 'With' + Type + name[1:]

                class Temp(base, unittest.TestCase, Mixin):
                    __module__ = __name__

                result[newname] = Temp
                Temp.__name__ = newname
                Temp.__module__ = Mixin.__module__

    return result


class ProcessesMixin(object):
    __module__ = __name__
    TYPE = 'processes'
    Process = multiprocessing.Process
    locals().update(get_attributes(multiprocessing, ('Queue', 'Lock', 'RLock', 'Semaphore',
                                                     'BoundedSemaphore', 'Condition',
                                                     'Event', 'Value', 'Array', 'RawValue',
                                                     'RawArray', 'current_process',
                                                     'active_children', 'Pipe', 'connection',
                                                     'JoinableQueue')))


testcases_processes = create_test_cases(ProcessesMixin, type='processes')
globals().update(testcases_processes)

class ManagerMixin(object):
    __module__ = __name__
    TYPE = 'manager'
    Process = multiprocessing.Process
    manager = object.__new__(multiprocessing.managers.SyncManager)
    locals().update(get_attributes(manager, ('Queue', 'Lock', 'RLock', 'Semaphore',
                                             'BoundedSemaphore', 'Condition', 'Event',
                                             'Value', 'Array', 'list', 'dict', 'Namespace',
                                             'JoinableQueue')))


testcases_manager = create_test_cases(ManagerMixin, type='manager')
globals().update(testcases_manager)

class ThreadsMixin(object):
    __module__ = __name__
    TYPE = 'threads'
    Process = multiprocessing.dummy.Process
    locals().update(get_attributes(multiprocessing.dummy, ('Queue', 'Lock', 'RLock',
                                                           'Semaphore', 'BoundedSemaphore',
                                                           'Condition', 'Event',
                                                           'Value', 'Array', 'current_process',
                                                           'active_children', 'Pipe',
                                                           'connection', 'dict',
                                                           'list', 'Namespace', 'JoinableQueue')))


testcases_threads = create_test_cases(ThreadsMixin, type='threads')
globals().update(testcases_threads)

class OtherTest(unittest.TestCase):
    __module__ = __name__

    def test_deliver_challenge_auth_failure(self):

        class _FakeConnection(object):
            __module__ = __name__

            def recv_bytes(self, size):
                return 'something bogus'

            def send_bytes(self, data):
                pass

        self.assertRaises(multiprocessing.AuthenticationError, multiprocessing.connection.deliver_challenge, _FakeConnection(), 'abc')

    def test_answer_challenge_auth_failure(self):

        class _FakeConnection(object):
            __module__ = __name__

            def __init__(self):
                self.count = 0

            def recv_bytes(self, size):
                self.count += 1
                if self.count == 1:
                    return multiprocessing.connection.CHALLENGE
                elif self.count == 2:
                    return 'something bogus'
                return ''

            def send_bytes(self, data):
                pass

        self.assertRaises(multiprocessing.AuthenticationError, multiprocessing.connection.answer_challenge, _FakeConnection(), 'abc')


testcases_other = [
 OtherTest, TestInvalidHandle]

def test_main(run=None):
    if sys.platform.startswith('linux'):
        try:
            lock = multiprocessing.RLock()
        except OSError:
            from test.test_support import TestSkipped
            raise TestSkipped('OSError raises on RLock creation, see issue 3111!')

    if run is None:
        from test.test_support import run_unittest as run
    util.get_temp_dir()
    multiprocessing.get_logger().setLevel(LOG_LEVEL)
    ProcessesMixin.pool = multiprocessing.Pool(4)
    ThreadsMixin.pool = multiprocessing.dummy.Pool(4)
    ManagerMixin.manager.__init__()
    ManagerMixin.manager.start()
    ManagerMixin.pool = ManagerMixin.manager.Pool(4)
    testcases = sorted(testcases_processes.values(), key=lambda tc: tc.__name__) + sorted(testcases_threads.values(), key=lambda tc: tc.__name__) + sorted(testcases_manager.values(), key=lambda tc: tc.__name__) + testcases_other
    loadTestsFromTestCase = unittest.defaultTestLoader.loadTestsFromTestCase
    suite = unittest.TestSuite((loadTestsFromTestCase(tc) for tc in testcases))
    run(suite)
    ThreadsMixin.pool.terminate()
    ProcessesMixin.pool.terminate()
    ManagerMixin.pool.terminate()
    ManagerMixin.manager.shutdown()
    del ProcessesMixin.pool
    del ThreadsMixin.pool
    del ManagerMixin.pool
    return


def main():
    test_main(unittest.TextTestRunner(verbosity=2).run)


if __name__ == '__main__':
    main()