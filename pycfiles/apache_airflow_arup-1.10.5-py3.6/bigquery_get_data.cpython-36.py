# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_get_data.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4687 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class BigQueryGetDataOperator(BaseOperator):
    __doc__ = "\n    Fetches the data from a BigQuery table (alternatively fetch data for selected columns)\n    and returns data in a python list. The number of elements in the returned list will\n    be equal to the number of rows fetched. Each element in the list will again be a list\n    where element would represent the columns values for that row.\n\n    **Example Result**: ``[['Tony', '10'], ['Mike', '20'], ['Steve', '15']]``\n\n    .. note::\n        If you pass fields to ``selected_fields`` which are in different order than the\n        order of columns already in\n        BQ table, the data will still be in the order of BQ table.\n        For example if the BQ table has 3 columns as\n        ``[A,B,C]`` and you pass 'B,A' in the ``selected_fields``\n        the data would still be of the form ``'A,B'``.\n\n    **Example**: ::\n\n        get_data = BigQueryGetDataOperator(\n            task_id='get_data_from_bq',\n            dataset_id='test_dataset',\n            table_id='Transaction_partitions',\n            max_results='100',\n            selected_fields='DATE',\n            bigquery_conn_id='airflow-service-account'\n        )\n\n    :param dataset_id: The dataset ID of the requested table. (templated)\n    :type dataset_id: str\n    :param table_id: The table ID of the requested table. (templated)\n    :type table_id: str\n    :param max_results: The maximum number of records (rows) to be fetched\n        from the table. (templated)\n    :type max_results: str\n    :param selected_fields: List of fields to return (comma-separated). If\n        unspecified, all fields are returned.\n    :type selected_fields: str\n    :param bigquery_conn_id: reference to a specific BigQuery hook.\n    :type bigquery_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    "
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