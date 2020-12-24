# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/generic_transfer.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3123 bytes
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base_hook import BaseHook

class GenericTransfer(BaseOperator):
    """GenericTransfer"""
    template_fields = ('sql', 'destination_table', 'preoperator')
    template_ext = ('.sql', '.hql')
    ui_color = '#b0f07c'

    @apply_defaults
    def __init__(self, sql, destination_table, source_conn_id, destination_conn_id, preoperator=None, *args, **kwargs):
        (super(GenericTransfer, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.destination_table = destination_table
        self.source_conn_id = source_conn_id
        self.destination_conn_id = destination_conn_id
        self.preoperator = preoperator

    def execute(self, context):
        source_hook = BaseHook.get_hook(self.source_conn_id)
        self.log.info('Extracting data from %s', self.source_conn_id)
        self.log.info('Executing: \n %s', self.sql)
        results = source_hook.get_records(self.sql)
        destination_hook = BaseHook.get_hook(self.destination_conn_id)
        if self.preoperator:
            self.log.info('Running preoperator')
            self.log.info(self.preoperator)
            destination_hook.run(self.preoperator)
        self.log.info('Inserting rows into %s', self.destination_conn_id)
        destination_hook.insert_rows(table=(self.destination_table), rows=results)