# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/aws_athena_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2900 bytes
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_athena_hook import AWSAthenaHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator

class AthenaSensor(BaseSensorOperator):
    """AthenaSensor"""
    INTERMEDIATE_STATES = ('QUEUED', 'RUNNING')
    FAILURE_STATES = ('FAILED', 'CANCELLED')
    SUCCESS_STATES = ('SUCCEEDED', )
    template_fields = [
     'query_execution_id']
    template_ext = ()
    ui_color = '#66c3ff'

    @apply_defaults
    def __init__(self, query_execution_id, max_retires=None, aws_conn_id='aws_default', sleep_time=10, *args, **kwargs):
        (super(AthenaSensor, self).__init__)(*args, **kwargs)
        self.aws_conn_id = aws_conn_id
        self.query_execution_id = query_execution_id
        self.hook = None
        self.sleep_time = sleep_time
        self.max_retires = max_retires

    def poke(self, context):
        self.hook = self.get_hook()
        self.hook.get_conn()
        state = self.hook.poll_query_status(self.query_execution_id, self.max_retires)
        if state in self.FAILURE_STATES:
            raise AirflowException('Athena sensor failed')
        if state in self.INTERMEDIATE_STATES:
            return False
        else:
            return True

    def get_hook(self):
        return AWSAthenaHook(self.aws_conn_id, self.sleep_time)