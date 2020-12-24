# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/task/scheduler/task_source.py
# Compiled at: 2017-10-10 07:17:45
# Size of source mod 2**32: 15841 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from datetime import datetime, timedelta, MAXYEAR, timezone
from calendar import monthrange, weekday
from wasp_general.verify import verify_type, verify_value
from wasp_general.datetime import utc_datetime
from wasp_general.thread import WCriticalResource
from wasp_general.task.scheduler.proto import WTaskSourceProto, WScheduleRecord, WScheduleTask, WSchedulerServiceProto

class WBasicTaskSource(WTaskSourceProto):

    @verify_type(scheduler=WSchedulerServiceProto)
    def __init__(self, scheduler_service):
        self._WBasicTaskSource__service = scheduler_service

    def scheduler_service(self):
        return self._WBasicTaskSource__service


class WCronSchedule:
    __calendar__ = {1: 31,  2: 29,  3: 31,  4: 30,  5: 31,  6: 30,  7: 31,  8: 31,  9: 30,  10: 31,  11: 30,  12: 31}

    @verify_type(start_datetime=(datetime, None), minute=(int, None), hour=(int, None), day_of_month=(int, None))
    @verify_type(day_of_week=(int, None), month=(int, None))
    @verify_value(minute=lambda x: x is None or 0 <= x <= 59)
    @verify_value(hour=lambda x: x is None or 0 <= x <= 23)
    @verify_value(day_of_month=lambda x: x is None or 1 <= x <= 31)
    @verify_value(day_of_week=lambda x: x is None or 1 <= x <= 7)
    @verify_value(month=lambda x: x is None or 1 <= x <= 12)
    def __init__(self, start_datetime=None, minute=None, hour=None, day_of_month=None, day_of_week=None, month=None):
        if month is not None:
            if day_of_month is not None and day_of_month > WCronSchedule.__calendar__[month]:
                raise ValueError('Invalid day and month combination')
        self._WCronSchedule__start_datetime = start_datetime if start_datetime is not None else self.now()
        self._WCronSchedule__next_start = None
        self._WCronSchedule__minute = minute
        self._WCronSchedule__hour = hour
        self._WCronSchedule__day_of_month = day_of_month
        self._WCronSchedule__day_of_week = day_of_week
        self._WCronSchedule__month = month
        self.update()

    def start_datetime(self):
        return self._WCronSchedule__start_datetime

    @verify_type(start_datetime=datetime)
    def _set_start_datetime(self, start_datetime):
        self._WCronSchedule__start_datetime = start_datetime
        self._WCronSchedule__next_start = None

    @verify_type('paranoid', year=int, month=int, day=int, hour=int, minute=int)
    @verify_value('paranoid', year=lambda x: x > 0)
    @verify_value('paranoid', month=lambda x: x is None or 1 <= x <= 12)
    @verify_value('paranoid', day=lambda x: x is None or 1 <= x <= 31)
    @verify_value('paranoid', hour=lambda x: x is None or 0 <= x <= 23)
    @verify_value('paranoid', minute=lambda x: x is None or 0 <= x <= 59)
    def _datetime(self, year, month, day, hour, minute):
        return datetime(year, month, day, hour, minute)

    def next_start(self):
        return self._WCronSchedule__next_start

    def minute(self):
        return self._WCronSchedule__minute

    def hour(self):
        return self._WCronSchedule__hour

    def day_of_month(self):
        return self._WCronSchedule__day_of_month

    def day_of_week(self):
        return self._WCronSchedule__day_of_week

    def month(self):
        return self._WCronSchedule__month

    def no_frequency(self):
        result = self.minute() is None and self.hour() is None and self.day_of_month() is None
        return result is True and self.day_of_week() is None and self.month() is None

    def final_datetime(self):
        return datetime(MAXYEAR, 12, 31, 23, 59)

    @classmethod
    def now(cls):
        return datetime.now()

    def update(self):
        if self.no_frequency() is True:
            return
        for year, month in self.month_iterator():
            for day in self.day_iterator(year, month):
                for hour, minute in self.time_iterator(year, month, day):
                    self._WCronSchedule__next_start = self._datetime(year, month, day, hour, minute)
                    return

    @verify_type(omit_skipped=bool)
    def complete(self, omit_skipped=True):
        if self.no_frequency() is True:
            return
        next_start = self.next_start()
        seconds_last_minute = next_start.second
        seconds_last_hour = next_start.minute * 60 + seconds_last_minute
        seconds_last_day = next_start.hour * 24 * 60 * 60 + seconds_last_hour
        time_shift = 0
        if self.month() is not None:
            year = next_start.year
            month = next_start.month
            if month < 12:
                month += 1
            else:
                year += 1
                month = 1
            time_shift = (self._datetime(year, month, 1, 0, 0) - next_start).total_seconds()
        else:
            if self.day_of_week() is not None:
                time_shift = 604800 - seconds_last_day
            else:
                if self.day_of_month() is not None:
                    time_shift = 86400 - seconds_last_day
                else:
                    if self.hour() is not None:
                        time_shift = 3600 - seconds_last_hour
                    elif self.minute() is not None:
                        time_shift = 60 - seconds_last_minute
            time_shift += 1
            new_start = next_start + timedelta(seconds=time_shift)
            if omit_skipped is True:
                now = self.now()
                if now > new_start:
                    new_start = now
        self._set_start_datetime(new_start)
        self.update()

    def month_iterator(self):
        if self.no_frequency():
            return
        start_datetime = self.start_datetime()
        start_year = start_datetime.year
        start_month = start_datetime.month
        final_datetime = self.final_datetime()
        max_year = final_datetime.year
        max_month = final_datetime.month
        month = self.month()
        year = start_year
        if month is not None:
            if month < start_month:
                year += 1
            if year > max_year or year == max_year and month > max_month:
                return
            while year < max_year or year == max_year and month < max_month:
                yield (
                 year, month)
                year += 1

        else:
            month = start_month
            while year < max_year or year == max_year and month < max_month:
                yield (
                 year, month)
                if month < 12:
                    month += 1
                else:
                    year += 1
                    month = 1

    def day_iterator(self, year, month):
        if self.no_frequency():
            return
        start_datetime = self.start_datetime()
        days_in_month = monthrange(year, month)[1]
        day_of_month = self.day_of_month()
        day_of_week = self.day_of_week()
        final_datetime = self.final_datetime()
        if year == final_datetime.year:
            if month == final_datetime.month:
                days_in_month = final_datetime.day
        start_day = start_datetime.day
        if year != start_datetime.year or month != start_datetime.month:
            start_day = 1
        if day_of_month is None and day_of_week is None:
            day = start_day
            while day <= days_in_month:
                yield day
                day += 1

        else:
            if day_of_month is not None and day_of_week is None:
                if start_day <= days_in_month:
                    yield day_of_month
            else:
                if day_of_month is not None and day_of_week is not None:
                    if start_day <= days_in_month:
                        if weekday(year, month, day_of_month) == day_of_week:
                            yield day_of_month
                else:
                    current_weekday = weekday(year, month, start_day)
                    delta = day_of_week - current_weekday
                    if delta < 0:
                        delta += 7
                    day = start_day + delta
                    while day <= days_in_month:
                        yield day
                        day += 7

    def time_iterator(self, year, month, day):
        start_datetime = self.start_datetime()
        max_hour = 23
        max_minute = 59
        hour = self.hour()
        minute = self.minute()
        final_datetime = self.final_datetime()
        if year == final_datetime.year:
            if month == final_datetime.month and day == self.final_datetime():
                max_hour = final_datetime.hour
                max_minute = final_datetime.minute
        start_hour = start_datetime.hour
        start_minute = start_datetime.minute
        if year != start_datetime.year or month != start_datetime.month or day != start_datetime.day:
            start_hour = 0
            start_minute = 0
        if hour is None and minute is None:
            hour = start_hour
            minute = start_minute
            while (start_hour <= hour < max_hour or hour) == max_hour:
                if start_minute <= minute <= max_minute:
                    yield (
                     hour, minute)
                    if minute < 59:
                        minute += 1
                else:
                    minute = 0
                    hour += 1

        else:
            if hour is not None and minute is None:
                minute = start_minute
                if start_hour <= hour <= max_hour:
                    while minute <= max_minute:
                        yield (
                         hour, minute)
                        minute += 1

            elif hour is not None and minute is not None:
                if not start_hour <= hour < max_hour:
                    pass
        if hour == max_hour:
            if start_minute <= minute <= max_minute:
                yield (
                 hour, minute)
        else:
            hour = start_hour
            if start_minute > minute:
                hour += 1
            while (start_hour <= hour < max_hour or hour) == max_hour:
                if start_minute <= minute <= max_minute:
                    yield (
                     hour, minute)
                    hour += 1

    @classmethod
    @verify_type(scheduled=str)
    def from_string(cls, scheduled):
        return cls.from_string_tokens(*filter(lambda x: len(x) > 0, scheduled.strip().split(' ')))

    @classmethod
    @verify_type(tokens=str)
    def from_string_tokens(cls, *tokens):
        if len(tokens) != 5:
            raise ValueError('Malformed cron-schedule')
        tokens = [int(x) if x != '*' else None for x in tokens]
        if len(tokens) != 5:
            raise ValueError('Malformed cron-schedule')
        return cls(cls.now(), minute=tokens[0], hour=tokens[1], day_of_month=tokens[2], day_of_week=tokens[3], month=tokens[4])


