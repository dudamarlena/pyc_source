# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/aws_firehose_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1837 bytes
from airflow.contrib.hooks.aws_hook import AwsHook

class AwsFirehoseHook(AwsHook):
    """AwsFirehoseHook"""

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