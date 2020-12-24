# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_gizmos/tethys_gizmos/views/gizmos/fetchclimate.py
# Compiled at: 2014-10-02 18:50:27
import inspect, requests, json
from django.http import JsonResponse
from django.views.generic import ListView
from django.http import HttpResponse
from ...lib.fetchclimate.fc_grid import FCGrid
from ...lib.fetchclimate.fc_response import FCResponse
from ...lib.fetchclimate.fc_request import FCRequest
from ...lib.fetchclimate.fc_time_series import FCTimeSeries
from ...lib.fetchclimate.fc_temporal_domain import FCTemporalDomain

class FCConfiguration(object):

    def __init__(self, options):
        self.config = []
        self.timeout = 180000
        self.options = options if options else {}
        self.serviceUrl = options['serviceUrl'] if 'serviceUrl' in options else ''
        self.getConfiguration()

    def getConfiguration(self):
        timestamp = '/api/configuration?timestamp=' + self.options['timestamp'] if 'timestamp' in self.options else '/api/configuration'
        headers = {'data-type': 'json'}
        r = requests.get(self.serviceUrl + timestamp, headers=headers, timeout=self.timeout)
        if r.status_code == requests.codes.ok:
            self.config = r.json()
        else:
            self.config = 'Error: ' + str(r.status_code)

    def getDataSourceByID(self, source_id):
        dataSource = self.config['DataSources']
        for source in dataSource:
            if source['ID'] == int(source_id):
                return source['Name']

        return

    def getDataSources(self, variable_src_ids):
        if len(variable_src_ids) > 0:
            dataSources = []
            for i in range(0, len(variable_src_ids)):
                dataSources.append(self.getDataSourceByID(variable_src_ids[i]))

        else:
            dataSources = None
        return dataSources

    def getDataDescriptionByName(self, name):
        environmentalVariables = self.config['EnvironmentalVariables']
        for source in environmentalVariables:
            if source['Name'] == name:
                return source['Description']

        return

    def getDataUnitsbyName(self, name):
        environmentalVariables = self.config['EnvironmentalVariables']
        for source in environmentalVariables:
            if source['Name'] == name:
                return source['Units']

        return


class FetchClimateGizmoView(object):
    """
  Docs
  """

    def __init__(self):
        self.timeout = 180000
        self.plots = []
        self.data = {}
        self.means = {}
        self.temporalDomain = None
        return

    def initRequest(self):
        variable_src_ids = [ int(src_id) for src_id in self.variable_data['sources'] ] if isinstance(self.variable_data['sources'], list) else []
        return FCRequest({'spatial': self.grid, 'temporal': self.temporalDomain, 'variable': self.variable_data['name'], 
           'dataSources': self.FCConfig.getDataSources(variable_src_ids)})

    def initDataRequest(self):
        print 'Request Ready for grid: ' + self.grid.name + ', variable: ' + self.variable_data['name'] + '. Posting!'
        request = self.initRequest()
        return request.doPost()

    def getDataFromResponse(self, response):
        success = False
        if response:
            self.data[self.variable_data['name']] = {}
            self.data[self.variable_data['name']][self.grid.name] = response.getData()
            self.means[self.variable_data['name']] = {}
            self.means[self.variable_data['name']][self.grid.name] = response.findDataMean()
            success = True
        else:
            self.means[self.variable_data['name']] = {}
            self.means[self.variable_data['name']][self.grid.name] = None
        return {'data': self.means[self.variable_data['name']][self.grid.name], 'success': success}

    def initFromPost(self, post_info):
        self.serviceUrl = post_info['serviceUrl'] if len(post_info['serviceUrl']) > 0 else 'http://fetchclimate2.cloudapp.net'
        self.FCConfig = FCConfiguration({'serviceUrl': self.serviceUrl})
        time_data = json.loads(post_info['time'])
        self.temporalDomain = FCTemporalDomain(time_data['years'], time_data['yc'], time_data['days'], time_data['dc'], time_data['hours'], time_data['hc'])
        grid_data = json.loads(post_info['grid'])
        if grid_data['gridType'] == 'CellGrid':
            grid_points = grid_data['gridData']['boundingBox']
            grid_resolution = grid_data['gridData']['gridResolution']
            self.grid = FCGrid('CellGrid', grid_points[0], grid_points[1], grid_resolution[0], grid_points[2], grid_points[3], grid_resolution[1], grid_data['gridData']['title'])
        elif grid_data['gridType'] == 'Points':
            grid_points = grid_data['gridData']['location']
            self.grid = FCGrid('Points', [grid_points[0]], [grid_points[1]], None, None, None, None, grid_data['gridData']['title'])
        self.variable_data = json.loads(post_info['variable'])
        return


def data_request_single(request):
    post_info = request.GET
    gizmoView = FetchClimateGizmoView()
    gizmoView.initFromPost(post_info)
    response = gizmoView.initDataRequest()
    data = gizmoView.getDataFromResponse(response)
    timeseries = FCTimeSeries(gizmoView.temporalDomain, data['data'])
    response_data = {}
    if data['success']:
        response_data = JsonResponse({'data': timeseries.timeSeriesDateToMilisecond(), 'dataName': gizmoView.FCConfig.getDataDescriptionByName(gizmoView.variable_data['name']), 
           'dataUnits': gizmoView.FCConfig.getDataUnitsbyName(gizmoView.variable_data['name']), 
           'dataSize': timeseries.timeSeriesDataSize()})
    return response_data