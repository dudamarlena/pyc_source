# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_distribution/geobricks_distribution/rest/distribution_main.py
# Compiled at: 2015-01-12 06:51:11
from flask import Flask
from flask.ext.cors import CORS
from geobricks_distribution.config.config import config
from geobricks_distribution.rest import distribution_rest
import logging
app = Flask(__name__)
cors = CORS(app, resources={'/*': {'origins': '*'}})
url_prefix = '/geobricks_distribution'
app.register_blueprint(distribution_rest.app, url_prefix=url_prefix)
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

def start_services():
    app.run(host=config['settings']['host'], port=config['settings']['port'], debug=config['settings']['debug'], threaded=True)


if __name__ == '__main__':
    start_services()