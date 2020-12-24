# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/odata/odata_connector.py
# Compiled at: 2020-04-21 04:11:51
# Size of source mod 2**32: 2016 bytes
import pandas as pd
from odata import ODataService
from odata.metadata import MetaData
from pydantic import Field, HttpUrl
from toucan_connectors.auth import Auth
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

def metadata_init_patched(self, service):
    self._original_init(service)
    self.url = service.url.rstrip('/') + '/$metadata'


MetaData._original_init = MetaData.__init__
MetaData.__init__ = metadata_init_patched

class ODataDataSource(ToucanDataSource):
    entity = Field(...,
      description='The entity path that will be appended to your baseroute URL. For example "geo/countries". For more details, see this <a href="https://www.odata.org/getting-started/basic-tutorial/">tutorial</a>')
    entity: str
    query = Field(...,
      description='JSON object of parameters with parameter name as key and value as value. For example {"$filter": "my_value", "$skip": 100} (equivalent to "$filter=my_value&$skip=100" in parameterized URL). For more details on query parameters convention, see <a href="https://www.odata.org/documentation/odata-version-2-0/uri-conventions/">this documentation</a>',
      widget='json')
    query: dict


class ODataConnector(ToucanConnector):
    data_source_model: ODataDataSource
    baseroute = Field(..., title='API endpoint', description='Baseroute URL')
    baseroute: HttpUrl
    auth = Field(None, title='Authentication type')
    auth: Auth

    def _retrieve_data(self, data_source: ODataDataSource) -> pd.DataFrame:
        if self.auth:
            session = self.auth.get_session()
        else:
            session = None
        service = ODataService((self.baseroute), reflect_entities=True, session=session)
        entities = service.entities[data_source.entity]
        data = service.query(entities).raw(data_source.query)
        return pd.DataFrame(data)