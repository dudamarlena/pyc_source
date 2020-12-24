# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeorest/pgeorest/spatialquery.py
# Compiled at: 2014-08-28 04:41:10
import json
from flask import Blueprint, Response
from flask.ext.cors import cross_origin
from pgeo.error.custom_exceptions import PGeoException, errors
from pgeo.utils import log
from pgeo.config.settings import settings
from pgeo.db.postgresql.common import DBConnection
from flask import request
app = Blueprint(__name__, __name__)
log = log.logger(__name__)
spatial_db = DBConnection(settings['db']['spatial'])

@app.route('/')
def index():
    return 'Welcome to the Spatial Query module!'


@app.route('/db/<datasource>/<query>/', methods=['GET'])
@app.route('/db/<datasource>/<query>', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def query_db(datasource, query):
    try:
        spatial_db = DBConnection(settings['db'][datasource])
        result = spatial_db.query(query)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())