class WCronLocalTZSchedule(WCronSchedule):
    pass


class WCronUTCSchedule(WCronSchedule):

    @verify_type('paranoid', start_datetime=(datetime, None), minute=(int, None), hour=(int, None))
    @verify_type('paranoid', day_of_month=(int, None), day_of_week=(int, None), month=(int, None))
    @verify_value('paranoid', minute=lambda x: x is None or 0 <= x <= 59)
    @verify_value('paranoid', hour=lambda x: x is None or 0 <= x <= 23)
    @verify_value('paranoid', day_of_month=lambda x: x is None or 1 <= x <= 31)
    @verify_value('paranoid', day_of_week=lambda x: x is None or 1 <= x <= 7)
    @verify_value('paranoid', month=lambda x: x is None or 1 <= x <= 12)
    @verify_value(start_datetime=lambda x: x.tzinfo is not None and x.tzinfo == timezone.utc)
    def __init__(self, start_datetime=None, minute=None, hour=None, day_of_month=None, day_of_week=None, month=None):
        WCronSchedule.__init__(self, start_datetime, minute=minute, hour=hour, day_of_month=day_of_month, day_of_week=day_of_week, month=month)

    @verify_type(start_datetime=datetime)
    @verify_value(start_datetime=lambda x: x.tzinfo is not None and x.tzinfo == timezone.utc)
    def _set_start_datetime(self, start_datetime):
        WCronSchedule._set_start_datetime(self, start_datetime)

    @verify_type('paranoid', year=int, month=int, day=int, hour=int, minute=int)
    @verify_value('paranoid', year=lambda x: x > 0)
    @verify_value('paranoid', month=lambda x: x is None or 1 <= x <= 12)
    @verify_value('paranoid', day=lambda x: x is None or 1 <= x <= 31)
    @verify_value('paranoid', hour=lambda x: x is None or 0 <= x <= 23)
    @verify_value('paranoid', minute=lambda x: x is None or 0 <= x <= 59)
    def _datetime(self, year, month, day, hour, minute):
        return utc_datetime(datetime(year, month, day, hour, minute), local_value=False)

    @classmethod
    def now(cls):
        return utc_datetime()


