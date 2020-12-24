# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kyoukai/backends/httptools_.py
# Compiled at: 2018-02-07 20:02:45
# Size of source mod 2**32: 17025 bytes
"""
A high-performance HTTP/1.1 backend for the Kyoukai webserver using `httptools 
<https://github.com/MagicStack/httptools>`_.
"""
import asyncio, base64, gzip, logging, traceback, warnings, zlib
from io import BytesIO
import httptools
from asphalt.core import Context
from werkzeug.exceptions import MethodNotAllowed, BadRequest, InternalServerError
from werkzeug.wrappers import Response
from kyoukai.backends.http2 import H2KyoukaiProtocol
from kyoukai.wsgi import to_wsgi_environment, get_formatted_response
CRITICAL_ERROR_TEXT = 'HTTP/1.0 500 INTERNAL SERVER ERROR\nServer: Kyoukai\nX-Powered-By: Kyoukai\nX-HTTP-Backend: httptools\nContent-Type: text/html; charset=utf-8\nContent-Length: 310\n\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>Critical Server Error</title>\n<h1>Critical Server Error</h1>\n<p>An unrecoverable error has occurred within Kyoukai.\nIf you are the developer, please report this at <a href="https://github.com/SunDwarf/Kyoukai">the \nKyoukai issue tracker.</a>\n'.replace('\n', '\r\n')
HTTP_SWITCHING_PROTOCOLS = 'HTTP/1.1 101 SWITCHING PROTOCOLS\nConnection: Upgrade\nUpgrade: h2c\nServer: Kyoukai\nX-Powered-By: Kyoukai\nX-HTTP-Backend: httptools\nContent-Length: 0\n\n'.replace('\n', '\r\n')
HTTP_TOO_BIG = 'HTTP/1.1 413 PAYLOAD TOO LARGE\nServer: Kyoukai\nX-Powered-By: Kyoukai\nX-HTTP-Backend: httptools\nContent-Length: 0\n\n'.replace('\n', '\r\n')
HTTP_INVALID_COMPRESSION = 'HTTP/1.1 400 BAD REQUEST\nServer: Kyoukai\nX-Powered-By: Kyoukai\nX-HTTP-Backend: httptools\nContent-Length: 25\n\nInvalid compressed data\n'.replace('\n', '\r\n')
PROTOCOL_CLASS = 'KyoukaiProtocol'

