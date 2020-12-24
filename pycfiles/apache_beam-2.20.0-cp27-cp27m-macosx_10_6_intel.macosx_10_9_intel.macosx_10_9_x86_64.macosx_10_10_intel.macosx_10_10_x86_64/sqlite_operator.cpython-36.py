# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/sqlite_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2037 bytes
from airflow.hooks.sqlite_hook import SqliteHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SqliteOperator(BaseOperator):
    """SqliteOperator"""
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#cdaaed'

    @apply_defaults
    def __init__(self, sql, sqlite_conn_id='sqlite_default', parameters=None, *args, **kwargs):
        (super(SqliteOperator, self).__init__)(*args, **kwargs)
        self.sqlite_conn_id = sqlite_conn_id
        self.sql = sql
        self.parameters = parameters or []

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = SqliteHook(sqlite_conn_id=(self.sqlite_conn_id))
        hook.run((self.sql), parameters=(self.parameters))