# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_to_bigquery.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4743 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class BigQueryToBigQueryOperator(BaseOperator):
    """BigQueryToBigQueryOperator"""
    template_fields = ('source_project_dataset_tables', 'destination_project_dataset_table',
                       'labels')
    template_ext = ('.sql', )
    ui_color = '#e6f0e4'

    @apply_defaults
    def __init__(self, source_project_dataset_tables, destination_project_dataset_table, write_disposition='WRITE_EMPTY', create_disposition='CREATE_IF_NEEDED', bigquery_conn_id='bigquery_default', delegate_to=None, labels=None, encryption_configuration=None, *args, **kwargs):
        (super(BigQueryToBigQueryOperator, self).__init__)(*args, **kwargs)
        self.source_project_dataset_tables = source_project_dataset_tables
        self.destination_project_dataset_table = destination_project_dataset_table
        self.write_disposition = write_disposition
        self.create_disposition = create_disposition
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to
        self.labels = labels
        self.encryption_configuration = encryption_configuration

    def execute(self, context):
        self.log.info('Executing copy of %s into: %s', self.source_project_dataset_tables, self.destination_project_dataset_table)
        hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), delegate_to=(self.delegate_to))
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.run_copy(source_project_dataset_tables=(self.source_project_dataset_tables),
          destination_project_dataset_table=(self.destination_project_dataset_table),
          write_disposition=(self.write_disposition),
          create_disposition=(self.create_disposition),
          labels=(self.labels),
          encryption_configuration=(self.encryption_configuration))