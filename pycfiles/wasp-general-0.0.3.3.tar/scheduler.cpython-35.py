# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/task/scheduler/scheduler.py
# Compiled at: 2017-10-17 13:58:54
# Size of source mod 2**32: 22020 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from datetime import timezone
from threading import Event
from wasp_general.verify import verify_type, verify_value, verify_subclass
from wasp_general.thread import WCriticalResource
from wasp_general.datetime import utc_datetime
from wasp_general.task.scheduler.proto import WScheduleTask, WRunningRecordRegistryProto, WSchedulerServiceProto
from wasp_general.task.scheduler.proto import WScheduleRecord, WTaskSourceProto
from wasp_general.task.thread import WPollingThreadTask

class WSchedulerWatchdog(WCriticalResource, WPollingThreadTask):
    __doc__ = ' Class that is looking for execution process of scheduled task. Each scheduled task has its own\n\twatchdog. Watchdog that will un-register stopped task from registry of running tasks\n\t'
    __thread_polling_timeout__ = WPollingThreadTask.__thread_polling_timeout__ / 2
    __scheduled_task_startup_timeout__ = WPollingThreadTask.__thread_polling_timeout__ / 2
    __lock_acquiring_timeout__ = 5
    __thread_name_prefix__ = 'TaskScheduler-Watchdog-'

    @classmethod
    @verify_type('paranoid', record=WScheduleRecord)
    def create(cls, record, registry):
        """ Core method for watchdog creation. Derived classes may redefine this method in order to change
                watchdog creation process

                :param record: schedule record that is ready to be executed
                :param registry: registry that is created this watchdog and registry that must be notified of           scheduled task stopping
                :return:
                """
        return cls(record, registry)

    @verify_type(record=WScheduleRecord)
    def __init__(self, record, registry):
        """ Create new watch dog.

                :param record: schedule record that is ready to be executed
                :param registry: registry that is created this watch dog and registry that must be notified of          scheduled task stopping

                note: :class:`.WRunningRecordRegistry` is using :meth:`.WSchedulerWatchdog.create` method for watch
                dog creation
                """
        WCriticalResource.__init__(self)
        WPollingThreadTask.__init__(self, thread_name=self.__thread_name_prefix__ + str(record.task_uid()))
        if isinstance(registry, WRunningRecordRegistry) is False:
            raise TypeError('Invalid registry type')
        self._WSchedulerWatchdog__record = record
        self._WSchedulerWatchdog__registry = registry
        self._WSchedulerWatchdog__task = None

    def record(self):
        """ Return scheduler record

                :return: WScheduleRecord
                """
        return self._WSchedulerWatchdog__record

    def registry(self):
        """ Return parent registry

                :return: WRunningRecordRegistry
                """
        return self._WSchedulerWatchdog__registry

    def start(self):
        """ Start scheduled task and start watching

                :return: None
                """
        self._WSchedulerWatchdog__dog_started()
        WPollingThreadTask.start(self)

    def thread_started(self):
        """ Start watchdog thread function

                :return: None
                """
        self._WSchedulerWatchdog__thread_started()
        WPollingThreadTask.thread_started(self)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def __dog_started(self):
        """ Prepare watchdog for scheduled task starting

                :return: None
                """
        if self._WSchedulerWatchdog__task is not None:
            raise RuntimeError('Unable to start task. In order to start a new task - at first stop it')
        self._WSchedulerWatchdog__task = self.record().task()
        if isinstance(self._WSchedulerWatchdog__task, WScheduleTask) is False:
            task_class = self._WSchedulerWatchdog__task.__class__.__qualname__
            raise RuntimeError('Unable to start unknown type of task: %s' % task_class)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def __thread_started(self):
        """ Start a scheduled task

                :return: None
                """
        if self._WSchedulerWatchdog__task is None:
            raise RuntimeError('Unable to start thread without "start" method call')
        self._WSchedulerWatchdog__task.start()
        self._WSchedulerWatchdog__task.start_event().wait(self.__scheduled_task_startup_timeout__)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def _polling_iteration(self):
        """ Poll for scheduled task stop events

                :return: None
                """
        if self._WSchedulerWatchdog__task is None:
            self.ready_event().set()
        elif self._WSchedulerWatchdog__task.check_events() is True:
            self.ready_event().set()
            self.registry().task_finished(self)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def thread_stopped(self):
        """ Stop scheduled task beacuse of watchdog stop

                :return: None
                """
        if self._WSchedulerWatchdog__task is not None:
            if self._WSchedulerWatchdog__task.stop_event().is_set() is False:
                self._WSchedulerWatchdog__task.stop()
            self._WSchedulerWatchdog__task = None


