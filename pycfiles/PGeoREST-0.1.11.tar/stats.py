# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeorest/pgeorest/stats.py
# Compiled at: 2014-08-28 10:11:50
import json
from flask import Blueprint, Response
from flask.ext.cors import cross_origin
import copy
from pgeo.error.custom_exceptions import PGeoException, errors
from pgeo.utils import log
from pgeo.config.settings import settings
from pgeo.stats.raster import Stats
from flask import request
app = Blueprint(__name__, __name__)
log = log.logger(__name__)
stats = Stats(settings)
raster_statistics = {'raster': {'uid': None}, 
   'stats': {'force': True}}
raster_histogram = {'raster': {'uid': None}, 
   'stats': {'force': True, 
             'buckets': 256}}

@app.route('/')
def index():
    """
        Welcome message
        @return: welcome message
    """
    return 'Welcome to the stats module!'


@app.route('/raster/<layer>/', methods=['GET'])
@app.route('/raster/<layer>', methods=['GET'])
def get_stats(layer):
    """
    Extracts all the statistics of a layer
    @param layer: workspace:layername
    @return: json with the raster statistics
    """
    try:
        if ':' not in layer:
            return PGeoException('Please Specify a workspace for ' + str(layer), status_code=500)
        else:
            json_stats = raster_statistics
            json_stats['raster']['uid'] = layer
            return Response(json.dumps(stats.get_stats(json_stats)), content_type='application/json; charset=utf-8')

    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())


@app.route('/raster/<layer>/hist/', methods=['GET'])
@app.route('/raster/<layer>/hist', methods=['GET'])
@cross_origin()
def get_histogram(layer):
    """
    Extracts histogram from a layer
    @param layer: workspace:layername
    @return: json with the raster statistics
    """
    try:
        if ':' not in layer:
            return PGeoException('Please Specify a workspace for ' + str(layer), status_code=500)
        else:
            json_stats = raster_histogram
            json_stats['raster']['uid'] = layer
            return Response(json.dumps(stats.get_histogram(json_stats)), content_type='application/json; charset=utf-8')

    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())


@app.route('/raster/<layer>/hist/<buckets>/', methods=['GET'])
@app.route('/raster/<layer>/hist/<buckets>', methods=['GET'])
@cross_origin(origins='*')
def get_histogram_buckets(layer, buckets):
    """
    Extracts histogram from a layer
    TODO: add a boolean and buckets
    default: boolean = True, buckets = 256
    @param layer: workspace:layername
    @param buckets: number of buckets i.e. 256
    @return: json with the raster statistics
    """
    try:
        if ':' not in layer:
            return PGeoException('Please Specify a workspace for ' + str(layer), status_code=500)
        else:
            json_stats = raster_histogram
            json_stats['raster']['uid'] = layer
            json_stats['stats']['buckets'] = int(buckets)
            return Response(json.dumps(stats.get_histogram(json_stats)), content_type='application/json; charset=utf-8')

    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())


@app.route('/raster/<layer>/lat/<lat>/lon/<lon>/', methods=['GET'])
@app.route('/raster/<layer>/lat/<lat>/lon/<lon>', methods=['GET'])
@cross_origin(origins='*')
def get_lat_lon(layer, lat, lon):
    """
    Get the value of the layer at lat/lon position
    @param layer: workspace:layername
    @param lat: latitude
    @param lon: longitude
    @return: json with the raster statistics
    """
    try:
        if ':' not in layer:
            return PGeoException('Please Specify a workspace for ' + str(layer), status_code=500)
        else:
            return Response({'TODO': 'TODO'}, content_type='application/json; charset=utf-8')

    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())


@app.route('/raster/spatial_query/', methods=['POST'])
@app.route('/raster/spatial_query', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_stats_by_layer():
    try:
        user_json = request.get_json()
        s = stats.zonal_stats(user_json)
        return Response(json.dumps(s), content_type='application/json; charset=utf-8')
    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())


@app.route('/rasters/spatial_query/', methods=['POST'])
@app.route('/rasters/spatial_query', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_stats_by_layers():
    try:
        user_json = request.get_json()
        response = []
        for uid in user_json['raster']['uids']:
            json_stat = copy.deepcopy(user_json)
            json_stat['raster']['uid'] = uid
            s = {}
            s[uid] = stats.zonal_stats(json_stat)
            response.append(s)

        return Response(json.dumps(response), content_type='application/json; charset=utf-8')
    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())