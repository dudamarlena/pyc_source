# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/time_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1505 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils import timezone
from airflow.utils.decorators import apply_defaults

class TimeSensor(BaseSensorOperator):
    __doc__ = '\n    Waits until the specified time of the day.\n\n    :param target_time: time after which the job succeeds\n    :type target_time: datetime.time\n    '

    @apply_defaults
    def __init__(self, target_time, *args, **kwargs):
        (super(TimeSensor, self).__init__)(*args, **kwargs)
        self.target_time = target_time

    def poke(self, context):
        self.log.info('Checking if the time (%s) has come', self.target_time)
        return timezone.utcnow().time() > self.target_time