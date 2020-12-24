# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/executors/local_executor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 8904 bytes
__doc__ = '\nLocalExecutor runs tasks by spawning processes in a controlled fashion in different\nmodes. Given that BaseExecutor has the option to receive a `parallelism` parameter to\nlimit the number of process spawned, when this parameter is `0` the number of processes\nthat LocalExecutor can spawn is unlimited.\n\nThe following strategies are implemented:\n1. Unlimited Parallelism (self.parallelism == 0): In this strategy, LocalExecutor will\nspawn a process every time `execute_async` is called, that is, every task submitted to the\nLocalExecutor will be executed in its own process. Once the task is executed and the\nresult stored in the `result_queue`, the process terminates. There is no need for a\n`task_queue` in this approach, since as soon as a task is received a new process will be\nallocated to the task. Processes used in this strategy are of class LocalWorker.\n\n2. Limited Parallelism (self.parallelism > 0): In this strategy, the LocalExecutor spawns\nthe number of processes equal to the value of `self.parallelism` at `start` time,\nusing a `task_queue` to coordinate the ingestion of tasks and the work distribution among\nthe workers, which will take a task as soon as they are ready. During the lifecycle of\nthe LocalExecutor, the worker processes are running waiting for tasks, once the\nLocalExecutor receives the call to shutdown the executor a poison token is sent to the\nworkers to terminate them. Processes used in this strategy are of class QueuedLocalWorker.\n\nArguably, `SequentialExecutor` could be thought as a LocalExecutor with limited\nparallelism of just 1 worker, i.e. `self.parallelism = 1`.\nThis option could lead to the unification of the executor implementations, running\nlocally, into just one `LocalExecutor` with multiple modes.\n'
import multiprocessing, subprocess
from builtins import range
from queue import Empty
from airflow.executors.base_executor import BaseExecutor
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.state import State

class LocalWorker(multiprocessing.Process, LoggingMixin):
    """LocalWorker"""

    def __init__(self, result_queue):
        super(LocalWorker, self).__init__()
        self.daemon = True
        self.result_queue = result_queue
        self.key = None
        self.command = None

    def execute_work(self, key, command):
        """
        Executes command received and stores result state in queue.
        :param key: the key to identify the TI
        :type key: tuple(dag_id, task_id, execution_date)
        :param command: the command to execute
        :type command: str
        """
        if key is None:
            return
        self.log.info('%s running %s', self.__class__.__name__, command)
        try:
            subprocess.check_call(command, close_fds=True)
            state = State.SUCCESS
        except subprocess.CalledProcessError as e:
            state = State.FAILED
            self.log.error('Failed to execute task %s.', str(e))

        self.result_queue.put((key, state))

    def run(self):
        self.execute_work(self.key, self.command)


class QueuedLocalWorker(LocalWorker):
    """QueuedLocalWorker"""

    def __init__(self, task_queue, result_queue):
        super(QueuedLocalWorker, self).__init__(result_queue=result_queue)
        self.task_queue = task_queue

    def run(self):
        while True:
            key, command = self.task_queue.get()
            try:
                if key is None:
                    break
                self.execute_work(key, command)
            finally:
                self.task_queue.task_done()


class LocalExecutor(BaseExecutor):
    """LocalExecutor"""

    class _UnlimitedParallelism(object):
        """LocalExecutor._UnlimitedParallelism"""

        def __init__(self, executor):
            """
            :param executor: the executor instance to implement.
            :type executor: LocalExecutor
            """
            self.executor = executor

        def start(self):
            self.executor.workers_used = 0
            self.executor.workers_active = 0

        def execute_async(self, key, command):
            """
            :param key: the key to identify the TI
            :type key: tuple(dag_id, task_id, execution_date)
            :param command: the command to execute
            :type command: str
            """
            local_worker = LocalWorker(self.executor.result_queue)
            local_worker.key = key
            local_worker.command = command
            self.executor.workers_used += 1
            self.executor.workers_active += 1
            local_worker.start()

        def sync(self):
            while not self.executor.result_queue.empty():
                results = self.executor.result_queue.get()
                (self.executor.change_state)(*results)
                self.executor.workers_active -= 1

        def end(self):
            while self.executor.workers_active > 0:
                self.executor.sync()

    class _LimitedParallelism(object):
        """LocalExecutor._LimitedParallelism"""

        def __init__(self, executor):
            self.executor = executor

        def start(self):
            self.queue = self.executor.manager.Queue()
            self.executor.workers = [QueuedLocalWorker(self.queue, self.executor.result_queue) for _ in range(self.executor.parallelism)]
            self.executor.workers_used = len(self.executor.workers)
            for w in self.executor.workers:
                w.start()

        def execute_async(self, key, command):
            """
            :param key: the key to identify the TI
            :type key: tuple(dag_id, task_id, execution_date)
            :param command: the command to execute
            :type command: str
            """
            self.queue.put((key, command))

        def sync(self):
            while True:
                try:
                    results = self.executor.result_queue.get_nowait()
                    try:
                        (self.executor.change_state)(*results)
                    finally:
                        self.executor.result_queue.task_done()

                except Empty:
                    break

        def end(self):
            for _ in self.executor.workers:
                self.queue.put((None, None))

            self.queue.join()
            self.executor.sync()

    def start(self):
        self.manager = multiprocessing.Manager()
        self.result_queue = self.manager.Queue()
        self.workers = []
        self.workers_used = 0
        self.workers_active = 0
        self.impl = LocalExecutor._UnlimitedParallelism(self) if self.parallelism == 0 else LocalExecutor._LimitedParallelism(self)
        self.impl.start()

    def execute_async(self, key, command, queue=None, executor_config=None):
        self.impl.execute_async(key=key, command=command)

    def sync(self):
        self.impl.sync()

    def end(self):
        self.impl.end()
        self.manager.shutdown()