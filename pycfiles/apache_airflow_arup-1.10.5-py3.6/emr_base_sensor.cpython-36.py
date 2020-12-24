# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/emr_base_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2221 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils import apply_defaults
from airflow.exceptions import AirflowException

class EmrBaseSensor(BaseSensorOperator):
    __doc__ = '\n    Contains general sensor behavior for EMR.\n    Subclasses should implement get_emr_response() and state_from_response() methods.\n    Subclasses should also implement NON_TERMINAL_STATES and FAILED_STATE constants.\n    '
    ui_color = '#66c3ff'

    @apply_defaults
    def __init__(self, aws_conn_id='aws_default', *args, **kwargs):
        (super(EmrBaseSensor, self).__init__)(*args, **kwargs)
        self.aws_conn_id = aws_conn_id

    def poke(self, context):
        response = self.get_emr_response()
        if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
            self.log.info('Bad HTTP response: %s', response)
            return False
        state = self.state_from_response(response)
        self.log.info('Job flow currently %s', state)
        if state in self.NON_TERMINAL_STATES:
            return False
        else:
            if state in self.FAILED_STATE:
                final_message = 'EMR job failed'
                failure_message = self.failure_message_from_response(response)
                if failure_message:
                    final_message += ' ' + failure_message
                raise AirflowException(final_message)
            return True