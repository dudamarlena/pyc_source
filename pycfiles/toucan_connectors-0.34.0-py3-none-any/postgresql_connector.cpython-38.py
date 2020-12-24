# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/postgres/postgresql_connector.py
# Compiled at: 2020-04-21 04:11:52
# Size of source mod 2**32: 2396 bytes
import pandas as pd, psycopg2 as pgsql
from pydantic import Field, SecretStr, constr
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class PostgresDataSource(ToucanDataSource):
    database = Field(..., description='The name of the database you want to query')
    database: str
    query = Field(...,
      description='You can write your SQL query here', widget='sql')
    query: constr(min_length=1)


class PostgresConnector(ToucanConnector):
    __doc__ = '\n    Import data from PostgreSQL.\n    '
    data_source_model: PostgresDataSource
    hostname = Field(None,
      description='Use this parameter if you have a domain name (preferred option as more dynamic). If not, please use the "host" parameter')
    hostname: str
    host = Field(None,
      description='Use this parameter if you have an IP address. If not, please use the "hostname" parameter (preferred option as more dynamic)')
    host: str
    port = Field(None, description='The listening port of your database server')
    port: int
    user = Field(..., description='Your login username')
    user: str
    password = Field(None, description='Your login password')
    password: SecretStr
    charset = Field(None, description='If you need to specify a specific character encoding.')
    charset: str
    connect_timeout = Field(None,
      title='Connection timeout',
      description='You can set a connection timeout in seconds here, i.e. the maximum length of time you want to wait for the server to respond. None by default')
    connect_timeout: int

    def get_connection_params(self, *, database='postgres'):
        con_params = dict(user=(self.user),
          host=(self.host if self.host else self.hostname),
          client_encoding=(self.charset),
          dbname=database,
          password=(self.password.get_secret_value() if self.password else None),
          port=(self.port),
          connect_timeout=(self.connect_timeout))
        return {v:k for k, v in con_params.items() if v is not None if v is not None}

    def _retrieve_data(self, data_source):
        connection = (pgsql.connect)(**self.get_connection_params(database=(data_source.database)))
        query_params = data_source.parameters or {}
        df = pd.read_sql((data_source.query), con=connection, params=query_params)
        connection.close()
        return df