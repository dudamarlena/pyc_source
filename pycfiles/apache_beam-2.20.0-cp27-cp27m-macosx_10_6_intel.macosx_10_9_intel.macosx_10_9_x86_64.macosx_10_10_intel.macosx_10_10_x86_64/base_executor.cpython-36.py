# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/executors/base_executor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7454 bytes
from builtins import range
from collections import OrderedDict
import airflow.utils.dag_processing
from airflow import configuration
from airflow.settings import Stats
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.state import State
PARALLELISM = configuration.conf.getint('core', 'PARALLELISM')

class BaseExecutor(LoggingMixin):

    def __init__(self, parallelism=PARALLELISM):
        """
        Class to derive in order to interface with executor-type systems
        like Celery, Mesos, Yarn and the likes.

        :param parallelism: how many jobs should run at one time. Set to
            ``0`` for infinity
        :type parallelism: int
        """
        self.parallelism = parallelism
        self.queued_tasks = OrderedDict()
        self.running = {}
        self.event_buffer = {}

    def start(self):
        """
        Executors may need to get things started. For example LocalExecutor
        starts N workers.
        """
        pass

    def queue_command(self, simple_task_instance, command, priority=1, queue=None):
        key = simple_task_instance.key
        if key not in self.queued_tasks:
            if key not in self.running:
                self.log.info('Adding to queue: %s', command)
                self.queued_tasks[key] = (command, priority, queue, simple_task_instance)
        else:
            self.log.info('could not queue task %s', key)

    def queue_task_instance(self, task_instance, mark_success=False, pickle_id=None, ignore_all_deps=False, ignore_depends_on_past=False, ignore_task_deps=False, ignore_ti_state=False, pool=None, cfg_path=None):
        pool = pool or task_instance.pool
        command = task_instance.command_as_list(local=True,
          mark_success=mark_success,
          ignore_all_deps=ignore_all_deps,
          ignore_depends_on_past=ignore_depends_on_past,
          ignore_task_deps=ignore_task_deps,
          ignore_ti_state=ignore_ti_state,
          pool=pool,
          pickle_id=pickle_id,
          cfg_path=cfg_path)
        self.queue_command((airflow.utils.dag_processing.SimpleTaskInstance(task_instance)),
          command,
          priority=(task_instance.task.priority_weight_total),
          queue=(task_instance.task.queue))

    def has_task(self, task_instance):
        """
        Checks if a task is either queued or running in this executor

        :param task_instance: TaskInstance
        :return: True if the task is known to this executor
        """
        if task_instance.key in self.queued_tasks or task_instance.key in self.running:
            return True

    def sync(self):
        """
        Sync will get called periodically by the heartbeat method.
        Executors should override this to perform gather statuses.
        """
        pass

    def heartbeat(self):
        if not self.parallelism:
            open_slots = len(self.queued_tasks)
        else:
            open_slots = self.parallelism - len(self.running)
        num_running_tasks = len(self.running)
        num_queued_tasks = len(self.queued_tasks)
        self.log.debug('%s running task instances', num_running_tasks)
        self.log.debug('%s in queue', num_queued_tasks)
        self.log.debug('%s open slots', open_slots)
        Stats.gauge('executor.open_slots', open_slots)
        Stats.gauge('executor.queued_tasks', num_queued_tasks)
        Stats.gauge('executor.running_tasks', num_running_tasks)
        self.trigger_tasks(open_slots)
        self.log.debug('Calling the %s sync method', self.__class__)
        self.sync()

    def trigger_tasks(self, open_slots):
        """
        Trigger tasks

        :param open_slots: Number of open slots
        :return:
        """
        sorted_queue = sorted([(k, v) for k, v in self.queued_tasks.items()], key=(lambda x: x[1][1]),
          reverse=True)
        for i in range(min((open_slots, len(self.queued_tasks)))):
            key, (command, _, queue, simple_ti) = sorted_queue.pop(0)
            self.queued_tasks.pop(key)
            self.running[key] = command
            self.execute_async(key=key, command=command,
              queue=queue,
              executor_config=(simple_ti.executor_config))

    def change_state(self, key, state):
        self.log.debug('Changing state: %s', key)
        self.running.pop(key, None)
        self.event_buffer[key] = state

    def fail(self, key):
        self.change_state(key, State.FAILED)

    def success(self, key):
        self.change_state(key, State.SUCCESS)

    def get_event_buffer(self, dag_ids=None):
        """
        Returns and flush the event buffer. In case dag_ids is specified
        it will only return and flush events for the given dag_ids. Otherwise
        it returns and flushes all

        :param dag_ids: to dag_ids to return events for, if None returns all
        :return: a dict of events
        """
        cleared_events = dict()
        if dag_ids is None:
            cleared_events = self.event_buffer
            self.event_buffer = dict()
        else:
            for key in list(self.event_buffer.keys()):
                dag_id, _, _, _ = key
                if dag_id in dag_ids:
                    cleared_events[key] = self.event_buffer.pop(key)

        return cleared_events

    def execute_async(self, key, command, queue=None, executor_config=None):
        """
        This method will execute the command asynchronously.
        """
        raise NotImplementedError()

    def end(self):
        """
        This method is called when the caller is done submitting job and is
        wants to wait synchronously for the job submitted previously to be
        all done.
        """
        raise NotImplementedError()

    def terminate(self):
        """
        This method is called when the daemon receives a SIGTERM
        """
        raise NotImplementedError()