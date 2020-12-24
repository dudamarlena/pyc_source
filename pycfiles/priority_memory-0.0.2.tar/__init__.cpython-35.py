# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PriorityThreadPoolExecutor/__init__.py
# Compiled at: 2019-03-08 02:56:51
# Size of source mod 2**32: 5646 bytes
import sys, queue, random, atexit, weakref, threading
from concurrent.futures.thread import ThreadPoolExecutor, _base, _WorkItem, _python_exit, _threads_queues
NULL_ENTRY = (
 sys.maxsize, _WorkItem(None, None, (), {}))
_shutdown = False

def python_exit():
    """

    Cleanup before system exit

    """
    global _shutdown
    _shutdown = True
    items = list(_threads_queues.items())
    for t, q in items:
        q.put(NULL_ENTRY)

    for t, q in items:
        t.join()


atexit.unregister(_python_exit)
atexit.register(python_exit)

def _worker(executor_reference, work_queue):
    """

    Worker

    :param executor_reference: executor function
    :type executor_reference: callable
    :param work_queue: work queue
    :type work_queue: queue.PriorityQueue

    """
    try:
        while 1:
            work_item = work_queue.get(block=True)
            if work_item[0] != sys.maxsize:
                work_item = work_item[1]
                work_item.run()
                del work_item
                continue
                executor = executor_reference()
                if _shutdown or executor is None or executor._shutdown:
                    work_queue.put(NULL_ENTRY)
                    return
                del executor

    except BaseException:
        _base.LOGGER.critical('Exception in worker', exc_info=True)


class PriorityThreadPoolExecutor(ThreadPoolExecutor):
    """PriorityThreadPoolExecutor"""

    def __init__(self, max_workers=None):
        """

        Initializes a new PriorityThreadPoolExecutor instance

        :param max_workers: the maximum number of threads that can be used to execute the given calls
        :type max_workers: int

        """
        super(PriorityThreadPoolExecutor, self).__init__(max_workers)
        self._work_queue = queue.PriorityQueue()

    def submit(self, fn, *args, **kwargs):
        """

        Sending the function to the execution queue

        :param fn: function being executed
        :type fn: callable
        :param args: function's positional arguments
        :param kwargs: function's keywords arguments
        :return: future instance
        :rtype: _base.Future

        Added keyword:

        - priority (integer later sys.maxsize)

        """
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            priority = kwargs.get('priority', random.randint(0, sys.maxsize - 1))
            if 'priority' in kwargs:
                del kwargs['priority']
            f = _base.Future()
            w = _WorkItem(f, fn, args, kwargs)
            self._work_queue.put((priority, w))
            self._adjust_thread_count()
            return f

    def _adjust_thread_count(self):
        """

        Attempt to start a new thread

        """

        def weak_ref_cb(_, q=self._work_queue):
            q.put(NULL_ENTRY)

        if len(self._threads) < self._max_workers:
            t = threading.Thread(target=_worker, args=(
             weakref.ref(self, weak_ref_cb),
             self._work_queue))
            t.daemon = True
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue

    def shutdown(self, wait=True):
        """

        Pool shutdown

        :param wait: if True wait for all threads to complete
        :type wait: bool

        """
        with self._shutdown_lock:
            self._shutdown = True
            self._work_queue.put(NULL_ENTRY)
        if wait:
            for t in self._threads:
                t.join()