# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/emr_add_steps_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2370 bytes
from airflow.models import BaseOperator
from airflow.utils import apply_defaults
from airflow.exceptions import AirflowException
from airflow.contrib.hooks.emr_hook import EmrHook

class EmrAddStepsOperator(BaseOperator):
    __doc__ = '\n    An operator that adds steps to an existing EMR job_flow.\n\n    :param job_flow_id: id of the JobFlow to add steps to. (templated)\n    :type job_flow_id: str\n    :param aws_conn_id: aws connection to uses\n    :type aws_conn_id: str\n    :param steps: boto3 style steps to be added to the jobflow. (templated)\n    :type steps: list\n    '
    template_fields = ['job_flow_id', 'steps']
    template_ext = ()
    ui_color = '#f9c915'

    @apply_defaults
    def __init__(self, job_flow_id, aws_conn_id='s3_default', steps=None, *args, **kwargs):
        (super(EmrAddStepsOperator, self).__init__)(*args, **kwargs)
        steps = steps or []
        self.job_flow_id = job_flow_id
        self.aws_conn_id = aws_conn_id
        self.steps = steps

    def execute(self, context):
        emr = EmrHook(aws_conn_id=(self.aws_conn_id)).get_conn()
        self.log.info('Adding steps to %s', self.job_flow_id)
        response = emr.add_job_flow_steps(JobFlowId=(self.job_flow_id), Steps=(self.steps))
        if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
            raise AirflowException('Adding steps failed: %s' % response)
        else:
            self.log.info('Steps %s added to JobFlow', response['StepIds'])
            return response['StepIds']