# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 31785 bytes
"""
This module contains Google BigQuery operators.
"""
import json
from typing import Iterable
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook, _parse_gcs_url
from airflow.exceptions import AirflowException
from airflow.models.baseoperator import BaseOperator, BaseOperatorLink
from airflow.models.taskinstance import TaskInstance
from airflow.utils.decorators import apply_defaults

class BigQueryConsoleLink(BaseOperatorLink):
    __doc__ = '\n    Helper class for constructing BigQuery link.\n    '
    name = 'BigQuery Console'

    def get_link(self, operator, dttm):
        ti = TaskInstance(task=operator, execution_date=dttm)
        job_id = ti.xcom_pull(task_ids=(operator.task_id), key='job_id')
        if job_id:
            return 'https://console.cloud.google.com/bigquery?j={job_id}'.format(job_id=job_id)
        else:
            return ''


class BigQueryOperator(BaseOperator):
    __doc__ = '\n    Executes BigQuery SQL queries in a specific BigQuery database\n\n    :param bql: (Deprecated. Use `sql` parameter instead) the sql code to be\n        executed (templated)\n    :type bql: Can receive a str representing a sql statement,\n        a list of str (sql statements), or reference to a template file.\n        Template reference are recognized by str ending in \'.sql\'.\n    :param sql: the sql code to be executed (templated)\n    :type sql: Can receive a str representing a sql statement,\n        a list of str (sql statements), or reference to a template file.\n        Template reference are recognized by str ending in \'.sql\'.\n    :param destination_dataset_table: A dotted\n        ``(<project>.|<project>:)<dataset>.<table>`` that, if set, will store the results\n        of the query. (templated)\n    :type destination_dataset_table: str\n    :param write_disposition: Specifies the action that occurs if the destination table\n        already exists. (default: \'WRITE_EMPTY\')\n    :type write_disposition: str\n    :param create_disposition: Specifies whether the job is allowed to create new tables.\n        (default: \'CREATE_IF_NEEDED\')\n    :type create_disposition: str\n    :param allow_large_results: Whether to allow large results.\n    :type allow_large_results: bool\n    :param flatten_results: If true and query uses legacy SQL dialect, flattens\n        all nested and repeated fields in the query results. ``allow_large_results``\n        must be ``true`` if this is set to ``false``. For standard SQL queries, this\n        flag is ignored and results are never flattened.\n    :type flatten_results: bool\n    :param bigquery_conn_id: reference to a specific BigQuery hook.\n    :type bigquery_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param udf_config: The User Defined Function configuration for the query.\n        See https://cloud.google.com/bigquery/user-defined-functions for details.\n    :type udf_config: list\n    :param use_legacy_sql: Whether to use legacy SQL (true) or standard SQL (false).\n    :type use_legacy_sql: bool\n    :param maximum_billing_tier: Positive integer that serves as a multiplier\n        of the basic price.\n        Defaults to None, in which case it uses the value set in the project.\n    :type maximum_billing_tier: int\n    :param maximum_bytes_billed: Limits the bytes billed for this job.\n        Queries that will have bytes billed beyond this limit will fail\n        (without incurring a charge). If unspecified, this will be\n        set to your project default.\n    :type maximum_bytes_billed: float\n    :param api_resource_configs: a dictionary that contain params\n        \'configuration\' applied for Google BigQuery Jobs API:\n        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs\n        for example, {\'query\': {\'useQueryCache\': False}}. You could use it\n        if you need to provide some params that are not supported by BigQueryOperator\n        like args.\n    :type api_resource_configs: dict\n    :param schema_update_options: Allows the schema of the destination\n        table to be updated as a side effect of the load job.\n    :type schema_update_options: Optional[Union[list, tuple, set]]\n    :param query_params: a list of dictionary containing query parameter types and\n        values, passed to BigQuery. The structure of dictionary should look like\n        \'queryParameters\' in Google BigQuery Jobs API:\n        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs.\n        For example, [{ \'name\': \'corpus\', \'parameterType\': { \'type\': \'STRING\' },\n        \'parameterValue\': { \'value\': \'romeoandjuliet\' } }].\n    :type query_params: list\n    :param labels: a dictionary containing labels for the job/query,\n        passed to BigQuery\n    :type labels: dict\n    :param priority: Specifies a priority for the query.\n        Possible values include INTERACTIVE and BATCH.\n        The default value is INTERACTIVE.\n    :type priority: str\n    :param time_partitioning: configure optional time partitioning fields i.e.\n        partition by field, type and expiration as per API specifications.\n    :type time_partitioning: dict\n    :param cluster_fields: Request that the result of this query be stored sorted\n        by one or more columns. This is only available in conjunction with\n        time_partitioning. The order of columns given determines the sort order.\n    :type cluster_fields: list[str]\n    :param location: The geographic location of the job. Required except for\n        US and EU. See details at\n        https://cloud.google.com/bigquery/docs/locations#specifying_your_location\n    :type location: str\n    :param encryption_configuration: [Optional] Custom encryption configuration (e.g., Cloud KMS keys).\n        **Example**: ::\n\n            encryption_configuration = {\n                "kmsKeyName": "projects/testp/locations/us/keyRings/test-kr/cryptoKeys/test-key"\n            }\n    :type encryption_configuration: dict\n    '
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
    __doc__ = '\n    Creates a new, empty table in the specified BigQuery dataset,\n    optionally with schema.\n\n    The schema to be used for the BigQuery table may be specified in one of\n    two ways. You may either directly pass the schema fields in, or you may\n    point the operator to a Google cloud storage object name. The object in\n    Google cloud storage must be a JSON file with the schema fields in it.\n    You can also create a table without schema.\n\n    :param project_id: The project to create the table into. (templated)\n    :type project_id: str\n    :param dataset_id: The dataset to create the table into. (templated)\n    :type dataset_id: str\n    :param table_id: The Name of the table to be created. (templated)\n    :type table_id: str\n    :param schema_fields: If set, the schema field list as defined here:\n        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.schema\n\n        **Example**: ::\n\n            schema_fields=[{"name": "emp_name", "type": "STRING", "mode": "REQUIRED"},\n                           {"name": "salary", "type": "INTEGER", "mode": "NULLABLE"}]\n\n    :type schema_fields: list\n    :param gcs_schema_object: Full path to the JSON file containing\n        schema (templated). For\n        example: ``gs://test-bucket/dir1/dir2/employee_schema.json``\n    :type gcs_schema_object: str\n    :param time_partitioning: configure optional time partitioning fields i.e.\n        partition by field, type and  expiration as per API specifications.\n\n        .. seealso::\n            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#timePartitioning\n    :type time_partitioning: dict\n    :param bigquery_conn_id: Reference to a specific BigQuery hook.\n    :type bigquery_conn_id: str\n    :param google_cloud_storage_conn_id: Reference to a specific Google\n        cloud storage hook.\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any. For this to\n        work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param labels: a dictionary containing labels for the table, passed to BigQuery\n\n        **Example (with schema JSON in GCS)**: ::\n\n            CreateTable = BigQueryCreateEmptyTableOperator(\n                task_id=\'BigQueryCreateEmptyTableOperator_task\',\n                dataset_id=\'ODS\',\n                table_id=\'Employees\',\n                project_id=\'internal-gcp-project\',\n                gcs_schema_object=\'gs://schema-bucket/employee_schema.json\',\n                bigquery_conn_id=\'airflow-service-account\',\n                google_cloud_storage_conn_id=\'airflow-service-account\'\n            )\n\n        **Corresponding Schema file** (``employee_schema.json``): ::\n\n            [\n              {\n                "mode": "NULLABLE",\n                "name": "emp_name",\n                "type": "STRING"\n              },\n              {\n                "mode": "REQUIRED",\n                "name": "salary",\n                "type": "INTEGER"\n              }\n            ]\n\n        **Example (with schema in the DAG)**: ::\n\n            CreateTable = BigQueryCreateEmptyTableOperator(\n                task_id=\'BigQueryCreateEmptyTableOperator_task\',\n                dataset_id=\'ODS\',\n                table_id=\'Employees\',\n                project_id=\'internal-gcp-project\',\n                schema_fields=[{"name": "emp_name", "type": "STRING", "mode": "REQUIRED"},\n                               {"name": "salary", "type": "INTEGER", "mode": "NULLABLE"}],\n                bigquery_conn_id=\'airflow-service-account\',\n                google_cloud_storage_conn_id=\'airflow-service-account\'\n            )\n    :type labels: dict\n    :param encryption_configuration: [Optional] Custom encryption configuration (e.g., Cloud KMS keys).\n        **Example**: ::\n\n            encryption_configuration = {\n                "kmsKeyName": "projects/testp/locations/us/keyRings/test-kr/cryptoKeys/test-key"\n            }\n    :type encryption_configuration: dict\n    '
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
    __doc__ = '\n    Creates a new external table in the dataset with the data in Google Cloud\n    Storage.\n\n    The schema to be used for the BigQuery table may be specified in one of\n    two ways. You may either directly pass the schema fields in, or you may\n    point the operator to a Google cloud storage object name. The object in\n    Google cloud storage must be a JSON file with the schema fields in it.\n\n    :param bucket: The bucket to point the external table to. (templated)\n    :type bucket: str\n    :param source_objects: List of Google cloud storage URIs to point\n        table to. (templated)\n        If source_format is \'DATASTORE_BACKUP\', the list must only contain a single URI.\n    :type source_objects: list\n    :param destination_project_dataset_table: The dotted ``(<project>.)<dataset>.<table>``\n        BigQuery table to load data into (templated). If ``<project>`` is not included,\n        project will be the project defined in the connection json.\n    :type destination_project_dataset_table: str\n    :param schema_fields: If set, the schema field list as defined here:\n        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.schema\n\n        **Example**: ::\n\n            schema_fields=[{"name": "emp_name", "type": "STRING", "mode": "REQUIRED"},\n                           {"name": "salary", "type": "INTEGER", "mode": "NULLABLE"}]\n\n        Should not be set when source_format is \'DATASTORE_BACKUP\'.\n    :type schema_fields: list\n    :param schema_object: If set, a GCS object path pointing to a .json file that\n        contains the schema for the table. (templated)\n    :type schema_object: str\n    :param source_format: File format of the data.\n    :type source_format: str\n    :param compression: [Optional] The compression type of the data source.\n        Possible values include GZIP and NONE.\n        The default value is NONE.\n        This setting is ignored for Google Cloud Bigtable,\n        Google Cloud Datastore backups and Avro formats.\n    :type compression: str\n    :param skip_leading_rows: Number of rows to skip when loading from a CSV.\n    :type skip_leading_rows: int\n    :param field_delimiter: The delimiter to use for the CSV.\n    :type field_delimiter: str\n    :param max_bad_records: The maximum number of bad records that BigQuery can\n        ignore when running the job.\n    :type max_bad_records: int\n    :param quote_character: The value that is used to quote data sections in a CSV file.\n    :type quote_character: str\n    :param allow_quoted_newlines: Whether to allow quoted newlines (true) or not (false).\n    :type allow_quoted_newlines: bool\n    :param allow_jagged_rows: Accept rows that are missing trailing optional columns.\n        The missing values are treated as nulls. If false, records with missing trailing\n        columns are treated as bad records, and if there are too many bad records, an\n        invalid error is returned in the job result. Only applicable to CSV, ignored\n        for other formats.\n    :type allow_jagged_rows: bool\n    :param bigquery_conn_id: Reference to a specific BigQuery hook.\n    :type bigquery_conn_id: str\n    :param google_cloud_storage_conn_id: Reference to a specific Google\n        cloud storage hook.\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any. For this to\n        work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param src_fmt_configs: configure optional fields specific to the source format\n    :type src_fmt_configs: dict\n    :param labels: a dictionary containing labels for the table, passed to BigQuery\n    :type labels: dict\n    :param encryption_configuration: [Optional] Custom encryption configuration (e.g., Cloud KMS keys).\n        **Example**: ::\n\n            encryption_configuration = {\n                "kmsKeyName": "projects/testp/locations/us/keyRings/test-kr/cryptoKeys/test-key"\n            }\n    :type encryption_configuration: dict\n    '
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
    __doc__ = "\n    This operator deletes an existing dataset from your Project in Big query.\n    https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/delete\n\n    :param project_id: The project id of the dataset.\n    :type project_id: str\n    :param dataset_id: The dataset to be deleted.\n    :type dataset_id: str\n\n    **Example**: ::\n\n        delete_temp_data = BigQueryDeleteDatasetOperator(dataset_id = 'temp-dataset',\n                                                         project_id = 'temp-project',\n                                                         bigquery_conn_id='_my_gcp_conn_',\n                                                         task_id='Deletetemp',\n                                                         dag=dag)\n    "
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
    __doc__ = '\n    This operator is used to create new dataset for your Project in Big query.\n    https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#resource\n\n    :param project_id: The name of the project where we want to create the dataset.\n        Don\'t need to provide, if projectId in dataset_reference.\n    :type project_id: str\n    :param dataset_id: The id of dataset. Don\'t need to provide,\n        if datasetId in dataset_reference.\n    :type dataset_id: str\n    :param dataset_reference: Dataset reference that could be provided with request body.\n        More info:\n        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#resource\n    :type dataset_reference: dict\n\n        **Example**: ::\n\n            create_new_dataset = BigQueryCreateEmptyDatasetOperator(\n                                    dataset_id = \'new-dataset\',\n                                    project_id = \'my-project\',\n                                    dataset_reference = {"friendlyName": "New Dataset"}\n                                    bigquery_conn_id=\'_my_gcp_conn_\',\n                                    task_id=\'newDatasetCreator\',\n                                    dag=dag)\n\n    '
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