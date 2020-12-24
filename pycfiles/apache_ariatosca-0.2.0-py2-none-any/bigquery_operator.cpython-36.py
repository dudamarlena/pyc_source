# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 31785 bytes
__doc__ = '\nThis module contains Google BigQuery operators.\n'
import json
from typing import Iterable
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook, _parse_gcs_url
from airflow.exceptions import AirflowException
from airflow.models.baseoperator import BaseOperator, BaseOperatorLink
from airflow.models.taskinstance import TaskInstance
from airflow.utils.decorators import apply_defaults

class BigQueryConsoleLink(BaseOperatorLink):
    """BigQueryConsoleLink"""
    name = 'BigQuery Console'

    def get_link(self, operator, dttm):
        ti = TaskInstance(task=operator, execution_date=dttm)
        job_id = ti.xcom_pull(task_ids=(operator.task_id), key='job_id')
        if job_id:
            return 'https://console.cloud.google.com/bigquery?j={job_id}'.format(job_id=job_id)
        else:
            return ''


class BigQueryOperator(BaseOperator):
    """BigQueryOperator"""
    template_fields = ('bql', 'sql', 'destination_dataset_table', 'labels')
    template_ext = ('.sql', )
    ui_color = '#e4f0e8'
    operator_extra_links = (
     BigQueryConsoleLink(),)

    @apply_defaults
    def __init__(self, bql=None, sql=None, destination_dataset_table=None, write_disposition='WRITE_EMPTY', allow_large_results=False, flatten_results=None, bigquery_conn_id='bigquery_default', delegate_to=None, udf_config=None, use_legacy_sql=True, maximum_billing_tier=None, maximum_bytes_billed=None, create_disposition='CREATE_IF_NEEDED', schema_update_options=(), query_params=None, labels=None, priority='INTERACTIVE', time_partitioning=None, api_resource_configs=None, cluster_fields=None, location=None, encryption_configuration=None, *args, **kwargs):
        (super(BigQueryOperator, self).__init__)(*args, **kwargs)
        self.bql = bql
        self.sql = sql if sql else bql
        self.destination_dataset_table = destination_dataset_table
        self.write_disposition = write_disposition
        self.create_disposition = create_disposition
        self.allow_large_results = allow_large_results
        self.flatten_results = flatten_results
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to
        self.udf_config = udf_config
        self.use_legacy_sql = use_legacy_sql
        self.maximum_billing_tier = maximum_billing_tier
        self.maximum_bytes_billed = maximum_bytes_billed
        self.schema_update_options = schema_update_options
        self.query_params = query_params
        self.labels = labels
        self.bq_cursor = None
        self.priority = priority
        self.time_partitioning = time_partitioning
        self.api_resource_configs = api_resource_configs
        self.cluster_fields = cluster_fields
        self.location = location
        self.encryption_configuration = encryption_configuration
        if self.bql:
            import warnings
            warnings.warn(('Deprecated parameter `bql` used in Task id: {}. Use `sql` parameter instead to pass the sql to be executed. `bql` parameter is deprecated and will be removed in a future version of Airflow.'.format(self.task_id)),
              category=DeprecationWarning)
        if self.sql is None:
            raise TypeError('{} missing 1 required positional argument: `sql`'.format(self.task_id))

    def execute(self, context):
        if self.bq_cursor is None:
            self.log.info('Executing: %s', self.sql)
            hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id),
              use_legacy_sql=(self.use_legacy_sql),
              delegate_to=(self.delegate_to),
              location=(self.location))
            conn = hook.get_conn()
            self.bq_cursor = conn.cursor()
        else:
            if isinstance(self.sql, str):
                job_id = self.bq_cursor.run_query(sql=(self.sql),
                  destination_dataset_table=(self.destination_dataset_table),
                  write_disposition=(self.write_disposition),
                  allow_large_results=(self.allow_large_results),
                  flatten_results=(self.flatten_results),
                  udf_config=(self.udf_config),
                  maximum_billing_tier=(self.maximum_billing_tier),
                  maximum_bytes_billed=(self.maximum_bytes_billed),
                  create_disposition=(self.create_disposition),
                  query_params=(self.query_params),
                  labels=(self.labels),
                  schema_update_options=(self.schema_update_options),
                  priority=(self.priority),
                  time_partitioning=(self.time_partitioning),
                  api_resource_configs=(self.api_resource_configs),
                  cluster_fields=(self.cluster_fields),
                  encryption_configuration=(self.encryption_configuration))
            else:
                if isinstance(self.sql, Iterable):
                    job_id = [self.bq_cursor.run_query(sql=s, destination_dataset_table=(self.destination_dataset_table), write_disposition=(self.write_disposition), allow_large_results=(self.allow_large_results), flatten_results=(self.flatten_results), udf_config=(self.udf_config), maximum_billing_tier=(self.maximum_billing_tier), maximum_bytes_billed=(self.maximum_bytes_billed), create_disposition=(self.create_disposition), query_params=(self.query_params), labels=(self.labels), schema_update_options=(self.schema_update_options), priority=(self.priority), time_partitioning=(self.time_partitioning), api_resource_configs=(self.api_resource_configs), cluster_fields=(self.cluster_fields), encryption_configuration=(self.encryption_configuration)) for s in self.sql]
                else:
                    raise AirflowException("argument 'sql' of type {} is neither a string nor an iterable".format(type(str)))
        context['task_instance'].xcom_push(key='job_id', value=job_id)

    def on_kill(self):
        super(BigQueryOperator, self).on_kill()
        if self.bq_cursor is not None:
            self.log.info('Cancelling running query')
            self.bq_cursor.cancel_query()


