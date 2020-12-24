# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/server/server.py
# Compiled at: 2017-12-28 15:14:53
try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from http.server import HTTPServer, BaseHTTPRequestHandler

import logging, logging.handlers, os, os.path
try:
    from SocketServer import ThreadingMixIn
except ImportError:
    from socketserver import ThreadingMixIn

import signal, sys
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
import flawless.lib.config
from flawless.lib.storage import DiskStorage
from flawless.server.api import Flawless
from flawless.server.service import FlawlessThriftServiceHandler
from flawless.server.webapp import FlawlessWebServiceHandler
log = logging.getLogger(__name__)
config = flawless.lib.config.get()

class SimpleThreadedHTTPServer(ThreadingMixIn, HTTPServer):

    def attach_service(self, service):
        self.service = service

    def server_close(self):
        HTTPServer.server_close(self)


class SimpleRequestHTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parts = urlparse.urlparse(self.path)
        kwargs = dict(urlparse.parse_qsl(parts.query))
        ret = None
        try:
            try:
                if hasattr(self.server.service, parts.path[1:] or 'index'):
                    ret = getattr(self.server.service, parts.path[1:] or 'index')(**kwargs)
                    self.send_response(200)
                    self.send_header('Content-Length', len(ret or ''))
                    self.send_header('Content-Type', 'text/html')
                else:
                    self.send_response(404)
            except Exception as e:
                log.exception(e)
                self.send_response(500)

        finally:
            self.end_headers()

        if ret:
            self.wfile.write(bytes(ret.encode('utf8')))
        return

    def do_POST(self):
        parts = urlparse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length'))
        req_str = self.rfile.read(content_length).decode('utf8')
        ret = None
        try:
            try:
                ret = getattr(self.server.service, parts.path[1:])(req_str)
                self.send_response(200)
                if ret:
                    self.send_header('Content-Length', len(ret))
                    self.send_header('Content-Type', 'text/html')
            except Exception as e:
                log.exception(e)
                self.send_response(500)

        finally:
            self.end_headers()

        if ret:
            self.wfile.write(bytes(ret.encode('utf8')))
        return


def serve(conf_path, storage_factory=None):
    """This method starts the server. There are two processes, one is an HTTP server that shows
    and admin interface and the second is a Thrift server that the client code calls.

    Arguments:
        `conf_path` - The path to your flawless.cfg file
        `storage_factory` - You can pass in your own storage class that implements StorageInterface. You must implement
                            storage_cls if you want Flawless to be horizontally scalable, since by default it will just
                            store everything on the local disk.
    """
    flawless.lib.config.init_config(conf_path)
    if not os.path.exists(config.data_dir_path):
        os.makedirs(config.data_dir_path)
    storage_factory = storage_factory or (lambda partition: DiskStorage(partition=partition))
    root_logger = logging.getLogger()
    root_handler = logging.handlers.TimedRotatingFileHandler(filename=config.log_file, when='d', interval=1, backupCount=config.log_days_to_keep)
    root_logger.setLevel(getattr(logging, config.log_level))
    root_logger.addHandler(root_handler)
    child_pid = os.fork()
    if child_pid == 0:
        handler = FlawlessWebServiceHandler(storage_factory=storage_factory)
        server = SimpleThreadedHTTPServer(('', config.http_port), SimpleRequestHTTPHandler)
        server.attach_service(handler)
        server.request_queue_size = 50
        try:
            server.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            server.server_close()

    else:
        handler = FlawlessThriftServiceHandler(storage_factory=storage_factory)
        processor = Flawless.Processor(handler)
        transport = TSocket.TServerSocket(port=config.port)
        tfactory = TTransport.TFramedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
        try:
            server.serve()
        except (KeyboardInterrupt, SystemExit):
            handler.errors_seen.sync()
            transport.close()
            os.kill(child_pid, signal.SIGINT)


def main():
    conf_path = flawless.lib.config.default_path
    if len(sys.argv) > 1:
        conf_path = sys.argv[1]
    serve(conf_path)


if __name__ == '__main__':
    main()