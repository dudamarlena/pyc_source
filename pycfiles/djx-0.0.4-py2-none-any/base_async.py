# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/workers/base_async.py
# Compiled at: 2019-02-14 00:35:18
from datetime import datetime
import errno, socket, ssl, sys, gunicorn.http as http, gunicorn.http.wsgi as wsgi, gunicorn.util as util, gunicorn.workers.base as base
from gunicorn import six
ALREADY_HANDLED = object()

class AsyncWorker(base.Worker):

    def __init__(self, *args, **kwargs):
        super(AsyncWorker, self).__init__(*args, **kwargs)
        self.worker_connections = self.cfg.worker_connections

    def timeout_ctx(self):
        raise NotImplementedError()

    def is_already_handled(self, respiter):
        return respiter == ALREADY_HANDLED

    def handle(self, listener, client, addr):
        req = None
        try:
            try:
                parser = http.RequestParser(self.cfg, client)
                try:
                    listener_name = listener.getsockname()
                    if not self.cfg.keepalive:
                        req = six.next(parser)
                        self.handle_request(listener_name, req, client, addr)
                    else:
                        proxy_protocol_info = {}
                        while True:
                            req = None
                            with self.timeout_ctx():
                                req = six.next(parser)
                            if not req:
                                break
                            if req.proxy_protocol_info:
                                proxy_protocol_info = req.proxy_protocol_info
                            else:
                                req.proxy_protocol_info = proxy_protocol_info
                            self.handle_request(listener_name, req, client, addr)

                except http.errors.NoMoreData as e:
                    self.log.debug('Ignored premature client disconnection. %s', e)
                except StopIteration as e:
                    self.log.debug('Closing connection. %s', e)
                except ssl.SSLError:
                    six.reraise(*sys.exc_info())
                except EnvironmentError:
                    six.reraise(*sys.exc_info())
                except Exception as e:
                    self.handle_error(req, client, addr, e)

            except ssl.SSLError as e:
                if e.args[0] == ssl.SSL_ERROR_EOF:
                    self.log.debug('ssl connection closed')
                    client.close()
                else:
                    self.log.debug('Error processing SSL request.')
                    self.handle_error(req, client, addr, e)
            except EnvironmentError as e:
                if e.errno not in (errno.EPIPE, errno.ECONNRESET):
                    self.log.exception('Socket error processing request.')
                elif e.errno == errno.ECONNRESET:
                    self.log.debug('Ignoring connection reset')
                else:
                    self.log.debug('Ignoring EPIPE')
            except Exception as e:
                self.handle_error(req, client, addr, e)

        finally:
            util.close(client)

        return

    def handle_request(self, listener_name, req, sock, addr):
        request_start = datetime.now()
        environ = {}
        resp = None
        try:
            try:
                self.cfg.pre_request(self, req)
                resp, environ = wsgi.create(req, sock, addr, listener_name, self.cfg)
                environ['wsgi.multithread'] = True
                self.nr += 1
                if self.alive and self.nr >= self.max_requests:
                    self.log.info('Autorestarting worker after current request.')
                    resp.force_close()
                    self.alive = False
                if not self.cfg.keepalive:
                    resp.force_close()
                respiter = self.wsgi(environ, resp.start_response)
                if self.is_already_handled(respiter):
                    return False
                try:
                    if isinstance(respiter, environ['wsgi.file_wrapper']):
                        resp.write_file(respiter)
                    else:
                        for item in respiter:
                            resp.write(item)

                    resp.close()
                    request_time = datetime.now() - request_start
                    self.log.access(resp, req, environ, request_time)
                finally:
                    if hasattr(respiter, 'close'):
                        respiter.close()

                if resp.should_close():
                    raise StopIteration()
            except StopIteration:
                raise
            except EnvironmentError:
                six.reraise(*sys.exc_info())
            except Exception:
                if resp and resp.headers_sent:
                    self.log.exception('Error handling request')
                    try:
                        sock.shutdown(socket.SHUT_RDWR)
                        sock.close()
                    except EnvironmentError:
                        pass

                    raise StopIteration()
                raise

        finally:
            try:
                self.cfg.post_request(self, req, environ, resp)
            except Exception:
                self.log.exception('Exception in post_request hook')

        return True