# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4591 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class BigQueryToCloudStorageOperator(BaseOperator):
    __doc__ = '\n    Transfers a BigQuery table to a Google Cloud Storage bucket.\n\n    .. seealso::\n        For more details about these parameters:\n        https://cloud.google.com/bigquery/docs/reference/v2/jobs\n\n    :param source_project_dataset_table: The dotted\n        ``(<project>.|<project>:)<dataset>.<table>`` BigQuery table to use as the\n        source data. If ``<project>`` is not included, project will be the project\n        defined in the connection json. (templated)\n    :type source_project_dataset_table: str\n    :param destination_cloud_storage_uris: The destination Google Cloud\n        Storage URI (e.g. gs://some-bucket/some-file.txt). (templated) Follows\n        convention defined here:\n        https://cloud.google.com/bigquery/exporting-data-from-bigquery#exportingmultiple\n    :type destination_cloud_storage_uris: list\n    :param compression: Type of compression to use.\n    :type compression: str\n    :param export_format: File format to export.\n    :type export_format: str\n    :param field_delimiter: The delimiter to use when extracting to a CSV.\n    :type field_delimiter: str\n    :param print_header: Whether to print a header for a CSV file extract.\n    :type print_header: bool\n    :param bigquery_conn_id: reference to a specific BigQuery hook.\n    :type bigquery_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param labels: a dictionary containing labels for the job/query,\n        passed to BigQuery\n    :type labels: dict\n    '
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