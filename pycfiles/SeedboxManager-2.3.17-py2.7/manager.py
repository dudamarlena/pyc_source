# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/process/manager.py
# Compiled at: 2015-06-14 13:30:57
"""Manages the execution of tasks using parallel processes."""
import logging, concurrent.futures as conc_futures
from oslo_config import cfg
LOG = logging.getLogger(__name__)
cfg.CONF.import_group('process', 'seedbox.options')

class TaskManager(object):
    """Creates a pool of processes

    Executes the supplied tasks using the process pool.
    """

    def __init__(self):
        self.executor = conc_futures.ProcessPoolExecutor(cfg.CONF.process.max_processes)
        self.tasks = []

    def add_tasks(self, tasks):
        """Adds tasks to list of tasks to be executed.

        :param tasks: a task or list of tasks to add to the list of tasks to
                      execute
        """
        if isinstance(tasks, list):
            self.tasks.extend(tasks)
        else:
            self.tasks.append(tasks)

    def run(self):
        """Executes the list of tasks.

        :return: the result/output from each tasks
        :rtype: list
        """
        futures_task = [ self.executor.submit(task) for task in self.tasks ]
        del self.tasks[:]
        results = []
        for future in conc_futures.as_completed(futures_task):
            results.extend(future.result())

        return results

    def shutdown(self):
        """Shuts down the process pool to free up resources."""
        self.executor.shutdown()