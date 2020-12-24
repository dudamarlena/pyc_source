# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/snowflake_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3034 bytes
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SnowflakeOperator(BaseOperator):
    """SnowflakeOperator"""
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql, snowflake_conn_id='snowflake_default', parameters=None, autocommit=True, warehouse=None, database=None, role=None, schema=None, *args, **kwargs):
        (super(SnowflakeOperator, self).__init__)(*args, **kwargs)
        self.snowflake_conn_id = snowflake_conn_id
        self.sql = sql
        self.autocommit = autocommit
        self.parameters = parameters
        self.warehouse = warehouse
        self.database = database
        self.role = role
        self.schema = schema

    def get_hook(self):
        return SnowflakeHook(snowflake_conn_id=(self.snowflake_conn_id), warehouse=(self.warehouse),
          database=(self.database),
          role=(self.role),
          schema=(self.schema))

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = self.get_hook()
        hook.run((self.sql),
          autocommit=(self.autocommit),
          parameters=(self.parameters))