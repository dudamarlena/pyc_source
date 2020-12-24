# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_get_data.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4687 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class BigQueryGetDataOperator(BaseOperator):
    """BigQueryGetDataOperator"""
    template_fields = ('dataset_id', 'table_id', 'max_results')
    ui_color = '#e4f0e8'

    @apply_defaults
    def __init__(self, dataset_id, table_id, max_results='100', selected_fields=None, bigquery_conn_id='bigquery_default', delegate_to=None, *args, **kwargs):
        (super(BigQueryGetDataOperator, self).__init__)(*args, **kwargs)
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.max_results = max_results
        self.selected_fields = selected_fields
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        self.log.info('Fetching Data from:')
        self.log.info('Dataset: %s ; Table: %s ; Max Results: %s', self.dataset_id, self.table_id, self.max_results)
        hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), delegate_to=(self.delegate_to))
        conn = hook.get_conn()
        cursor = conn.cursor()
        response = cursor.get_tabledata(dataset_id=(self.dataset_id), table_id=(self.table_id),
          max_results=(self.max_results),
          selected_fields=(self.selected_fields))
        self.log.info('Total Extracted rows: %s', response['totalRows'])
        rows = response['rows']
        table_data = []
        for dict_row in rows:
            single_row = []
            for fields in dict_row['f']:
                single_row.append(fields['v'])

            table_data.append(single_row)

        return table_data