class BigQueryCreateEmptyTableOperator(BaseOperator):
    """BigQueryCreateEmptyTableOperator"""
    template_fields = ('dataset_id', 'table_id', 'project_id', 'gcs_schema_object',
                       'labels')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, dataset_id, table_id, project_id=None, schema_fields=None, gcs_schema_object=None, time_partitioning=None, bigquery_conn_id='bigquery_default', google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, labels=None, encryption_configuration=None, *args, **kwargs):
        (super(BigQueryCreateEmptyTableOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.schema_fields = schema_fields
        self.gcs_schema_object = gcs_schema_object
        self.bigquery_conn_id = bigquery_conn_id
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to
        self.time_partitioning = {} if time_partitioning is None else time_partitioning
        self.labels = labels
        self.encryption_configuration = encryption_configuration

    def execute(self, context):
        bq_hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), delegate_to=(self.delegate_to))
        if not self.schema_fields:
            if self.gcs_schema_object:
                gcs_bucket, gcs_object = _parse_gcs_url(self.gcs_schema_object)
                gcs_hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
                  delegate_to=(self.delegate_to))
                schema_fields = json.loads(gcs_hook.download(gcs_bucket, gcs_object).decode('utf-8'))
        else:
            schema_fields = self.schema_fields
        conn = bq_hook.get_conn()
        cursor = conn.cursor()
        cursor.create_empty_table(project_id=(self.project_id),
          dataset_id=(self.dataset_id),
          table_id=(self.table_id),
          schema_fields=schema_fields,
          time_partitioning=(self.time_partitioning),
          labels=(self.labels),
          encryption_configuration=(self.encryption_configuration))


