# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/server/server_basic.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jul 8, 2011\n\n@package: ally http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the basic web server based on the python build in http server (this type of server will only run on a single\nthread serving requests one at a time).\n'
from ally.container.ioc import injected
from ally.design.processor.assembly import Assembly
from ally.design.processor.execution import Processing, Chain
from ally.http.spec.server import RequestHTTP, ResponseHTTP, RequestContentHTTP, ResponseContentHTTP, HTTP_GET, HTTP_POST, HTTP_PUT, HTTP_DELETE, HTTP_OPTIONS, HTTP
from ally.support.util_io import readGenerator, IInputStream
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl
import logging
log = logging.getLogger(__name__)

class RequestHandler(BaseHTTPRequestHandler):
    """
    The server class that handles the HTTP requests.
    """

    def __init__(self, request, address, server):
        """
        Create the request.
        
        @param request: socket
            The connection request socket.
        @param address: tuple(string, integer)
            The client address.
        @param server: BasicServer
            The server that created the request.
        """
        assert isinstance(address, tuple), 'Invalid address %s' % address
        assert isinstance(server, BasicServer), 'Invalid server %s' % server
        self.server_version = server.serverVersion
        super().__init__(request, address, server)

    def do_GET(self):
        self._process(HTTP_GET)

    def do_POST(self):
        self._process(HTTP_POST)

    def do_PUT(self):
        self._process(HTTP_PUT)

    def do_DELETE(self):
        self._process(HTTP_DELETE)

    def do_OPTIONS(self):
        self._process(HTTP_OPTIONS)

    def _process(self, method):
        assert isinstance(method, str), 'Invalid method %s' % method
        proc = self.server.processing
        assert isinstance(proc, Processing), 'Invalid processing %s' % proc
        request, requestCnt = proc.ctx.request(), proc.ctx.requestCnt()
        assert isinstance(request, RequestHTTP), 'Invalid request %s' % request
        assert isinstance(requestCnt, RequestContentHTTP), 'Invalid request content %s' % requestCnt
        if RequestHTTP.clientIP in request:
            request.clientIP = self.client_address[0]
        url = urlparse(self.path)
        request.scheme, request.method = HTTP, method.upper()
        request.headers = dict(self.headers)
        request.uri = url.path.lstrip('/')
        request.parameters = parse_qsl(url.query, True, False)
        requestCnt.source = self.rfile
        chain = Chain(proc)
        chain.process(**proc.fillIn(request=request, requestCnt=requestCnt, response=proc.ctx.response(), responseCnt=proc.ctx.responseCnt())).doAll()
        response, responseCnt = chain.arg.response, chain.arg.responseCnt
        assert isinstance(response, ResponseHTTP), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContentHTTP), 'Invalid response content %s' % responseCnt
        if ResponseHTTP.headers in response and response.headers is not None:
            for name, value in response.headers.items():
                self.send_header(name, value)

        assert isinstance(response.status, int), 'Invalid response status code %s' % response.status
        if ResponseHTTP.text in response and response.text:
            text = response.text
        else:
            if ResponseHTTP.code in response and response.code:
                text = response.code
            else:
                text = None
        self.send_response(response.status, text)
        self.end_headers()
        if ResponseContentHTTP.source in responseCnt and responseCnt.source is not None:
            if isinstance(responseCnt.source, IInputStream):
                source = readGenerator(responseCnt.source)
            else:
                source = responseCnt.source
            for bytes in source:
                self.wfile.write(bytes)

        return

    def log_message(self, format, *args):
        if not log.debug(format, *args):
            assert True


@injected
class BasicServer(HTTPServer):
    """
    The basic server.
    """
    serverVersion = str
    serverHost = str
    serverPort = int
    requestHandlerFactory = RequestHandler
    assembly = Assembly

    def __init__(self):
        """
        Construct the server.
        """
        assert isinstance(self.serverVersion, str), 'Invalid server version %s' % self.serverVersion
        assert isinstance(self.serverHost, str), 'Invalid server host %s' % self.serverHost
        assert isinstance(self.serverPort, int), 'Invalid server port %s' % self.serverPort
        assert callable(self.requestHandlerFactory), 'Invalid request handler factory %s' % self.requestHandlerFactory
        assert isinstance(self.assembly, Assembly), 'Invalid assembly %s' % self.assembly
        super().__init__((self.serverHost, self.serverPort), self.requestHandlerFactory)
        self.processing = self.assembly.create(request=RequestHTTP, requestCnt=RequestContentHTTP, response=ResponseHTTP, responseCnt=ResponseContentHTTP)


def run(server):
    """
    Run the basic server.
    
    @param server: BasicServer
        The server to run.
    """
    assert isinstance(server, BasicServer), 'Invalid server %s' % server
    try:
        log.info('=' * 50 + ' Started HTTP server...')
        server.serve_forever()
    except KeyboardInterrupt:
        log.info('=' * 50 + ' ^C received, shutting down server')
        server.server_close()
    except:
        log.exception('=' * 50 + ' The server has stooped')
        try:
            server.server_close()
        except:
            pass