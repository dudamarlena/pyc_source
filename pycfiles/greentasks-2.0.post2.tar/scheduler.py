# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/andrean/dev/repos/librarian/greentasks/greentasks/scheduler.py
# Compiled at: 2016-09-15 11:02:41
import multiprocessing
from gevent import spawn_later
from gevent.queue import Queue, Empty as QueueEmpty
from .exceptions import InvalidTaskError
from .tasks import PackagedTask, Task

class TaskScheduler(object):
    """
    A very simple task scheduler built on top of gevent.

    Allows scheduling of periodic, one-off delayed and one-off ordered tasks.

    Periodic tasks will run repeatedly after their execution in the specified
    amount of time.

    One-off delayed tasks are executed only once after the specified delay has
    passed.

    One-off ordered tasks are put into a queue and are executed in the same
    order they were scheduled. The queue is processed in fixed intervals which
    is specified by the ``consume_tasks_delay`` parameter in the constructor of
    the scheduler. In each wakeup, exactly one task will be processed.

    Failing tasks are retried if the task implementation allows to do so.

    The ``multiprocessing`` flag controls whether tasks will be executed in
    all processes, or just the main one.
    """
    packaged_task_class = PackagedTask
    base_task_class = Task
    InvalidTaskError = InvalidTaskError

    def __init__(self, consume_tasks_delay=1, multiprocessing=True):
        self._queue = Queue()
        self._consume_tasks_delay = consume_tasks_delay
        self._async(self._consume_tasks_delay, self._consume)
        self._multiprocessing = multiprocessing

    def _async(self, delay, fn, *args, **kwargs):
        """
        Schedule a function with the passed in parameters to be executed
        asynchronously by gevent.
        """
        return spawn_later(delay, fn, *args, **kwargs)

    def _execute(self, packaged_task):
        """
        Delegate execution of ``packaged_task`` to py:meth:`~PackagedTask.run`,
        which handles the invocation of appropriate callbacks and errbacks and
        the resolving of the future object.

        The returned ``task_info`` structure is checked to see if the task has
        to be retried or rescheduled (in case of periodic tasks) and does so if
        any of the two is needed.
        """
        if not self._multiprocessing:
            current_proc = multiprocessing.current_process()
            if type(current_proc) is multiprocessing.Process:
                return
        task_info = packaged_task.run()
        delay = task_info.get('delay', None)
        if delay is not None:
            self._async(delay, self._execute, packaged_task)
        return

    def _consume(self):
        """
        Execute a single task from the queue, and reschedule consuming of the
        queue in py:attr:`~TaskScheduler._consume_tasks_delay` seconds.
        """
        try:
            try:
                packaged_task = self._queue.get_nowait()
            except QueueEmpty:
                pass
            else:
                self._execute(packaged_task)

        finally:
            self._async(self._consume_tasks_delay, self._consume)

    def schedule(self, task, args=None, kwargs=None, callback=None, errback=None, delay=None, periodic=False, retry_delay=None, max_retries=0):
        """
        Schedule a task for execution and return a packaged task object for it.

        ``task`` may be any callable and it should contain the task logic. If
        ``task`` is a subclass of py:class:`Task`, the parameters ``delay``,
        ``periodic``, ``retry_delay`` and ``max_retries`` will be ignored in
        favor of the ones defined on the class itself.

        ``args`` and ``kwargs`` contain the positional and keyword arguments to
        be passed to ``task``.

        ``callback`` and ``errback`` are callables to be invoked with the
        return value of ``task`` or the exception object raised if ``task``
        fails, respectively.

        ``delay`` is the amount of seconds in which ``task`` should be
        executed. If ``delay`` is not specified, the task will be put into a
        queue and honor the existing order of scheduled tasks, being executed
        only after the tasks scheduled prior to it are finished. If ``delay``
        is specified, the task will be scheduled to run NOT BEFORE the
        specified amount of seconds, not following any particular order, but
        there is no guarantee that it will run in exactly that time.

        The ``periodic`` flag has effect only on tasks which specified a
        ``delay``, and those tasks will be rescheduled automatically for the
        same ``delay`` every time after they are executed (unless ``task`` is
        a subclass of py:class:`Task` and it implemented custom rules to
        calculate the value of ``delay``.

        ``retry_delay`` is the amount of seconds in which ``task`` can be
        retried, in case it fails. The value of ``None`` prohibits retries.

        ``max_retires`` is the maximum number of retry attempts for a failing
        task.
        """
        packaged_task = self.packaged_task_class(task, args=args, kwargs=kwargs, callback=callback, errback=errback, delay=delay, periodic=periodic, retry_delay=retry_delay, max_retries=max_retries)
        task_instance = packaged_task.instantiate()
        if not task_instance:
            raise InvalidTaskError('Task cannot be instantiated.')
        start_delay = task_instance.get_start_delay()
        if start_delay is None:
            self._queue.put(packaged_task)
            return packaged_task
        else:
            self._async(start_delay, self._execute, packaged_task)
            return packaged_task