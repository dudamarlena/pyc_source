# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_to_bq.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 14174 bytes
import json
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageToBigQueryOperator(BaseOperator):
    __doc__ = '\n    Loads files from Google cloud storage into BigQuery.\n\n    The schema to be used for the BigQuery table may be specified in one of\n    two ways. You may either directly pass the schema fields in, or you may\n    point the operator to a Google cloud storage object name. The object in\n    Google cloud storage must be a JSON file with the schema fields in it.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GoogleCloudStorageToBigQueryOperator`\n\n    :param bucket: The bucket to load from. (templated)\n    :type bucket: str\n    :param source_objects: List of Google cloud storage URIs to load from. (templated)\n        If source_format is \'DATASTORE_BACKUP\', the list must only contain a single URI.\n    :type source_objects: list[str]\n    :param destination_project_dataset_table: The dotted\n        ``(<project>.|<project>:)<dataset>.<table>`` BigQuery table to load data into.\n        If ``<project>`` is not included, project will be the project defined in\n        the connection json. (templated)\n    :type destination_project_dataset_table: str\n    :param schema_fields: If set, the schema field list as defined here:\n        https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load\n        Should not be set when source_format is \'DATASTORE_BACKUP\'.\n        Parameter must be defined if \'schema_object\' is null and autodetect is False.\n    :type schema_fields: list\n    :param schema_object: If set, a GCS object path pointing to a .json file that\n        contains the schema for the table. (templated)\n        Parameter must be defined if \'schema_fields\' is null and autodetect is False.\n    :type schema_object: str\n    :param source_format: File format to export.\n    :type source_format: str\n    :param compression: [Optional] The compression type of the data source.\n        Possible values include GZIP and NONE.\n        The default value is NONE.\n        This setting is ignored for Google Cloud Bigtable,\n        Google Cloud Datastore backups and Avro formats.\n    :type compression: str\n    :param create_disposition: The create disposition if the table doesn\'t exist.\n    :type create_disposition: str\n    :param skip_leading_rows: Number of rows to skip when loading from a CSV.\n    :type skip_leading_rows: int\n    :param write_disposition: The write disposition if the table already exists.\n    :type write_disposition: str\n    :param field_delimiter: The delimiter to use when loading from a CSV.\n    :type field_delimiter: str\n    :param max_bad_records: The maximum number of bad records that BigQuery can\n        ignore when running the job.\n    :type max_bad_records: int\n    :param quote_character: The value that is used to quote data sections in a CSV file.\n    :type quote_character: str\n    :param ignore_unknown_values: [Optional] Indicates if BigQuery should allow\n        extra values that are not represented in the table schema.\n        If true, the extra values are ignored. If false, records with extra columns\n        are treated as bad records, and if there are too many bad records, an\n        invalid error is returned in the job result.\n    :type ignore_unknown_values: bool\n    :param allow_quoted_newlines: Whether to allow quoted newlines (true) or not (false).\n    :type allow_quoted_newlines: bool\n    :param allow_jagged_rows: Accept rows that are missing trailing optional columns.\n        The missing values are treated as nulls. If false, records with missing trailing\n        columns are treated as bad records, and if there are too many bad records, an\n        invalid error is returned in the job result. Only applicable to CSV, ignored\n        for other formats.\n    :type allow_jagged_rows: bool\n    :param max_id_key: If set, the name of a column in the BigQuery table\n        that\'s to be loaded. This will be used to select the MAX value from\n        BigQuery after the load occurs. The results will be returned by the\n        execute() command, which in turn gets stored in XCom for future\n        operators to use. This can be helpful with incremental loads--during\n        future executions, you can pick up from the max ID.\n    :type max_id_key: str\n    :param bigquery_conn_id: Reference to a specific BigQuery hook.\n    :type bigquery_conn_id: str\n    :param google_cloud_storage_conn_id: Reference to a specific Google\n        cloud storage hook.\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any. For this to\n        work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param schema_update_options: Allows the schema of the destination\n        table to be updated as a side effect of the load job.\n    :type schema_update_options: list\n    :param src_fmt_configs: configure optional fields specific to the source format\n    :type src_fmt_configs: dict\n    :param external_table: Flag to specify if the destination table should be\n        a BigQuery external table. Default Value is False.\n    :type external_table: bool\n    :param time_partitioning: configure optional time partitioning fields i.e.\n        partition by field, type and  expiration as per API specifications.\n        Note that \'field\' is not available in concurrency with\n        dataset.table$partition.\n    :type time_partitioning: dict\n    :param cluster_fields: Request that the result of this load be stored sorted\n        by one or more columns. This is only available in conjunction with\n        time_partitioning. The order of columns given determines the sort order.\n        Not applicable for external tables.\n    :type cluster_fields: list[str]\n    :param autodetect: [Optional] Indicates if we should automatically infer the\n        options and schema for CSV and JSON sources. (Default: ``True``).\n        Parameter must be setted to True if \'schema_fields\' and \'schema_object\' are undefined.\n        It is suggested to set to True if table are create outside of Airflow.\n    :type autodetect: bool\n    :param encryption_configuration: [Optional] Custom encryption configuration (e.g., Cloud KMS keys).\n        **Example**: ::\n\n            encryption_configuration = {\n                "kmsKeyName": "projects/testp/locations/us/keyRings/test-kr/cryptoKeys/test-key"\n            }\n    :type encryption_configuration: dict\n    '
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