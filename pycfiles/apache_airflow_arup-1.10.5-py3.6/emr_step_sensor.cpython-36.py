# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/emr_step_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2682 bytes
from airflow.contrib.hooks.emr_hook import EmrHook
from airflow.contrib.sensors.emr_base_sensor import EmrBaseSensor
from airflow.utils import apply_defaults

class EmrStepSensor(EmrBaseSensor):
    __doc__ = '\n    Asks for the state of the step until it reaches a terminal state.\n    If it fails the sensor errors, failing the task.\n\n    :param job_flow_id: job_flow_id which contains the step check the state of\n    :type job_flow_id: str\n    :param step_id: step to check the state of\n    :type step_id: str\n    '
    NON_TERMINAL_STATES = [
     'PENDING', 'RUNNING', 'CONTINUE', 'CANCEL_PENDING']
    FAILED_STATE = ['CANCELLED', 'FAILED', 'INTERRUPTED']
    template_fields = ['job_flow_id', 'step_id']
    template_ext = ()

    @apply_defaults
    def __init__(self, job_flow_id, step_id, *args, **kwargs):
        (super(EmrStepSensor, self).__init__)(*args, **kwargs)
        self.job_flow_id = job_flow_id
        self.step_id = step_id

    def get_emr_response(self):
        emr = EmrHook(aws_conn_id=(self.aws_conn_id)).get_conn()
        self.log.info('Poking step %s on cluster %s', self.step_id, self.job_flow_id)
        return emr.describe_step(ClusterId=(self.job_flow_id), StepId=(self.step_id))

    @staticmethod
    def state_from_response(response):
        return response['Step']['Status']['State']

    @staticmethod
    def failure_message_from_response(response):
        fail_details = response['Step']['Status'].get('FailureDetails')
        if fail_details:
            return 'for reason {} with message {} and log file {}'.format(fail_details.get('Reason'), fail_details.get('Message'), fail_details.get('LogFile'))