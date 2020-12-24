# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/server/seeker.py
# Compiled at: 2012-07-12 07:27:19
import os, time, socket, threading, SocketServer
from setproctitle import setproctitle
from mole.server import Server
from mole.planner import Planner
from mole.event import EventError
from mole.helper.log import getLogger
from mole.output.serialize import OutputSerialize
try:
    import cPickle as pickle
except ImportError:
    import pickle

BUFSIZE = 1024

class ServerSeekerTCPRequestHandler(SocketServer.StreamRequestHandler):
    """Handle the seeker thread to perform a search."""

    def handle(self):
        query = self.request.recv(BUFSIZE).rstrip('\r\n')
        self.server.log.info('%-15s: start query: %s' % (
         '%s:%d' % self.client_address, query))
        self.plan = Planner.parse(query, context=self.server.config)
        if self.plan.has_input():
            self.plan.add_output(OutputSerialize())
            self.server.log.info('%-15s: start seek plan: %s' % (
             '%s:%d' % self.client_address, repr(self.plan)))
            t = time.time()
            for x in self.plan():
                print >> self.wfile, x

            self.server.log.info('%-15s: finished query in %2fs: %s' % (
             '%s:%d' % self.client_address,
             time.time() - t,
             query))


class ServerSeekerTCP(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    log = None


class ServerSeeker(Server):
    """Create an Seeker server thread"""

    def __init__(self, config, logger=None):
        self.config = config
        if logger:
            self.log = logger
        else:
            self.log = getLogger('mole: seeker')
        self.config = config

    def __call__(self, config):
        return self.execute(config)

    def run(self):
        setproctitle('mole: seeker')
        server = ServerSeekerTCP((self.config.server.host,
         self.config.server.port), ServerSeekerTCPRequestHandler)
        server.log = self.log
        server.config = self.config.config
        self.log.info('[MASTER] start seeker server on %s:%d' % (
         self.config.server.host, self.config.server.port))
        server.serve_forever()

    def cancel(self):
        self.log.warning('[MASTER]: stopping seeker due to cancel interrupt')