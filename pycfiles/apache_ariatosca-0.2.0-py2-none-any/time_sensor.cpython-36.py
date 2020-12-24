# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/time_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1505 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils import timezone
from airflow.utils.decorators import apply_defaults

class TimeSensor(BaseSensorOperator):
    """TimeSensor"""

    @apply_defaults
    def __init__(self, target_time, *args, **kwargs):
        (super(TimeSensor, self).__init__)(*args, **kwargs)
        self.target_time = target_time

    def poke(self, context):
        self.log.info('Checking if the time (%s) has come', self.target_time)
        return timezone.utcnow().time() > self.target_time