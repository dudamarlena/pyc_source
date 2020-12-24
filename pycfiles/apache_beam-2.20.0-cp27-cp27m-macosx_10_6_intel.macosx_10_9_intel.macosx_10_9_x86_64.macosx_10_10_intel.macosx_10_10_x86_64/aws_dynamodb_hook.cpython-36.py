# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/aws_dynamodb_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2370 bytes
from airflow.exceptions import AirflowException
from airflow.contrib.hooks.aws_hook import AwsHook

class AwsDynamoDBHook(AwsHook):
    """AwsDynamoDBHook"""

    def __init__(self, table_keys=None, table_name=None, region_name=None, *args, **kwargs):
        self.table_keys = table_keys
        self.table_name = table_name
        self.region_name = region_name
        (super(AwsDynamoDBHook, self).__init__)(*args, **kwargs)

    def get_conn(self):
        self.conn = self.get_resource_type('dynamodb', self.region_name)
        return self.conn

    def write_batch_data(self, items):
        """
        Write batch items to dynamodb table with provisioned throughout capacity.
        """
        dynamodb_conn = self.get_conn()
        try:
            table = dynamodb_conn.Table(self.table_name)
            with table.batch_writer(overwrite_by_pkeys=(self.table_keys)) as (batch):
                for item in items:
                    batch.put_item(Item=item)

            return True
        except Exception as general_error:
            raise AirflowException('Failed to insert items in dynamodb, error: {error}'.format(error=(str(general_error))))