# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/generic_transfer.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3123 bytes
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base_hook import BaseHook

class GenericTransfer(BaseOperator):
    __doc__ = '\n    Moves data from a connection to another, assuming that they both\n    provide the required methods in their respective hooks. The source hook\n    needs to expose a `get_records` method, and the destination a\n    `insert_rows` method.\n\n    This is meant to be used on small-ish datasets that fit in memory.\n\n    :param sql: SQL query to execute against the source database. (templated)\n    :type sql: str\n    :param destination_table: target table. (templated)\n    :type destination_table: str\n    :param source_conn_id: source connection\n    :type source_conn_id: str\n    :param destination_conn_id: source connection\n    :type destination_conn_id: str\n    :param preoperator: sql statement or list of statements to be\n        executed prior to loading the data. (templated)\n    :type preoperator: str or list[str]\n    '
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