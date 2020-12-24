# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoaladep/gcp/bigquery/bigquery.py
# Compiled at: 2020-03-10 05:49:04
# Size of source mod 2**32: 1041 bytes
from google.cloud import bigquery

class Bigquery(Object):

    def __init__(self, project_id):
        """[Init function]
        
        Arguments:
            project_id {[string]} -- [Project ID in cloud platform]
        """
        self.bigquery_client = bigquery.Client(project=project_id)

    def query(self, query_sql):
        """[Get data from table]
        
        Arguments:
            kiquery_sqlnd {[string]} -- [SQL Statement]
        
        Returns:
            result[dict] -- [Dictionary of data]
        """
        result = []
        try:
            query_job = self.bigquery_client.query(query_sql)
            result = query_job.result()
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        return result

    def insert_data(self, database_name, table_name, data):
        list_column_name = list(data.keys())
        list_value_data = list(data.values())
        query_sql = 'insert into {}.{} ({}) values {}'.format(database_name, table_name, list_column_name, list_value_data)