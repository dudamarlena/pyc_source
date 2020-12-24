# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/time_delta_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1863 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils import timezone
from airflow.utils.decorators import apply_defaults

class TimeDeltaSensor(BaseSensorOperator):
    """TimeDeltaSensor"""

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