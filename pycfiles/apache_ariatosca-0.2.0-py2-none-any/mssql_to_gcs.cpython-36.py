# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/mssql_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3216 bytes
__doc__ = '\nMsSQL to GCS operator.\n'
import decimal
from airflow.utils.decorators import apply_defaults
from airflow.hooks.mssql_hook import MsSqlHook
from airflow.contrib.operators.sql_to_gcs import BaseSQLToGoogleCloudStorageOperator

class MsSqlToGoogleCloudStorageOperator(BaseSQLToGoogleCloudStorageOperator):
    """MsSqlToGoogleCloudStorageOperator"""
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