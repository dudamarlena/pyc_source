# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/toucan_toco/toucan_toco_connector.py
# Compiled at: 2020-03-19 08:41:10
# Size of source mod 2**32: 1289 bytes
from enum import Enum
import pandas as pd
from toucan_client import ToucanClient
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class Endpoints(str, Enum):
    users = 'users'
    small_apps = 'small-apps'
    config = 'config'


class ToucanTocoDataSource(ToucanDataSource):
    __doc__ = '\n    Use the `all_small_apps` parameter to get results from an endpoint on all small apps.\n    '
    endpoint: Endpoints
    all_small_apps = False
    all_small_apps: bool


class ToucanTocoConnector(ToucanConnector):
    __doc__ = '\n    Get data from a Toucan Toco instance, usefull to build analytics applications.\n    '
    data_source_model: ToucanTocoDataSource
    host: str
    username: str
    password: str

    def _retrieve_data(self, data_source: ToucanTocoDataSource) -> pd.DataFrame:

        def g(o):
            return o.get().json()

        tc = ToucanClient((self.host), auth=(self.username, self.password))
        if data_source.all_small_apps:
            ret = []
            for app in g(tc['small-apps']):
                ret.append({'small_app':app['id'], 
                 'response':g(tc[app['id']][data_source.endpoint])})
            else:
                return pd.DataFrame(ret)

        return pd.DataFrame(g(tc[data_source.endpoint]))