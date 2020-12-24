# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/aws_sns_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1789 bytes
import json
from airflow.contrib.hooks.aws_hook import AwsHook

class AwsSnsHook(AwsHook):
    """AwsSnsHook"""

    def __init__(self, *args, **kwargs):
        (super(AwsSnsHook, self).__init__)(*args, **kwargs)

    def get_conn(self):
        """
        Get an SNS connection
        """
        self.conn = self.get_client_type('sns')
        return self.conn

    def publish_to_target(self, target_arn, message):
        """
        Publish a message to a topic or an endpoint.

        :param target_arn: either a TopicArn or an EndpointArn
        :type target_arn: str
        :param message: the default message you want to send
        :param message: str
        """
        conn = self.get_conn()
        messages = {'default': message}
        return conn.publish(TargetArn=target_arn,
          Message=(json.dumps(messages)),
          MessageStructure='json')