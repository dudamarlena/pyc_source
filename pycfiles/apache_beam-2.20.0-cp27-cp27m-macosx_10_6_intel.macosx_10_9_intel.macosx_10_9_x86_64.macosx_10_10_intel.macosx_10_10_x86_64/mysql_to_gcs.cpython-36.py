# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/mysql_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4792 bytes
__doc__ = '\nMySQL to GCS operator.\n'
import base64, calendar, sys
from datetime import date, datetime, timedelta
from decimal import Decimal
from MySQLdb.constants import FIELD_TYPE
from airflow.hooks.mysql_hook import MySqlHook
from airflow.utils.decorators import apply_defaults
from airflow.contrib.operators.sql_to_gcs import BaseSQLToGoogleCloudStorageOperator
PY3 = sys.version_info[0] == 3

class MySqlToGoogleCloudStorageOperator(BaseSQLToGoogleCloudStorageOperator):
    """MySqlToGoogleCloudStorageOperator"""
    ui_color = '#a0e08c'
    type_map = {FIELD_TYPE.BIT: 'INTEGER', 
     FIELD_TYPE.DATETIME: 'TIMESTAMP', 
     FIELD_TYPE.DATE: 'TIMESTAMP', 
     FIELD_TYPE.DECIMAL: 'FLOAT', 
     FIELD_TYPE.NEWDECIMAL: 'FLOAT', 
     FIELD_TYPE.DOUBLE: 'FLOAT', 
     FIELD_TYPE.FLOAT: 'FLOAT', 
     FIELD_TYPE.INT24: 'INTEGER', 
     FIELD_TYPE.LONG: 'INTEGER', 
     FIELD_TYPE.LONGLONG: 'INTEGER', 
     FIELD_TYPE.SHORT: 'INTEGER', 
     FIELD_TYPE.TIME: 'TIME', 
     FIELD_TYPE.TIMESTAMP: 'TIMESTAMP', 
     FIELD_TYPE.TINY: 'INTEGER', 
     FIELD_TYPE.YEAR: 'INTEGER'}

    @apply_defaults
    def __init__(self, mysql_conn_id='mysql_default', ensure_utc=False, *args, **kwargs):
        (super(MySqlToGoogleCloudStorageOperator, self).__init__)(*args, **kwargs)
        self.mysql_conn_id = mysql_conn_id
        self.ensure_utc = ensure_utc

    def query(self):
        """
        Queries mysql and returns a cursor to the results.
        """
        mysql = MySqlHook(mysql_conn_id=(self.mysql_conn_id))
        conn = mysql.get_conn()
        cursor = conn.cursor()
        if self.ensure_utc:
            tz_query = "SET time_zone = '+00:00'"
            self.log.info('Executing: %s', tz_query)
            cursor.execute(tz_query)
        self.log.info('Executing: %s', self.sql)
        cursor.execute(self.sql)
        return cursor

    def field_to_bigquery(self, field):
        field_type = self.type_map.get(field[1], 'STRING')
        field_mode = 'NULLABLE' if field[6] or field_type == 'TIMESTAMP' else 'REQUIRED'
        return {'name':field[0], 
         'type':field_type, 
         'mode':field_mode}

    def convert_type(self, value, schema_type):
        """
        Takes a value from MySQLdb, and converts it to a value that's safe for
        JSON/Google cloud storage/BigQuery. Dates are converted to UTC seconds.
        Decimals are converted to floats. Binary type fields are encoded with base64,
        as imported BYTES data must be base64-encoded according to Bigquery SQL
        date type documentation: https://cloud.google.com/bigquery/data-types

        :param value: MySQLdb column value
        :type value: Any
        :param schema_type: BigQuery data type
        :type schema_type: str
        """
        if isinstance(value, (datetime, date)):
            return calendar.timegm(value.timetuple())
        else:
            if isinstance(value, timedelta):
                return value.total_seconds()
            else:
                if isinstance(value, Decimal):
                    return float(value)
                if schema_type == 'BYTES':
                    col_val = base64.standard_b64encode(value)
                    if PY3:
                        col_val = col_val.decode('ascii')
                    return col_val
            return value