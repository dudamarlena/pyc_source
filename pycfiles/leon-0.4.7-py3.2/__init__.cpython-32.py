# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/leon/__init__.py
# Compiled at: 2013-05-08 06:42:14
import sys, logging
log = logging.getLogger('leon')
import cherrypy
from leon.web_handler import WebHandler as _WebHandler
from leon.arg_conversions import list_of

def init_logging_system(app):
    """
    :param app: The Leon application
    :type app: WebHandler
    """
    handler = None
    if app.is_in_development_mode():
        print('Leon: Starting in development mode')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('[%(relativeCreated)-5d %(levelname)-8s %(name)s] %(message)s'))
        logging.root.setLevel(logging.DEBUG)
    else:
        print('Leon: Starting in production mode')
        logging.root.setLevel(logging.WARN)
    cherrypy.log.access_log.propagate = False
    cherrypy.log.error_log.setLevel(logging.WARN)
    cherrypy.log.error_log.addHandler(handler)
    logging.root.addHandler(handler)
    return


def create(config=None, init_logging=True):
    """
    :param config: Optional configuration dict
    :type config: dict
    :param init_logging:
    :return: The Leon application
    :rtype: WebHandler
    """
    app = _WebHandler(config)
    if init_logging:
        init_logging_system(app)
    return app


def start_server(app, host='0.0.0.0', port=8080):
    """
    :param app: The Leon application to start
    :type app: WebHandler
    """
    cherrypy.server.socket_host = host
    cherrypy.server.socket_port = port
    cherrypy.quickstart(app)