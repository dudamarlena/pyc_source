# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/instrumentation/metrics/structures/threadpool.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 7202 bytes
import itertools, queue, threading, weakref
from concurrent.futures import _base
from concurrent.futures import thread
from concurrent.futures.thread import ThreadPoolExecutor, _WorkItem
try:
    from concurrent.futures.thread import BrokenThreadPool
except ImportError:
    BrokenThreadPool = RuntimeError

import typing as tp
from satella.time import measure
from satella.instrumentation.metrics.metric_types import EmptyMetric, MetricLevel, CallableMetric

def _worker(executor_reference, work_queue, initializer, initargs):
    if initializer is not None:
        try:
            initializer(*initargs)
        except BaseException:
            _base.LOGGER.critical('Exception in initializer:', exc_info=True)
            executor = executor_reference()
            if executor is not None:
                executor._initializer_failed()
            return

    try:
        while True:
            work_item = work_queue.get(block=True)
            if work_item is not None:
                executor = executor_reference()
                work_item.measure.stop()
                executor.waiting_time_metric.handle(executor.metric_level, work_item.measure())
                del executor
                with measure() as (measurement):
                    work_item.run()
                executor = executor_reference()
                executor.executing_time_metric.handle(executor.metric_level, measurement())
                del work_item
                if executor is not None:
                    executor._idle_semaphore.release()
                del executor
            else:
                executor = executor_reference()
                if thread._shutdown or executor is None or executor._shutdown:
                    if executor is not None:
                        executor._shutdown = True
                    work_queue.put(None)
                    return
                del executor

    except BaseException:
        _base.LOGGER.critical('Exception in worker', exc_info=True)


class MetrifiedThreadPoolExecutor(ThreadPoolExecutor):
    __doc__ = "\n    A thread pool executor that provides execution statistics as metrics.\n\n    This class will also backport some of Python 3.8's characteristics of the thread pool executor to earlier Pythons,\n    thread name prefix, initializer, initargs and BrokenThreadPool behaviour.\n\n    :param time_spent_waiting: a metric (can be aggregate) to which times spent waiting in the queue will be deposited\n    :param time_spent_executing: a metric (can be aggregate) to which times spent executing will be deposited\n    :param waiting_tasks: a fresh CallableMetric that will be patched to yield the number of currently waiting tasks\n    :param metric_level: a level with which to log to these two metrics\n    "
    _counter = itertools.count().__next__

    def __init__(self, max_workers=None, thread_name_prefix='', initializer=None, initargs=(), time_spent_waiting=None, time_spent_executing=None, waiting_tasks=None, metric_level=MetricLevel.RUNTIME):
        super().__init__(max_workers)
        self._initializer = initializer
        self._initargs = initargs
        self._idle_semaphore = threading.Semaphore(0)
        self._broken = False
        if not hasattr(self, '_thread_name_prefix'):
            self._thread_name_prefix = thread_name_prefix or 'ThreadPoolExecutor-%d' % self._counter()
        self.waiting_time_metric = time_spent_waiting or EmptyMetric('')
        self.executing_time_metric = time_spent_executing or EmptyMetric('')
        self.metric_level = metric_level
        if waiting_tasks is not None:
            waiting_tasks.callable = lambda : self._work_queue.qsize()

    def submit(*args, **kwargs):
        if len(args) >= 2:
            self, fn, *args = args
        else:
            if not args:
                raise TypeError("descriptor 'submit' of 'ThreadPoolExecutor' object needs an argument")
            else:
                if 'fn' in kwargs:
                    fn = kwargs.pop('fn')
                    self, *args = args
                    import warnings
                    warnings.warn("Passing 'fn' as keyword argument is deprecated", DeprecationWarning,
                      stacklevel=2)
                else:
                    raise TypeError('submit expected at least 1 positional argument, got %d' % (len(args) - 1))
        with self._shutdown_lock:
            if self._broken:
                raise BrokenThreadPool(self._broken)
            else:
                if self._shutdown:
                    raise RuntimeError('cannot schedule new futures after shutdown')
                if thread._shutdown:
                    raise RuntimeError('cannot schedule new futures after interpreter shutdown')
            f = _base.Future()
            w = _WorkItem(f, fn, args, kwargs)
            w.measure = measure()
            self._work_queue.put(w)
            self._adjust_thread_count()
            return f

    def _adjust_thread_count(self):
        if self._idle_semaphore.acquire(timeout=0):
            return

        def weakref_cb(_, q=self._work_queue):
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self._thread_name_prefix or self,
             num_threads)
            t = threading.Thread(name=thread_name, target=_worker, args=(
             weakref.ref(self, weakref_cb),
             self._work_queue,
             self._initializer,
             self._initargs))
            t.daemon = True
            t.start()
            self._threads.add(t)
            thread._threads_queues[t] = self._work_queue

    def _initializer_failed(self):
        with self._shutdown_lock:
            self._broken = 'A thread initializer failed, the thread pool is not usable anymore'
            while 1:
                try:
                    work_item = self._work_queue.get_nowait()
                except queue.Empty:
                    break

                if work_item is not None:
                    work_item.future.set_exception(BrokenThreadPool(self._broken))