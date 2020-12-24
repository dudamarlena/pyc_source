# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cleber/.pyenv/versions/powerlibs_aws_sqs/lib/python3.6/site-packages/powerlibs/aws/sqs/base.py
# Compiled at: 2017-08-16 17:04:44
# Size of source mod 2**32: 835 bytes
import os, logging, boto3
from cached_property import cached_property

class SQSBase:

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_region=None):
        self.aws_access_key_id = aws_access_key_id or os.environ['AWS_ACCESS_KEY_ID']
        self.aws_secret_access_key = aws_secret_access_key or os.environ['AWS_SECRET_ACCESS_KEY']
        self.aws_region = aws_region or os.environ['AWS_REGION']
        self.logger = logging.getLogger()

    @cached_property
    def sqs_client(self):
        return boto3.resource('sqs',
          (self.aws_region),
          aws_access_key_id=(self.aws_access_key_id),
          aws_secret_access_key=(self.aws_secret_access_key))

    def get_queue(self, name):
        return self.sqs_client.get_queue_by_name(QueueName=name)