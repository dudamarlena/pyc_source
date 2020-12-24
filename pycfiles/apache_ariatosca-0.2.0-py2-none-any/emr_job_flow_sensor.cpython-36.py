# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/emr_job_flow_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2438 bytes
from airflow.contrib.hooks.emr_hook import EmrHook
from airflow.contrib.sensors.emr_base_sensor import EmrBaseSensor
from airflow.utils import apply_defaults

class EmrJobFlowSensor(EmrBaseSensor):
    """EmrJobFlowSensor"""
    NON_TERMINAL_STATES = [
     'STARTING', 'BOOTSTRAPPING', 'RUNNING',
     'WAITING', 'TERMINATING']
    FAILED_STATE = ['TERMINATED_WITH_ERRORS']
    template_fields = ['job_flow_id']
    template_ext = ()

    @apply_defaults
    def __init__(self, job_flow_id, *args, **kwargs):
        (super(EmrJobFlowSensor, self).__init__)(*args, **kwargs)
        self.job_flow_id = job_flow_id

    def get_emr_response(self):
        emr = EmrHook(aws_conn_id=(self.aws_conn_id)).get_conn()
        self.log.info('Poking cluster %s', self.job_flow_id)
        return emr.describe_cluster(ClusterId=(self.job_flow_id))

    @staticmethod
    def state_from_response(response):
        return response['Cluster']['Status']['State']

    @staticmethod
    def failure_message_from_response(response):
        state_change_reason = response['Cluster']['Status'].get('StateChangeReason')
        if state_change_reason:
            return 'for code: {} with message {}'.format(state_change_reason.get('Code', 'No code'), state_change_reason.get('Message', 'Unknown'))