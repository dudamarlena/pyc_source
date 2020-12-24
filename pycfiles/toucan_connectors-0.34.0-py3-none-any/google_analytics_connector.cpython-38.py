# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/google_analytics/google_analytics_connector.py
# Compiled at: 2020-04-21 04:11:51
# Size of source mod 2**32: 6735 bytes
from typing import List
import pandas as pd
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pydantic import BaseModel, Field
from toucan_connectors.common import nosql_apply_parameters_to_query
from toucan_connectors.google_credentials import GoogleCredentials
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource
API = 'analyticsreporting'
SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
VERSION = 'v4'

class Dimension(BaseModel):
    name: str
    histogramBuckets = None
    histogramBuckets: List[str]


class DimensionFilter(BaseModel):
    dimensionName: str
    operator: str
    expressions = None
    expressions: List[str]
    caseSensitive = False
    caseSensitive: bool

    class Config:
        extra = 'allow'


class DimensionFilterClause(BaseModel):
    operator: str
    filters: List[DimensionFilter]


class DateRange(BaseModel):
    startDate: str
    endDate: str


class Metric(BaseModel):
    expression: str
    alias = None
    alias: str

    class Config:
        extra = 'allow'


class MetricFilter(BaseModel):
    metricName: str
    operator: str
    comparisonValue: str

    class Config:
        extra = 'allow'


class MetricFilterClause(BaseModel):
    operator: str
    filters: List[MetricFilter]


class OrderBy(BaseModel):
    fieldName: str
    orderType = None
    orderType: str
    sortOrder = None
    sortOrder: str


class Pivot(BaseModel):
    dimensions = None
    dimensions: List[Dimension]
    dimensionFilterClauses = None
    dimensionFilterClauses: List[DimensionFilterClause]
    metrics = None
    metrics: List[Metric]
    startGroup = None
    startGroup: int
    maxGroupCount = None
    maxGroupCount: int


class Cohort(BaseModel):
    name: str
    type: str
    dateRange = None
    dateRange: DateRange


class CohortGroup(BaseModel):
    cohorts: List[Cohort]
    lifetimeValue = False
    lifetimeValue: bool


class Segment(BaseModel):
    segmentId = None
    segmentId: str


class ReportRequest(BaseModel):
    viewId: str
    dateRanges = None
    dateRanges: List[DateRange]
    samplingLevel = None
    samplingLevel: str
    dimensions = None
    dimensions: List[Dimension]
    dimensionFilterClauses = None
    dimensionFilterClauses: List[DimensionFilterClause]
    metrics = None
    metrics: List[Metric]
    metricFilterClauses = None
    metricFilterClauses: List[MetricFilterClause]
    filtersExpression = ''
    filtersExpression: str
    orderBys = []
    orderBys: List[OrderBy]
    segments = []
    segments: List[Segment]
    pivots = None
    pivots: List[Pivot]
    cohortGroup = None
    cohortGroup: CohortGroup
    pageToken = ''
    pageToken: str
    pageSize = 10000
    pageSize: int
    includeEmptyRows = False
    includeEmptyRows: bool
    hideTotals = False
    hideTotals: bool
    hideValueRanges = False
    hideValueRanges: bool


def get_dict_from_response(report, request_date_ranges):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])
    all_rows = []
    for row_index, row in enumerate(rows):
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])
        for i, values in enumerate(dateRangeValues):
            for metricHeader, value in zip(metricHeaders, values.get('values')):
                row_dict = {'row_index':row_index,  'date_range_id':i, 
                 'metric_name':metricHeader.get('name')}
                if request_date_ranges:
                    if len(request_date_ranges) >= i:
                        row_dict['start_date'] = request_date_ranges[i].startDate
                        row_dict['end_date'] = request_date_ranges[i].endDate
                elif metricHeader.get('type') == 'INTEGER':
                    row_dict['metric_value'] = int(value)
                else:
                    if metricHeader.get('type') == 'FLOAT':
                        row_dict['metric_value'] = float(value)
                    else:
                        row_dict['metric_value'] = value
                for dimension_name, dimension_value in zip(dimensionHeaders, dimensions):
                    row_dict[dimension_name] = dimension_value
                else:
                    all_rows.append(row_dict)

        else:
            return all_rows


def get_query_results(service, report_request):
    response = service.reports().batchGet(body={'reportRequests': report_request.dict()}).execute()
    return response.get('reports', [])[0]


class GoogleAnalyticsDataSource(ToucanDataSource):
    report_request = Field(...,
      title='Report request',
      description='See the complete <a href="https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#reportrequest">Google documentation</a>')
    report_request: ReportRequest


class GoogleAnalyticsConnector(ToucanConnector):
    data_source_model: GoogleAnalyticsDataSource
    credentials = Field(...,
      title='Google Credentials',
      description='For authentication, download an authentication file from your <a href="https://console.developers.google.com/apis/credentials">Google Console</a> and use the values here. This is an oauth2 credential file. For more information see this <a href="https://gspread.readthedocs.io/en/latest/oauth2.html">documentation</a>. You should use "service_account" credentials, which is the preferred type of credentials to use when authenticating on behalf of a service or application')
    credentials: GoogleCredentials
    scope = Field([
     SCOPE],
      description='OAuth 2.0 scopes define the level of access you need to request the Google APIs. For more information, see this <a href="https://developers.google.com/identity/protocols/googlescopes">documentation</a>')
    scope: List[str]

    def _retrieve_data(self, data_source: GoogleAnalyticsDataSource) -> pd.DataFrame:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.credentials.dict(), self.scope)
        service = build(API, VERSION, credentials=credentials)
        report_request = ReportRequest(**nosql_apply_parameters_to_query(data_source.report_request.dict(), data_source.parameters))
        report = get_query_results(service, report_request)
        reports_data = [pd.DataFrame(get_dict_from_response(report, report_request.dateRanges))]
        while 'nextPageToken' in report:
            report_request.pageToken = report['nextPageToken']
            report = get_query_results(service, report_request)
            reports_data.append(pd.DataFrame(get_dict_from_response(report, report_request.dateRanges)))

        return pd.concat(reports_data)