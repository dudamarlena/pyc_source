# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_geostatistics/geobricks_geostatistics/rest/geostatistics_main.py
# Compiled at: 2015-03-11 12:56:49
from flask import Flask
from flask.ext.cors import CORS
from geobricks_geostatistics.config.config import config
from geobricks_geostatistics.rest import geostatistics_rest
import logging
app = Flask(__name__)
cors = CORS(app, resources={'/*': {'origins': '*'}})
url_prefix = '/geostatistics'
app.register_blueprint(geostatistics_rest.app, url_prefix=url_prefix)
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

def start_engine():
    app.run(host=config['settings']['host'], port=config['settings']['port'], debug=config['settings']['debug'], threaded=True)


if __name__ == '__main__':
    start_engine()