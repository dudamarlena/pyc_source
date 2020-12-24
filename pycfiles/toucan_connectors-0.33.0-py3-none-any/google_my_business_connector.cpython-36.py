# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/google_my_business/google_my_business_connector.py
# Compiled at: 2020-04-08 11:34:17
# Size of source mod 2**32: 3024 bytes
from typing import List
import pandas as pd, pyjq
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pandas.io.json import json_normalize
from pydantic import BaseModel
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource
API_SERVICE_NAME = 'mybusiness'
API_VERSION = 'v4'
DISCOVERY_URI = f"https://developers.google.com/my-business/samples/{API_SERVICE_NAME}_google_rest_{API_VERSION}.json"

class Metric(BaseModel):
    metric: str
    options = None
    options: List[str]


class TimeRange(BaseModel):
    start_time: str
    end_time: str


class GoogleMyBusinessDataSource(ToucanDataSource):
    location_ids = None
    location_ids: List[str]
    metric_requests: List[Metric]
    time_range: TimeRange


class GoogleCredentials(BaseModel):
    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str


class GoogleMyBusinessConnector(ToucanConnector):
    data_source_model: GoogleMyBusinessDataSource
    credentials: GoogleCredentials
    scopes = ['https://www.googleapis.com/auth/business.manage']
    scopes: List[str]

    def build_service(self):
        credentials = Credentials.from_authorized_user_info((self.credentials.dict()),
          scopes=(self.scopes))
        service = build(API_SERVICE_NAME,
          API_VERSION,
          credentials=credentials,
          discoveryServiceUrl=DISCOVERY_URI)
        return service

    def _retrieve_data(self, data_source: GoogleMyBusinessDataSource) -> pd.DataFrame:
        service = self.build_service()
        accounts = service.accounts().list().execute()
        name = accounts['accounts'][0]['name']
        if data_source.location_ids:
            location_names = [f"{name}/locations/{id}" for id in data_source.location_ids]
        else:
            locations = service.accounts().locations().list(parent=name).execute()
            location_names = [l['name'] for l in locations['locations']]
        query = {'locationNames':location_names, 
         'basicRequest':{'metricRequests':data_source.dict()['metric_requests'], 
          'timeRange':data_source.dict()['time_range']}}
        report_insights = service.accounts().locations().reportInsights(name=name, body=query).execute()
        location_metrics = report_insights['locationMetrics']
        f = '\n            .[] as $in |\n            $in.metricValues[] as $mv |\n            $in | del(.metricValues) as $in2 |\n            $in2 *  if $mv.dimensionalValues != null then\n                      {"metric": $mv.metric} * $mv.dimensionalValues[]\n                    else\n                      {"metric": $mv.metric} * $mv.totalValue\n                    end\n        '
        res = pyjq.all(f, location_metrics)
        df = json_normalize(res)
        return df