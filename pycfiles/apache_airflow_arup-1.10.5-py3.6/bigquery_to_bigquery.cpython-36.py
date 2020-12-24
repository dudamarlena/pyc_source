# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_to_bigquery.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4743 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class BigQueryToBigQueryOperator(BaseOperator):
    __doc__ = '\n    Copies data from one BigQuery table to another.\n\n    .. seealso::\n        For more details about these parameters:\n        https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.copy\n\n    :param source_project_dataset_tables: One or more\n        dotted ``(project:|project.)<dataset>.<table>`` BigQuery tables to use as the\n        source data. If ``<project>`` is not included, project will be the\n        project defined in the connection json. Use a list if there are multiple\n        source tables. (templated)\n    :type source_project_dataset_tables: list|string\n    :param destination_project_dataset_table: The destination BigQuery\n        table. Format is: ``(project:|project.)<dataset>.<table>`` (templated)\n    :type destination_project_dataset_table: str\n    :param write_disposition: The write disposition if the table already exists.\n    :type write_disposition: str\n    :param create_disposition: The create disposition if the table doesn\'t exist.\n    :type create_disposition: str\n    :param bigquery_conn_id: reference to a specific BigQuery hook.\n    :type bigquery_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param labels: a dictionary containing labels for the job/query,\n        passed to BigQuery\n    :type labels: dict\n    :param encryption_configuration: [Optional] Custom encryption configuration (e.g., Cloud KMS keys).\n        **Example**: ::\n\n            encryption_configuration = {\n                "kmsKeyName": "projects/testp/locations/us/keyRings/test-kr/cryptoKeys/test-key"\n            }\n    :type encryption_configuration: dict\n    '
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