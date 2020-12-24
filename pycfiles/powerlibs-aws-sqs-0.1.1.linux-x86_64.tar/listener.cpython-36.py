# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cleber/.pyenv/versions/powerlibs_aws_sqs/lib/python3.6/site-packages/powerlibs/aws/sqs/listener.py
# Compiled at: 2017-08-16 17:04:44
# Size of source mod 2**32: 927 bytes
import json
from .base import SQSBase

class SQSListener(SQSBase):

    def receive_messages(self, max_number_of_message=1, wait_time=5, visibility_timeout=30):
        return self.sqs_queue.receive_messages(MaxNumberOfMessages=max_number_of_message,
          WaitTimeSeconds=wait_time,
          VisibilityTimeout=visibility_timeout)

    def process_messages(self, max_messages=None):
        counter = 0
        for message in self.receive_messages():
            body = json.loads(message.body)
            payload = json.loads(body['Message'])
            ret = self.process_message(payload)
            if ret is True:
                message.delete()
            if max_messages is not None:
                counter += 1
                if counter >= max_messages:
                    return

    def process_message(self, message):
        self.logger.info('Processing message: {}'.format(message))