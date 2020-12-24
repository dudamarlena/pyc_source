# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/micro_strategy/micro_strategy_connector.py
# Compiled at: 2020-03-19 08:41:10
# Size of source mod 2**32: 4497 bytes
from enum import Enum
import pandas as pd
from pandas.io.json import json_normalize
from pydantic import Field, HttpUrl, SecretStr
from toucan_connectors.common import nosql_apply_parameters_to_query
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource
from .client import Client
from .data import fill_viewfilter_with_ids, flatten_json, get_attr_names, get_definition, get_metric_names

class Dataset(str, Enum):
    cube = 'cube'
    report = 'report'
    search = 'search'


class Subtypes(int, Enum):
    cube = 776
    report = 768


class MicroStrategyDataSource(ToucanDataSource):
    __doc__ = '\n    Specify whether you want to use the `cube` or `reports` endpoints and a microstrategy doc id.\n    '
    id = Field(None,
      title='Cube / Report ID', description='In the form "BD91AF40492D2C188240DEAF7D9D1510"')
    id: str
    dataset: Dataset
    viewfilter = Field(None,
      title='View filters',
      description='You can apply Microstrategy View Filters here. Please find configuration details in our <a href="https://docs.toucantoco.com/concepteur/power-apps-with-data/02-add-data-to-small-app.html#microstrategy-connector"> documentation</a>')
    viewfilter: dict
    offset = Field(0,
      description='If you need to skip results, specify here the number of rows to skip')
    offset: int
    limit = Field(100,
      title='Limit the number of results to:',
      description='Specify -1 if you do not want to limit the number of returned rows')
    limit: int


class MicroStrategyConnector(ToucanConnector):
    __doc__ = '\n    Import data from MicroStrategy using the [JSON Data API](http://bit.ly/2HCzf04) for cubes and\n    reports.\n    '
    data_source_model: MicroStrategyDataSource
    base_url = Field(...,
      title='API base URL',
      description='The URL of your MicroStrategy environment API. For example "https://demo.microstrategy.com/MicroStrategyLibrary2/api/"',
      examples=[
     'https://demo.microstrategy.com/MicroStrategyLibrary2/api/'])
    base_url: HttpUrl
    username = Field(..., description='Your login username')
    username: str
    password = Field(None, description='Your login password')
    password: SecretStr
    project_id = Field(...,
      title='projectID',
      description='The unique ID of your MicroStrategy project. In the form "B7CA92F04B9FAE8D941C3E9B7E0CD754"',
      examples=[
     'https://demo.microstrategy.com/MicroStrategyLibrary2/api/'])
    project_id: str

    def _retrieve_metadata(self, data_source: MicroStrategyDataSource) -> pd.DataFrame:
        client = Client(self.base_url, self.project_id, self.username, self.password)
        results = client.list_objects([st.value for st in Subtypes], data_source.id, data_source.offset, data_source.limit)
        df = json_normalize(results['result'])
        subtypes_mapping = {st.name:st.value for st in Subtypes}
        df['subtype'] = df['subtype'].replace(subtypes_mapping)
        return df

    def _retrieve_data(self, data_source: MicroStrategyDataSource) -> pd.DataFrame:
        """Retrieves cube or report data, flattens return dataframe"""
        if data_source.dataset == Dataset.search:
            return self._retrieve_metadata(data_source)
        else:
            client = Client(self.base_url, self.project_id, self.username, self.password)
            query_func = getattr(client, data_source.dataset)
            if not data_source.viewfilter:
                results = query_func(id=(data_source.id),
                  offset=(data_source.offset),
                  limit=(data_source.limit))
            else:
                results = query_func(id=(data_source.id), limit=0)
            dfn = get_definition(results)
            data_source.viewfilter = nosql_apply_parameters_to_query(data_source.viewfilter, data_source.parameters)
            viewfilter = fill_viewfilter_with_ids(data_source.viewfilter, dfn)
            results = query_func(id=(data_source.id),
              viewfilter=viewfilter,
              offset=(data_source.offset),
              limit=(data_source.limit))
        attributes = get_attr_names(results)
        metrics = get_metric_names(results)
        rows = flatten_json(results['result']['data']['root'], attributes, metrics)
        return json_normalize(rows)