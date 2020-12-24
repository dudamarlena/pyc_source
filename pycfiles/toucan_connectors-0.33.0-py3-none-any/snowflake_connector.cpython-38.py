# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/snowflake/snowflake_connector.py
# Compiled at: 2020-04-21 04:11:51
# Size of source mod 2**32: 2480 bytes
from os import path
import pandas as pd, snowflake.connector
from pydantic import Field, SecretStr, constr
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class Path(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not path.exists(v):
            raise ValueError('path does not exists: v')
        return v


class SnowflakeDataSource(ToucanDataSource):
    database = Field(None, description='The name of the database you want to query')
    database: str
    warehouse = Field(None, description='The name of the warehouse you want to query')
    warehouse: str
    query = Field(...,
      description='You can write your SQL query here', widget='sql')
    query: constr(min_length=1)


class SnowflakeConnector(ToucanConnector):
    __doc__ = '\n    Import data from Snowflake data warehouse.\n    '
    data_source_model: SnowflakeDataSource
    user = Field(..., description='Your login username')
    user: str
    password = Field(..., description='Your login password')
    password: SecretStr
    account = Field(...,
      description='The full name of your Snowflake account. It might require the region and cloud platform where your account is located, in the form of: "your_account_name.region_id.cloud_platform". See more details <a href="https://docs.snowflake.net/manuals/user-guide/python-connector-api.html#label-account-format-info">here</a>.')
    account: str
    ocsp_response_cache_filename = Field(None,
      title='OCSP response cache filename',
      description='The path of the <a href="https://docs.snowflake.net/manuals/user-guide/python-connector-example.html#caching-ocsp-responses">OCSP cache file</a>')
    ocsp_response_cache_filename: Path

    def _retrieve_data(self, data_source: SnowflakeDataSource) -> pd.DataFrame:
        connection = snowflake.connector.connect(user=(self.user),
          password=(self.password.get_secret_value()),
          account=(self.account),
          database=(data_source.database),
          warehouse=(data_source.warehouse),
          ocsp_response_cache_filename=(self.ocsp_response_cache_filename))
        connection.cursor().execute(f"USE WAREHOUSE {data_source.warehouse}")
        df = pd.read_sql((data_source.query), con=connection)
        connection.close()
        return df