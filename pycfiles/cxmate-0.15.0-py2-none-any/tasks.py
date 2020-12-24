# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tasks.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: tasks.py'
from collections import deque
from threading import Thread, Lock, Event
from time import sleep

class Task(object):
    """A task object represents some unit of work to be done.

    :param method: The actual method (function) to execute.
    :type method: function
    :param args: Arguments to pass to the named method to run.
    :type args: list
    """

    def __init__(self, method, *args, **kwargs):
        """Default constructor for the Task class."""
        self.status = 'Queued'
        self.result = None
        self.error = None
        self._method = method
        self._args = args
        self._kwargs = kwargs
        self._finished = Event()
        return

    def join(self):
        """Wait for this task to finish."""
        self._finished.wait()

    def is_alive(self):
        """Return true if this task hasn't been finished.

        :returns: Whether or not the task is still alive.
        :rtype: boolean

        """
        return not self._finished.is_set()

    def _run(self):
        """Execute this task. Should only be called by TaskWorker."""
        self.status = 'In Progress'
        try:
            self.result = self._method(*self._args, **self._kwargs)
            self.status = 'Completed'
        except Exception as err:
            self.error = err
            self.status = 'Failed'

        self._finished.set()


class TaskQueue(object):
    """A task queue, consisting of a queue and a number of workers.

    :param threads: Number of threads to create (if needed).
    :type threads: integer
    :param delay: Time to wait between
    """

    def __init__(self, threads=48, delay=0):
        """Default constructor for the TaskQueue class."""
        self.threads = threads
        self.delay = delay
        self._lock = Lock()
        self._queue = deque()
        self._workers = 0

    def put(self, method, *args, **kwargs):
        """Add a task to the task queue, and spawn a worker if we're not full.

        :param method: Named method to run.
        :type method: string
        :param args: Arguments to pass to the named method to run.
        :type args: list

        :returns: A Task that will be executed by a worker at a later time.
        :rtype: Task

        """
        self._lock.acquire()
        task = Task(method, *args, **kwargs)
        self._queue.append(task)
        if self._workers < self.threads:
            TaskWorker(task_queue=self, delay=self.delay)
            self._workers += 1
        self._lock.release()
        return task

    def get(self):
        """
        Get a task from the task queue. Mainly used by workers.

        :returns: A Task object that hasn't been executed yet.
        :rtype: Task

        :raises IndexError: If there are no tasks in the queue.

        """
        self._lock.acquire()
        try:
            return self._queue.popleft()
        finally:
            self._lock.release()

    def _remove_worker(self):
        """Decrement the worker count. Should only be used by TaskWorker."""
        self._lock.acquire()
        self._workers -= 1
        self._lock.release()


class TaskWorker(Thread):
    """A worker thread that runs tasks from a TaskQueue.

    :param task_queue: Task queue to get tasks from.
    :type task_queue: TaskQueue
    :param delay: Time to wait in-between execution.

    """

    def __init__(self, task_queue, delay=0):
        super(TaskWorker, self).__init__()
        self.daemon = True
        self._task_queue = task_queue
        self._delay = delay
        self.start()

    def run(self):
        """Repeatedly get tasks from the TaskQueue and execute them."""
        try:
            while True:
                sleep(self._delay)
                task = self._task_queue.get()
                task._run()

        except Exception:
            self._task_queue._remove_worker()


DEFAULT_TASK_QUEUE = TaskQueue()