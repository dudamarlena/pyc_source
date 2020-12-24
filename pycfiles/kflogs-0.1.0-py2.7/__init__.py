# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/kflogs/__init__.py
# Compiled at: 2017-04-26 02:53:10
"""
Amazon Kinesis Firehose logging handler and utilities
"""
__author__ = 'Masashi Terui <marcy9114+pypi@gmail.com>'
__status__ = 'beta'
__version__ = '0.1.0'
__date__ = '26 April 2017'
import logging, json

class KinesisFirehoseHandler(logging.Handler):
    """
    Amazon Kinesis Firehose logging handler
    """

    def __init__(self, *args, **kwargs):
        import boto3
        super(KinesisFirehoseHandler, self).__init__(level=kwargs.pop('level', logging.NOTSET))
        self.stream_name = kwargs.pop('stream_name', None)
        self.client = boto3.client('firehose', **kwargs)
        return

    def emit(self, record):
        try:
            self.client.put_record(DeliveryStreamName=self.stream_name, Record={'Data': self.format(record)})
        except:
            self.handleError(record)


class SimpleJsonFormatter(logging.Formatter):
    """
    Simply JSON log formatter for Amazon Kinesis Firehose logging
    """

    def format(self, record):
        ret = {}
        for attr, value in record.__dict__.items():
            if attr == 'asctime':
                value = self.formatTime(record)
            if attr == 'exc_info' and value is not None:
                value = self.formatException(value)
            if attr == 'stack_info' and value is not None:
                value = self.formatStack(value)
            ret[attr] = value

        return json.dumps(ret)