class KyoukaiProtocol(asyncio.Protocol):
    __doc__ = '\n    The base protocol for Kyoukai using httptools for a HTTP/1.0 or HTTP/1.1 interface.\n    '
    MAX_BODY_SIZE = 12582912

    def __init__(self, component, parent_context: Context, server_ip: str, server_port: int):
        """
        :param component: The :class:`kyoukai.asphalt.KyoukaiComponent` associated with this request.
        :param parent_context: The parent context for this request.
            A new HTTPRequestContext will be derived from this.
        """
        self.component = component
        self.app = component.app
        self.parent_context = parent_context
        self.server_ip = server_ip
        self.server_port = server_port
        self.transport = None
        self.lock = asyncio.Lock()
        self.parser = httptools.HttpRequestParser(self)
        self.waiter = None
        self.ip, self.client_port = (None, None)
        self.headers = []
        self.body = BytesIO()
        self.full_url = ''
        self.loop = self.app.loop
        self.logger = logging.getLogger('Kyoukai.HTTP11')

    def replace(self, other: type, *args, **kwargs) -> type:
        """
        Replaces our type with the other.
        """
        component = self.component
        app = component.app
        self.__class__ = other
        (other.__init__)(self, component, app, *args, **kwargs)
        return self

    def on_message_begin(self):
        """
        Called when a message begins.
        """
        self.body = BytesIO()
        self.headers = []
        self.full_url = ''

    def on_header(self, name: bytes, value: bytes):
        """
        Called when a header has been received.

        :param name: The name of the header.
        :param value: The value of the header.
        """
        self.headers.append((name.decode(), value.decode()))

    def on_headers_complete(self):
        """
        Called when the headers have been completely sent.
        """
        pass

    def on_body(self, body: bytes):
        """
        Called when part of the body has been received.

        :param body: The body text.
        """
        self.body.write(body)
        if self.body.tell() >= self.MAX_BODY_SIZE:
            self.write(HTTP_TOO_BIG)
            self.close()

    def on_url(self, url: bytes):
        """
        Called when a URL is received from the client.
        """
        self.full_url = url.decode('utf-8')

    def on_message_complete(self):
        """
        Called when a message is complete.
        This creates the worker task which will begin processing the request.
        """
        task = self.loop.create_task(self._wait_wrapper())
        self.waiter = task

    def connection_made(self, transport: asyncio.WriteTransport):
        """
        Called when a connection is made via asyncio.

        :param transport: The transport this is using.
        """
        try:
            self.ip, self.client_port = transport.get_extra_info('peername')
            self.logger.debug('Connection received from {}:{}'.format(self.ip, self.client_port))
        except ValueError:
            warnings.warn('getpeername() returned None, cannot provide transport information.')
            self.ip, self.client_port = (None, None)

        self.transport = transport
        ssl_sock = self.transport.get_extra_info('ssl_object')
        if ssl_sock is not None:
            negotiated_protocol = ssl_sock.selected_alpn_protocol()
            if negotiated_protocol is None:
                negotiated_protocol = ssl_sock.selected_npn_protocol()
            if negotiated_protocol == 'h2':
                transport = self.transport
                new_self = self.replace(H2KyoukaiProtocol)
                type(new_self).connection_made(new_self, transport)
                return
        self.component.connection_made.dispatch(protocol=self)

    def connection_lost(self, exc):
        self.logger.debug('Connection lost from {}:{}'.format(self.ip, self.client_port))
        self.component.connection_lost.dispatch(protocol=self)

    def data_received(self, data: bytes):
        """
        Called when data is received into the connection.
        """
        try:
            self.parser.feed_data(data)
        except httptools.HttpParserInvalidMethodError as e:
            self.handle_parser_exception(e)
        except httptools.HttpParserError as e:
            traceback.print_exc()
            self.handle_parser_exception(e)
        except httptools.HttpParserUpgrade as e:
            for name, header in self.headers:
                if name.lower() == 'upgrade':
                    upgrade = header
                    break
            else:
                self.handle_parser_exception(e)
                return

            if upgrade.lower() == 'h2c':
                for name, header in self.headers:
                    if name.lower() == 'http2-settings':
                        http2_settings = header
                        break
                else:
                    self.handle_parser_exception(e)
                    return

                self.logger.info('Upgrading HTTP/1.1 to HTTP/2 connection.')
                decoded = base64.urlsafe_b64decode(http2_settings)
                self.write(HTTP_SWITCHING_PROTOCOLS)
                transport = self.transport
                new_self = self.replace(H2KyoukaiProtocol)
                new_self.conn.initiate_upgrade_connection(decoded)
                type(new_self).connection_made(new_self, transport)
                return
            if upgrade.lower() == 'websocket':
                self.handle_parser_exception(e)
                return
            self.handle_parser_exception(e)
            return

    def handle_parser_exception(self, exc: Exception):
        """
        Handles an exception when parsing.

        This will not call into the app (hence why it is a normal function, and not a coroutine).
        It will also close the connection when it's done.

        :param exc: The exception to handle.
        """
        if isinstance(exc, httptools.HttpParserInvalidMethodError):
            r = MethodNotAllowed()
        else:
            if isinstance(exc, httptools.HttpParserError):
                r = BadRequest()
            else:
                if isinstance(exc, httptools.HttpParserUpgrade):
                    r = BadRequest(description='Invalid upgrade header.')
                else:
                    r = InternalServerError()
        new_environ = to_wsgi_environment(headers=(self.headers), method='', path='/', http_version='1.0',
          body=None)
        new_environ['SERVER_NAME'] = self.component.get_server_name()
        new_environ['SERVER_PORT'] = str(self.server_port)
        new_environ['REMOTE_ADDR'] = self.ip
        self.raw_write(get_formatted_response(r, new_environ))
        self.parser = httptools.HttpRequestParser(self)
        self.close()

    async def _wait_wrapper(self):
        try:
            try:
                if hasattr(self, '_wait'):
                    await self._wait()
                else:
                    return
            except:
                self.logger.critical("Error in Kyoukai's HTTP handling!", exc_info=True)
                self._raw_write(CRITICAL_ERROR_TEXT.encode())
                self.close()

        finally:
            if hasattr(self, 'waiter'):
                self.waiter.cancel()
                self.waiter = None
                self.parser = httptools.HttpRequestParser(self)

    async def _wait(self):
        """
        The main core of the protocol.

        This constructs a new Werkzeug request from the headers.
        """
        told = self.body.tell()
        if told:
            self.logger.debug('Read {} bytes of body data from the connection'.format(told))
            self.body.seek(0)
            body = self.body
        else:
            body = None
        version = self.parser.get_http_version()
        method = self.parser.get_method().decode()
        for header, value in self.headers:
            if header == 'Content-Encoding' and body is not None:
                if value == 'identity':
                    pass
                else:
                    if value == 'gzip':
                        self.logger.debug('Decoding body data as gzip.')
                        try:
                            decompressed_data = gzip.decompress(body.read())
                        except zlib.error:
                            self.write(HTTP_INVALID_COMPRESSION)
                            self.close()
                            return

                        body = BytesIO(decompressed_data)
                    else:
                        if value == 'deflate':
                            z = zlib.decompressobj(6, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
                            try:
                                decompressed_data = z.decompress(body.read())
                            except zlib.error:
                                self.write(HTTP_INVALID_COMPRESSION)
                                self.close()
                                return

                            body = BytesIO(decompressed_data)
                        else:
                            self.logger.error('Unknown Content-Encoding sent by client: {}'.format(value))

        new_environ = to_wsgi_environment(headers=(self.headers), method=method, path=(self.full_url), http_version=version,
          body=body)
        new_environ['kyoukai.protocol'] = self
        new_environ['SERVER_NAME'] = self.component.get_server_name()
        new_environ['SERVER_PORT'] = str(self.server_port)
        new_environ['REMOTE_ADDR'] = self.ip
        new_environ['REMOTE_PORT'] = self.client_port
        new_r = self.app.request_class(new_environ, False)
        async with self.lock:
            try:
                try:
                    result = await self.app.process_request(new_r, self.parent_context)
                except Exception:
                    self.logger.exception('Error in Kyoukai request handling!')
                    self._raw_write(CRITICAL_ERROR_TEXT.encode('utf-8'))
                    return
                else:
                    self.write_response(result, new_environ)
            finally:
                if not self.parser.should_keep_alive():
                    self.close()
                self.parser = httptools.HttpRequestParser(self)

    def close(self):
        return self.transport.close()

    def write_response(self, response: Response, fake_environ: dict):
        """
        Writes a Werkzeug response to the transport.
        """
        return self.raw_write(get_formatted_response(response, fake_environ))

    def write(self, data: str):
        """
        Writes data to the socket.
        """
        d = data.encode()
        return self.raw_write(d)

    def raw_write(self, data: bytes):
        """
        Writes data to the transport.
        """
        return self._raw_write(data)

    def _raw_write(self, data: bytes):
        """
        Does a raw write to the underlying transport, if we can.

        :param data: The data to write.
        """
        try:
            self.transport.write(data)
        except OSError:
            return