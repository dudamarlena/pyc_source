# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/workers/ggevent.py
# Compiled at: 2019-02-14 00:35:18
import errno, os, sys
from datetime import datetime
from functools import partial
import time
_socket = __import__('socket')
if sys.platform == 'darwin':
    os.environ['EVENT_NOKQUEUE'] = '1'
try:
    import gevent
except ImportError:
    raise RuntimeError('You need gevent installed to use this worker.')

from gevent.pool import Pool
from gevent.server import StreamServer
from gevent.socket import wait_write, socket
from gevent import pywsgi
import gunicorn
from gunicorn.http.wsgi import base_environ
from gunicorn.workers.base_async import AsyncWorker
from gunicorn.http.wsgi import sendfile as o_sendfile
VERSION = 'gevent/%s gunicorn/%s' % (gevent.__version__, gunicorn.__version__)

def _gevent_sendfile(fdout, fdin, offset, nbytes):
    while True:
        try:
            return o_sendfile(fdout, fdin, offset, nbytes)
        except OSError as e:
            if e.args[0] == errno.EAGAIN:
                wait_write(fdout)
            else:
                raise


def patch_sendfile():
    from gunicorn.http import wsgi
    if o_sendfile is not None:
        setattr(wsgi, 'sendfile', _gevent_sendfile)
    return


class GeventWorker(AsyncWorker):
    server_class = None
    wsgi_handler = None

    def patch(self):
        from gevent import monkey
        monkey.noisy = False
        if gevent.version_info[0] == 0:
            monkey.patch_all()
        else:
            monkey.patch_all(subprocess=True)
        patch_sendfile()
        sockets = []
        for s in self.sockets:
            if sys.version_info[0] == 3:
                sockets.append(socket(s.FAMILY, _socket.SOCK_STREAM, fileno=s.sock.fileno()))
            else:
                sockets.append(socket(s.FAMILY, _socket.SOCK_STREAM, _sock=s))

        self.sockets = sockets

    def notify(self):
        super(GeventWorker, self).notify()
        if self.ppid != os.getppid():
            self.log.info('Parent changed, shutting down: %s', self)
            sys.exit(0)

    def timeout_ctx(self):
        return gevent.Timeout(self.cfg.keepalive, False)

    def run(self):
        servers = []
        ssl_args = {}
        if self.cfg.is_ssl:
            ssl_args = dict(server_side=True, **self.cfg.ssl_options)
        for s in self.sockets:
            s.setblocking(1)
            pool = Pool(self.worker_connections)
            if self.server_class is not None:
                environ = base_environ(self.cfg)
                environ.update({'wsgi.multithread': True, 
                   'SERVER_SOFTWARE': VERSION})
                server = self.server_class(s, application=self.wsgi, spawn=pool, log=self.log, handler_class=self.wsgi_handler, environ=environ, **ssl_args)
            else:
                hfun = partial(self.handle, s)
                server = StreamServer(s, handle=hfun, spawn=pool, **ssl_args)
            server.start()
            servers.append(server)

        while self.alive:
            self.notify()
            gevent.sleep(1.0)

        try:
            for server in servers:
                if hasattr(server, 'close'):
                    server.close()
                if hasattr(server, 'kill'):
                    server.kill()

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
            for server in servers:
                server.stop(timeout=1)

        except:
            pass

        return

    def handle(self, listener, client, addr):
        client.setblocking(1)
        super(GeventWorker, self).handle(listener, client, addr)

    def handle_request(self, listener_name, req, sock, addr):
        try:
            super(GeventWorker, self).handle_request(listener_name, req, sock, addr)
        except gevent.GreenletExit:
            pass
        except SystemExit:
            pass

    def handle_quit(self, sig, frame):
        gevent.spawn(super(GeventWorker, self).handle_quit, sig, frame)

    def handle_usr1(self, sig, frame):
        gevent.spawn(super(GeventWorker, self).handle_usr1, sig, frame)

    if gevent.version_info[0] == 0:

        def init_process(self):
            self.patch()
            import gevent.core
            gevent.core.reinit()
            gevent.core.dns_shutdown(fail_requests=1)
            gevent.core.dns_init()
            super(GeventWorker, self).init_process()

    else:

        def init_process(self):
            self.patch()
            from gevent import hub
            hub.reinit()
            super(GeventWorker, self).init_process()


class GeventResponse(object):
    status = None
    headers = None
    sent = None

    def __init__(self, status, headers, clength):
        self.status = status
        self.headers = headers
        self.sent = clength


class PyWSGIHandler(pywsgi.WSGIHandler):

    def log_request(self):
        start = datetime.fromtimestamp(self.time_start)
        finish = datetime.fromtimestamp(self.time_finish)
        response_time = finish - start
        resp_headers = getattr(self, 'response_headers', {})
        resp = GeventResponse(self.status, resp_headers, self.response_length)
        if hasattr(self, 'headers'):
            req_headers = self.headers.items()
        else:
            req_headers = []
        self.server.log.access(resp, req_headers, self.environ, response_time)

    def get_environ(self):
        env = super(PyWSGIHandler, self).get_environ()
        env['gunicorn.sock'] = self.socket
        env['RAW_URI'] = self.path
        return env


class PyWSGIServer(pywsgi.WSGIServer):
    pass


class GeventPyWSGIWorker(GeventWorker):
    """The Gevent StreamServer based workers."""
    server_class = PyWSGIServer
    wsgi_handler = PyWSGIHandler