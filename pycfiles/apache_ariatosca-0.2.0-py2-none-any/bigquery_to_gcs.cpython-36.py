# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4591 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class BigQueryToCloudStorageOperator(BaseOperator):
    """BigQueryToCloudStorageOperator"""
    template_fields = ('source_project_dataset_table', 'destination_cloud_storage_uris',
                       'labels')
    template_ext = ()
    ui_color = '#e4e6f0'

    @apply_defaults
    def __init__(self, source_project_dataset_table, destination_cloud_storage_uris, compression='NONE', export_format='CSV', field_delimiter=',', print_header=True, bigquery_conn_id='bigquery_default', delegate_to=None, labels=None, *args, **kwargs):
        (super(BigQueryToCloudStorageOperator, self).__init__)(*args, **kwargs)
        self.source_project_dataset_table = source_project_dataset_table
        self.destination_cloud_storage_uris = destination_cloud_storage_uris
        self.compression = compression
        self.export_format = export_format
        self.field_delimiter = field_delimiter
        self.print_header = print_header
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to
        self.labels = labels

    def execute(self, context):
        self.log.info('Executing extract of %s into: %s', self.source_project_dataset_table, self.destination_cloud_storage_uris)
        hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), delegate_to=(self.delegate_to))
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.run_extract(source_project_dataset_table=(self.source_project_dataset_table),
          destination_cloud_storage_uris=(self.destination_cloud_storage_uris),
          compression=(self.compression),
          export_format=(self.export_format),
          field_delimiter=(self.field_delimiter),
          print_header=(self.print_header),
          labels=(self.labels))