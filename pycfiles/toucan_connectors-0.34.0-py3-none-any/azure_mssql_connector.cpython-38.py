# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/azure_mssql/azure_mssql_connector.py
# Compiled at: 2020-04-21 04:11:51
# Size of source mod 2**32: 2091 bytes
import re, pandas as pd, pyodbc
from pydantic import Field, SecretStr, constr
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource
CLOUD_HOST = 'database.windows.net'

class AzureMSSQLDataSource(ToucanDataSource):
    database = Field(..., description='The name of the database you want to query')
    database: str
    query = Field(...,
      description='You can write your SQL query here', widget='sql')
    query: constr(min_length=1)


class AzureMSSQLConnector(ToucanConnector):
    __doc__ = '\n    Import data from Microsoft Azure SQL Server.\n    '
    data_source_model: AzureMSSQLDataSource
    host = Field(...,
      description='The domain name (preferred option as more dynamic) or the hardcoded IP address of your database server')
    host: str
    user = Field(..., description='Your login username')
    user: str
    password = Field(..., description='Your login password')
    password: SecretStr
    connect_timeout = Field(None,
      title='Connection timeout',
      description='You can set a connection timeout in seconds here, i.e. the maximum length of time you want to wait for the server to respond. None by default')
    connect_timeout: int

    def get_connection_params(self, *, database=None):
        base_host = re.sub(f".{CLOUD_HOST}$", '', self.host)
        user = f"{self.user}@{base_host}" if '@' not in self.user else self.user
        con_params = {'driver':'{ODBC Driver 17 for SQL Server}', 
         'server':f"{base_host}.{CLOUD_HOST}", 
         'database':database, 
         'user':user, 
         'password':self.password.get_secret_value(), 
         'timeout':self.connect_timeout}
        return {v:k for k, v in con_params.items() if v is not None if v is not None}

    def _retrieve_data(self, datasource: AzureMSSQLDataSource) -> pd.DataFrame:
        connection = (pyodbc.connect)(**self.get_connection_params(database=(datasource.database)))
        df = pd.read_sql((datasource.query), con=connection)
        connection.close()
        return df