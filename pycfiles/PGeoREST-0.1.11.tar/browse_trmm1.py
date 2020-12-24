# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeorest/pgeorest/browse_trmm1.py
# Compiled at: 2014-09-01 03:54:11
from ftplib import FTP
import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from pgeo.config.settings import read_config_file_json
from pgeo.error.custom_exceptions import PGeoException
from pgeo.error.custom_exceptions import errors
from pgeo.dataproviders import trmm1 as t
browse_trmm1 = Blueprint('browse_trmm1', __name__)
conf = read_config_file_json('trmm1', 'data_providers')

@browse_trmm1.route('/')
@cross_origin(origins='*')
def list_years_service():
    try:
        out = t.list_years()
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_trmm1.route('/<year>')
@browse_trmm1.route('/<year>/')
@cross_origin(origins='*')
def list_months_service(year):
    try:
        out = t.list_months(year)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_trmm1.route('/<year>/<month>')
@browse_trmm1.route('/<year>/<month>/')
@cross_origin(origins='*')
def list_layers_service(year, month):
    try:
        out = t.list_layers(year, month)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException as e:
        raise PGeoException(e.get_message(), e.get_status_code())