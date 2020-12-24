# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/vertica_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1929 bytes
from airflow.contrib.hooks.vertica_hook import VerticaHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class VerticaOperator(BaseOperator):
    """VerticaOperator"""
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#b4e0ff'

    @apply_defaults
    def __init__(self, sql, vertica_conn_id='vertica_default', *args, **kwargs):
        (super(VerticaOperator, self).__init__)(*args, **kwargs)
        self.vertica_conn_id = vertica_conn_id
        self.sql = sql

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = VerticaHook(vertica_conn_id=(self.vertica_conn_id))
        hook.run(sql=(self.sql))