# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/google_cloud_mysql/google_cloud_mysql_connector.py
# Compiled at: 2020-04-08 11:34:17
# Size of source mod 2**32: 2380 bytes
import pandas as pd, pymysql
from pydantic import Field, SecretStr, constr
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class GoogleCloudMySQLDataSource(ToucanDataSource):
    database = Field(..., description='The name of the database you want to query')
    database: str
    query = Field(...,
      description='You can write your SQL query here', widget='sql')
    query: constr(min_length=1)


class GoogleCloudMySQLConnector(ToucanConnector):
    __doc__ = '\n    Import data from Google Cloud MySQL database.\n    '
    data_source_model: GoogleCloudMySQLDataSource
    host = Field(...,
      description='The domain name (preferred option as more dynamic) or the hardcoded IP address of your database server')
    host: str
    port = Field(None, description='The listening port of your database server')
    port: int
    user = Field(..., description='Your login username')
    user: str
    password = Field(..., description='Your login password')
    password: SecretStr
    charset = Field('utf8mb4',
      title='Charset',
      description='Character encoding. You should generally let the default "utf8mb4" here.')
    charset: str
    connect_timeout = Field(None,
      title='Connection timeout',
      description='You can set a connection timeout in seconds here, i.e. the maximum length of time you want to wait for the server to respond. None by default')
    connect_timeout: int

    def get_connection_params(self, *, database=None):
        conv = pymysql.converters.conversions.copy()
        conv[246] = float
        con_params = {'host':self.host, 
         'user':self.user, 
         'password':self.password.get_secret_value() if self.password else None, 
         'port':self.port, 
         'database':database, 
         'charset':self.charset, 
         'connect_timeout':self.connect_timeout, 
         'conv':conv, 
         'cursorclass':pymysql.cursors.DictCursor}
        return {v:k for k, v in con_params.items() if v is not None if v is not None}

    def _retrieve_data(self, data_source: GoogleCloudMySQLDataSource) -> pd.DataFrame:
        connection = (pymysql.connect)(**self.get_connection_params(database=(data_source.database)))
        df = pd.read_sql((data_source.query), con=connection)
        connection.close()
        return df