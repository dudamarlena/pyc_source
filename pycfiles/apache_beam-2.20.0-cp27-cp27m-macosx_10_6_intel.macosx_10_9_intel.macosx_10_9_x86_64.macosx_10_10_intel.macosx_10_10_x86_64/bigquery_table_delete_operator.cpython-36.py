# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_table_delete_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2764 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class BigQueryTableDeleteOperator(BaseOperator):
    """BigQueryTableDeleteOperator"""
    template_fields = ('deletion_dataset_table', )
    ui_color = '#ffd1dc'

    @apply_defaults
    def __init__(self, deletion_dataset_table, bigquery_conn_id='bigquery_default', delegate_to=None, ignore_if_missing=False, *args, **kwargs):
        (super(BigQueryTableDeleteOperator, self).__init__)(*args, **kwargs)
        self.deletion_dataset_table = deletion_dataset_table
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to
        self.ignore_if_missing = ignore_if_missing

    def execute(self, context):
        self.log.info('Deleting: %s', self.deletion_dataset_table)
        hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), delegate_to=(self.delegate_to))
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.run_table_delete(deletion_dataset_table=(self.deletion_dataset_table),
          ignore_if_missing=(self.ignore_if_missing))