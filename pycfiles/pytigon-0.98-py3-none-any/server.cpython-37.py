# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/websockets/websockets/server.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 38186 bytes
"""
:mod:`websockets.server` defines the WebSocket server APIs.

"""
import asyncio, collections.abc, email.utils, functools, http, logging, socket, sys, warnings
from types import TracebackType
from typing import Any, Awaitable, Callable, Generator, List, Optional, Sequence, Set, Tuple, Type, Union, cast
from .exceptions import AbortHandshake, InvalidHandshake, InvalidHeader, InvalidMessage, InvalidOrigin, InvalidUpgrade, NegotiationError
from extensions.base import Extension, ServerExtensionFactory
from extensions.permessage_deflate import ServerPerMessageDeflateFactory
from .handshake import build_response, check_request
from .headers import build_extension, parse_extension, parse_subprotocol
from .http import USER_AGENT, Headers, HeadersLike, MultipleValuesError, read_request
from .protocol import WebSocketCommonProtocol
from .typing import ExtensionHeader, Origin, Subprotocol
__all__ = [
 'serve', 'unix_serve', 'WebSocketServerProtocol', 'WebSocketServer']
logger = logging.getLogger(__name__)
HeadersLikeOrCallable = Union[(HeadersLike, Callable[([str, Headers], HeadersLike)])]
HTTPResponse = Tuple[(http.HTTPStatus, HeadersLike, bytes)]

