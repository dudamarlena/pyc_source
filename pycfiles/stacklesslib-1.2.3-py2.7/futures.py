# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\futures.py
# Compiled at: 2017-12-11 20:12:50
import sys, traceback, collections, stackless, itertools
from .errors import TimeoutError, CancelledError
from . import util, threadpool
from .util import atomic
from weakref import WeakSet
from . import wait as _waitmodule

class ExecutorBase(object):
    """Base class for TaskFactories"""

    def submit(self, fn, *args, **kwargs):
        return self.submit_future(Future(), (fn, args, kwargs))

    def submit_args(self, fn, args=(), kwargs={}):
        return self.submit_future(Future(), (fn, args, kwargs))

    def map(self, fn, *iterables, **kwds):
        timeout = kwds.pop('timeout', None)
        if kwds:
            raise TypeError
        t = util.Timeouts(timeout)
        kw = {}
        futures = [ self.submit_future(Future(), (fn, args, kw)) for args in zip(*iterables) ]

        def generator():
            for f in futures:
                with t.timeout():
                    result = f.result()
                yield result

        return generator()

    @staticmethod
    def execute_future(future, job):
        fn, args, kwargs = job
        future.execute(fn, args, kwargs)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.shutdown(True)

    def shutdown(self, wait=True):
        pass


class ThreadPoolExecutorBase(ExecutorBase):
    """Runs futures on a given threadpool"""

    def __init__(self, pool):
        self.pool = pool

    def submit_future(self, future, job):

        def job_function():
            self.execute_future(future, job)

        self.pool.submit(job_function)
        return future

    def shutdown(self, wait=True):
        self.pool.shutdown(wait)


class NullExecutor(ExecutorBase):
    """This executor will not do anything"""

    def submit_future(self, future, job):
        return future


class DirectExecutor(ExecutorBase):
    """This executor just runs the job straight away."""

    def submit_future(self, future, job):
        self.execute_future(future, job)
        return future


class SimpleTaskletExecutor(ExecutorBase):
    """Runs the job as a new tasklet on this thread"""

    def submit_future(self, future, job):
        self.start_tasklet(self.execute_future, (future, job))
        return future

    def start_tasklet(self, func, args):
        """Start execution of a tasklet and return it. Can be overridden."""
        return stackless.tasklet(func)(*args)


class ImmediateTaskletExecutor(SimpleTaskletExecutor):
    """Runs the job as a new tasklet and switches to it directly"""

    def submit_future(self, future, job):
        self.start_tasklet(self.execute_future, (future, job)).run()
        return future


null_executor = NullExecutor()
direct_executor = DirectExecutor()
thread_executor = ThreadPoolExecutorBase(threadpool.DummyThreadPool())
tasklet_executor = SimpleTaskletExecutor()
immediate_tasklet_executor = ImmediateTaskletExecutor()

class WaitingExecutorMixIn(object):
    """This mixin keeps track of issued futures so that we can wait for them all wholesale"""

    def __init__(self, *args, **kwargs):
        self.futures = WeakSet()

    def submit_future(self, future, job):
        if self.futures is None:
            raise RuntimeError
        future = super(WaitingExecutorMixIn, self).submit_future(future, job)
        self.futures.add(future)
        return future

    def shutdown(self, wait=True):
        if self.futures:
            futures = set(self.futures)
            if wait:
                _wait(futures)
            self.futures = None
        super(WaitingExecutorMixIn, self).shutdown(wait)
        return


class BoundedExecutorMixIn(object):
    """This mixin allows the caller to put a limit on the number active futures"""

    def __init__(self, max_workers=None):
        self.max_workers = max_workers
        self.n_workers = 0
        self.jobs = collections.deque()

    def submit_future(self, future, job):
        with atomic():
            if self.max_workers == None or self.n_workers < self.max_workers:
                self.n_workers += 1
                try:
                    future = super(BoundedExecutorMixIn, self).submit_future(future, job)
                except:
                    self.n_workers -= 1
                    raise

            else:
                future = Future()
                self.jobs.append((future, job))
            return future
        return

    def execute_future(self, future, job):
        try:
            super(BoundedExecutorMixIn, self).execute_future(future, job)
        finally:
            self.n_workers -= 1
            self.pump()

    def pump(self):
        with atomic():
            if self.jobs and self.n_workers < self.max_workers:
                future, job = self.jobs.popleft()
                self.submit_future(future, job)


class ThreadPoolExecutor(WaitingExecutorMixIn, ThreadPoolExecutorBase):

    def __init__(self, max_workers=None):
        WaitingExecutorMixIn.__init__(self)
        pool = threadpool.SimpleThreadPool(n_threads=max_workers)
        ThreadPoolExecutorBase.__init__(self, pool)


