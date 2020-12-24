# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socketio/sgunicorn.py
# Compiled at: 2014-02-03 00:13:04
import os, gevent, time
from gevent.pool import Pool
from gevent.server import StreamServer
from gunicorn.workers.ggevent import GeventPyWSGIWorker
from gunicorn.workers.ggevent import PyWSGIHandler
from gunicorn.workers.ggevent import GeventResponse
from gunicorn import version_info as gunicorn_version
from socketio.server import SocketIOServer
from socketio.handler import SocketIOHandler
from geventwebsocket.handler import WebSocketHandler
from datetime import datetime
from functools import partial

class GunicornWSGIHandler(PyWSGIHandler, SocketIOHandler):
    pass


class GunicornWebSocketWSGIHandler(WebSocketHandler):

    def log_request(self):
        start = datetime.fromtimestamp(self.time_start)
        finish = datetime.fromtimestamp(self.time_finish)
        response_time = finish - start
        resp = GeventResponse(self.status, [], self.response_length)
        req_headers = [ h.split(':', 1) for h in self.headers.headers ]
        self.server.log.access(resp, req_headers, self.environ, response_time)


class GeventSocketIOBaseWorker(GeventPyWSGIWorker):
    """ The base gunicorn worker class """
    transports = None

    def __init__(self, age, ppid, socket, app, timeout, cfg, log):
        if os.environ.get('POLICY_SERVER', None) is None:
            if self.policy_server:
                os.environ['POLICY_SERVER'] = 'true'
        else:
            self.policy_server = False
        super(GeventSocketIOBaseWorker, self).__init__(age, ppid, socket, app, timeout, cfg, log)
        return

    def run(self):
        if gunicorn_version >= (0, 17, 0):
            servers = []
            ssl_args = {}
            if self.cfg.is_ssl:
                ssl_args = dict(server_side=True, do_handshake_on_connect=False, **self.cfg.ssl_options)
            for s in self.sockets:
                s.setblocking(1)
                pool = Pool(self.worker_connections)
                if self.server_class is not None:
                    self.server_class.base_env['wsgi.multiprocess'] = self.cfg.workers > 1
                    server = self.server_class(s, application=self.wsgi, spawn=pool, resource=self.resource, log=self.log, policy_server=self.policy_server, handler_class=self.wsgi_handler, ws_handler_class=self.ws_wsgi_handler, **ssl_args)
                else:
                    hfun = partial(self.handle, s)
                    server = StreamServer(s, handle=hfun, spawn=pool, **ssl_args)
                server.start()
                servers.append(server)

            pid = os.getpid()
            try:
                while self.alive:
                    self.notify()
                    if pid == os.getpid() and self.ppid != os.getppid():
                        self.log.info('Parent changed, shutting down: %s', self)
                        break
                    gevent.sleep(1.0)

            except KeyboardInterrupt:
                pass
            else:
                try:
                    [ server.stop_accepting() for server in servers ]
                    ts = time.time()
                    while time.time() - ts <= self.cfg.graceful_timeout:
                        accepting = 0
                        for server in servers:
                            if server.pool.free_count() != server.pool.size:
                                accepting += 1

                        if not accepting:
                            return
                        self.notify()
                        gevent.sleep(1.0)

                    self.log.warning('Worker graceful timeout (pid:%s)' % self.pid)
                    [ server.stop(timeout=1) for server in servers ]
                except:
                    pass

        else:
            self.socket.setblocking(1)
            pool = Pool(self.worker_connections)
            self.server_class.base_env['wsgi.multiprocess'] = self.cfg.workers > 1
            server = self.server_class(self.socket, application=self.wsgi, spawn=pool, resource=self.resource, log=self.log, policy_server=self.policy_server, handler_class=self.wsgi_handler, ws_handler_class=self.ws_wsgi_handler)
            server.start()
            pid = os.getpid()
            try:
                while self.alive:
                    self.notify()
                    if pid == os.getpid() and self.ppid != os.getppid():
                        self.log.info('Parent changed, shutting down: %s', self)
                        break
                    gevent.sleep(1.0)

            except KeyboardInterrupt:
                pass

            try:
                server.kill()
                ts = time.time()
                while time.time() - ts <= self.cfg.graceful_timeout:
                    if server.pool.free_count() == server.pool.size:
                        return
                    self.notify()
                    gevent.sleep(1.0)

                self.log.warning('Worker graceful timeout (pid:%s)' % self.pid)
                server.stop(timeout=1)
            except:
                pass

            return


class GeventSocketIOWorker(GeventSocketIOBaseWorker):
    """
    Default gunicorn worker utilizing gevent

    Uses the namespace 'socket.io' and defaults to the flash policy server
    being disabled.
    """
    server_class = SocketIOServer
    wsgi_handler = GunicornWSGIHandler
    ws_wsgi_handler = GunicornWebSocketWSGIHandler
    resource = 'socket.io'
    policy_server = True


class NginxGeventSocketIOWorker(GeventSocketIOWorker):
    """
    Worker which will not attempt to connect via websocket transport

    Nginx is not compatible with websockets and therefore will not add the
    wsgi.websocket key to the wsgi environment.
    """
    transports = [
     'xhr-polling']