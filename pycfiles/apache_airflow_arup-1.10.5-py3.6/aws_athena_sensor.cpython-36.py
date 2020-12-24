# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/aws_athena_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2900 bytes
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_athena_hook import AWSAthenaHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator

class AthenaSensor(BaseSensorOperator):
    __doc__ = "\n    Asks for the state of the Query until it reaches a failure state or success state.\n    If it fails, failing the task.\n\n    :param query_execution_id: query_execution_id to check the state of\n    :type query_execution_id: str\n    :param max_retires: Number of times to poll for query state before\n        returning the current state, defaults to None\n    :type max_retires: int\n    :param aws_conn_id: aws connection to use, defaults to 'aws_default'\n    :type aws_conn_id: str\n    :param sleep_time: Time to wait between two consecutive call to\n        check query status on athena, defaults to 10\n    :type sleep_time: int\n    "
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