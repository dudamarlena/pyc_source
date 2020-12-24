# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/routes/router.py
# Compiled at: 2020-04-13 07:58:16
# Size of source mod 2**32: 1646 bytes
import logging
from flask import Flask

class Router:
    """Router"""

    def __init__(self, name):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class Router')
        self.name = name
        self.app = Flask(self.name)

    def run(self, host='0.0.0.0', port=None, debug=None):
        """ runs the development flask server

        :param host: default hostname
        :param port: the port of the webserver
        :param debug: run with debug output
        """
        self.app.run(host=host, port=port, debug=debug)

    def add_endpoint(self, endpoint=None, endpoint_name=None, method=None, handler=None):
        """ adds an endpoint to the application

        :param endpoint: specific endpoint for the app
        :param endpoint_name: endpoint name for the app
        :param method: method for handler call (POST, PUT, DELETE, GET)
        :param handler: handler function/method to execute
        """
        if method == 'POST':
            self.app.add_url_rule(endpoint, endpoint_name, handler, methods=['POST'])
        else:
            if method == 'PUT':
                self.app.add_url_rule(endpoint, endpoint_name, handler, methods=['PUT'])
            else:
                if method == 'DELETE':
                    self.app.add_url_rule(endpoint, endpoint_name, handler, methods=['DELETE'])
                else:
                    self.app.add_url_rule(endpoint, endpoint_name, handler)