class WRunningRecordRegistry(WCriticalResource, WRunningRecordRegistryProto, WPollingThreadTask):
    __doc__ = ' Registry of started scheduled records. Has :meth:`.WRunningRecordRegistry.cleanup_event` event that is set\n\twhen any of running scheduled task stopped. This event starts process of internal clean up (descriptors that\n\twere created for the record - will be removed)\n\t'
    __thread_polling_timeout__ = WPollingThreadTask.__thread_polling_timeout__ / 4
    __watchdog_startup_timeout__ = WSchedulerWatchdog.__thread_polling_timeout__
    __lock_acquiring_timeout__ = 5
    __thread_name__ = 'SchedulerRegistry'

    @verify_subclass(watchdog_cls=(WSchedulerWatchdog, None))
    @verify_type(thread_name_suffix=(str, None))
    def __init__(self, watchdog_cls=None, thread_name_suffix=None):
        """ Create new registry

                :param watchdog_cls: watchdog that should be used (:class:`.WSchedulerWatchdog` by default)
                :param thread_name_suffix: suffix to thread name
                """
        WCriticalResource.__init__(self)
        WRunningRecordRegistryProto.__init__(self)
        thread_name = self.__thread_name__
        if thread_name_suffix is not None:
            thread_name += thread_name_suffix
        WPollingThreadTask.__init__(self, thread_name=thread_name)
        self._WRunningRecordRegistry__running_registry = []
        self._WRunningRecordRegistry__done_registry = []
        self._WRunningRecordRegistry__cleanup_event = Event()
        self._WRunningRecordRegistry__watchdog_cls = watchdog_cls if watchdog_cls is not None else WSchedulerWatchdog

    def cleanup_event(self):
        """ Return "cleanup" event

                :return: Event
                """
        return self._WRunningRecordRegistry__cleanup_event

    def watchdog_class(self):
        """ Return watchdog class that is used by this registry

                :return: WSchedulerWatchdog class or subclass
                """
        return self._WRunningRecordRegistry__watchdog_cls

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    @verify_type('paranoid', record=WScheduleRecord)
    def exec(self, record):
        """ Start the given schedule record (no time checks are made by this method, task will be started as is)

                :param record: schedule record to start

                :return: None
                """
        watchdog_cls = self.watchdog_class()
        watchdog = watchdog_cls.create(record, self)
        watchdog.start()
        watchdog.start_event().wait(self.__watchdog_startup_timeout__)
        self._WRunningRecordRegistry__running_registry.append(watchdog)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def running_records(self):
        """ Return schedule records that are running at the moment

                :return: tuple of WScheduleRecord
                """
        return tuple([x.record() for x in self._WRunningRecordRegistry__running_registry])

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def __len__(self):
        """ Return number of running records

                :return: int
                """
        return len(self._WRunningRecordRegistry__running_registry)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    @verify_type(watchdog=WSchedulerWatchdog)
    def task_finished(self, watchdog):
        """ Handle/process scheduled task stop

                :param watchdog: watchdog of task that was stopped

                :return: None
                """
        if watchdog in self._WRunningRecordRegistry__running_registry:
            self._WRunningRecordRegistry__running_registry.remove(watchdog)
            self._WRunningRecordRegistry__done_registry.append(watchdog)
            self.cleanup_event().set()

    def _polling_iteration(self):
        """ Poll for cleanup event

                :return: None
                """
        if self.cleanup_event().is_set() is True:
            self.cleanup()

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def cleanup(self):
        """ Do cleanup (stop and remove watchdogs that are no longer needed)

                :return: None
                """
        for task in self._WRunningRecordRegistry__done_registry:
            task.stop()

        self._WRunningRecordRegistry__done_registry.clear()
        self.cleanup_event().clear()

    def thread_stopped(self):
        """ Handle registry stop

                :return: None
                """
        self.cleanup()
        self.stop_running_tasks()

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def stop_running_tasks(self):
        """ Terminate all the running tasks

                :return: None
                """
        for task in self._WRunningRecordRegistry__running_registry:
            task.stop()

        self._WRunningRecordRegistry__running_registry.clear()


