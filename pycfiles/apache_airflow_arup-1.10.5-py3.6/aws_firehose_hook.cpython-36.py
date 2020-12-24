# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/aws_firehose_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1837 bytes
from airflow.contrib.hooks.aws_hook import AwsHook

class AwsFirehoseHook(AwsHook):
    __doc__ = '\n    Interact with AWS Kinesis Firehose.\n    :param delivery_stream: Name of the delivery stream\n    :type delivery_stream: str\n    :param region_name: AWS region name (example: us-east-1)\n    :type region_name: str\n    '

    def __init__(self, delivery_stream, region_name=None, *args, **kwargs):
        self.delivery_stream = delivery_stream
        self.region_name = region_name
        (super(AwsFirehoseHook, self).__init__)(*args, **kwargs)

    def get_conn(self):
        """
        Returns AwsHook connection object.
        """
        self.conn = self.get_client_type('firehose', self.region_name)
        return self.conn

    def put_records(self, records):
        """
        Write batch records to Kinesis Firehose
        """
        firehose_conn = self.get_conn()
        response = firehose_conn.put_record_batch(DeliveryStreamName=(self.delivery_stream),
          Records=records)
        return response