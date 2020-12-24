# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/aws_sqs_publish_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3064 bytes
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_sqs_hook import SQSHook

class SQSPublishOperator(BaseOperator):
    """SQSPublishOperator"""
    template_fields = ('sqs_queue', 'message_content', 'delay_seconds')
    ui_color = '#6ad3fa'

    @apply_defaults
    def __init__(self, sqs_queue, message_content, message_attributes=None, delay_seconds=0, aws_conn_id='aws_default', *args, **kwargs):
        (super(SQSPublishOperator, self).__init__)(*args, **kwargs)
        self.sqs_queue = sqs_queue
        self.aws_conn_id = aws_conn_id
        self.message_content = message_content
        self.delay_seconds = delay_seconds
        self.message_attributes = message_attributes or {}

    def execute(self, context):
        """
        Publish the message to SQS queue

        :param context: the context object
        :type context: dict
        :return: dict with information about the message sent
            For details of the returned dict see :py:meth:`botocore.client.SQS.send_message`
        :rtype: dict
        """
        hook = SQSHook(aws_conn_id=(self.aws_conn_id))
        result = hook.send_message(queue_url=(self.sqs_queue), message_body=(self.message_content),
          delay_seconds=(self.delay_seconds),
          message_attributes=(self.message_attributes))
        self.log.info('result is send_message is %s', result)
        return result