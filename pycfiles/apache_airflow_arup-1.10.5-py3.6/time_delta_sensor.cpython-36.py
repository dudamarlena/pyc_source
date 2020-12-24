# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/time_delta_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1863 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils import timezone
from airflow.utils.decorators import apply_defaults

class TimeDeltaSensor(BaseSensorOperator):
    __doc__ = "\n    Waits for a timedelta after the task's execution_date + schedule_interval.\n    In Airflow, the daily task stamped with ``execution_date``\n    2016-01-01 can only start running on 2016-01-02. The timedelta here\n    represents the time after the execution period has closed.\n\n    :param delta: time length to wait after execution_date before succeeding\n    :type delta: datetime.timedelta\n    "

    @apply_defaults
    def __init__(self, delta, *args, **kwargs):
        (super(TimeDeltaSensor, self).__init__)(*args, **kwargs)
        self.delta = delta

    def poke(self, context):
        dag = context['dag']
        target_dttm = dag.following_schedule(context['execution_date'])
        target_dttm += self.delta
        self.log.info('Checking if the time (%s) has come', target_dttm)
        return timezone.utcnow() > target_dttm