class BigQueryCreateExternalTableOperator(BaseOperator):
    """BigQueryCreateExternalTableOperator"""
    template_fields = ('bucket', 'source_objects', 'schema_object', 'destination_project_dataset_table',
                       'labels')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, source_objects, destination_project_dataset_table, schema_fields=None, schema_object=None, source_format='CSV', compression='NONE', skip_leading_rows=0, field_delimiter=',', max_bad_records=0, quote_character=None, allow_quoted_newlines=False, allow_jagged_rows=False, bigquery_conn_id='bigquery_default', google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, src_fmt_configs=None, labels=None, encryption_configuration=None, *args, **kwargs):
        (super(BigQueryCreateExternalTableOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.source_objects = source_objects
        self.schema_object = schema_object
        self.destination_project_dataset_table = destination_project_dataset_table
        self.schema_fields = schema_fields
        self.source_format = source_format
        self.compression = compression
        self.skip_leading_rows = skip_leading_rows
        self.field_delimiter = field_delimiter
        self.max_bad_records = max_bad_records
        self.quote_character = quote_character
        self.allow_quoted_newlines = allow_quoted_newlines
        self.allow_jagged_rows = allow_jagged_rows
        self.bigquery_conn_id = bigquery_conn_id
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to
        self.src_fmt_configs = src_fmt_configs if src_fmt_configs is not None else dict()
        self.labels = labels
        self.encryption_configuration = encryption_configuration

    def execute(self, context):
        bq_hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), delegate_to=(self.delegate_to))
        if not self.schema_fields:
            if self.schema_object:
                if self.source_format != 'DATASTORE_BACKUP':
                    gcs_hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
                      delegate_to=(self.delegate_to))
                    schema_fields = json.loads(gcs_hook.download(self.bucket, self.schema_object).decode('utf-8'))
        else:
            schema_fields = self.schema_fields
        source_uris = ['gs://{}/{}'.format(self.bucket, source_object) for source_object in self.source_objects]
        conn = bq_hook.get_conn()
        cursor = conn.cursor()
        cursor.create_external_table(external_project_dataset_table=(self.destination_project_dataset_table),
          schema_fields=schema_fields,
          source_uris=source_uris,
          source_format=(self.source_format),
          compression=(self.compression),
          skip_leading_rows=(self.skip_leading_rows),
          field_delimiter=(self.field_delimiter),
          max_bad_records=(self.max_bad_records),
          quote_character=(self.quote_character),
          allow_quoted_newlines=(self.allow_quoted_newlines),
          allow_jagged_rows=(self.allow_jagged_rows),
          src_fmt_configs=(self.src_fmt_configs),
          labels=(self.labels),
          encryption_configuration=(self.encryption_configuration))


class BigQueryDeleteDatasetOperator(BaseOperator):
    """BigQueryDeleteDatasetOperator"""
    template_fields = ('dataset_id', 'project_id')
    ui_color = '#f00004'

    @apply_defaults
    def __init__(self, dataset_id, project_id=None, bigquery_conn_id='bigquery_default', delegate_to=None, *args, **kwargs):
        self.dataset_id = dataset_id
        self.project_id = project_id
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to
        self.log.info('Dataset id: %s', self.dataset_id)
        self.log.info('Project id: %s', self.project_id)
        (super(BigQueryDeleteDatasetOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        bq_hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), delegate_to=(self.delegate_to))
        conn = bq_hook.get_conn()
        cursor = conn.cursor()
        cursor.delete_dataset(project_id=(self.project_id),
          dataset_id=(self.dataset_id))


class BigQueryCreateEmptyDatasetOperator(BaseOperator):
    """BigQueryCreateEmptyDatasetOperator"""
    template_fields = ('dataset_id', 'project_id')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, dataset_id, project_id=None, dataset_reference=None, bigquery_conn_id='bigquery_default', delegate_to=None, *args, **kwargs):
        self.dataset_id = dataset_id
        self.project_id = project_id
        self.bigquery_conn_id = bigquery_conn_id
        self.dataset_reference = dataset_reference if dataset_reference else {}
        self.delegate_to = delegate_to
        self.log.info('Dataset id: %s', self.dataset_id)
        self.log.info('Project id: %s', self.project_id)
        (super(BigQueryCreateEmptyDatasetOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        bq_hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), delegate_to=(self.delegate_to))
        conn = bq_hook.get_conn()
        cursor = conn.cursor()
        cursor.create_empty_dataset(project_id=(self.project_id),
          dataset_id=(self.dataset_id),
          dataset_reference=(self.dataset_reference))