class WPostponedRecordRegistry:
    __doc__ = ' Registry for postponed records.\n\t'

    @verify_type(maximum_records=(int, None))
    @verify_value(maximum_records=lambda x: x is None or x >= 0)
    def __init__(self, maximum_records=None):
        """ Create new registry

                :param maximum_records: maximum number of tasks to postpone (no limit by default)
                """
        self._WPostponedRecordRegistry__records = []
        self._WPostponedRecordRegistry__maximum_records = maximum_records

    def maximum_records(self):
        """ Return maximum number of records to postpone

                :return: int
                """
        return self._WPostponedRecordRegistry__maximum_records

    @verify_type(record=WScheduleRecord)
    def postpone(self, record):
        """ Postpone (if required) the given task. The real action is depended on task postpone policy

                :param record: record to postpone
                :return: None
                """
        maximum_records = self.maximum_records()
        if maximum_records is not None and len(self._WPostponedRecordRegistry__records) >= maximum_records:
            record.task_dropped()
            return
        task_policy = record.policy()
        task_group_id = record.task_group_id()
        if task_policy == WScheduleRecord.PostponePolicy.wait:
            self._WPostponedRecordRegistry__postpone_record(record)
        else:
            if task_policy == WScheduleRecord.PostponePolicy.drop:
                record.task_dropped()
            else:
                if task_policy == WScheduleRecord.PostponePolicy.postpone_first:
                    if task_group_id is None:
                        self._WPostponedRecordRegistry__postpone_record(record)
                    else:
                        record_found = None
                        for previous_scheduled_record, task_index in self._WPostponedRecordRegistry__search_record(task_group_id):
                            if previous_scheduled_record.policy() != task_policy:
                                raise RuntimeError('Invalid tasks policies')
                            record_found = previous_scheduled_record
                            break

                        if record_found is not None:
                            record.task_dropped()
                        else:
                            self._WPostponedRecordRegistry__postpone_record(record)
                else:
                    if task_policy == WScheduleRecord.PostponePolicy.postpone_last:
                        if task_group_id is None:
                            self._WPostponedRecordRegistry__postpone_record(record)
                        else:
                            record_found = None
                            for previous_scheduled_record, task_index in self._WPostponedRecordRegistry__search_record(task_group_id):
                                if previous_scheduled_record.policy() != task_policy:
                                    raise RuntimeError('Invalid tasks policies')
                                record_found = task_index
                                break

                            if record_found is not None:
                                self._WPostponedRecordRegistry__records.pop(record_found).task_dropped()
                            self._WPostponedRecordRegistry__postpone_record(record)
                    else:
                        raise RuntimeError('Invalid policy spotted')

    @verify_type(task_group_id=str)
    def __search_record(self, task_group_id):
        """ Search (iterate over) for tasks with the given task id

                :param task_group_id: target id

                :return: None
                """
        for i in range(len(self._WPostponedRecordRegistry__records)):
            record = self._WPostponedRecordRegistry__records[i]
            if record.task_group_id() == task_group_id:
                yield (
                 record, i)

    @verify_type(record=WScheduleRecord)
    def __postpone_record(self, record):
        """ Save the record and trigger 'postpone' method

                :param record: record to save

                :return: None
                """
        self._WPostponedRecordRegistry__records.append(record)
        record.task_postponed()

    def has_records(self):
        """ Check if there are postponed records. True - there is at least one postpone record,
                False - otherwise

                :return: bool
                """
        return len(self._WPostponedRecordRegistry__records) > 0

    def __len__(self):
        """ Return number of postponed records

                :return: int
                """
        return len(self._WPostponedRecordRegistry__records)

    def __iter__(self):
        """ Iterate over postponed records. Once record is yield from this method, this record is removed
                from registry immediately

                :return: None
                """
        while len(self._WPostponedRecordRegistry__records) > 0:
            yield self._WPostponedRecordRegistry__records.pop(0)


