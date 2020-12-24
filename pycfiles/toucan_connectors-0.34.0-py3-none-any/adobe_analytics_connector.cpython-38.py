# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/adobe_analytics/adobe_analytics_connector.py
# Compiled at: 2020-04-21 04:11:51
# Size of source mod 2**32: 1740 bytes
from enum import Enum
from typing import List, Union
import pandas as pd
from adobe_analytics import Client, ReportDefinition
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class Granularity(str, Enum):
    hour = 'hour'
    day = 'day'
    week = 'week'
    month = 'month'
    quarter = 'quarter'
    year = 'year'


class AdobeAnalyticsDataSource(ToucanDataSource):
    suite_id: str
    dimensions = []
    dimensions: Union[(List[Union[(str, dict)]], str)]
    metrics: Union[(List[str], str)]
    segments = None
    segments: Union[(List[str], str)]
    date_from: str
    date_to: str
    last_days = None
    last_days: int
    granularity = None
    granularity: Granularity
    source = None
    source: str

    @property
    def report_definition(self):
        return ReportDefinition(segments=(self.segments),
          dimensions=(self.dimensions),
          metrics=(self.metrics),
          date_from=(self.date_from),
          date_to=(self.date_to),
          last_days=(self.last_days),
          granularity=(self.granularity),
          source=(self.source))


class AdobeAnalyticsConnector(ToucanConnector):
    __doc__ = "\n    Adobe Analytics Connector using Adobe Analytics' REST API v1.4.\n    It provides a high-level interfaces for reporting queries (including Data Warehouse requests).\n    "
    data_source_model: AdobeAnalyticsDataSource
    username: str
    password: str
    endpoint = Client.DEFAULT_ENDPOINT
    endpoint: str

    def _retrieve_data(self, data_source: AdobeAnalyticsDataSource) -> pd.DataFrame:
        suites = Client(self.username, self.password, self.endpoint).suites()
        df = suites[data_source.suite_id].download(data_source.report_definition)
        df['suite_id'] = data_source.suite_id
        return df