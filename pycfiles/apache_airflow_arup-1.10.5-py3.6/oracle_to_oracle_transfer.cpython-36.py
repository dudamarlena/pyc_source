# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/oracle_to_oracle_transfer.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3698 bytes
from airflow.hooks.oracle_hook import OracleHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class OracleToOracleTransfer(BaseOperator):
    __doc__ = '\n    Moves data from Oracle to Oracle.\n\n\n    :param oracle_destination_conn_id: destination Oracle connection.\n    :type oracle_destination_conn_id: str\n    :param destination_table: destination table to insert rows.\n    :type destination_table: str\n    :param oracle_source_conn_id: source Oracle connection.\n    :type oracle_source_conn_id: str\n    :param source_sql: SQL query to execute against the source Oracle\n        database. (templated)\n    :type source_sql: str\n    :param source_sql_params: Parameters to use in sql query. (templated)\n    :type source_sql_params: dict\n    :param rows_chunk: number of rows per chunk to commit.\n    :type rows_chunk: int\n    '
    template_fields = ('source_sql', 'source_sql_params')
    ui_color = '#e08c8c'

    @apply_defaults
    def __init__(self, oracle_destination_conn_id, destination_table, oracle_source_conn_id, source_sql, source_sql_params=None, rows_chunk=5000, *args, **kwargs):
        (super(OracleToOracleTransfer, self).__init__)(*args, **kwargs)
        if source_sql_params is None:
            source_sql_params = {}
        self.oracle_destination_conn_id = oracle_destination_conn_id
        self.destination_table = destination_table
        self.oracle_source_conn_id = oracle_source_conn_id
        self.source_sql = source_sql
        self.source_sql_params = source_sql_params
        self.rows_chunk = rows_chunk

    def _execute(self, src_hook, dest_hook, context):
        with src_hook.get_conn() as (src_conn):
            cursor = src_conn.cursor()
            self.log.info('Querying data from source: %s', self.oracle_source_conn_id)
            cursor.execute(self.source_sql, self.source_sql_params)
            target_fields = list(map(lambda field: field[0], cursor.description))
            rows_total = 0
            rows = cursor.fetchmany(self.rows_chunk)
            while len(rows) > 0:
                rows_total = rows_total + len(rows)
                dest_hook.bulk_insert_rows((self.destination_table), rows, target_fields=target_fields,
                  commit_every=(self.rows_chunk))
                rows = cursor.fetchmany(self.rows_chunk)
                self.log.info('Total inserted: %s rows', rows_total)

            self.log.info('Finished data transfer.')
            cursor.close()

    def execute(self, context):
        src_hook = OracleHook(oracle_conn_id=(self.oracle_source_conn_id))
        dest_hook = OracleHook(oracle_conn_id=(self.oracle_destination_conn_id))
        self._execute(src_hook, dest_hook, context)