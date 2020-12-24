# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeorest/pgeorest/__init__.py
# Compiled at: 2014-09-01 09:00:54
from flask import Flask
from flask.ext.cors import CORS
from pgeorest.browse_modis import browse_modis
from pgeorest.download import download
from pgeorest.browse_trmm2 import browse_trmm2
from pgeorest.schema import schema
from pgeorest.filesystem import filesystem
from pgeorest.metadata import metadata
from pgeorest.search import search
from pgeorest import stats
from pgeorest import spatialquery
from pgeorest import distribution
import logging
app = Flask(__name__)
cors = CORS(app, resources={'/*': {'origins': '*'}})
app.register_blueprint(browse_modis, url_prefix='/browse/modis')
app.register_blueprint(browse_trmm2, url_prefix='/browse/trmm2')
app.register_blueprint(download, url_prefix='/download')
app.register_blueprint(schema, url_prefix='/schema')
app.register_blueprint(filesystem, url_prefix='/filesystem')
app.register_blueprint(metadata, url_prefix='/metadata')
app.register_blueprint(search, url_prefix='/search')
app.register_blueprint(stats.app, url_prefix='/stats')
app.register_blueprint(spatialquery.app, url_prefix='/spatialquery')
app.register_blueprint(distribution.app, url_prefix='/distribution')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)