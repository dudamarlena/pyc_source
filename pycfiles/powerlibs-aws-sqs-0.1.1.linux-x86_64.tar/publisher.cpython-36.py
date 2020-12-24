# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cleber/.pyenv/versions/powerlibs_aws_sqs/lib/python3.6/site-packages/powerlibs/aws/sqs/publisher.py
# Compiled at: 2017-08-17 15:44:25
# Size of source mod 2**32: 1055 bytes
import json
from .base import SQSBase

class SQSPublisher(SQSBase):

    @staticmethod
    def translate_attributes_into_amazon_bizarre_format(attributes):
        translated_attributes = {}
        for key, value in attributes.items():
            if isinstance(value, str):
                translated_attributes[key] = {'DataType':'String',  'StringValue':value}
            else:
                if isinstance(value, (int, float)):
                    translated_attributes[key] = {'DataType':'Number',  'StringValue':value}

        return translated_attributes

    def publish(self, queue_name, payload, attributes=None):
        queue = self.get_queue(queue_name)
        attributes = self.translate_attributes_into_amazon_bizarre_format(attributes) if attributes else None
        response = queue.send_message(MessageAttributes=attributes,
          MessageBody=(json.dumps(payload)))
        return response.get('MessageId')