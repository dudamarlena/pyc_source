# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_table_delete_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2764 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class BigQueryTableDeleteOperator(BaseOperator):
    __doc__ = '\n    Deletes BigQuery tables\n\n    :param deletion_dataset_table: A dotted\n        ``(<project>.|<project>:)<dataset>.<table>`` that indicates which table\n        will be deleted. (templated)\n    :type deletion_dataset_table: str\n    :param bigquery_conn_id: reference to a specific BigQuery hook.\n    :type bigquery_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param ignore_if_missing: if True, then return success even if the\n        requested table does not exist.\n    :type ignore_if_missing: bool\n    '
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