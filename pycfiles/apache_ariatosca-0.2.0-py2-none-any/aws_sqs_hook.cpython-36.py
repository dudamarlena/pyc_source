# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/aws_sqs_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2862 bytes
from airflow.contrib.hooks.aws_hook import AwsHook

class SQSHook(AwsHook):
    """SQSHook"""

    def get_conn(self):
        return self.get_client_type('sqs')

    def create_queue(self, queue_name, attributes=None):
        """
        Create queue using connection object

        :param queue_name: name of the queue.
        :type queue_name: str
        :param attributes: additional attributes for the queue (default: None)
            For details of the attributes parameter see :py:meth:`botocore.client.SQS.create_queue`
        :type attributes: dict

        :return: dict with the information about the queue
            For details of the returned value see :py:meth:`botocore.client.SQS.create_queue`
        :rtype: dict
        """
        return self.get_conn().create_queue(QueueName=queue_name, Attributes=(attributes or {}))

    def send_message(self, queue_url, message_body, delay_seconds=0, message_attributes=None):
        """
        Send message to the queue

        :param queue_url: queue url
        :type queue_url: str
        :param message_body: the contents of the message
        :type message_body: str
        :param delay_seconds: seconds to delay the message
        :type delay_seconds: int
        :param message_attributes: additional attributes for the message (default: None)
            For details of the attributes parameter see :py:meth:`botocore.client.SQS.send_message`
        :type message_attributes: dict

        :return: dict with the information about the message sent
            For details of the returned value see :py:meth:`botocore.client.SQS.send_message`
        :rtype: dict
        """
        return self.get_conn().send_message(QueueUrl=queue_url, MessageBody=message_body,
          DelaySeconds=delay_seconds,
          MessageAttributes=(message_attributes or {}))