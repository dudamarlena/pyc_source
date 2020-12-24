# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/weekday_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4291 bytes
import six
from airflow.contrib.utils.weekday import WeekDay
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils import timezone
from airflow.utils.decorators import apply_defaults

class DayOfWeekSensor(BaseSensorOperator):
    """DayOfWeekSensor"""

    @apply_defaults
    def __init__(self, week_day, use_task_execution_day=False, *args, **kwargs):
        (super(DayOfWeekSensor, self).__init__)(*args, **kwargs)
        self.week_day = week_day
        self.use_task_execution_day = use_task_execution_day
        if isinstance(self.week_day, six.string_types):
            self._week_day_num = {
             WeekDay.get_weekday_number(week_day_str=(self.week_day))}
        else:
            if isinstance(self.week_day, WeekDay):
                self._week_day_num = {
                 self.week_day}
            else:
                if isinstance(self.week_day, set):
                    if all(isinstance(day, six.string_types) for day in self.week_day):
                        self._week_day_num = {WeekDay.get_weekday_number(day) for day in week_day}
                    elif all(isinstance(day, WeekDay) for day in self.week_day):
                        self._week_day_num = self.week_day
                else:
                    raise TypeError('Unsupported Type for week_day parameter: {}. It should be one of str, set or Weekday enum type'.format(type(week_day)))

    def poke(self, context):
        self.log.info('Poking until weekday is in %s, Today is %s', self.week_day, WeekDay(timezone.utcnow().isoweekday()).name)
        if self.use_task_execution_day:
            return context['execution_date'].isoweekday() in self._week_day_num
        else:
            return timezone.utcnow().isoweekday() in self._week_day_num