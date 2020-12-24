# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/thrift/cppserver.py
# Compiled at: 2015-08-18 19:34:31
"""Thrift Server task using TNonblockingServer"""
from __future__ import absolute_import
from sparts.sparts import option
from sparts.tasks.thrift.server import ThriftServerTask
from thrift.server.TCppServer import TCppServer

class CPPServerTask(ThriftServerTask):
    """Spin up a thrift TNonblockingServer in a sparts worker thread"""
    DEFAULT_PORT = 0
    OPT_PREFIX = 'thrift'
    bound_host = bound_port = None
    port = option(default=lambda cls: cls.DEFAULT_PORT, type=int, metavar='PORT', help='Port to run server on [%(default)s]')
    num_threads = option(name='threads', default=4, type=int, metavar='N', help='Server Worker Threads [%(default)s]')

    def initTask(self):
        """Overridden to bind sockets, etc"""
        super(CPPServerTask, self).initTask()
        self._stopped = False
        self.server = TCppServer(self.processor)
        self.server.setPort(self.port)
        self.server.setNWorkerThreads(self.num_threads)
        self.server.setup()
        self.bound_addrs = [
         self.server.getAddress()]
        for addrinfo in self.bound_addrs:
            self.bound_host, self.bound_port = addrinfo[0:2]
            self.logger.info('%s Server Started on %s', self.name, self._fmt_hostport(self.bound_host, self.bound_port))

    def _fmt_hostport(self, host, port):
        if ':' in host:
            return '[%s]:%d' % (host, port)
        else:
            return '%s:%d' % (host, port)

    def stop(self):
        """Overridden to tell the thrift server to shutdown asynchronously"""
        self.server.stop()

    def _runloop(self):
        """Overridden to execute TNonblockingServer's main loop"""
        self.server.serve()