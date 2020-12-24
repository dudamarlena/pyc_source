# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/postgres_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2696 bytes
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class PostgresOperator(BaseOperator):
    """PostgresOperator"""
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql, postgres_conn_id='postgres_default', autocommit=False, parameters=None, database=None, *args, **kwargs):
        (super(PostgresOperator, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.postgres_conn_id = postgres_conn_id
        self.autocommit = autocommit
        self.parameters = parameters
        self.database = database

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        self.hook = PostgresHook(postgres_conn_id=(self.postgres_conn_id), schema=(self.database))
        self.hook.run((self.sql), (self.autocommit), parameters=(self.parameters))
        for output in self.hook.conn.notices:
            self.log.info(output)