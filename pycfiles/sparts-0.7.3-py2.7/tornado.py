# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/tornado.py
# Compiled at: 2015-02-07 04:24:17
"""This module contains tornado-related helper tasks and classes."""
from __future__ import absolute_import
from six import itervalues
from sparts.counters import counter
from sparts.sparts import option
from sparts.vtask import VTask, SkipTask
import tornado.ioloop, tornado.web, tornado.httpserver, tornado.netutil, grp, os

class TornadoIOLoopTask(VTask):
    """Configure and run the Tornado IO Loop in a sparts task"""
    OPT_PREFIX = 'tornado'

    def initTask(self):
        super(TornadoIOLoopTask, self).initTask()
        needed = getattr(self.service, 'REQUIRE_TORNADO', False)
        for t in self.service.tasks:
            if isinstance(t, TornadoTask):
                needed = True

        if not needed:
            raise SkipTask('No TornadoTasks found or enabled')
        self.ioloop = tornado.ioloop.IOLoop.instance()

    def _runloop(self):
        self.ioloop.start()

    def stop(self):
        self.ioloop.stop()
        super(TornadoIOLoopTask, self).stop()


class TornadoTask(VTask):
    """Base class for tasks that require the tornado IO Loop.
    
    Implicitly configures the tornado IO Loop task as a dependency.
    
    The ioloop can be accessed via `self.ioloop`"""
    DEPS = [
     TornadoIOLoopTask]

    def initTask(self):
        super(TornadoTask, self).initTask()
        self.ioloop_task = self.service.requireTask('TornadoIOLoopTask')

    @property
    def ioloop(self):
        return self.ioloop_task.ioloop


class TornadoHTTPTask(TornadoTask):
    """A loopless task that implements an HTTP server using Tornado.
    
    It is loopless because it depends on tornado's separate IOLoop task.  You
    will need to subclass this to do something more useful."""
    LOOPLESS = True
    OPT_PREFIX = 'http'
    DEFAULT_PORT = 0
    DEFAULT_HOST = ''
    DEFAULT_SOCK = ''
    requests = counter()
    host = option(metavar='HOST', default=lambda cls: cls.DEFAULT_HOST, help='Address to bind server to [%(default)s]')
    port = option(metavar='PORT', default=lambda cls: cls.DEFAULT_PORT, help='Port to run server on [%(default)s]')
    sock = option(metavar='PATH', default=lambda cls: cls.DEFAULT_SOCK, help='Default path to use for local file socket [%(default)s]')
    group = option(name='sock-group', metavar='GROUP', default='', help='Group to create unix files as [%(default)s]')

    def getApplicationConfig(self):
        """Override this to register custom handlers / routes."""
        return [
         (
          '/', HelloWorldHandler)]

    def initTask(self):
        super(TornadoHTTPTask, self).initTask()
        self.app = tornado.web.Application(self.getApplicationConfig(), log_function=self.tornadoRequestLog)
        self.server = tornado.httpserver.HTTPServer(self.app)
        if self.sock:
            assert self.host == self.DEFAULT_HOST, 'Do not specify host *and* sock (%s, %s)' % (
             self.host, self.sock)
            assert int(self.port) == self.DEFAULT_PORT, 'Do not specify port *and* sock (%s, %s)' % (
             self.port, self.DEFAULT_PORT)
            gid, mode = (-1, 384)
            if self.group != '':
                e = grp.getgrnam(self.group)
                gid, mode = e.gr_gid, 432
            sock = tornado.netutil.bind_unix_socket(self.sock, mode=mode)
            if gid != -1:
                os.chown(self.sock, -1, gid)
            self.server.add_sockets([sock])
        else:
            self.server.listen(self.port, self.host)
        self.bound_addrs = []
        for sock in itervalues(self.server._sockets):
            sockaddr = sock.getsockname()
            self.bound_addrs.append(sockaddr)
            self.logger.info('%s Server Started on %s (port %s)', self.name, sockaddr[0], sockaddr[1])

    @property
    def bound_v4_addrs(self):
        return [ a[0] for a in self.bound_addrs if len(a) == 2 ]

    @property
    def bound_v6_addrs(self):
        return [ a[0] for a in self.bound_addrs if len(a) == 4 ]

    def tornadoRequestLog(self, handler):
        self.requests.increment()

    def stop(self):
        super(TornadoHTTPTask, self).stop()
        self.server.stop()


class HelloWorldHandler(tornado.web.RequestHandler):
    """A sample twisted web handler for use in the default http server task"""

    def get(self):
        self.write('Hello, world')