class TaskletExecutor(WaitingExecutorMixIn, BoundedExecutorMixIn, SimpleTaskletExecutor):

    def __init__(self, max_workers=None):
        WaitingExecutorMixIn.__init__(self, max_workers)
        BoundedExecutorMixIn.__init__(self)
        SimpleTaskletExecutor.__init__(self)


PENDING = 'PENDING'
RUNNING = 'RUNNING'
CANCELLED = 'CANCELLED'
CANCELLED_AND_NOTIFIED = 'CANCELLED_AND_NOTIFIED'
FINISHED = 'FINISHED'

class Future(_waitmodule.WaitSite):
    """A tasklet based future object"""

    def __init__(self):
        super(Future, self).__init__()
        self.state = PENDING
        self._result = None
        self.tasklet = None
        return

    def execute(self, fn, args=(), kwargs={}):
        """Execute job and future on the current tasklet"""
        try:
            try:
                if self.attach():
                    self.set_result(fn(*args, **kwargs))
            except TaskletExit as e:
                self.set_cancelled(e.args)
            except BaseException:
                self.set_exception(*sys.exc_info())

        except:
            print >> sys.stderr, 'Unhandled exception in ', callable
            traceback.print_exc()

    def attach(self):
        with atomic():
            assert self.state in (PENDING, CANCELLED)
            if self.state is PENDING:
                self.state = RUNNING
                self.tasklet = stackless.getcurrent()
                return True

    def cancel(self, args=()):
        with atomic():
            if self.tasklet:
                self.tasklet.raise_exception(TaskletExit, *args)
            self.set_cancelled(args)
        return True

    def cancelled(self):
        return self.state is CANCELLED

    def running(self):
        return self.state is RUNNING

    def done(self):
        """True if the task has completed execution"""
        return self.state in (CANCELLED, FINISHED)

    def result(self, timeout=None):
        """Wait for the execution of the task and return its result or raise
           its exception.
        """
        self.wait(timeout)
        success, result = self._result
        if success:
            return result
        if result:
            if self.state is FINISHED:
                raise result[0], result[1], result[2]
            assert self.state is CANCELLED
            raise CancelledError(*result[1])

    def exception(self, timeout=None):
        """Wait for the execution of the task and return its result or raise
           its exception.
        """
        self.wait(timeout)
        success, result = self._result
        if success or self.state is FINISHED:
            return result
        if not self.state is CANCELLED:
            raise AssertionError
            raise CancelledError(*result[1])

    def wait(self, timeout=None):
        """Wait until the future has finished or been cancelled"""
        with atomic():
            if not self.done():
                _waitmodule.swait(self, timeout)

    def waitsite_signalled(self):
        return self._result

    def set_result(self, result):
        with atomic():
            if self._result is None:
                assert self.state == RUNNING
                self._result = (True, result)
                self.state = FINISHED
                self.waitsite_signal()
            else:
                assert self.state == CANCELLED
        return

    def set_exception(self, exc, val=None, tb=None):
        with atomic():
            if self._result is None:
                assert self.state == RUNNING
                if val is None:
                    val = exc
                    exc = type(exc)
                elif isinstance(val, tuple):
                    val = exc(*val)
                self._result = (
                 False, (exc, val, tb))
                self.state = FINISHED
                self.waitsite_signal()
            else:
                assert self.state == CANCELLED
        return

    def set_cancelled(self, args=()):
        with atomic():
            if self._result is None:
                assert self.state in (RUNNING, PENDING)
                self._result = (False, (None, args))
                self.state = CANCELLED
                self.waitsite_signal()
        return


FIRST_COMPLETED = 0
FIRST_EXCEPTION = 1
ALL_COMPLETED = 2

def wait(fs, timeout=None, return_when=ALL_COMPLETED):
    done = set()
    fs1, fs2 = itertools.tee(fs, 2)
    finished = False
    for f in fs1:
        if f.done():
            done.add(f)
            if return_when == FIRST_COMPLETED:
                finished = True
            elif return_when == FIRST_EXCEPTION:
                if not f.cancelled() and f.exception():
                    finished = True

    not_done = set(fs2) - done
    if finished:
        return (done, not_done)
    for f in _waitmodule.iwait_no_raise(not_done, timeout):
        done.add(f)
        if return_when == FIRST_COMPLETED:
            break
        elif return_when == FIRST_EXCEPTION:
            if not f.cancelled() and f.exception():
                break

    not_done -= done
    return (done, not_done)


_wait = wait
as_completed = _waitmodule.iwait

def all_results(fs, timeout=None):
    with util.timeout(timeout):
        return [ f.result() for f in fs ]


def any_result(fs, timeout=None):
    for i in as_completed(fs, timeout):
        return i.result()