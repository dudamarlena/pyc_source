# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/geobricks/geobricks/server/geobricks_raster_correlation/geobricks_raster_correlation/rest/raster_correlation_rest.py
# Compiled at: 2015-06-04 04:11:33
import json
from flask import Blueprint
from flask import Response, request
from flask.ext.cors import cross_origin
from geobricks_raster_correlation.core.raster_correlation_core import get_correlation_json
app = Blueprint(__name__, __name__)

@app.route('/discovery/')
@cross_origin(origins='*')
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {'name': 'Raster correlation service', 
       'description': 'Functionalities to correlate raster data.', 
       'type': 'SERVICE'}
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@app.route('/raster/', methods=['POST'])
@app.route('/raster', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_scatter_plot():
    try:
        user_json = request.get_json()
        result = get_correlation_json(user_json)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception as e:
        raise Exception(e.get_message(), e.get_status_code())


@app.route('/test/raster', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_scatter_plot_test():
    try:
        obj = {'raster': [
                    {'workspace': 'workspace', 
                       'layerName': 'wheat_actual_biomprod_201010_doukkala', 
                       'datasource': 'geoserver'},
                    {'workspace': 'workspace', 
                       'layerName': 'wheat_potential_biomprod_201010_doukkala', 
                       'datasource': 'geoserver'}], 
           'stats': {'correlation': {'bins': 20}}}
        result = get_correlation_json(obj)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception as e:
        raise Exception(e.get_message(), e.get_status_code())