class WebSocketServerProtocol(WebSocketCommonProtocol):
    __doc__ = "\n    :class:`~asyncio.Protocol` subclass implementing a WebSocket server.\n\n    This class inherits most of its methods from\n    :class:`~websockets.protocol.WebSocketCommonProtocol`.\n\n    For the sake of simplicity, it doesn't rely on a full HTTP implementation.\n    Its support for HTTP responses is very limited.\n\n    "
    is_client = False
    side = 'server'

    def __init__(self, ws_handler, ws_server, *, origins=None, extensions=None, subprotocols=None, extra_headers=None, process_request=None, select_subprotocol=None, **kwargs):
        if origins is not None:
            if '' in origins:
                warnings.warn("use None instead of '' in origins", DeprecationWarning)
                origins = [None if origin == '' else origin for origin in origins]
        self.ws_handler = ws_handler
        self.ws_server = ws_server
        self.origins = origins
        self.available_extensions = extensions
        self.available_subprotocols = subprotocols
        self.extra_headers = extra_headers
        self._process_request = process_request
        self._select_subprotocol = select_subprotocol
        (super().__init__)(**kwargs)

    def connection_made(self, transport):
        """
        Register connection and initialize a task to handle it.

        """
        super().connection_made(transport)
        self.ws_server.register(self)
        self.handler_task = self.loop.create_task(self.handler())

    async def handler(self) -> None:
        """
        Handle the lifecycle of a WebSocket connection.

        Since this method doesn't have a caller able to handle exceptions, it
        attemps to log relevant ones and guarantees that the TCP connection is
        closed before exiting.

        """
        try:
            try:
                try:
                    path = await self.handshake(origins=(self.origins),
                      available_extensions=(self.available_extensions),
                      available_subprotocols=(self.available_subprotocols),
                      extra_headers=(self.extra_headers))
                except ConnectionError:
                    logger.debug('Connection error in opening handshake', exc_info=True)
                    raise
                except Exception as exc:
                    try:
                        if isinstance(exc, AbortHandshake):
                            status, headers, body = exc.status, exc.headers, exc.body
                        else:
                            if isinstance(exc, InvalidOrigin):
                                logger.debug('Invalid origin', exc_info=True)
                                status, headers, body = http.HTTPStatus.FORBIDDEN, Headers(), f"Failed to open a WebSocket connection: {exc}.\n".encode()
                            else:
                                if isinstance(exc, InvalidUpgrade):
                                    logger.debug('Invalid upgrade', exc_info=True)
                                    status, headers, body = http.HTTPStatus.UPGRADE_REQUIRED, Headers([('Upgrade', 'websocket')]), f"Failed to open a WebSocket connection: {exc}.\n\nYou cannot access a WebSocket server directly with a browser. You need a WebSocket client.\n".encode()
                                else:
                                    if isinstance(exc, InvalidHandshake):
                                        logger.debug('Invalid handshake', exc_info=True)
                                        status, headers, body = http.HTTPStatus.BAD_REQUEST, Headers(), f"Failed to open a WebSocket connection: {exc}.\n".encode()
                                    else:
                                        logger.warning('Error in opening handshake', exc_info=True)
                                        status, headers, body = http.HTTPStatus.INTERNAL_SERVER_ERROR, Headers(), b'Failed to open a WebSocket connection.\nSee server log for more information.\n'
                        headers.setdefault('Date', email.utils.formatdate(usegmt=True))
                        headers.setdefault('Server', USER_AGENT)
                        headers.setdefault('Content-Length', str(len(body)))
                        headers.setdefault('Content-Type', 'text/plain')
                        headers.setdefault('Connection', 'close')
                        self.write_http_response(status, headers, body)
                        self.fail_connection()
                        await self.wait_closed()
                        return
                    finally:
                        exc = None
                        del exc

                try:
                    await self.ws_handler(self, path)
                except Exception:
                    logger.error('Error in connection handler', exc_info=True)
                    if not self.closed:
                        self.fail_connection(1011)
                    raise

                try:
                    await self.close()
                except ConnectionError:
                    logger.debug('Connection error in closing handshake', exc_info=True)
                    raise
                except Exception:
                    logger.warning('Error in closing handshake', exc_info=True)
                    raise

            except Exception:
                try:
                    self.transport.close()
                except Exception:
                    pass

        finally:
            self.ws_server.unregister(self)

    async def read_http_request(self) -> Tuple[(str, Headers)]:
        """
        Read request line and headers from the HTTP request.

        If the request contains a body, it may be read from ``self.reader``
        after this coroutine returns.

        :raises ~websockets.exceptions.InvalidMessage: if the HTTP message is
            malformed or isn't an HTTP/1.1 GET request

        """
        try:
            path, headers = await read_request(self.reader)
        except Exception as exc:
            try:
                raise InvalidMessage('did not receive a valid HTTP request') from exc
            finally:
                exc = None
                del exc

        logger.debug('%s < GET %s HTTP/1.1', self.side, path)
        logger.debug('%s < %r', self.side, headers)
        self.path = path
        self.request_headers = headers
        return (
         path, headers)

    def write_http_response(self, status: http.HTTPStatus, headers: Headers, body: Optional[bytes]=None) -> None:
        """
        Write status line and headers to the HTTP response.

        This coroutine is also able to write a response body.

        """
        self.response_headers = headers
        logger.debug('%s > HTTP/1.1 %d %s', self.side, status.value, status.phrase)
        logger.debug('%s > %r', self.side, headers)
        response = f"HTTP/1.1 {status.value} {status.phrase}\r\n"
        response += str(headers)
        self.transport.write(response.encode())
        if body is not None:
            logger.debug('%s > body (%d bytes)', self.side, len(body))
            self.transport.write(body)

    async def process_request(self, path: str, request_headers: Headers) -> Optional[HTTPResponse]:
        """
        Intercept the HTTP request and return an HTTP response if appropriate.

        If ``process_request`` returns ``None``, the WebSocket handshake
        continues. If it returns 3-uple containing a status code, response
        headers and a response body, that HTTP response is sent and the
        connection is closed. In that case:

        * The HTTP status must be a :class:`~http.HTTPStatus`.
        * HTTP headers must be a :class:`~websockets.http.Headers` instance, a
          :class:`~collections.abc.Mapping`, or an iterable of ``(name,
          value)`` pairs.
        * The HTTP response body must be :class:`bytes`. It may be empty.

        This coroutine may be overridden in a :class:`WebSocketServerProtocol`
        subclass, for example:

        * to return a HTTP 200 OK response on a given path; then a load
          balancer can use this path for a health check;
        * to authenticate the request and return a HTTP 401 Unauthorized or a
          HTTP 403 Forbidden when authentication fails.

        Instead of subclassing, it is possible to override this method by
        passing a ``process_request`` argument to the :func:`serve` function
        or the :class:`WebSocketServerProtocol` constructor. This is
        equivalent, except ``process_request`` won't have access to the
        protocol instance, so it can't store information for later use.

        ``process_request`` is expected to complete quickly. If it may run for
        a long time, then it should await :meth:`wait_closed` and exit if
        :meth:`wait_closed` completes, or else it could prevent the server
        from shutting down.

        :param path: request path, including optional query string
        :param request_headers: request headers

        """
        if self._process_request is not None:
            response = self._process_request(path, request_headers)
            if isinstance(response, Awaitable):
                return await response
            warnings.warn('declare process_request as a coroutine', DeprecationWarning)
            return response

    @staticmethod
    def process_origin(headers: Headers, origins: Optional[Sequence[Optional[Origin]]]=None) -> Optional[Origin]:
        """
        Handle the Origin HTTP request header.

        :param headers: request headers
        :param origins: optional list of acceptable origins
        :raises ~websockets.exceptions.InvalidOrigin: if the origin isn't
            acceptable

        """
        try:
            origin = cast(Origin, headers.get('Origin'))
        except MultipleValuesError:
            raise InvalidHeader('Origin', 'more than one Origin header found')

        if origins is not None:
            if origin not in origins:
                raise InvalidOrigin(origin)
        return origin

    @staticmethod
    def process_extensions(headers: Headers, available_extensions: Optional[Sequence[ServerExtensionFactory]]) -> Tuple[(Optional[str], List[Extension])]:
        """
        Handle the Sec-WebSocket-Extensions HTTP request header.

        Accept or reject each extension proposed in the client request.
        Negotiate parameters for accepted extensions.

        Return the Sec-WebSocket-Extensions HTTP response header and the list
        of accepted extensions.

        :rfc:`6455` leaves the rules up to the specification of each
        :extension.

        To provide this level of flexibility, for each extension proposed by
        the client, we check for a match with each extension available in the
        server configuration. If no match is found, the extension is ignored.

        If several variants of the same extension are proposed by the client,
        it may be accepted severel times, which won't make sense in general.
        Extensions must implement their own requirements. For this purpose,
        the list of previously accepted extensions is provided.

        This process doesn't allow the server to reorder extensions. It can
        only select a subset of the extensions proposed by the client.

        Other requirements, for example related to mandatory extensions or the
        order of extensions, may be implemented by overriding this method.

        :param headers: request headers
        :param extensions: optional list of supported extensions
        :raises ~websockets.exceptions.InvalidHandshake: to abort the
            handshake with an HTTP 400 error code

        """
        response_header_value = None
        extension_headers = []
        accepted_extensions = []
        header_values = headers.get_all('Sec-WebSocket-Extensions')
        if header_values:
            if available_extensions:
                parsed_header_values = sum([parse_extension(header_value) for header_value in header_values], [])
                for name, request_params in parsed_header_values:
                    for ext_factory in available_extensions:
                        if ext_factory.name != name:
                            continue
                        try:
                            response_params, extension = ext_factory.process_request_params(request_params, accepted_extensions)
                        except NegotiationError:
                            continue

                        extension_headers.append((name, response_params))
                        accepted_extensions.append(extension)
                        break

        if extension_headers:
            response_header_value = build_extension(extension_headers)
        return (response_header_value, accepted_extensions)

    def process_subprotocol(self, headers: Headers, available_subprotocols: Optional[Sequence[Subprotocol]]) -> Optional[Subprotocol]:
        """
        Handle the Sec-WebSocket-Protocol HTTP request header.

        Return Sec-WebSocket-Protocol HTTP response header, which is the same
        as the selected subprotocol.

        :param headers: request headers
        :param available_subprotocols: optional list of supported subprotocols
        :raises ~websockets.exceptions.InvalidHandshake: to abort the
            handshake with an HTTP 400 error code

        """
        subprotocol = None
        header_values = headers.get_all('Sec-WebSocket-Protocol')
        if header_values:
            if available_subprotocols:
                parsed_header_values = sum([parse_subprotocol(header_value) for header_value in header_values], [])
                subprotocol = self.select_subprotocol(parsed_header_values, available_subprotocols)
        return subprotocol

    def select_subprotocol(self, client_subprotocols: Sequence[Subprotocol], server_subprotocols: Sequence[Subprotocol]) -> Optional[Subprotocol]:
        """
        Pick a subprotocol among those offered by the client.

        If several subprotocols are supported by the client and the server,
        the default implementation selects the preferred subprotocols by
        giving equal value to the priorities of the client and the server.

        If no subprotocol is supported by the client and the server, it
        proceeds without a subprotocol.

        This is unlikely to be the most useful implementation in practice, as
        many servers providing a subprotocol will require that the client uses
        that subprotocol. Such rules can be implemented in a subclass.

        Instead of subclassing, it is possible to override this method by
        passing a ``select_subprotocol`` argument to the :func:`serve`
        function or the :class:`WebSocketServerProtocol` constructor

        :param client_subprotocols: list of subprotocols offered by the client
        :param server_subprotocols: list of subprotocols available on the server

        """
        if self._select_subprotocol is not None:
            return self._select_subprotocol(client_subprotocols, server_subprotocols)
        else:
            subprotocols = set(client_subprotocols) & set(server_subprotocols)
            return subprotocols or None
        priority = lambda p: client_subprotocols.index(p) + server_subprotocols.index(p)
        return sorted(subprotocols, key=priority)[0]

    async def handshake(self, origins: Optional[Sequence[Optional[Origin]]]=None, available_extensions: Optional[Sequence[ServerExtensionFactory]]=None, available_subprotocols: Optional[Sequence[Subprotocol]]=None, extra_headers: Optional[HeadersLikeOrCallable]=None) -> str:
        """
        Perform the server side of the opening handshake.

        Return the path of the URI of the request.

        :param origins: list of acceptable values of the Origin HTTP header;
            include ``None`` if the lack of an origin is acceptable
        :param available_extensions: list of supported extensions in the order
            in which they should be used
        :param available_subprotocols: list of supported subprotocols in order
            of decreasing preference
        :param extra_headers: sets additional HTTP response headers when the
            handshake succeeds; it can be a :class:`~websockets.http.Headers`
            instance, a :class:`~collections.abc.Mapping`, an iterable of
            ``(name, value)`` pairs, or a callable taking the request path and
            headers in arguments and returning one of the above.
        :raises ~websockets.exceptions.InvalidHandshake: if the handshake
            fails

        """
        path, request_headers = await self.read_http_request()
        early_response_awaitable = self.process_request(path, request_headers)
        if isinstance(early_response_awaitable, Awaitable):
            early_response = await early_response_awaitable
        else:
            warnings.warn('declare process_request as a coroutine', DeprecationWarning)
            early_response = early_response_awaitable
        if not self.ws_server.is_serving():
            early_response = (http.HTTPStatus.SERVICE_UNAVAILABLE, [],
             b'Server is shutting down.\n')
        if early_response is not None:
            raise AbortHandshake(*early_response)
        key = check_request(request_headers)
        self.origin = self.process_origin(request_headers, origins)
        extensions_header, self.extensions = self.process_extensions(request_headers, available_extensions)
        protocol_header = self.subprotocol = self.process_subprotocol(request_headers, available_subprotocols)
        response_headers = Headers()
        build_response(response_headers, key)
        if extensions_header is not None:
            response_headers['Sec-WebSocket-Extensions'] = extensions_header
        if protocol_header is not None:
            response_headers['Sec-WebSocket-Protocol'] = protocol_header
        if callable(extra_headers):
            extra_headers = extra_headers(path, self.request_headers)
        if extra_headers is not None:
            if isinstance(extra_headers, Headers):
                extra_headers = extra_headers.raw_items()
            else:
                if isinstance(extra_headers, collections.abc.Mapping):
                    extra_headers = extra_headers.items()
                for name, value in extra_headers:
                    response_headers[name] = value

        response_headers.setdefault('Date', email.utils.formatdate(usegmt=True))
        response_headers.setdefault('Server', USER_AGENT)
        self.write_http_response(http.HTTPStatus.SWITCHING_PROTOCOLS, response_headers)
        self.connection_open()
        return path


