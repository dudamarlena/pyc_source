# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/sagemaker_base_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2804 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerBaseSensor(BaseSensorOperator):
    __doc__ = '\n    Contains general sensor behavior for SageMaker.\n    Subclasses should implement get_sagemaker_response()\n    and state_from_response() methods.\n    Subclasses should also implement NON_TERMINAL_STATES and FAILED_STATE methods.\n    '
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, aws_conn_id='aws_default', *args, **kwargs):
        (super(SageMakerBaseSensor, self).__init__)(*args, **kwargs)
        self.aws_conn_id = aws_conn_id

    def poke(self, context):
        response = self.get_sagemaker_response()
        if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
            self.log.info('Bad HTTP response: %s', response)
            return False
        state = self.state_from_response(response)
        self.log.info('Job currently %s', state)
        if state in self.non_terminal_states():
            return False
        else:
            if state in self.failed_states():
                failed_reason = self.get_failed_reason_from_response(response)
                raise AirflowException('Sagemaker job failed for the following reason: %s' % failed_reason)
            return True

    def non_terminal_states(self):
        raise NotImplementedError('Please implement non_terminal_states() in subclass')

    def failed_states(self):
        raise NotImplementedError('Please implement failed_states() in subclass')

    def get_sagemaker_response(self):
        raise NotImplementedError('Please implement get_sagemaker_response() in subclass')

    def get_failed_reason_from_response(self, response):
        return 'Unknown'

    def state_from_response(self, response):
        raise NotImplementedError('Please implement state_from_response() in subclass')