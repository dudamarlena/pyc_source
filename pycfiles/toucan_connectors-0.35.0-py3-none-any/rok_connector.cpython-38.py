# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/rok/rok_connector.py
# Compiled at: 2020-03-19 08:41:10
# Size of source mod 2**32: 1565 bytes
import pandas as pd, requests
from pydantic import Field
from toucan_connectors.common import FilterSchema, transform_with_jq
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class RokDataSource(ToucanDataSource):
    database: str
    query = Field(..., description='GQL string')
    query: str
    filter = FilterSchema
    filter: str


class RokConnector(ToucanConnector):
    data_source_model: RokDataSource
    host: str
    username: str
    password: str

    def _retrieve_data(self, data_source: RokDataSource) -> pd.DataFrame:
        endpoint = f"{self.host}/graphql?DatabaseName={data_source.database}"
        auth_query = '\n            query Auth($database: String!, $user: String!, $password: String!)\n            {authenticate(database: $database, user: $user, password: $password)}'
        auth_vars = {'database':data_source.database, 
         'user':self.username, 
         'password':self.password}
        auth_res = requests.post(endpoint,
          json={'query':auth_query,  'variables':auth_vars}).json()
        if 'errors' in auth_res:
            raise ValueError(str(auth_res['errors']))
        payload = {'query':data_source.query,  'variables':data_source.parameters}
        headers = {'Token': auth_res['data']['authenticate']}
        res = requests.post(endpoint, json=payload, headers=headers).json()
        if 'errors' in res:
            raise ValueError(str(res['errors']))
        return pd.DataFrame(transform_with_jq(res, data_source.filter))