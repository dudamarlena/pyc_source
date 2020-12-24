# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sns_publish_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2129 bytes
from airflow.contrib.hooks.aws_sns_hook import AwsSnsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SnsPublishOperator(BaseOperator):
    """SnsPublishOperator"""
    template_fields = [
     'message']
    template_ext = ()

    @apply_defaults
    def __init__(self, target_arn, message, aws_conn_id='aws_default', *args, **kwargs):
        (super(SnsPublishOperator, self).__init__)(*args, **kwargs)
        self.target_arn = target_arn
        self.message = message
        self.aws_conn_id = aws_conn_id

    def execute(self, context):
        sns = AwsSnsHook(aws_conn_id=(self.aws_conn_id))
        self.log.info('Sending SNS notification to {} using {}:\n{}'.format(self.target_arn, self.aws_conn_id, self.message))
        return sns.publish_to_target(target_arn=(self.target_arn),
          message=(self.message))