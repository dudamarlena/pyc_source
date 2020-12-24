# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jr/GoogleDrive/Dev/python/tinflask/tinflask/web.py
# Compiled at: 2015-03-06 18:15:51
# Size of source mod 2**32: 2106 bytes
import json, sys, time
from os import environ
from flask import Flask
import tinflask.handlers

class Application(object):
    __doc__ = 'tinflask.web.Application instance.\n\n    The built-in `/status` endpoint now requires authorization.\n    Keys endpoints are also added to hot-reload authorized/private keys, and\n    simple listing of loaded public keys.\n\n    A new instance will set the global key function within tinflask.handlers for\n    all signed/authorized endpoints. This key function retrieves private keys\n    for the authorization process.\n    '

    def __init__(self, handlers=None, **settings):
        """Creates a new tinflask/app with the given handlers and settings.

        - If an `ENDPOINT` environment variable is set all handlers will be prefixed with it.
        - The `status` endpoint is re-added as a signed endpoint.
        - Key endpoints `keys`, `keys/private`, and `keys/authorized` are also added as signed endpoints.
        """
        self.app = Flask(__name__)
        try:
            port_str = environ.get('PORT', '8080')
            self.port = int(port_str)
        except ValueError:
            self.port = 8080

        self.debug = True if environ.get('DEBUG') == 'true' else False
        self.address = environ.get('HOST', '0.0.0.0')
        self.jobs = []
        self.app.route('/ping')(tinflask.handlers.ping)
        self.app.route('/time')(tinflask.handlers.time)
        status_handler = tinflask.handlers.status(self.jobs)
        self.app.route('/status')(status_handler)

    def add_status_job(self, name, timeout, job_func):
        """Adds the given status job to the collection of jobs.
        """
        self.jobs.append((name, timeout, job_func))

    def run(self):
        """Starts the Flask service using the address, port, and debug values
        found from either environment variables or config variables.
        """
        self.app.run(host=self.address, port=self.port, debug=self.debug)