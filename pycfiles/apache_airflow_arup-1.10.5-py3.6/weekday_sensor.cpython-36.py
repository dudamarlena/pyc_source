# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/weekday_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4291 bytes
import six
from airflow.contrib.utils.weekday import WeekDay
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils import timezone
from airflow.utils.decorators import apply_defaults

class DayOfWeekSensor(BaseSensorOperator):
    __doc__ = '\n    Waits until the first specified day of the week. For example, if the execution\n    day of the task is \'2018-12-22\' (Saturday) and you pass \'FRIDAY\', the task will wait\n    until next Friday.\n\n    **Example** (with single day): ::\n\n        weekend_check = DayOfWeekSensor(\n            task_id=\'weekend_check\',\n            week_day=\'Saturday\',\n            use_task_execution_day=True,\n            dag=dag)\n\n    **Example** (with multiple day using set): ::\n\n        weekend_check = DayOfWeekSensor(\n            task_id=\'weekend_check\',\n            week_day={\'Saturday\', \'Sunday\'},\n            use_task_execution_day=True,\n            dag=dag)\n\n    **Example** (with :class:`~airflow.contrib.utils.weekday.WeekDay` enum): ::\n\n        # import WeekDay Enum\n        from airflow.contrib.utils.weekday import WeekDay\n\n        weekend_check = DayOfWeekSensor(\n            task_id=\'weekend_check\',\n            week_day={WeekDay.SATURDAY, WeekDay.SUNDAY},\n            use_task_execution_day=True,\n            dag=dag)\n\n    :param week_day: Day of the week to check (full name). Optionally, a set\n        of days can also be provided using a set.\n        Example values:\n\n            * ``"MONDAY"``,\n            * ``{"Saturday", "Sunday"}``\n            * ``{WeekDay.TUESDAY}``\n            * ``{WeekDay.SATURDAY, WeekDay.SUNDAY}``\n\n    :type week_day: set or str or airflow.contrib.utils.weekday.WeekDay\n    :param use_task_execution_day: If ``True``, uses task\'s execution day to compare\n        with week_day. Execution Date is Useful for backfilling.\n        If ``False``, uses system\'s day of the week. Useful when you\n        don\'t want to run anything on weekdays on the system.\n    :type use_task_execution_day: bool\n    '

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