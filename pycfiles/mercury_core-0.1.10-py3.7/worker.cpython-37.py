# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/task_managers/base/worker.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 1467 bytes
import logging, time
log = logging.getLogger(__name__)

class Worker(object):
    __doc__ = 'Worker executing tasks'

    def __init__(self, task_handler, maximum_requests, maximum_age, handler_args, handler_kwargs):
        """Create a new Worker to execute tasks.

        :param task_handler: Task handler to fetch and execute tasks.
        :param maximum_requests: Maximum number of tasks this worker can
            execute.
        :param maximum_age: Maximum age of the worker.
        """
        self.maximum_requests = maximum_requests
        self.maximum_age = maximum_age
        self.birth = None
        self.kill_signal = None
        self.handled_tasks = 0
        self.task = task_handler(*handler_args, **handler_kwargs)

    def start(self):
        """Start the worker.

        The worker fetches and executes tasks as long as its maximum number
        of tasks is not reached.
        """
        self.birth = time.time()
        while self.handled_tasks < self.maximum_requests:
            if self.kill_signal:
                log.info('Shutting down... I served my masters well: %s tasks ,lived %s seconds' % (
                 self.handled_tasks,
                 time.time() - self.birth))
                break
            task = self.task.fetch()
            if not task:
                continue
            self.task.execute()
            self.handled_tasks += 1