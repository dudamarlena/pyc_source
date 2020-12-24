# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/clue/bzrserver/server.py
# Compiled at: 2009-03-01 11:10:34
import os
from clue.bzrserver import wsgi
from clue.bzrserver import utils
from wsgiref import simple_server

class Server(object):

    def __init__(self, configfile, host, port, show_access=False, passwdfile=None, bzrdir=None, logger=None):
        self.configfile = configfile
        self.host = host
        self.port = int(port)
        self.show_access = show_access
        self.passwdfile = passwdfile
        self.bzrdir = bzrdir
        if not bzrdir:
            self.bzrdir = os.path.abspath(os.getcwd())
        self.logger = logger
        if logger is None:
            self.logger = utils.logger
        return

    def run_server(self):
        self.logger.info('Serving path: %s' % self.bzrdir)
        app = wsgi.make_secured_app({}, self.bzrdir, configfile=self.configfile, passwdfile=self.passwdfile, logger=self.logger)

        class RequestHandler(simple_server.WSGIRequestHandler):
            show_access = self.show_access
            logger = self.logger

            def log_request(self, *args, **kw):
                if self.show_access:
                    self.logger.info(str(args) + str(kw))

        httpd = simple_server.make_server(self.host, self.port, app, handler_class=RequestHandler)
        self.logger.info('Now listening on %s:%i' % (self.host, self.port))
        httpd.serve_forever()