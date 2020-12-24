# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/dataiku/dataiku_connector.py
# Compiled at: 2020-04-21 04:11:51
# Size of source mod 2**32: 1100 bytes
from io import StringIO
import dataikuapi, pandas as pd
from pydantic import Field
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class DataikuDataSource(ToucanDataSource):
    dataset: str


class DataikuConnector(ToucanConnector):
    __doc__ = '\n    This is a basic connector for [Dataiku](https://www.dataiku.com/) using their\n    [DSS API](https://doc.dataiku.com/dss/2.0/api/index.html).\n    '
    data_source_model: DataikuDataSource
    host: str = Field(...,
      description='The domain name (preferred option as more dynamic) or the hardcoded IP address of your Dataiku server')
    apiKey: str = Field(..., title='API key')
    project: str

    def _retrieve_data(self, data_source: DataikuDataSource) -> pd.DataFrame:
        client = dataikuapi.DSSClient(self.host, self.apiKey)
        data_url = f"/projects/{self.project}/datasets/{data_source.dataset}/data/"
        stream = client._perform_raw('GET', data_url, params={'format': 'tsv-excel-header'})
        return pd.read_csv((StringIO(stream.text)), sep='\t')