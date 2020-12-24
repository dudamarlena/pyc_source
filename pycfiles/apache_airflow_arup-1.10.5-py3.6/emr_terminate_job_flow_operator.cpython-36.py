# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/emr_terminate_job_flow_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2135 bytes
from airflow.models import BaseOperator
from airflow.utils import apply_defaults
from airflow.exceptions import AirflowException
from airflow.contrib.hooks.emr_hook import EmrHook

class EmrTerminateJobFlowOperator(BaseOperator):
    __doc__ = '\n    Operator to terminate EMR JobFlows.\n\n    :param job_flow_id: id of the JobFlow to terminate. (templated)\n    :type job_flow_id: str\n    :param aws_conn_id: aws connection to uses\n    :type aws_conn_id: str\n    '
    template_fields = ['job_flow_id']
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