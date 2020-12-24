# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_to_bq.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 14174 bytes
import json
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageToBigQueryOperator(BaseOperator):
    """GoogleCloudStorageToBigQueryOperator"""
    template_fields = ('bucket', 'source_objects', 'schema_object', 'destination_project_dataset_table')
    template_ext = ('.sql', )
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, source_objects, destination_project_dataset_table, schema_fields=None, schema_object=None, source_format='CSV', compression='NONE', create_disposition='CREATE_IF_NEEDED', skip_leading_rows=0, write_disposition='WRITE_EMPTY', field_delimiter=',', max_bad_records=0, quote_character=None, ignore_unknown_values=False, allow_quoted_newlines=False, allow_jagged_rows=False, max_id_key=None, bigquery_conn_id='bigquery_default', google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, schema_update_options=(), src_fmt_configs=None, external_table=False, time_partitioning=None, cluster_fields=None, autodetect=True, encryption_configuration=None, *args, **kwargs):
        (super(GoogleCloudStorageToBigQueryOperator, self).__init__)(*args, **kwargs)
        if src_fmt_configs is None:
            src_fmt_configs = {}
        if time_partitioning is None:
            time_partitioning = {}
        self.bucket = bucket
        self.source_objects = source_objects
        self.schema_object = schema_object
        self.destination_project_dataset_table = destination_project_dataset_table
        self.schema_fields = schema_fields
        self.source_format = source_format
        self.compression = compression
        self.create_disposition = create_disposition
        self.skip_leading_rows = skip_leading_rows
        self.write_disposition = write_disposition
        self.field_delimiter = field_delimiter
        self.max_bad_records = max_bad_records
        self.quote_character = quote_character
        self.ignore_unknown_values = ignore_unknown_values
        self.allow_quoted_newlines = allow_quoted_newlines
        self.allow_jagged_rows = allow_jagged_rows
        self.external_table = external_table
        self.max_id_key = max_id_key
        self.bigquery_conn_id = bigquery_conn_id
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to
        self.schema_update_options = schema_update_options
        self.src_fmt_configs = src_fmt_configs
        self.time_partitioning = time_partitioning
        self.cluster_fields = cluster_fields
        self.autodetect = autodetect
        self.encryption_configuration = encryption_configuration

    def execute(self, context):
        bq_hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), delegate_to=(self.delegate_to))
        if not self.schema_fields:
            if self.schema_object:
                if self.source_format != 'DATASTORE_BACKUP':
                    gcs_hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
                      delegate_to=(self.delegate_to))
                    schema_fields = json.loads(gcs_hook.download(self.bucket, self.schema_object).decode('utf-8'))
            if self.schema_object is None:
                if self.autodetect is False:
                    raise ValueError('At least one of `schema_fields`, `schema_object`, or `autodetect` must be passed.')
            schema_fields = None
        else:
            schema_fields = self.schema_fields
        source_uris = ['gs://{}/{}'.format(self.bucket, source_object) for source_object in self.source_objects]
        conn = bq_hook.get_conn()
        cursor = conn.cursor()
        if self.external_table:
            cursor.create_external_table(external_project_dataset_table=(self.destination_project_dataset_table),
              schema_fields=schema_fields,
              source_uris=source_uris,
              source_format=(self.source_format),
              compression=(self.compression),
              skip_leading_rows=(self.skip_leading_rows),
              field_delimiter=(self.field_delimiter),
              max_bad_records=(self.max_bad_records),
              quote_character=(self.quote_character),
              ignore_unknown_values=(self.ignore_unknown_values),
              allow_quoted_newlines=(self.allow_quoted_newlines),
              allow_jagged_rows=(self.allow_jagged_rows),
              src_fmt_configs=(self.src_fmt_configs),
              encryption_configuration=(self.encryption_configuration))
        else:
            cursor.run_load(destination_project_dataset_table=(self.destination_project_dataset_table),
              schema_fields=schema_fields,
              source_uris=source_uris,
              source_format=(self.source_format),
              autodetect=(self.autodetect),
              create_disposition=(self.create_disposition),
              skip_leading_rows=(self.skip_leading_rows),
              write_disposition=(self.write_disposition),
              field_delimiter=(self.field_delimiter),
              max_bad_records=(self.max_bad_records),
              quote_character=(self.quote_character),
              ignore_unknown_values=(self.ignore_unknown_values),
              allow_quoted_newlines=(self.allow_quoted_newlines),
              allow_jagged_rows=(self.allow_jagged_rows),
              schema_update_options=(self.schema_update_options),
              src_fmt_configs=(self.src_fmt_configs),
              time_partitioning=(self.time_partitioning),
              cluster_fields=(self.cluster_fields),
              encryption_configuration=(self.encryption_configuration))
        if self.max_id_key:
            cursor.execute('SELECT MAX({}) FROM {}'.format(self.max_id_key, self.destination_project_dataset_table))
            row = cursor.fetchone()
            max_id = row[0] if row[0] else 0
            self.log.info('Loaded BQ data with max %s.%s=%s', self.destination_project_dataset_table, self.max_id_key, max_id)
            return max_id