# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/mssql_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3216 bytes
"""
MsSQL to GCS operator.
"""
import decimal
from airflow.utils.decorators import apply_defaults
from airflow.hooks.mssql_hook import MsSqlHook
from airflow.contrib.operators.sql_to_gcs import BaseSQLToGoogleCloudStorageOperator

class MsSqlToGoogleCloudStorageOperator(BaseSQLToGoogleCloudStorageOperator):
    __doc__ = "Copy data from Microsoft SQL Server to Google Cloud Storage\n    in JSON or CSV format.\n\n    :param mssql_conn_id: Reference to a specific MSSQL hook.\n    :type mssql_conn_id: str\n\n    **Example**:\n        The following operator will export data from the Customers table\n        within the given MSSQL Database and then upload it to the\n        'mssql-export' GCS bucket (along with a schema file). ::\n\n            export_customers = MsSqlToGoogleCloudStorageOperator(\n                task_id='export_customers',\n                sql='SELECT * FROM dbo.Customers;',\n                bucket='mssql-export',\n                filename='data/customers/export.json',\n                schema_filename='schemas/export.json',\n                mssql_conn_id='mssql_default',\n                google_cloud_storage_conn_id='google_cloud_default',\n                dag=dag\n            )\n    "
    ui_color = '#e0a98c'
    type_map = {3:'INTEGER', 
     4:'TIMESTAMP', 
     5:'NUMERIC'}

    @apply_defaults
    def __init__(self, mssql_conn_id='mssql_default', *args, **kwargs):
        (super(MsSqlToGoogleCloudStorageOperator, self).__init__)(*args, **kwargs)
        self.mssql_conn_id = mssql_conn_id

    def query(self):
        """
        Queries MSSQL and returns a cursor of results.

        :return: mssql cursor
        """
        mssql = MsSqlHook(mssql_conn_id=(self.mssql_conn_id))
        conn = mssql.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.sql)
        return cursor

    def field_to_bigquery(self, field):
        return {'name':field[0].replace(' ', '_'), 
         'type':self.type_map.get(field[1], 'STRING'), 
         'mode':'NULLABLE'}

    @classmethod
    def convert_type(cls, value, schema_type):
        """
        Takes a value from MSSQL, and converts it to a value that's safe for
        JSON/Google Cloud Storage/BigQuery.
        """
        if isinstance(value, decimal.Decimal):
            return float(value)
        else:
            return value