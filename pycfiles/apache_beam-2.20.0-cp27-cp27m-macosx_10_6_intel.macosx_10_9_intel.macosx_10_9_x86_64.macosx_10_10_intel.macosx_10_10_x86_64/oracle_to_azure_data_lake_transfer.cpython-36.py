# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/oracle_to_azure_data_lake_transfer.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4641 bytes
from airflow.hooks.oracle_hook import OracleHook
from airflow.contrib.hooks.azure_data_lake_hook import AzureDataLakeHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.file import TemporaryDirectory
import unicodecsv as csv, os

class OracleToAzureDataLakeTransfer(BaseOperator):
    """OracleToAzureDataLakeTransfer"""
    template_fields = ('filename', 'sql', 'sql_params')
    ui_color = '#e08c8c'

    @apply_defaults
    def __init__(self, filename, azure_data_lake_conn_id, azure_data_lake_path, oracle_conn_id, sql, sql_params=None, delimiter=',', encoding='utf-8', quotechar='"', quoting=csv.QUOTE_MINIMAL, *args, **kwargs):
        (super(OracleToAzureDataLakeTransfer, self).__init__)(*args, **kwargs)
        if sql_params is None:
            sql_params = {}
        self.filename = filename
        self.oracle_conn_id = oracle_conn_id
        self.sql = sql
        self.sql_params = sql_params
        self.azure_data_lake_conn_id = azure_data_lake_conn_id
        self.azure_data_lake_path = azure_data_lake_path
        self.delimiter = delimiter
        self.encoding = encoding
        self.quotechar = quotechar
        self.quoting = quoting

    def _write_temp_file(self, cursor, path_to_save):
        with open(path_to_save, 'wb') as (csvfile):
            csv_writer = csv.writer(csvfile, delimiter=(self.delimiter), encoding=(self.encoding),
              quotechar=(self.quotechar),
              quoting=(self.quoting))
            csv_writer.writerow(map(lambda field: field[0], cursor.description))
            csv_writer.writerows(cursor)
            csvfile.flush()

    def execute(self, context):
        oracle_hook = OracleHook(oracle_conn_id=(self.oracle_conn_id))
        azure_data_lake_hook = AzureDataLakeHook(azure_data_lake_conn_id=(self.azure_data_lake_conn_id))
        self.log.info('Dumping Oracle query results to local file')
        conn = oracle_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.sql, self.sql_params)
        with TemporaryDirectory(prefix='airflow_oracle_to_azure_op_') as (temp):
            self._write_temp_file(cursor, os.path.join(temp, self.filename))
            self.log.info('Uploading local file to Azure Data Lake')
            azure_data_lake_hook.upload_file(os.path.join(temp, self.filename), os.path.join(self.azure_data_lake_path, self.filename))
        cursor.close()
        conn.close()