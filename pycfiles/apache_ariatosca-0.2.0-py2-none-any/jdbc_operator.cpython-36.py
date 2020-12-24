# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/jdbc_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2355 bytes
from airflow.hooks.jdbc_hook import JdbcHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class JdbcOperator(BaseOperator):
    """JdbcOperator"""
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql, jdbc_conn_id='jdbc_default', autocommit=False, parameters=None, *args, **kwargs):
        (super(JdbcOperator, self).__init__)(*args, **kwargs)
        self.parameters = parameters
        self.sql = sql
        self.jdbc_conn_id = jdbc_conn_id
        self.autocommit = autocommit

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        self.hook = JdbcHook(jdbc_conn_id=(self.jdbc_conn_id))
        self.hook.run((self.sql), (self.autocommit), parameters=(self.parameters))