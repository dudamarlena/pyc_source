# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/pyjznet/threadpool.py
# Compiled at: 2014-12-11 22:22:36
from __future__ import print_function
import threading, time
from Queue import Queue

class Executor(object):

    def start(self):
        pass


class TaskPool(object):
    """TODO: concurrent queue"""

    def __init__(self):
        self._queue = Queue()

    def push(self, task):
        self._queue.put(task)

    def poll(self):
        if self._queue.qsize() > 0:
            try:
                return self._queue.get_nowait()
            except Exception as e:
                return

        else:
            return
        return

    def is_empty(self):
        return self._queue.qsize() < 1

    def available(self):
        return self._queue.qsize() > 0


class TaskThread(threading.Thread):

    def __init__(self, task_pool):
        threading.Thread.__init__(self)
        self._task_pool = task_pool

    def run(self):
        while True:
            task = self._task_pool.poll()
            if task is not None:
                task()
            time.sleep(0.05)

        return


class FixedThreadsExecutor(Executor):
    """TODO: check thread status and create new thread if some died"""

    def __init__(self, thread_count):
        self._thread_count = thread_count if thread_count > 0 else 1
        self._threads = []
        self._task_pool = TaskPool()

    def _init_threads(self):
        for i in range(self._thread_count):
            t = TaskThread(self._task_pool)
            self._threads.append(t)
            t.start()

    def start(self):
        self._init_threads()

    def submit(self, task):
        self._task_pool.push(task)