class WebSocketServer:
    __doc__ = "\n    WebSocket server returned by :func:`~websockets.server.serve`.\n\n    This class provides the same interface as\n    :class:`~asyncio.AbstractServer`, namely the\n    :meth:`~asyncio.AbstractServer.close` and\n    :meth:`~asyncio.AbstractServer.wait_closed` methods.\n\n    It keeps track of WebSocket connections in order to close them properly\n    when shutting down.\n\n    Instances of this class store a reference to the :class:`~asyncio.Server`\n    object returned by :meth:`~asyncio.loop.create_server` rather than inherit\n    from :class:`~asyncio.Server` in part because\n    :meth:`~asyncio.loop.create_server` doesn't support passing a custom\n    :class:`~asyncio.Server` class.\n\n    "

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.websockets = set()
        self.close_task = None
        self.closed_waiter = loop.create_future()

    def wrap(self, server: asyncio.AbstractServer) -> None:
        """
        Attach to a given :class:`~asyncio.Server`.

        Since :meth:`~asyncio.loop.create_server` doesn't support injecting a
        custom ``Server`` class, the easiest solution that doesn't rely on
        private :mod:`asyncio` APIs is to:

        - instantiate a :class:`WebSocketServer`
        - give the protocol factory a reference to that instance
        - call :meth:`~asyncio.loop.create_server` with the factory
        - attach the resulting :class:`~asyncio.Server` with this method

        """
        self.server = server

    def register(self, protocol: WebSocketServerProtocol) -> None:
        """
        Register a connection with this server.

        """
        self.websockets.add(protocol)

    def unregister(self, protocol: WebSocketServerProtocol) -> None:
        """
        Unregister a connection with this server.

        """
        self.websockets.remove(protocol)

    def is_serving(self) -> bool:
        """
        Tell whether the server is accepting new connections or shutting down.

        """
        try:
            return self.server.is_serving()
        except AttributeError:
            return self.server.sockets is not None

    def close(self) -> None:
        """
        Close the server.

        This method:

        * closes the underlying :class:`~asyncio.Server`;
        * rejects new WebSocket connections with an HTTP 503 (service
          unavailable) error; this happens when the server accepted the TCP
          connection but didn't complete the WebSocket opening handshake prior
          to closing;
        * closes open WebSocket connections with close code 1001 (going away).

        :meth:`close` is idempotent.

        """
        if self.close_task is None:
            self.close_task = self.loop.create_task(self._close())

    async def _close(self) -> None:
        """
        Implementation of :meth:`close`.

        This calls :meth:`~asyncio.Server.close` on the underlying
        :class:`~asyncio.Server` object to stop accepting new connections and
        then closes open connections with close code 1001.

        """
        self.server.close()
        await self.server.wait_closed()
        await asyncio.sleep(0,
          loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
        if self.websockets:
            await asyncio.wait([websocket.close(1001) for websocket in self.websockets],
              loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
        if self.websockets:
            await asyncio.wait([websocket.handler_task for websocket in self.websockets],
              loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
        self.closed_waiter.set_result(None)

    async def wait_closed(self) -> None:
        """
        Wait until the server is closed.

        When :meth:`wait_closed` returns, all TCP connections are closed and
        all connection handlers have returned.

        """
        await asyncio.shield(self.closed_waiter)

    @property
    def sockets(self) -> Optional[List[socket.socket]]:
        """
        List of :class:`~socket.socket` objects the server is listening to.

        ``None`` if the server is closed.

        """
        return self.server.sockets


class Serve:
    __doc__ = '\n\n    Create, start, and return a WebSocket server on ``host`` and ``port``.\n\n    Whenever a client connects, the server accepts the connection, creates a\n    :class:`WebSocketServerProtocol`, performs the opening handshake, and\n    delegates to the connection handler defined by ``ws_handler``. Once the\n    handler completes, either normally or with an exception, the server\n    performs the closing handshake and closes the connection.\n\n    Awaiting :func:`serve` yields a :class:`WebSocketServer`. This instance\n    provides :meth:`~websockets.server.WebSocketServer.close` and\n    :meth:`~websockets.server.WebSocketServer.wait_closed` methods for\n    terminating the server and cleaning up its resources.\n\n    When a server is closed with :meth:`~WebSocketServer.close`, it closes all\n    connections with close code 1001 (going away). Connections handlers, which\n    are running the ``ws_handler`` coroutine, will receive a\n    :exc:`~websockets.exceptions.ConnectionClosedOK` exception on their\n    current or next interaction with the WebSocket connection.\n\n    :func:`serve` can also be used as an asynchronous context manager. In\n    this case, the server is shut down when exiting the context.\n\n    :func:`serve` is a wrapper around the event loop\'s\n    :meth:`~asyncio.loop.create_server` method. It creates and starts a\n    :class:`~asyncio.Server` with :meth:`~asyncio.loop.create_server`. Then it\n    wraps the :class:`~asyncio.Server` in a :class:`WebSocketServer`  and\n    returns the :class:`WebSocketServer`.\n\n    The ``ws_handler`` argument is the WebSocket handler. It must be a\n    coroutine accepting two arguments: a :class:`WebSocketServerProtocol` and\n    the request URI.\n\n    The ``host`` and ``port`` arguments, as well as unrecognized keyword\n    arguments, are passed along to :meth:`~asyncio.loop.create_server`.\n\n    For example, you can set the ``ssl`` keyword argument to a\n    :class:`~ssl.SSLContext` to enable TLS.\n\n    The ``create_protocol`` parameter allows customizing the\n    :class:`~asyncio.Protocol` that manages the connection. It should be a\n    callable or class accepting the same arguments as\n    :class:`WebSocketServerProtocol` and returning an instance of\n    :class:`WebSocketServerProtocol` or a subclass. It defaults to\n    :class:`WebSocketServerProtocol`.\n\n    The behavior of ``ping_interval``, ``ping_timeout``, ``close_timeout``,\n    ``max_size``, ``max_queue``, ``read_limit``, and ``write_limit`` is\n    described in :class:`~websockets.protocol.WebSocketCommonProtocol`.\n\n    :func:`serve` also accepts the following optional arguments:\n\n    * ``compression`` is a shortcut to configure compression extensions;\n      by default it enables the "permessage-deflate" extension; set it to\n      ``None`` to disable compression\n    * ``origins`` defines acceptable Origin HTTP headers; include ``None`` if\n      the lack of an origin is acceptable\n    * ``extensions`` is a list of supported extensions in order of\n      decreasing preference\n    * ``subprotocols`` is a list of supported subprotocols in order of\n      decreasing preference\n    * ``extra_headers`` sets additional HTTP response headers  when the\n      handshake succeeds; it can be a :class:`~websockets.http.Headers`\n      instance, a :class:`~collections.abc.Mapping`, an iterable of ``(name,\n      value)`` pairs, or a callable taking the request path and headers in\n      arguments and returning one of the above\n    * ``process_request`` allows intercepting the HTTP request; it must be a\n      coroutine taking the request path and headers in argument; see\n      :meth:`~WebSocketServerProtocol.process_request` for details\n    * ``select_subprotocol`` allows customizing the logic for selecting a\n      subprotocol; it must be a callable taking the subprotocols offered by\n      the client and available on the server in argument; see\n      :meth:`~WebSocketServerProtocol.select_subprotocol` for details\n\n    Since there\'s no useful way to propagate exceptions triggered in handlers,\n    they\'re sent to the ``\'websockets.server\'`` logger instead. Debugging is\n    much easier if you configure logging to print them::\n\n        import logging\n        logger = logging.getLogger(\'websockets.server\')\n        logger.setLevel(logging.ERROR)\n        logger.addHandler(logging.StreamHandler())\n\n    '

    def __init__(self, ws_handler: Callable[([WebSocketServerProtocol, str], Awaitable[Any])], host: Optional[Union[(str, Sequence[str])]]=None, port: Optional[int]=None, *, path: Optional[str]=None, create_protocol: Optional[Type[WebSocketServerProtocol]]=None, ping_interval: float=20, ping_timeout: float=20, close_timeout: Optional[float]=None, max_size: int=1048576, max_queue: int=32, read_limit: int=65536, write_limit: int=65536, loop: Optional[asyncio.AbstractEventLoop]=None, legacy_recv: bool=False, klass: Optional[Type[WebSocketServerProtocol]]=None, timeout: Optional[float]=None, compression: Optional[str]='deflate', origins: Optional[Sequence[Optional[Origin]]]=None, extensions: Optional[Sequence[ServerExtensionFactory]]=None, subprotocols: Optional[Sequence[Subprotocol]]=None, extra_headers: Optional[HeadersLikeOrCallable]=None, process_request: Optional[Callable[([str, Headers], Awaitable[Optional[HTTPResponse]])]]=None, select_subprotocol: Optional[Callable[([Sequence[Subprotocol], Sequence[Subprotocol]], Subprotocol)]]=None, **kwargs: Any) -> None:
        if timeout is None:
            timeout = 10
        else:
            warnings.warn('rename timeout to close_timeout', DeprecationWarning)
        if close_timeout is None:
            close_timeout = timeout
        elif klass is None:
            klass = WebSocketServerProtocol
        else:
            warnings.warn('rename klass to create_protocol', DeprecationWarning)
        if create_protocol is None:
            create_protocol = klass
        if loop is None:
            loop = asyncio.get_event_loop()
        ws_server = WebSocketServer(loop)
        secure = kwargs.get('ssl') is not None
        if compression == 'deflate':
            if extensions is None:
                extensions = []
            extensions = any((ext_factory.name == ServerPerMessageDeflateFactory.name for ext_factory in extensions)) or list(extensions) + [ServerPerMessageDeflateFactory()]
        else:
            if compression is not None:
                raise ValueError(f"unsupported compression: {compression}")
            else:
                factory = functools.partial(create_protocol,
                  ws_handler,
                  ws_server,
                  host=host,
                  port=port,
                  secure=secure,
                  ping_interval=ping_interval,
                  ping_timeout=ping_timeout,
                  close_timeout=close_timeout,
                  max_size=max_size,
                  max_queue=max_queue,
                  read_limit=read_limit,
                  write_limit=write_limit,
                  loop=loop,
                  legacy_recv=legacy_recv,
                  origins=origins,
                  extensions=extensions,
                  subprotocols=subprotocols,
                  extra_headers=extra_headers,
                  process_request=process_request,
                  select_subprotocol=select_subprotocol)
                if path is None:
                    create_server = (functools.partial)(
                     (loop.create_server), factory, host, port, **kwargs)
                else:
                    if not (host is None and port is None):
                        raise AssertionError
                create_server = (functools.partial)(
                 (loop.create_unix_server), factory, path, **kwargs)
            self._create_server = create_server
            self.ws_server = ws_server

    async def __aenter__(self) -> WebSocketServer:
        return await self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        self.ws_server.close()
        await self.ws_server.wait_closed()

    def __await__(self) -> Generator[(Any, None, WebSocketServer)]:
        return self.__await_impl__().__await__()

    async def __await_impl__(self) -> WebSocketServer:
        server = await self._create_server()
        self.ws_server.wrap(server)
        return self.ws_server

    __iter__ = __await__


serve = Serve

def unix_serve(ws_handler: Callable[([WebSocketServerProtocol, str], Awaitable[Any])], path: str, **kwargs: Any) -> Serve:
    """
    Similar to :func:`serve`, but for listening on Unix sockets.

    This function calls the event loop's
    :meth:`~asyncio.loop.create_unix_server` method.

    It is only available on Unix.

    It's useful for deploying a server behind a reverse proxy such as nginx.

    :param path: file system path to the Unix socket

    """
    return serve(ws_handler, path=path, **kwargs)