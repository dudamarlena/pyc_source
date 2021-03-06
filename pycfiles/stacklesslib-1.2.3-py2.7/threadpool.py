# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\threadpool.py
# Compiled at: 2017-12-11 20:12:50
"""
Threadpool classes.  These are used when we want to dispatch work to happen on "real" threads.
"""
import collections, threading
from . import locks, main
from .util import tasklet_call
if hasattr(threading, 'real_threading'):
    _realthreading = threading.real_threading
    _RealThread = threading.real_threading.Thread
else:
    _realthreading = threading
    _RealThread = threading.Thread

class DummyThreadPool(object):
    """
    A dummy threadpool which always starts a new thread for each request
    """

    def __init__(self, stack_size=None):
        self.stack_size = stack_size

    def shutdown(self, wait=True):
        pass

    def start_thread(self, target):
        stack_size = self.stack_size
        if stack_size is not None:
            prev_stacksize = _realthreading.stack_size()
            _realthreading.stack_size(stack_size)
        try:
            thread = _RealThread(target=target)
            thread.start()
            return thread
        finally:
            if stack_size is not None:
                _realthreading.stack_size(prev_stacksize)

        return

    def submit(self, job):
        self.start_thread(job)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.shutdown()


class SimpleThreadPool(DummyThreadPool):

    def __init__(self, n_threads=1, stack_size=None):
        super(SimpleThreadPool, self).__init__(stack_size)
        self.threads_max = n_threads
        self.threads_n = 0
        self.threads_executing = 0
        self.cond = _realthreading.Condition()
        self.queue = collections.deque()

    def shutdown(self, wait=True):
        with self.cond:
            self.threads_max = 0
            self.cond.notify_all()
            if wait:
                while self.threads_n:
                    self.cond.wait()

    def submit(self, job):
        with self.cond:
            ready = self.threads_n - self.threads_executing
            if not ready and self.threads_n < self.threads_max:
                self.threads_n += 1
                try:
                    self.start_thread(self._threadfunc)
                except:
                    self.threads_n -= 1
                    raise

            self.queue.append(job)
            self.cond.notify()

    def _threadfunc(self):

        def predicate():
            return self.threads_n > self.threads_max or self.queue

        with self.cond:
            try:
                while True:
                    while not predicate():
                        self.cond.wait()

                    if self.threads_n > self.threads_max:
                        return
                    job = self.queue.popleft()
                    self.threads_executing += 1
                    try:
                        with locks.released(self.cond):
                            job()
                    finally:
                        self.threads_executing -= 1
                        job = None

            finally:
                self.threads_n -= 1
                self.cond.notify()

        return


def call_on_thread(function, args=(), kwargs={}, stack_size=None, pool=None, timeout=None, on_abandoned=None):
    """Run the given function on a different thread and return the result
       This function blocks on a channel until the result is available.
       Ideal for performing OS type tasks, such as saving files or compressing
    """
    if not pool:
        pool = DummyThreadPool(stack_size)

    def wrapped():
        try:
            return function(*args, **kwargs)
        finally:
            main.mainloop.interrupt_wait()

    def dispatcher(function):
        pool.submit(function)

    return tasklet_call(wrapped, dispatcher=dispatcher, timeout=timeout, on_abandoned=on_abandoned)