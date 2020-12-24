# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_mapclassify/geobricks_mapclassify/rest/mapclassify_rest.py
# Compiled at: 2015-04-01 04:02:21
import json, os, urllib2
from flask import Blueprint
from flask import Response, request, send_from_directory
from flask.ext.cors import cross_origin
from geobricks_common.core.log import logger
from geobricks_mapclassify.config.config import config
from geobricks_mapclassify.core.mapclassify import MapClassify, get_distribution_folder
log = logger(__file__)
app = Blueprint('classification_sld', 'classification_sld')

@app.route('/')
@cross_origin(origins='*')
def root():
    """
    Root REST service.
    @return: Welcome message.
    """
    return 'Welcome to Geobricks Map Classify Service!'


@app.route('/discovery/')
@app.route('/discovery')
@cross_origin(origins='*')
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {'name': 'Classification SLD service', 
       'description': 'Functionalities to create SLD based on classification values', 
       'type': 'SERVICE'}
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@app.route('/download/sld/<id>/', methods=['GET'])
@app.route('/download/sld/<id>', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_zip_file(id):
    try:
        distribution_folder = get_distribution_folder(config)
        path = os.path.join(distribution_folder)
        log.info(path)
        return send_from_directory(directory=path, filename=str(id))
    except Exception as e:
        log.error(e)
        raise Exception(e)


@app.route('/join/', methods=['POST'])
@app.route('/join', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_rasters_spatial_query():
    try:
        user_json = request.get_json()
        log.info(user_json)
        base_url = config['settings']['base_url'] if 'base_url' in config['settings'] else ''
        distribution_url = request.host_url + base_url + 'mapclassify/download/sld/'
        mapclassify = MapClassify(config)
        result = mapclassify.classify(user_json, distribution_url)
        print result
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception as e:
        log.error(e)


@app.route('/request/', methods=['GET'])
@app.route('/request', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def proxy():
    try:
        url = request.args.get('urlWMS')
        if url is None:
            raise Exception('Parameter is not set')
        r = urllib2.urlopen(url + '?' + request.query_string).read()
        return Response(r, content_type='text/plain; charset=utf-8')
    except Exception as e:
        log.error(e)

    return