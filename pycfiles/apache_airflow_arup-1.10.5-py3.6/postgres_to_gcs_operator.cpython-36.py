# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/postgres_to_gcs_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3499 bytes
"""
PostgreSQL to GCS operator.
"""
import datetime
from decimal import Decimal
import time, sys
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults
from airflow.contrib.operators.sql_to_gcs import BaseSQLToGoogleCloudStorageOperator
PY3 = sys.version_info[0] == 3

class PostgresToGoogleCloudStorageOperator(BaseSQLToGoogleCloudStorageOperator):
    __doc__ = '\n    Copy data from Postgres to Google Cloud Storage in JSON or CSV format.\n\n    :param postgres_conn_id: Reference to a specific Postgres hook.\n    :type postgres_conn_id: str\n    '
    ui_color = '#a0e08c'
    type_map = {1114:'TIMESTAMP', 
     1184:'TIMESTAMP', 
     1082:'TIMESTAMP', 
     1083:'TIMESTAMP', 
     1005:'INTEGER', 
     1007:'INTEGER', 
     1016:'INTEGER', 
     20:'INTEGER', 
     21:'INTEGER', 
     23:'INTEGER', 
     16:'BOOLEAN', 
     700:'FLOAT', 
     701:'FLOAT', 
     1700:'FLOAT'}

    @apply_defaults
    def __init__(self, postgres_conn_id='postgres_default', *args, **kwargs):
        (super(PostgresToGoogleCloudStorageOperator, self).__init__)(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id

    def query(self):
        """
        Queries Postgres and returns a cursor to the results.
        """
        hook = PostgresHook(postgres_conn_id=(self.postgres_conn_id))
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.sql, self.parameters)
        return cursor

    def field_to_bigquery(self, field):
        return {'name':field[0], 
         'type':self.type_map.get(field[1], 'STRING'), 
         'mode':'REPEATED' if field[1] in (1009, 1005, 1007, 1016) else 'NULLABLE'}

    def convert_type(self, value, schema_type):
        """
        Takes a value from Postgres, and converts it to a value that's safe for
        JSON/Google Cloud Storage/BigQuery. Dates are converted to UTC seconds.
        Decimals are converted to floats. Times are converted to seconds.
        """
        if isinstance(value, (datetime.datetime, datetime.date)):
            return time.mktime(value.timetuple())
        else:
            if isinstance(value, datetime.time):
                formated_time = time.strptime(str(value), '%H:%M:%S')
                return datetime.timedelta(hours=(formated_time.tm_hour),
                  minutes=(formated_time.tm_min),
                  seconds=(formated_time.tm_sec)).seconds
            if isinstance(value, Decimal):
                return float(value)
            return value