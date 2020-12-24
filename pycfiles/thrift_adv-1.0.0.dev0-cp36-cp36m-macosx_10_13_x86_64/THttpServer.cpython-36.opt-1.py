# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/server/THttpServer.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 4302 bytes
import ssl
from six.moves import BaseHTTPServer
from thrift.server import TServer
from thrift.transport import TTransport

class ResponseException(Exception):
    __doc__ = 'Allows handlers to override the HTTP response\n\n    Normally, THttpServer always sends a 200 response.  If a handler wants\n    to override this behavior (e.g., to simulate a misconfigured or\n    overloaded web server during testing), it can raise a ResponseException.\n    The function passed to the constructor will be called with the\n    RequestHandler as its only argument.\n    '

    def __init__(self, handler):
        self.handler = handler


class THttpServer(TServer.TServer):
    __doc__ = 'A simple HTTP-based Thrift server\n\n    This class is not very performant, but it is useful (for example) for\n    acting as a mock version of an Apache-based PHP Thrift endpoint.\n    '

    def __init__(self, processor, server_address, inputProtocolFactory, outputProtocolFactory=None, server_class=BaseHTTPServer.HTTPServer, **kwargs):
        """Set up protocol factories and HTTP (or HTTPS) server.

        See BaseHTTPServer for server_address.
        See TServer for protocol factories.

        To make a secure server, provide the named arguments:
        * cafile    - to validate clients [optional]
        * cert_file - the server cert
        * key_file  - the server's key
        """
        if outputProtocolFactory is None:
            outputProtocolFactory = inputProtocolFactory
        TServer.TServer.__init__(self, processor, None, None, None, inputProtocolFactory, outputProtocolFactory)
        thttpserver = self

        class RequestHander(BaseHTTPServer.BaseHTTPRequestHandler):

            def do_POST(self):
                itrans = TTransport.TFileObjectTransport(self.rfile)
                otrans = TTransport.TFileObjectTransport(self.wfile)
                itrans = TTransport.TBufferedTransport(itrans, int(self.headers['Content-Length']))
                otrans = TTransport.TMemoryBuffer()
                iprot = thttpserver.inputProtocolFactory.getProtocol(itrans)
                oprot = thttpserver.outputProtocolFactory.getProtocol(otrans)
                try:
                    thttpserver.processor.process(iprot, oprot)
                except ResponseException as exn:
                    exn.handler(self)
                else:
                    self.send_response(200)
                    self.send_header('content-type', 'application/x-thrift')
                    self.end_headers()
                    self.wfile.write(otrans.getvalue())

        self.httpd = server_class(server_address, RequestHander)
        if kwargs.get('cafile') or kwargs.get('cert_file') or kwargs.get('key_file'):
            context = ssl.create_default_context(cafile=(kwargs.get('cafile')))
            context.check_hostname = False
            context.load_cert_chain(kwargs.get('cert_file'), kwargs.get('key_file'))
            context.verify_mode = ssl.CERT_REQUIRED if kwargs.get('cafile') else ssl.CERT_NONE
            self.httpd.socket = context.wrap_socket((self.httpd.socket), server_side=True)

    def serve(self):
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.socket.close()