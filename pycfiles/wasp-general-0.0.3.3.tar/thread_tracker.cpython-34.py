# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/task/thread_tracker.py
# Compiled at: 2017-10-17 14:47:16
# Size of source mod 2**32: 20162 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from abc import ABCMeta, abstractmethod
import traceback
from enum import Enum
from wasp_general.verify import verify_type, verify_value
from wasp_general.task.thread import WThreadTask
from wasp_general.task.scheduler.proto import WScheduleTask, WScheduleRecord
from wasp_general.thread import WCriticalResource
from wasp_general.datetime import utc_datetime

class WTrackerEvents(Enum):
    __doc__ = ' Possible tracking events\n\t'
    start = 1
    stop = 2
    termination = 3
    exception = 4
    wait = 5
    drop = 6


class WThreadTrackerInfoStorageProto(metaclass=ABCMeta):
    __doc__ = ' Prototype for a storage that keeps thread task events like start event, normal stop, termination, raised\n\tunhandled exceptions) or scheduler events\n\t'

    @abstractmethod
    @verify_type(task=WThreadTask, event_details=(str, None))
    def register_start(self, task, event_details=None):
        """ Store start event

                :param task: task that is starting
                :param event_details: (optional) event details - any kind of data related to the given task and start           event

                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(task=WThreadTask, event_details=(str, None))
    def register_stop(self, task, event_details=None):
        """ Store stop event

                :param task: task that stopped
                :param event_details: (optional) event details - any kind of data related to the given task and stop            event

                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(task=WThreadTask, event_details=(str, None))
    def register_termination(self, task, event_details=None):
        """ Store termination event

                :param task: task that was terminated
                :param event_details: (optional) event details - any kind of data related to the given task and                 termination event

                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(task=WThreadTask, raised_exception=Exception, exception_details=str, event_details=(str, None))
    def register_exception(self, task, raised_exception, exception_details, event_details=None):
        """ Store exception event

                :param task: task that was terminated by unhandled exception
                :param raised_exception: unhandled exception
                :param exception_details: any kind of data related to the raised exception
                :param event_details: (optional) event details - any kind of data related to the given task and
                exception event

                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(task=WThreadTask, event_details=(str, None))
    def register_wait(self, task, event_details=None):
        """ Store event of task postponing (this event is used in a scheduler classes)

                :param task: task that was postponed
                :param event_details: (optional) event details - any kind of data related to the given task and
                postponing event

                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(task=WThreadTask, event_details=(str, None))
    def register_drop(self, task, event_details=None):
        """ Store event of task drop (this event is used in a scheduler classes)

                :param task: task that was dropped
                :param event_details: (optional) event details - any kind of data related to the given task and
                event of task drop

                :return: None
                """
        raise NotImplementedError('This method is abstract')


class WThreadTracker(WThreadTask):
    __doc__ = ' Threaded task that may register its events (start event, normal stop fact, task termination fact,\n\tunhandled exceptions)\n\n\t:note: Since there is an extra work that should be done, this class may be inappropriate for low-latency\n\tsituation. Also, registering events should be done quickly because of this task joining timeout.\n\t'

    @verify_type('paranoid', thread_name=(str, None), join_on_stop=bool, thread_join_timeout=(int, float, None))
    @verify_type(tracker_storage=(WThreadTrackerInfoStorageProto, None), track_start=bool, track_stop=bool)
    @verify_type(track_termination=bool, track_exception=bool)
    def __init__(self, tracker_storage=None, thread_name=None, join_on_stop=True, thread_join_timeout=None, track_start=True, track_stop=True, track_termination=True, track_exception=True):
        """ Create new tracker

                :param tracker_storage: storage that is used for registering eventd
                :param thread_name: same as 'thread_name' in :meth:`.WThreadTask.__init__`
                :param join_on_stop: same as 'join_on_stop' in :meth:`.WThreadTask.__init__`
                :param thread_join_timeout: same as 'thread_join_timeout' in :meth:`.WThreadTask.__init__`
                :param track_start: whether to register start event of this task or not
                :param track_stop: whether to register stop event of this task or not
                :param track_termination: whether to register termination event of this task or not
                :param track_exception: whether to register unhandled exception event or not
                """
        WThreadTask.__init__(self, thread_name=thread_name, join_on_stop=join_on_stop, ready_to_stop=True, thread_join_timeout=thread_join_timeout)
        self._WThreadTracker__tracker = tracker_storage
        self._WThreadTracker__track_start = track_start
        self._WThreadTracker__track_stop = track_stop
        self._WThreadTracker__track_termination = track_termination
        self._WThreadTracker__track_exception = track_exception

    def tracker_storage(self):
        """ Return linked storage

                :return: WThreadTrackerInfoStorageProto or None
                """
        return self._WThreadTracker__tracker

    def track_start(self):
        """ Return True if this task is tracking "start-event" otherwise - False

                :return: bool
                """
        return self._WThreadTracker__track_start

    def track_stop(self):
        """ Return True if this task is tracking "stop-event" otherwise - False

                :return: bool
                """
        return self._WThreadTracker__track_stop

    def track_termination(self):
        """ Return True if this task is tracking "termination-event" otherwise - False

                :return: bool
                """
        return self._WThreadTracker__track_termination

    def track_exception(self):
        """ Return True if this task is tracking unhandled exception event otherwise - False

                :return: bool
                """
        return self._WThreadTracker__track_exception

    @verify_type(event=WTrackerEvents)
    def event_details(self, event):
        """ Return task details that should be registered with a tracker storage

                :param event: source event that requested details

                :return: str or None
                """
        pass

    def start(self):
        """ :meth:`.WThreadTask.start` implementation. Register (if required) start event by a tracker storage

                :return: None
                """
        tracker = self.tracker_storage()
        if tracker is not None:
            if self.track_start() is True:
                details = self.event_details(WTrackerEvents.start)
                tracker.register_start(self, event_details=details)
        WThreadTask.start(self)

    def thread_stopped(self):
        """ :meth:`.WThreadTask.thread_stopped` implementation. Register (if required) stop and termination
                event by a tracker storage

                :return: None
                """
        tracker = self.tracker_storage()
        if tracker is not None:
            try:
                if self.ready_event().is_set() is True:
                    if self.track_stop() is True:
                        details = self.event_details(WTrackerEvents.stop)
                        tracker.register_stop(self, event_details=details)
                elif self.exception_event().is_set() is False:
                    if self.track_termination() is True:
                        details = self.event_details(WTrackerEvents.termination)
                        tracker.register_termination(self, event_details=details)
            except Exception as e:
                self.thread_tracker_exception(e)

    @verify_type(raised_exception=Exception)
    def thread_exception(self, raised_exception):
        """ :meth:`.WThreadTask.thread_exception` implementation. Register (if required) unhandled exception
                event by a tracker storage

                :param raised_exception: unhandled exception

                :return: None
                """
        tracker = self.tracker_storage()
        if tracker is not None:
            try:
                if self.track_exception() is True:
                    details = self.event_details(WTrackerEvents.exception)
                    tracker.register_exception(self, raised_exception, traceback.format_exc(), event_details=details)
            except Exception as e:
                self.thread_tracker_exception(e)

    @verify_type(raised_exception=Exception)
    def thread_tracker_exception(self, raised_exception):
        """ Method is called whenever an exception is raised during registering a event

                :param raised_exception: raised exception

                :return: None
                """
        print('Thread tracker execution was stopped by the exception. Exception: %s' % str(raised_exception))
        print('Traceback:')
        print(traceback.format_exc())


class WSimpleTrackerStorage(WCriticalResource, WThreadTrackerInfoStorageProto):
    __doc__ = ' Simple :class:`.WThreadTrackerInfoStorageProto` implementation which stores events in a operation memory\n\t'
    __critical_section_timeout__ = 1

    class Record:
        __doc__ = ' General record of single event\n\t\t'

        @verify_type(record_type=WTrackerEvents, thread_task=WThreadTask)
        @verify_type(event_details=(str, None))
        def __init__(self, record_type, thread_task, event_details=None):
            """ Create new record

                        :param record_type: tracking event
                        :param thread_task: original task
                        :param event_details: task details
                        """
            self.record_type = record_type
            self.thread_task = thread_task
            self.event_details = event_details
            self.registered_at = utc_datetime()

    class ExceptionRecord(Record):
        __doc__ = ' Record for unhandled exception\n\t\t'

        @verify_type('paranoid', task=WThreadTask, event_details=(str, None))
        @verify_type(exception=Exception, exception_details=str)
        def __init__(self, task, exception, exception_details, event_details=None):
            WSimpleTrackerStorage.Record.__init__(self, WTrackerEvents.exception, task, event_details=event_details)
            self.exception = exception
            self.exception_details = exception_details

    @verify_type(records_limit=(int, None), record_start=bool, record_stop=bool, record_termination=bool)
    @verify_type(record_exception=bool, record_wait=bool, record_drop=bool)
    def __init__(self, records_limit=None, record_start=True, record_stop=True, record_termination=True, record_exception=True, record_wait=True, record_drop=True):
        """ Create new storage

                :param records_limit: number of records to keep (if record limit is reached - new record will
                overwrite the oldest one)
                :param record_start:  whether to keep start events or not
                :param record_stop: whether to keep normal stop events or not
                :param record_termination: whether to keep termination stop events or not
                :param record_exception: whether to keep unhandled exceptions events or not
                :param record_wait: whether to keep postponing events or not
                :param record_drop: whether to keep drop events or not
                """
        WCriticalResource.__init__(self)
        WThreadTrackerInfoStorageProto.__init__(self)
        self._WSimpleTrackerStorage__limit = records_limit
        self._WSimpleTrackerStorage__registry = []
        self._WSimpleTrackerStorage__record_start = record_start
        self._WSimpleTrackerStorage__record_stop = record_stop
        self._WSimpleTrackerStorage__record_termination = record_termination
        self._WSimpleTrackerStorage__record_exception = record_exception
        self._WSimpleTrackerStorage__record_wait = record_wait
        self._WSimpleTrackerStorage__record_drop = record_drop

    def record_limit(self):
        """ Return maximum number of records to keep

                :return: int or None (for no limit)
                """
        return self._WSimpleTrackerStorage__limit

    def record_start(self):
        """ Return True if this storage is saving start events, otherwise - False

                :return: bool
                """
        return self._WSimpleTrackerStorage__record_start

    def record_stop(self):
        """ Return True if this storage is saving normal stop events, otherwise - False

                :return: bool
                """
        return self._WSimpleTrackerStorage__record_stop

    def record_termination(self):
        """ Return True if this storage is saving termination stop events, otherwise - False

                :return: bool
                """
        return self._WSimpleTrackerStorage__record_termination

    def record_exception(self):
        """ Return True if this storage is saving unhandled exceptions events, otherwise - False

                :return: bool
                """
        return self._WSimpleTrackerStorage__record_exception

    def record_wait(self):
        """ Return True if this storage is saving postponing events, otherwise - False

                :return: bool
                """
        return self._WSimpleTrackerStorage__record_wait

    def record_drop(self):
        """ Return True if this storage is saving dropping events, otherwise - False

                :return: bool
                """
        return self._WSimpleTrackerStorage__record_drop

    def register_start(self, task, event_details=None):
        """ :meth:`.WSimpleTrackerStorage.register_start` method implementation
                """
        if self.record_start() is True:
            record_type = WTrackerEvents.start
            record = WSimpleTrackerStorage.Record(record_type, task, event_details=event_details)
            self._WSimpleTrackerStorage__store_record(record)

    @verify_type(task=WThreadTask, details=(str, None))
    def register_stop(self, task, event_details=None):
        """ :meth:`.WSimpleTrackerStorage.register_stop` method implementation
                """
        if self.record_stop() is True:
            record_type = WTrackerEvents.stop
            record = WSimpleTrackerStorage.Record(record_type, task, event_details=event_details)
            self._WSimpleTrackerStorage__store_record(record)

    @verify_type(task=WThreadTask, details=(str, None))
    def register_termination(self, task, event_details=None):
        """ :meth:`.WSimpleTrackerStorage.register_termination` method implementation
                """
        if self.record_termination() is True:
            record_type = WTrackerEvents.termination
            record = WSimpleTrackerStorage.Record(record_type, task, event_details=event_details)
            self._WSimpleTrackerStorage__store_record(record)

    @verify_type(task=WThreadTask, raised_exception=Exception, exception_details=str, details=(str, None))
    def register_exception(self, task, raised_exception, exception_details, event_details=None):
        """ :meth:`.WSimpleTrackerStorage.register_exception` method implementation
                """
        if self.record_exception() is True:
            record = WSimpleTrackerStorage.ExceptionRecord(task, raised_exception, exception_details, event_details=event_details)
            self._WSimpleTrackerStorage__store_record(record)

    @verify_type(task=WThreadTask, details=(str, None))
    def register_wait(self, task, event_details=None):
        """ :meth:`.WSimpleTrackerStorage.register_wait` method implementation
                """
        if self.record_wait() is True:
            record_type = WTrackerEvents.wait
            record = WSimpleTrackerStorage.Record(record_type, task, event_details=event_details)
            self._WSimpleTrackerStorage__store_record(record)

    @verify_type(task=WThreadTask, details=(str, None))
    def register_drop(self, task, event_details=None):
        """ :meth:`.WSimpleTrackerStorage.register_drop` method implementation
                """
        if self.record_drop() is True:
            record_type = WTrackerEvents.drop
            record = WSimpleTrackerStorage.Record(record_type, task, event_details=event_details)
            self._WSimpleTrackerStorage__store_record(record)

    @WCriticalResource.critical_section(timeout=__critical_section_timeout__)
    def __store_record(self, record):
        """ Save record in a internal storage

                :param record: record to save

                :return: None
                """
        if isinstance(record, WSimpleTrackerStorage.Record) is False:
            raise TypeError('Invalid record type was')
        limit = self.record_limit()
        if limit is not None:
            if len(self._WSimpleTrackerStorage__registry) >= limit:
                self._WSimpleTrackerStorage__registry.pop(0)
        self._WSimpleTrackerStorage__registry.append(record)

    @WCriticalResource.critical_section(timeout=__critical_section_timeout__)
    def __registry_copy(self):
        """ Return copy of tracked events

                :return: list of WSimpleTrackerStorage.Record
                """
        return self._WSimpleTrackerStorage__registry.copy()

    def __iter__(self):
        """ Iterate over registered events (WSimpleTrackerStorage.Record). The newest record will be yield
                the first

                :return: generator
                """
        registry = self._WSimpleTrackerStorage__registry_copy()
        while len(registry) > 0:
            yield registry.pop(-1)

    @verify_type(requested_events=WTrackerEvents)
    def last_record(self, task_uid, *requested_events):
        """ Search over registered :class:`.WScheduleTask` instances and return the last record that matches
                search criteria.

                :param task_uid: uid of :class:`.WScheduleTask` instance
                :param requested_events: target events types

                :return: WSimpleTrackerStorage.Record or None
                """
        for record in self:
            if isinstance(record.thread_task, WScheduleTask) is False:
                continue
            if record.thread_task.uid() == task_uid:
                if len(requested_events) == 0 or record.record_type in requested_events:
                    return record
                continue


class WScheduleRecordTracker(WScheduleRecord):
    __doc__ = " Schedule record that may register scheduler events related to a scheduled task like 'postponing' event\n\tand 'drop' event.\n\n\t:note: Since there is an extra work that should be done, this class may be inappropriate for low-latency\n\tsituation. Also, registering events should be done quickly because of this task joining timeout.\n\t"

    @verify_type('paranoid', task=WScheduleTask, task_group_id=(str, None))
    @verify_value('paranoid', on_drop=lambda x: x is None or callable(x))
    @verify_value('paranoid', on_wait=lambda x: x is None or callable(x))
    @verify_type(task=WThreadTracker)
    @verify_type(track_wait=bool, track_drop=bool)
    def __init__(self, task, policy=None, task_group_id=None, on_drop=None, on_wait=None, track_wait=True, track_drop=True):
        """ Create new schedule record, that may track schedule events

                :param task: same as task in :meth:`.WScheduleRecord.__init__` except it must be                :class:`.WThreadTracker` instance
                :param policy: same as policy in :meth:`.WScheduleRecord.__init__`
                :param task_group_id: same as task_group_id in :meth:`.WScheduleRecord.__init__`
                :param on_drop: same as on_drop in :meth:`.WScheduleRecord.__init__`
                :param on_wait: same as on_wait in :meth:`.WScheduleRecord.__init__`
                :param track_wait: whether to register postponing event of this record or not
                :param track_drop: whether to register drop event of this record or not
                """
        WScheduleRecord.__init__(self, task, policy=policy, task_group_id=task_group_id, on_drop=on_drop, on_wait=on_wait)
        self._WScheduleRecordTracker__track_wait = track_wait
        self._WScheduleRecordTracker__track_drop = track_drop

    def track_wait(self):
        """ Return True if this task is tracking "postponing" event otherwise - False

                :return: bool
                """
        return self._WScheduleRecordTracker__track_wait

    def track_drop(self):
        """ Return True if this task is tracking "drop" event otherwise - False

                :return: bool
                """
        return self._WScheduleRecordTracker__track_drop

    def task_postponed(self):
        """ Track (if required) postponing event and do the same job as :meth:`.WScheduleRecord.task_postponed`
                method do

                :return: None
                """
        tracker = self.task().tracker_storage()
        if tracker is not None:
            if self.track_wait() is True:
                details = self.task().event_details(WTrackerEvents.wait)
                tracker.register_wait(self.task(), event_details=details)
        WScheduleRecord.task_postponed(self)

    def task_dropped(self):
        """ Track (if required) drop event and do the same job as :meth:`.WScheduleRecord.task_dropped`
                method do

                :return: None
                """
        tracker = self.task().tracker_storage()
        if tracker is not None:
            if self.track_drop() is True:
                details = self.task().event_details(WTrackerEvents.drop)
                tracker.register_drop(self.task(), event_details=details)
        WScheduleRecord.task_dropped(self)