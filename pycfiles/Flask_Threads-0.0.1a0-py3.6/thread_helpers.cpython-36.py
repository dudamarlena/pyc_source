# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flaskthreads/thread_helpers.py
# Compiled at: 2019-09-04 09:30:11
# Size of source mod 2**32: 6452 bytes
"""Implements ThreadPoolExecutor with flask AppContext."""
__author__ = 'Alexey Minakov (a@spb.host)'
import atexit
from concurrent.futures import _base
import itertools, queue, threading, weakref, os
from flask import _app_ctx_stack
from flask import has_app_context
APP_CONTEXT_ERROR = 'Running outside of Flask AppContext.'
_threads_queues = weakref.WeakKeyDictionary()
_shutdown = False

def _python_exit():
    global _shutdown
    _shutdown = True
    items = list(_threads_queues.items())
    for t, q in items:
        q.put(None)

    for t, q in items:
        t.join()


atexit.register(_python_exit)

class _WorkItemWithContext(object):

    def __init__(self, app_ctx, future, fn, args, kwargs):
        self.app_ctx = app_ctx
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if not self.future.set_running_or_notify_cancel():
            return
        try:
            try:
                self.app_ctx.push()
                result = (self.fn)(*self.args, **self.kwargs)
            except BaseException as exc:
                self.future.set_exception(exc)
                self = None
            else:
                self.future.set_result(result)
        finally:
            self.app_ctx.pop()


def _worker(executor_reference, work_queue):
    try:
        while True:
            work_item = work_queue.get(block=True)
            if work_item is not None:
                work_item.run()
                del work_item
            else:
                executor = executor_reference()
                if _shutdown or executor is None or executor._shutdown:
                    work_queue.put(None)
                    return
                del executor

    except BaseException:
        _base.LOGGER.critical('Exception in worker', exc_info=True)


class ThreadPoolWithAppContextExecutor(_base.Executor):
    _counter = itertools.count().__next__

    def __init__(self, max_workers=None, thread_name_prefix=''):
        """Initializes a new ThreadPoolExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
        """
        if max_workers is None:
            max_workers = (os.cpu_count() or 1) * 5
        else:
            if max_workers <= 0:
                raise ValueError('max_workers must be greater than 0')
            raise has_app_context() or RuntimeError(APP_CONTEXT_ERROR)
        self._app_ctx = _app_ctx_stack.top
        self._max_workers = max_workers
        self._work_queue = queue.Queue()
        self._threads = set()
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._thread_name_prefix = thread_name_prefix or 'ThreadPoolExecutor-%d' % self._counter()

    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            f = _base.Future()
            w = _WorkItemWithContext(self._app_ctx, f, fn, args, kwargs)
            self._work_queue.put(w)
            self._adjust_thread_count()
            return f

    submit.__doc__ = _base.Executor.submit.__doc__

    def _adjust_thread_count(self):

        def weakref_cb(_, q=self._work_queue):
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self._thread_name_prefix or self,
             num_threads)
            t = threading.Thread(name=thread_name, target=_worker, args=(
             weakref.ref(self, weakref_cb),
             self._work_queue))
            t.daemon = True
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue

    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown = True
            self._work_queue.put(None)
        if wait:
            for t in self._threads:
                t.join()

    shutdown.__doc__ = _base.Executor.shutdown.__doc__


class AppContextThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        if not has_app_context():
            raise RuntimeError(APP_CONTEXT_ERROR)
        self.app_ctx = _app_ctx_stack.top

    def run(self):
        try:
            self.app_ctx.push()
            super().run()
        finally:
            self.app_ctx.pop()