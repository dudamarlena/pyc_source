# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/aws_sqs_publish_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3064 bytes
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_sqs_hook import SQSHook

class SQSPublishOperator(BaseOperator):
    __doc__ = '\n    Publish message to a SQS queue.\n\n    :param sqs_queue: The SQS queue url (templated)\n    :type sqs_queue: str\n    :param message_content: The message content (templated)\n    :type message_content: str\n    :param message_attributes: additional attributes for the message (default: None)\n        For details of the attributes parameter see :py:meth:`botocore.client.SQS.send_message`\n    :type message_attributes: dict\n    :param delay_seconds: message delay (templated) (default: 1 second)\n    :type delay_seconds: int\n    :param aws_conn_id: AWS connection id (default: aws_default)\n    :type aws_conn_id: str\n    '
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