class WTaskSourceRegistry:
    __doc__ = ' Registry of tasks sources. It works as a dynamic queue - every task source notify this registry when\n\tnext task should be started. And this registry fetches those tasks that is about to start. Registry is able\n\tto return schedule records from different sources at one time.\n\t'

    def __init__(self):
        """ Create new registry
                """
        self._WTaskSourceRegistry__sources = {}
        self._WTaskSourceRegistry__next_start = None
        self._WTaskSourceRegistry__next_sources = []

    @verify_type(task_source=WTaskSourceProto)
    def add_source(self, task_source):
        """ Add new tasks source

                :param task_source:

                :return: None
                """
        next_start = task_source.next_start()
        self._WTaskSourceRegistry__sources[task_source] = next_start
        self._WTaskSourceRegistry__update(task_source)

    @verify_type(task_source=(WTaskSourceProto, None))
    def update(self, task_source=None):
        """ Recheck next start of records from all the sources (or from the given one only)

                :param task_source: if defined - source to check

                :return: None
                """
        if task_source is not None:
            self._WTaskSourceRegistry__update(task_source)
        else:
            self._WTaskSourceRegistry__update_all()

    def __update_all(self):
        """ Recheck next start of records from all the sources

                :return: None
                """
        self._WTaskSourceRegistry__next_start = None
        self._WTaskSourceRegistry__next_sources = []
        for source in self._WTaskSourceRegistry__sources:
            self._WTaskSourceRegistry__update(source)

    @verify_type(task_source=WTaskSourceProto)
    def __update(self, task_source):
        """ Recheck next start of tasks from the given one only

                :param task_source: source to check

                :return: None
                """
        next_start = task_source.next_start()
        if next_start is not None:
            if next_start.tzinfo is None or next_start.tzinfo != timezone.utc:
                raise ValueError('Invalid timezone information')
            if self._WTaskSourceRegistry__next_start is None or next_start < self._WTaskSourceRegistry__next_start:
                self._WTaskSourceRegistry__next_start = next_start
                self._WTaskSourceRegistry__next_sources = [task_source]
        elif next_start == self._WTaskSourceRegistry__next_start:
            self._WTaskSourceRegistry__next_sources.append(task_source)

    def check(self):
        """ Check if there are records that are ready to start and return them if there are any

                :return: tuple of WScheduleRecord or None (if there are no tasks to start)
                """
        if self._WTaskSourceRegistry__next_start is not None:
            utc_now = utc_datetime()
            if utc_now >= self._WTaskSourceRegistry__next_start:
                result = []
                for task_source in self._WTaskSourceRegistry__next_sources:
                    records = task_source.has_records()
                    if records is not None:
                        result.extend(records)

                self._WTaskSourceRegistry__update_all()
                if len(result) > 0:
                    pass
                return tuple(result)

    def task_sources(self):
        """ Return task sources that was added to this registry

                :return: tuple of WTaskSourceProto
                """
        return tuple(self._WTaskSourceRegistry__sources.keys())


