# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/lightspeed/lightspeed_connector.py
# Compiled at: 2020-03-23 03:28:52
# Size of source mod 2**32: 1126 bytes
import pandas as pd, pyjq
from pydantic import Field
from toucan_connectors.common import FilterSchema, nosql_apply_parameters_to_query
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class LightspeedDataSource(ToucanDataSource):
    endpoint = Field(...,
      title='Endpoint of the Lightspeed API',
      description='See https://developers.lightspeedhq.com/retail/endpoints/Account/')
    endpoint: str
    filter = FilterSchema
    filter: str


class LightspeedConnector(ToucanConnector):
    __doc__ = '\n    This is a connector for [Lightspeed](https://developers.lightspeedhq.com/retail/endpoints/Account/)\n    using [Bearer.sh](https://app.bearer.sh/)\n    '
    data_source_model: LightspeedDataSource
    bearer_integration = 'lightspeed'
    bearer_auth_id: str

    def _retrieve_data(self, data_source: LightspeedDataSource) -> pd.DataFrame:
        endpoint = nosql_apply_parameters_to_query(data_source.endpoint, data_source.parameters)
        data = self.bearer_oauth_get_endpoint(endpoint)
        data = pyjq.first(data_source.filter, data)
        return pd.DataFrame(data)