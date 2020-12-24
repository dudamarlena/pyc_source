# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/task/scheduler/proto.py
# Compiled at: 2017-10-19 09:31:36
# Size of source mod 2**32: 8528 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import uuid
from abc import ABCMeta, abstractmethod
from enum import Enum
from datetime import datetime, timezone
from wasp_general.verify import verify_type, verify_value
from wasp_general.task.thread import WThreadTask

class WScheduleTask(WThreadTask):
    __doc__ = ' Class represent task that may run by a scheduler\n\tEvery schedule task must be able:\n\t\t- to be stopped at any time\n\t\t- to return its status (running or stopped)\n\t\t- to notify when task end (thread event)\n\n\tnote: derived classes must implement :meth:`.WThreadTask.thread_started` and :meth:`.WThreadTask.thread_stopped`\n\tmethods in order to be instantiable\n\n\tEach task instance has "unique" identifier\n\t'
    __thread_name_prefix__ = 'ScheduledTask-'

    @verify_type('paranoid', thread_join_timeout=(int, float, None))
    def __init__(self, thread_join_timeout=None):
        """ Create new task

                :param thread_join_timeout: same as thread_join_timeout in :meth:`.WThreadTask.__init__` method
                """
        self._WScheduleTask__uid = self.generate_uid()
        WThreadTask.__init__(self, thread_name=self.__thread_name_prefix__ + str(self._WScheduleTask__uid), join_on_stop=True, ready_to_stop=True, thread_join_timeout=thread_join_timeout)

    def uid(self):
        return self._WScheduleTask__uid

    @classmethod
    def generate_uid(cls):
        """ Return "random" "unique" identifier

                :return: UUID
                """
        return uuid.uuid4()


class WScheduleRecord:
    __doc__ = ' This class specifies how :class:`.WScheduleTask` should run. It should be treated as scheduler record, that\n\tmay not have execution time.\n\n\t:class:`.WScheduleRecord` has a policy, that describes what scheduler should do if it can not run this task\n\tat the specified moment. This policy is a recommendation for a scheduler and a scheduler can omit it if\n\t(for example) a scheduler queue is full. In any case, if this task is dropped (skipped) or postponed (moved to\n\ta queue of waiting tasks) correlated callback is called. "on_drop" callback is called for skipped tasks\n\t(it invokes via :meth:`.WScheduleRecord.task_dropped` method) and "on_wait" for postponed tasks (via\n\t:meth:`.WScheduleRecord.task_postponed` method)\n\n\tnote: It is important that tasks with the same id (task_group_id) have the same postpone policy. If they do not\n\thave the same policy, then exception may be raised. No pre-checks are made to resolve this, because of\n\tunpredictable logic of different tasks from different sources\n\t'

    class PostponePolicy(Enum):
        __doc__ = " Specifies what should be with this task if a scheduler won't be able to run it (like if the\n\t\tscheduler limit of running tasks is reached).\n\t\t"
        wait = 1
        drop = 2
        postpone_first = 3
        postpone_last = 4

    @verify_type(task=WScheduleTask, task_group_id=(str, None))
    @verify_value(on_drop=lambda x: x is None or callable(x), on_wait=lambda x: x is None or callable(x))
    def __init__(self, task, policy=None, task_group_id=None, on_drop=None, on_wait=None):
        """ Create new schedule record

                :param task: task to run
                :param policy: postpone policy
                :param task_group_id: identifier that groups different scheduler records and single postpone policy
                :param on_drop: callback, that must be called if this task is skipped
                :param on_wait: callback, that must be called if this task is postponed
                """
        if policy is not None:
            if isinstance(policy, WScheduleRecord.PostponePolicy) is False:
                raise TypeError('Invalid policy object type')
        self._WScheduleRecord__task = task
        self._WScheduleRecord__policy = policy if policy is not None else WScheduleRecord.PostponePolicy.wait
        self._WScheduleRecord__task_group_id = task_group_id
        self._WScheduleRecord__on_drop = on_drop
        self._WScheduleRecord__on_wait = on_wait

    def task(self):
        """ Return task that should be run

                :return: WScheduleTask
                """
        return self._WScheduleRecord__task

    def task_uid(self):
        """ Shortcut for self.task().uid()
                """
        return self.task().uid()

    def policy(self):
        """ Return postpone policy

                :return: WScheduleRecord.PostponePolicy
                """
        return self._WScheduleRecord__policy

    def task_group_id(self):
        """ Return task id

                :return: str or None

                see :meth:`.WScheduleRecord.__init__`
                """
        return self._WScheduleRecord__task_group_id

    def task_postponed(self):
        """ Call a "on_wait" callback. This method is executed by a scheduler when it postpone this task

                :return: None
                """
        if self._WScheduleRecord__on_wait is not None:
            return self._WScheduleRecord__on_wait()

    def task_dropped(self):
        """ Call a "on_drop" callback. This method is executed by a scheduler when it skip this task

                :return: None
                """
        if self._WScheduleRecord__on_drop is not None:
            return self._WScheduleRecord__on_drop()


class WTaskSourceProto(metaclass=ABCMeta):
    __doc__ = " Prototype for scheduler record generator. :class:`.WSchedulerServiceProto` doesn't have scheduler as set of\n\trecords. Instead, a service uses this class as scheduler records holder and checks if it is time to execute\n\tthem.\n\t"

    @abstractmethod
    def has_records(self):
        """ Return records that should be run at the moment.

                :return: tuple of WScheduleRecord (tuple with one element at least) or None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def next_start(self):
        """ Return datetime when the next task should be executed.

                :return: datetime in UTC timezone
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def tasks_planned(self):
        """ Return number of records (tasks) that are planned to run

                :return: int
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def scheduler_service(self):
        """ Return associated scheduler service

                :return: WSchedulerServiceProto or None
                """
        raise NotImplementedError('This method is abstract')


class WRunningRecordRegistryProto(metaclass=ABCMeta):
    __doc__ = ' This class describes a registry of running tasks. It executes a scheduler record\n\t(:class:`.WScheduleRecord`), creates and store the related records (:class:`.WScheduleRecord`), and watches\n\tthat these tasks are running\n\t'

    @abstractmethod
    @verify_type(schedule_record=WScheduleRecord)
    def exec(self, schedule_record):
        """ Execute the given scheduler record (no time checks are made at this method, task executes as is)

                :param schedule_record: record to execute

                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def running_records(self):
        """ Return tuple of running tasks

                :return: tuple of WScheduleRecord
                """
        raise NotImplementedError('This method is abstract')


class WSchedulerServiceProto(metaclass=ABCMeta):
    __doc__ = ' Represent a scheduler. A core of wasp_general.task.scheduler module\n\t'

    @abstractmethod
    @verify_type(task_source=(WTaskSourceProto, None))
    def update(self, task_source=None):
        """ Update task sources information about next start. Update information for the specified source
                or for all of them

                :param task_source: if it is specified - then update information for this source only

                This method implementation must be thread-safe as different threads (different task source, different
                registries) may modify scheduler internal state.
                :return:
                """
        raise NotImplementedError('This method is abstract')