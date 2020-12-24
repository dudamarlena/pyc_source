# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/emr_terminate_job_flow_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2135 bytes
from airflow.models import BaseOperator
from airflow.utils import apply_defaults
from airflow.exceptions import AirflowException
from airflow.contrib.hooks.emr_hook import EmrHook

class EmrTerminateJobFlowOperator(BaseOperator):
    """EmrTerminateJobFlowOperator"""
    template_fields = [
     'job_flow_id']
    template_ext = ()
    ui_color = '#f9c915'

    @apply_defaults
    def __init__(self, job_flow_id, aws_conn_id='s3_default', *args, **kwargs):
        (super(EmrTerminateJobFlowOperator, self).__init__)(*args, **kwargs)
        self.job_flow_id = job_flow_id
        self.aws_conn_id = aws_conn_id

    def execute(self, context):
        emr = EmrHook(aws_conn_id=(self.aws_conn_id)).get_conn()
        self.log.info('Terminating JobFlow %s', self.job_flow_id)
        response = emr.terminate_job_flows(JobFlowIds=[self.job_flow_id])
        if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
            raise AirflowException('JobFlow termination failed: %s' % response)
        else:
            self.log.info('JobFlow with id %s terminated', self.job_flow_id)