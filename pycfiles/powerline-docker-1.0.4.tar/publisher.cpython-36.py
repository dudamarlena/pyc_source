# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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