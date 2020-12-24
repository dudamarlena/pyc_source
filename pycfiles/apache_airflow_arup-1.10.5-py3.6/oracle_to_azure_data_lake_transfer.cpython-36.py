# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Moves data from Oracle to Azure Data Lake. The operator runs the query against\n    Oracle and stores the file locally before loading it into Azure Data Lake.\n\n\n    :param filename: file name to be used by the csv file.\n    :type filename: str\n    :param azure_data_lake_conn_id: destination azure data lake connection.\n    :type azure_data_lake_conn_id: str\n    :param azure_data_lake_path: destination path in azure data lake to put the file.\n    :type azure_data_lake_path: str\n    :param oracle_conn_id: source Oracle connection.\n    :type oracle_conn_id: str\n    :param sql: SQL query to execute against the Oracle database. (templated)\n    :type sql: str\n    :param sql_params: Parameters to use in sql query. (templated)\n    :type sql_params: str\n    :param delimiter: field delimiter in the file.\n    :type delimiter: str\n    :param encoding: encoding type for the file.\n    :type encoding: str\n    :param quotechar: Character to use in quoting.\n    :type quotechar: str\n    :param quoting: Quoting strategy. See unicodecsv quoting for more information.\n    :type quoting: str\n    '
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