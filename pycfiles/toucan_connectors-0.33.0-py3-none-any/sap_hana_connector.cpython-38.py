# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/sap_hana/sap_hana_connector.py
# Compiled at: 2020-04-21 04:11:51
# Size of source mod 2**32: 1136 bytes
import pandas as pd, pyhdb
from pydantic import Field, SecretStr, constr
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class SapHanaDataSource(ToucanDataSource):
    query = Field(...,
      description='You can write your SQL query here', widget='sql')
    query: constr(min_length=1)


class SapHanaConnector(ToucanConnector):
    __doc__ = '\n    Import data from Sap Hana.\n    '
    data_source_model: SapHanaDataSource
    host = Field(...,
      description='The domain name (preferred option as more dynamic) or the hardcoded IP address of your database server')
    host: str
    port = Field(..., description='The listening port of your database server')
    port: int
    user = Field(..., description='Your login username')
    user: str
    password = Field(..., description='Your login password')
    password: SecretStr

    def _retrieve_data(self, data_source):
        connection = pyhdb.connect(self.host, self.port, self.user, self.password.get_secret_value())
        df = pd.read_sql((data_source.query), con=connection)
        connection.close()
        return df