class WSchedulerService(WCriticalResource, WSchedulerServiceProto, WPollingThreadTask):
    __doc__ = ' Main scheduler service. This class unites different registries to present entire scheduler\n\t'
    __thread_polling_timeout__ = WPollingThreadTask.__thread_polling_timeout__ / 8
    __lock_acquiring_timeout__ = 5
    __default_maximum_running_records__ = 10
    __thread_name_prefix__ = 'TaskScheduler'

    @verify_type('paranoid', maximum_postponed_records=(int, None))
    @verify_value('paranoid', maximum_postponed_records=lambda x: x is None or x > 0)
    @verify_type(maximum_running_records=(int, None), running_record_registry=(WRunningRecordRegistry, None))
    @verify_type(postponed_record_registry=(WPostponedRecordRegistry, None))
    @verify_type(thread_name_suffix=(str, None))
    @verify_value(maximum_running_records=lambda x: x is None or x > 0)
    def __init__(self, maximum_running_records=None, running_record_registry=None, maximum_postponed_records=None, postponed_record_registry=None, thread_name_suffix=None):
        """ Create new scheduler

                :param maximum_running_records: number of records that are able to run simultaneously           (WSchedulerService.__default_maximum_running_records__ is used as default value)
                :param running_record_registry: registry for running records
                :param maximum_postponed_records: number of records that are able to be postponed (no limit by default)
                :param postponed_record_registry: registry for postponed records
                :param thread_name_suffix: suffix to thread name
                """
        WCriticalResource.__init__(self)
        WSchedulerServiceProto.__init__(self)
        thread_name = self.__thread_name_prefix__
        if thread_name_suffix is not None:
            thread_name += thread_name_suffix
        WPollingThreadTask.__init__(self, thread_name=thread_name)
        if maximum_postponed_records is not None and postponed_record_registry is not None:
            raise ValueError('Conflict values found. Unable to instantiate scheduler service with "maximum_postponed_tasks" and "postponed_tasks_registry" values (chose one)')
        default = lambda x, y: x if x is not None else y
        self._WSchedulerService__maximum_running_records = default(maximum_running_records, self.__class__.__default_maximum_running_records__)
        self._WSchedulerService__running_record_registry = default(running_record_registry, WRunningRecordRegistry())
        self._WSchedulerService__postponed_record_registry = WPostponedRecordRegistry(maximum_postponed_records)
        self._WSchedulerService__sources_registry = WTaskSourceRegistry()
        self._WSchedulerService__awake_at = None

    def maximum_running_records(self):
        """ Return number of tasks that are able to run simultaneously

                :return: int
                """
        return self._WSchedulerService__maximum_running_records

    def maximum_postponed_records(self):
        """ Return number of tasks that are able to be postponed

                :return: int or None (for no limit)
                """
        return self._WSchedulerService__postponed_record_registry.maximum_records()

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    @verify_type('paranoid', task_source=WTaskSourceProto)
    def add_task_source(self, task_source):
        """ Add tasks source

                :param task_source: task source to add

                :return: None
                """
        self._WSchedulerService__sources_registry.add_source(task_source)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def task_sources(self):
        """ Return task sources that was added to this scheduler

                :return: tuple of WTaskSourceProto
                """
        return self._WSchedulerService__sources_registry.task_sources()

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    @verify_type('paranoid', task_source=(WTaskSourceProto, None))
    def update(self, task_source=None):
        """ Recheck next start of tasks from all the sources (or from the given one only)

                :param task_source: if defined - source to check

                :return: None
                """
        self._WSchedulerService__sources_registry.update(task_source=task_source)

    def running_records(self):
        """ Return scheduled tasks that are running at the moment

                :return: tuple of WScheduleRecord
                """
        return self._WSchedulerService__running_record_registry.running_records()

    def records_status(self):
        """ Return number of running and postponed tasks

                :return: tuple of two ints (first - running tasks, second - postponed tasks)
                """
        return (
         len(self._WSchedulerService__running_record_registry), len(self._WSchedulerService__postponed_record_registry))

    def thread_started(self):
        """ Start required registries and start this scheduler

                :return: None
                """
        self._WSchedulerService__running_record_registry.start()
        self._WSchedulerService__running_record_registry.start_event().wait()
        WPollingThreadTask.thread_started(self)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def _polling_iteration(self):
        """ Poll for different scheduler events like: there are tasks to run, there are tasks to postpone
                there are postponed tasks that should be running

                :return: None
                """
        scheduled_tasks = self._WSchedulerService__sources_registry.check()
        has_postponed_tasks = self._WSchedulerService__postponed_record_registry.has_records()
        maximum_tasks = self.maximum_running_records()
        if scheduled_tasks is not None or has_postponed_tasks is not None:
            running_tasks = len(self._WSchedulerService__running_record_registry)
            if running_tasks >= maximum_tasks:
                pass
            if scheduled_tasks is not None:
                for task in scheduled_tasks:
                    self._WSchedulerService__postponed_record_registry.postpone(task)

        elif has_postponed_tasks is True:
            for postponed_task in self._WSchedulerService__postponed_record_registry:
                self._WSchedulerService__running_record_registry.exec(postponed_task)
                running_tasks += 1
                if running_tasks >= maximum_tasks:
                    break

        if scheduled_tasks is not None:
            for task in scheduled_tasks:
                if running_tasks >= maximum_tasks:
                    self._WSchedulerService__postponed_record_registry.postpone(task)
                else:
                    self._WSchedulerService__running_record_registry.exec(task)
                    running_tasks += 1

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def thread_stopped(self):
        """ Stop registries and this scheduler

                :return: None
                """
        self._WSchedulerService__running_record_registry.stop()