class WCronScheduleRecord(WScheduleRecord):

    @verify_type('paranoid', task=WScheduleTask, task_group_id=(str, None))
    @verify_value('paranoid', on_drop=lambda x: x is None or callable(x))
    @verify_value('paranoid', on_wait=lambda x: x is None or callable(x))
    @verify_type(schedule=WCronSchedule, omit_skipped=bool)
    @verify_value(schedule=lambda x: isinstance(x, WCronLocalTZSchedule) or isinstance(x, WCronUTCSchedule))
    def __init__(self, cron_schedule, task, policy=None, task_group_id=None, on_drop=None, on_wait=None, omit_skipped=True):
        WScheduleRecord.__init__(self, task, policy=policy, task_group_id=task_group_id, on_drop=on_drop, on_wait=on_wait)
        self._WCronScheduleRecord__schedule = cron_schedule
        self._WCronScheduleRecord__omit_skipped = omit_skipped

    def cron_schedule(self):
        return self._WCronScheduleRecord__schedule

    def next_start(self):
        cron = self.cron_schedule()
        next_start = cron.next_start()
        if isinstance(cron, WCronLocalTZSchedule):
            return utc_datetime(dt=next_start)
        if isinstance(cron, WCronUTCSchedule):
            return next_start
        raise RuntimeError('Corrupted object!')

    def complete(self):
        self.cron_schedule().complete(omit_skipped=self._WCronScheduleRecord__omit_skipped)


