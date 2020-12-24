# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_api/app.py
# Compiled at: 2018-09-27 14:18:55
# Size of source mod 2**32: 2305 bytes
from flask import Flask, jsonify
from mercury_api.configuration import get_api_configuration
from mercury_api.exceptions import HTTPError
from mercury_api.transaction_log import setup_logging
from mercury_api.views.active import active_blueprint
from mercury_api.views.inventory import inventory_blueprint
from mercury_api.views.rpc import rpc_blueprint
from mercury_api.custom_converters import BlackListConverter
app = Flask(__name__)
log = setup_logging(app)
app.url_map.converters['blacklist'] = BlackListConverter

@app.errorhandler(HTTPError)
def http_error(error):
    """
    Sets the app error handler to modify the error message in the 
    response object and log it in the transactional logger.
    :param error: 
    :return: Flask response object
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    log.error(error.message)
    return response


@app.after_request
def log_request(response):
    """
    Logs the response status in the transactional logger after the
    request is processed.
    :param response: 
    :return: Flask response object 
    """
    log.info(response.status)
    return response


app.register_blueprint(active_blueprint, url_prefix='/api/active')
app.register_blueprint(inventory_blueprint, url_prefix='/api/inventory')
app.register_blueprint(rpc_blueprint, url_prefix='/api/rpc')
if __name__ == '__main__':
    config = get_api_configuration()
    app.run(host=(config.api.host), port=(config.api.port), debug=True)