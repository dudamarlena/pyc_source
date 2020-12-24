# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/hive_to_dynamodb.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4084 bytes
import json
from airflow.contrib.hooks.aws_dynamodb_hook import AwsDynamoDBHook
from airflow.hooks.hive_hooks import HiveServer2Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class HiveToDynamoDBTransferOperator(BaseOperator):
    """HiveToDynamoDBTransferOperator"""
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#a0e08c'

    @apply_defaults
    def __init__(self, sql, table_name, table_keys, pre_process=None, pre_process_args=None, pre_process_kwargs=None, region_name=None, schema='default', hiveserver2_conn_id='hiveserver2_default', aws_conn_id='aws_default', *args, **kwargs):
        (super(HiveToDynamoDBTransferOperator, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.table_name = table_name
        self.table_keys = table_keys
        self.pre_process = pre_process
        self.pre_process_args = pre_process_args
        self.pre_process_kwargs = pre_process_kwargs
        self.region_name = region_name
        self.schema = schema
        self.hiveserver2_conn_id = hiveserver2_conn_id
        self.aws_conn_id = aws_conn_id

    def execute(self, context):
        hive = HiveServer2Hook(hiveserver2_conn_id=(self.hiveserver2_conn_id))
        self.log.info('Extracting data from Hive')
        self.log.info(self.sql)
        data = hive.get_pandas_df((self.sql), schema=(self.schema))
        dynamodb = AwsDynamoDBHook(aws_conn_id=(self.aws_conn_id), table_name=(self.table_name),
          table_keys=(self.table_keys),
          region_name=(self.region_name))
        self.log.info('Inserting rows into dynamodb')
        if self.pre_process is None:
            dynamodb.write_batch_data(json.loads(data.to_json(orient='records')))
        else:
            dynamodb.write_batch_data(self.pre_process(data=data, args=(self.pre_process_args),
              kwargs=(self.pre_process_kwargs)))
        self.log.info('Done.')