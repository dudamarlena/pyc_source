# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/mssql_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2437 bytes
from airflow.hooks.mssql_hook import MsSqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class MsSqlOperator(BaseOperator):
    """MsSqlOperator"""
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql, mssql_conn_id='mssql_default', parameters=None, autocommit=False, database=None, *args, **kwargs):
        (super(MsSqlOperator, self).__init__)(*args, **kwargs)
        self.mssql_conn_id = mssql_conn_id
        self.sql = sql
        self.parameters = parameters
        self.autocommit = autocommit
        self.database = database

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = MsSqlHook(mssql_conn_id=(self.mssql_conn_id), schema=(self.database))
        hook.run((self.sql), autocommit=(self.autocommit), parameters=(self.parameters))