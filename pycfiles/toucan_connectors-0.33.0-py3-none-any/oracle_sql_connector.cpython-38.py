# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/oracle_sql/oracle_sql_connector.py
# Compiled at: 2020-04-21 04:11:51
# Size of source mod 2**32: 1635 bytes
import cx_Oracle, pandas as pd
from pydantic import Field, SecretStr, constr
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class OracleSQLDataSource(ToucanDataSource):
    query = Field(...,
      description='You can write your SQL query here', widget='sql')
    query: constr(min_length=1)


class OracleSQLConnector(ToucanConnector):
    data_source_model: OracleSQLDataSource
    dsn = Field(...,
      description='A path following the <a href="https://en.wikipedia.org/wiki/Data_source_name">DSN pattern</a>. The DSN host, port and service name are required.',
      examples=[
     'localhost:80/service'])
    dsn: str
    user = Field(None, description='Your login username')
    user: str
    password = Field(None, description='Your login password')
    password: SecretStr
    encoding = Field(None,
      title='Charset', description='If you need to specify a specific character encoding.')
    encoding: str

    def get_connection_params(self):
        con_params = {'user':self.user, 
         'password':self.password.get_secret_value() if self.password else None, 
         'dsn':self.dsn, 
         'encoding':self.encoding}
        return {v:k for k, v in con_params.items() if v is not None if v is not None}

    def _retrieve_data(self, data_source: OracleSQLDataSource) -> pd.DataFrame:
        connection = (cx_Oracle.connect)(**self.get_connection_params())
        query = data_source.query[:-1] if data_source.query.endswith(';') else data_source.query
        df = pd.read_sql(query, con=connection)
        connection.close()
        return df