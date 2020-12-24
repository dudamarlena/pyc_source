# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/aws_dynamodb_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2370 bytes
from airflow.exceptions import AirflowException
from airflow.contrib.hooks.aws_hook import AwsHook

class AwsDynamoDBHook(AwsHook):
    __doc__ = '\n    Interact with AWS DynamoDB.\n\n    :param table_keys: partition key and sort key\n    :type table_keys: list\n    :param table_name: target DynamoDB table\n    :type table_name: str\n    :param region_name: aws region name (example: us-east-1)\n    :type region_name: str\n    '

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