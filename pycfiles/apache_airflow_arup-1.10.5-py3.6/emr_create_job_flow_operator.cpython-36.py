# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/emr_create_job_flow_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2845 bytes
from airflow.contrib.hooks.emr_hook import EmrHook
from airflow.models import BaseOperator
from airflow.utils import apply_defaults
from airflow.exceptions import AirflowException

class EmrCreateJobFlowOperator(BaseOperator):
    __doc__ = '\n    Creates an EMR JobFlow, reading the config from the EMR connection.\n    A dictionary of JobFlow overrides can be passed that override\n    the config from the connection.\n\n    :param aws_conn_id: aws connection to uses\n    :type aws_conn_id: str\n    :param emr_conn_id: emr connection to use\n    :type emr_conn_id: str\n    :param job_flow_overrides: boto3 style arguments to override\n       emr_connection extra. (templated)\n    :type job_flow_overrides: dict\n    '
    template_fields = ['job_flow_overrides']
    template_ext = ()
    ui_color = '#f9c915'

    @apply_defaults
    def __init__(self, aws_conn_id='s3_default', emr_conn_id='emr_default', job_flow_overrides=None, region_name=None, *args, **kwargs):
        (super(EmrCreateJobFlowOperator, self).__init__)(*args, **kwargs)
        self.aws_conn_id = aws_conn_id
        self.emr_conn_id = emr_conn_id
        if job_flow_overrides is None:
            job_flow_overrides = {}
        self.job_flow_overrides = job_flow_overrides
        self.region_name = region_name

    def execute(self, context):
        emr = EmrHook(aws_conn_id=(self.aws_conn_id), emr_conn_id=(self.emr_conn_id),
          region_name=(self.region_name))
        self.log.info('Creating JobFlow using aws-conn-id: %s, emr-conn-id: %s', self.aws_conn_id, self.emr_conn_id)
        response = emr.create_job_flow(self.job_flow_overrides)
        if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
            raise AirflowException('JobFlow creation failed: %s' % response)
        else:
            self.log.info('JobFlow with id %s created', response['JobFlowId'])
            return response['JobFlowId']