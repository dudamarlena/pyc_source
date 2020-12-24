# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/hejtado/quido/app.py
# Compiled at: 2019-10-14 14:45:14
# Size of source mod 2**32: 1594 bytes
import os, logging.config
from hejtado.quido import app, blueprint
import hejtado.quido.api as api
from hejtado.quido.settings import *
import hejtado.quido.api.endpoints.relays as relays_namespace
import hejtado.quido.api.endpoints.thermometers as thermometers_namespace
from hejtado.quido.settings import QUIDO_API_VERSION
logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(flask_app):
    """
    Configure Flask app
    :param flask_app: Flask app instance
    :return: None
    """
    server_name = FLASK_SERVER + ':' + str(FLASK_PORT)
    flask_app.config['SERVER_NAME'] = server_name
    flask_app.config['PORT'] = FLASK_PORT
    flask_app.config['ENV'] = FLASK_ENV


def initialize_app(flask_app):
    """
    Initialize Flask app
    :param flask_app: Flask aplication instance
    :return: None
    """
    configure_app(flask_app)
    api.init_app(blueprint)
    api.add_namespace(relays_namespace)
    api.add_namespace(thermometers_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    """
    Main function
    :return:    Flask app instance
    """
    initialize_app(app)
    log.info('Starting server at http://{}/api/{}'.format(app.config['SERVER_NAME'], QUIDO_API_VERSION))
    return app.run(debug=FLASK_DEBUG)


if __name__ == '__main__':
    main()