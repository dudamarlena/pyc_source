# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/../pyipv8/ipv8/REST/rest_manager.py
# Compiled at: 2019-06-07 08:10:38
from __future__ import absolute_import
import logging
from traceback import format_tb
from twisted.internet import reactor
from twisted.internet.defer import maybeDeferred
from twisted.python.compat import intToBytes
from twisted.web import http, server
from .json_util import dumps
from .root_endpoint import RootEndpoint
from ..taskmanager import TaskManager

class RESTManager(TaskManager):
    """
    This class is responsible for managing the startup and closing of the HTTP API.
    """

    def __init__(self, session):
        super(RESTManager, self).__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self.session = session
        self.site = None
        self.root_endpoint = None
        return

    def start(self, port=8085):
        """
        Starts the HTTP API with the listen port as specified in the session configuration.
        """
        self.root_endpoint = RootEndpoint(self.session)
        site = server.Site(resource=self.root_endpoint)
        site.requestFactory = RESTRequest
        self.site = reactor.listenTCP(port, site, interface='127.0.0.1')

    def stop(self):
        """
        Stop the HTTP API and return a deferred that fires when the server has shut down.
        """
        return maybeDeferred(self.site.stopListening)


class RESTRequest(server.Request):
    """
    This class gracefully takes care of unhandled exceptions raised during the processing of any request.
    """
    defaultContentType = 'application/json'

    def __init__(self, *args, **kw):
        server.Request.__init__(self, *args, **kw)
        self._logger = logging.getLogger(self.__class__.__name__)
        self.setHeader('Access-Control-Allow-Origin', '*')

    def processingFailed(self, failure):
        self._logger.exception(failure)
        response = {'error': {'handled': False, 
                     'code': failure.value.__class__.__name__, 
                     'message': str(failure.value)}}
        if self.site.displayTracebacks:
            response['error']['trace'] = format_tb(failure.getTracebackObject())
        body = dumps(response, True).encode('utf-8')
        self.setResponseCode(http.INTERNAL_SERVER_ERROR)
        self.setHeader('Content-Type', self.defaultContentType)
        self.setHeader('Content-Length', intToBytes(len(body)))
        self.write(body)
        self.finish()
        return failure