class WCronTaskSource(WBasicTaskSource, WCriticalResource):

    @verify_type('paranoid', scheduler_service=WSchedulerServiceProto)
    def __init__(self, scheduler_service):
        WBasicTaskSource.__init__(self, scheduler_service=scheduler_service)
        WCriticalResource.__init__(self)
        self._WCronTaskSource__tasks = []
        self._WCronTaskSource__next_task = None

    @verify_type(record=WCronScheduleRecord)
    def add_record(self, record):
        self._WCronTaskSource__add_record(record)
        self.scheduler_service().update(task_source=self)

    @WCriticalResource.critical_section()
    @verify_type('paranoid', record=WCronScheduleRecord)
    def __add_record(self, record):
        self._WCronTaskSource__tasks.append(record)
        self._WCronTaskSource__update(record)

    @verify_type('paranoid', task=(WCronScheduleRecord, None))
    def __update(self, task=None):
        if task is not None:
            next_start = task.next_start()
            if self._WCronTaskSource__next_task is None or next_start < self._WCronTaskSource__next_task.next_start():
                self._WCronTaskSource__next_task = task
        else:
            if len(self._WCronTaskSource__tasks) > 0:
                next_task = self._WCronTaskSource__tasks[0]
                for task in self._WCronTaskSource__tasks[1:]:
                    if next_task.next_start() is None:
                        next_task = task
                    elif task.next_start() is not None and task.next_start() < next_task.next_start():
                        next_task = task
                        continue

                self._WCronTaskSource__next_task = next_task
            else:
                self._WCronTaskSource__next_task = None

    @WCriticalResource.critical_section()
    def tasks_planned(self):
        return len(self._WCronTaskSource__tasks)

    @WCriticalResource.critical_section()
    def has_records(self):
        if self._WCronTaskSource__next_task is not None:
            next_start = self._WCronTaskSource__next_task.next_start()
            if next_start is not None and next_start <= utc_datetime():
                result = [
                 self._WCronTaskSource__next_task]
                self._WCronTaskSource__next_task.complete()
                self._WCronTaskSource__update()
                return tuple(result)

    @WCriticalResource.critical_section()
    def next_start(self):
        if self._WCronTaskSource__next_task is not None:
            return self._WCronTaskSource__next_task.next_start()


class WInstantTaskSource(WBasicTaskSource, WCriticalResource):
    __lock_acquiring_timeout__ = 5

    @verify_type('paranoid', scheduler_service=WSchedulerServiceProto)
    def __init__(self, scheduler_service):
        WBasicTaskSource.__init__(self, scheduler_service=scheduler_service)
        WCriticalResource.__init__(self)
        self._WInstantTaskSource__records = []

    @verify_type('paranoid', record=WScheduleRecord)
    def add_record(self, record):
        self._WInstantTaskSource__add_record(record)
        self.scheduler_service().update(self)

    @verify_type(record=WScheduleRecord)
    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def __add_record(self, record):
        self._WInstantTaskSource__records.append(record)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def has_records(self):
        if len(self._WInstantTaskSource__records) > 0:
            result = self._WInstantTaskSource__records.copy()
            self._WInstantTaskSource__records = []
            return tuple(result)

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def next_start(self):
        if len(self._WInstantTaskSource__records) > 0:
            return utc_datetime()

    @WCriticalResource.critical_section(timeout=__lock_acquiring_timeout__)
    def tasks_planned(self):
        return len(self._WInstantTaskSource__records)