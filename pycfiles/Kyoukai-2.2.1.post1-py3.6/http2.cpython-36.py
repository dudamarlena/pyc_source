# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kyoukai/backends/http2.py
# Compiled at: 2018-02-07 20:02:45
# Size of source mod 2**32: 19116 bytes
"""
A HTTP/2 interface to Kyoukai.

This uses https://python-hyper.org/projects/h2/en/stable/asyncio-example.html as a reference and a base. Massive thanks
to the authors of this page.

This server has some notable pitfalls:

    - It ignores any priority data that is sent by the client.
    - It is not paticularly fast (unbenchmarked, but it can be assumed to be slower than the httptools backend.)
    - It does not fully implement all events.

Additionally, this server is **untested** - it can and probably will fail horribly in production. Use with caution :)
"""
import asyncio, collections, logging, ssl, sys, warnings
from functools import partial
from urllib.parse import urlsplit
import typing
from asphalt.core import Context
from h2.config import H2Configuration
from h2.connection import H2Connection
from h2.errors import ErrorCodes
from h2.events import DataReceived, RequestReceived, WindowUpdated, StreamEnded
from h2.exceptions import ProtocolError
from werkzeug.datastructures import MultiDict
from werkzeug.wrappers import Request, Response
from kyoukai.asphalt import KyoukaiBaseComponent
REQUEST_FINISHED = object()

def get_header(headers: typing.List[typing.Tuple[(str, str)]], name: str) -> str:
    """
    Gets a header from the list of headers, or None if it doesn't exist.
    """
    for header, value in headers:
        if header == name:
            return value


def create_wsgi_environment(r: 'H2State') -> MultiDict:
    """
    Creates a new WSGI environment from the RequestData provided.
    """
    path = get_header(r.headers, ':path')
    sp_path = urlsplit(path)
    server_name = get_header(r.headers, ':authority')
    try:
        server_name, port = server_name.split(':', 1)
    except ValueError as e:
        port = '8443'

    method = get_header(r.headers, ':method')
    environ = MultiDict({'PATH_INFO':sp_path.path, 
     'QUERY_STRING':sp_path.query, 
     'SERVER_PROTOCOL':'HTTP/2', 
     'REQUEST_METHOD':method, 
     'wsgi.version':(1, 0), 
     'wsgi.errors':sys.stderr, 
     'wsgi.url_scheme':get_header(r.headers, ':scheme'), 
     'wsgi.input':r, 
     'wsgi.async':True, 
     'wsgi.multithread':True, 
     'wsgi.multiprocess':False, 
     'wsgi.run_once':False, 
     'SERVER_NAME':server_name, 
     'SERVER_PORT':port, 
     'REMOTE_ADDR':r._protocol.ip, 
     'REMOTE_PORT':r._protocol.client_port})
    for header, value in r.headers:
        if not header.startswith(':'):
            environ.add('HTTP_{}'.format(header.replace('-', '_').upper()), value)

    return environ


class H2State:
    __doc__ = '\n    A temporary class that is used to store request data for a HTTP/2 connection.\n\n    This is also passed to the Werkzeug request to emit data.\n    '

    def __init__(self, headers: list, stream_id, protocol: 'H2KyoukaiProtocol'):
        self.stream_id = stream_id
        self._protocol = protocol
        self.headers = headers
        self.body = asyncio.Queue()
        self._emit_headers = None
        self._emit_status = None

    def insert_data(self, data: bytes):
        """
        Writes data from the stream into the body.
        """
        self.body.put_nowait(data)

    async def read_async(self, to_end=True):
        """
        There's no good way to do this - WSGI isn't async, after all.

        However, you can use `read_async` on the Werkzeug request (which we subclass) to wait until the request has
        finished streaming.

        :param to_end: If ``to_end`` is specified, then read until the end of the request.
            Otherwise, it will read one data chunk.
        """
        data = b''
        if to_end:
            while True:
                d = await self.body.get()
                if d == REQUEST_FINISHED:
                    break
                data += d

        else:
            d = await self.body.get()
        if not d == REQUEST_FINISHED:
            data += d
        return data

    def read(self, size: int=-1) -> bytes:
        """
        Reads data from the request until it's all done.

        :param size: The maximum amount of data to receive.
        """
        curr_data = b''
        while size < 0 or len(curr_data) < size:
            try:
                curr_data += self.body.get_nowait()
            except asyncio.QueueEmpty:
                break

        d = curr_data[:size]
        if len(curr_data) != len(d):
            self.body._queue.appendleft(curr_data[size:])
        return d

    def get_chunk(self) -> bytes:
        """
        Gets a chunk of data from the queue.
        """
        try:
            d = self.body.get_nowait()
            if d == REQUEST_FINISHED:
                return b''
        except asyncio.QueueEmpty:
            return b''
        else:
            return d

    def start_response(self, status: str, headers: typing.List[typing.Tuple[(str, str)]], exc_info=None):
        """
        The ``start_response`` callable that is plugged into a Werkzeug response.
        """
        self._emit_status = status.split(' ')[0]
        self._emit_headers = headers
        return lambda data: None

    def get_response_headers(self):
        """
        Called by the protocol once the Response is writable to submit the request to the HTTP/2 state machine.
        """
        headers = [
         (
          ':status', self._emit_status)]
        headers.extend(self._emit_headers)
        return headers

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_chunk()


class H2KyoukaiComponent(KyoukaiBaseComponent):
    __doc__ = '\n    A component subclass that creates H2KyoukaiProtocol instances.\n    '

    def __init__(self, app, ssl_keyfile, ssl_certfile, *, ip='127.0.0.1', port=4444):
        """
        Creates a new HTTP/2 SSL-based context.

        This will use the HTTP/2 protocol, disabling HTTP/1.1 support for this port. It is possible
        to run two ervers side-by-side, one HTTP/2 and one HTTP/1.1, if you run them on
        different ports.
        """
        super().__init__(app, ip, port)
        self.ssl_keyfile = ssl_keyfile
        self.ssl_certfile = ssl_certfile
        self.cfg['ssl'] = True
        self.cfg['http2'] = True

    def get_protocol(self, ctx: Context, serv_info: tuple):
        return H2KyoukaiProtocol(self, ctx)

    async def start(self, ctx: Context):
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=(self.ssl_certfile), keyfile=(self.ssl_keyfile))
        ssl_context.set_alpn_protocols(['h2'])
        try:
            ssl_context.set_npn_protocols(['h2'])
        except NotImplementedError:
            pass

        protocol = partial(self.get_protocol, ctx, (self._server_name, self.port))
        self.app.finalize()
        self.server = await self.app.loop.create_server(protocol, (self.ip), (self.port), ssl=ssl_context)
        self.logger.info('Kyoukai H2 serving on {}:{}'.format(self.ip, self.port))


class H2KyoukaiProtocol(asyncio.Protocol):
    __doc__ = '\n    The base protocol for Kyoukai, using H2.\n    '

    def __init__(self, component, parent_context: Context):
        self.component = component
        self.parent_context = parent_context
        config = H2Configuration(client_side=False, header_encoding='utf-8')
        self.conn = H2Connection(config=config)
        self.transport = None
        self.streams = {}
        self.stream_data = collections.defaultdict(lambda *args: asyncio.Queue())
        self.logger = logging.getLogger('Kyoukai.HTTP2')
        self.ip, self.client_port = (None, None)
        self._locked = collections.defaultdict(lambda *args: asyncio.Event())
        self.stream_tasks = {}

    def raw_write(self, data: bytes):
        """
        Writes to the underlying transport.
        """
        try:
            return self.transport.write(data)
        except (OSError, ConnectionError):
            return

    def connection_lost(self, exc):
        self.logger.debug('Connection lost from {}:{}'.format(self.ip, self.client_port))

    def connection_made(self, transport: asyncio.WriteTransport):
        """
        Called when a connection is made.

        :param transport: The transport made by the connection.
        """
        self.transport = transport
        try:
            self.ip, self.client_port = self.transport.get_extra_info('peername')
            self.logger.debug('Connection received from {}:{}'.format(self.ip, self.client_port))
        except ValueError:
            warnings.warn('getpeername() returned None, cannot provide transport information.')
            self.ip, self.client_port = (None, None)

        ssl_sock = self.transport.get_extra_info('ssl_object')
        if ssl_sock is None:
            warnings.warn('HTTP/2 connection established over a non-TLS stream!')
        else:
            negotiated_protocol = ssl_sock.selected_alpn_protocol()
        if negotiated_protocol is None:
            negotiated_protocol = ssl_sock.selected_npn_protocol()
        if negotiated_protocol != 'h2':
            self.close(1)
            return
        self.logger.debug('Started the HTTP/2 connection.')
        self.conn.initiate_connection()
        self.raw_write(self.conn.data_to_send())

    def data_received(self, data: bytes):
        """
        Called when data is received from the underlying socket.
        """
        try:
            events = self.conn.receive_data(data)
        except ProtocolError:
            self.close(1)
            return
        else:
            self.transport.write(self.conn.data_to_send())
            for event in events:
                self.logger.debug('Received HTTP/2 event {.__class__.__name__}'.format(event))
                if isinstance(event, RequestReceived):
                    self.request_received(event)
                else:
                    if isinstance(event, DataReceived):
                        self.receive_data(event)
                    else:
                        if isinstance(event, StreamEnded):
                            self.stream_complete(event)
                        else:
                            if isinstance(event, WindowUpdated):
                                self.window_opened(event)

    def _processing_done(self, environ: dict, stream_id):
        """
        Callback for when processing is done on a request.
        """

        def _inner(fut):
            result = fut.result()
            state = self.streams[stream_id]
            it = result(environ, state.start_response)
            headers = state.get_response_headers()
            self.conn.send_headers(stream_id, headers, end_stream=False)
            for i in it:
                self.stream_data[stream_id].put_nowait(i)

            self.stream_data[stream_id].put_nowait(REQUEST_FINISHED)

        return _inner

    async def sending_loop(self, stream_id):
        """
        This loop continues sending data to the client as it comes off of the queue.
        """
        while 1:
            self._locked[stream_id].clear()
            data = await self.stream_data[stream_id].get()
            if data == REQUEST_FINISHED:
                self.conn.end_stream(stream_id)
                self.raw_write(self.conn.data_to_send())
                return
            window_size = self.conn.local_flow_control_window(stream_id)
            chunk_size = min(window_size, len(data))
            data_to_send = data[:chunk_size]
            data_to_buffer = data[chunk_size:]
            if data_to_send:
                max_size = self.conn.max_outbound_frame_size
                chunks = (data_to_send[x:x + max_size] for x in range(0, len(data_to_send), max_size))
                for chunk in chunks:
                    self.conn.send_data(stream_id, chunk)

                self.raw_write(self.conn.data_to_send())
            if data_to_buffer:
                self.stream_data[stream_id]._queue.appendleft(data)
                await self._locked[stream_id].wait()
                self._locked[stream_id].clear()
                continue

    def request_received(self, event: RequestReceived):
        """
        Called when a request has been received.
        """
        r = H2State(event.headers, event.stream_id, self)
        self.streams[event.stream_id] = r
        app = self.component.app
        env = create_wsgi_environment(r)
        request = app.request_class(environ=env)
        loop = app.loop
        t = loop.create_task(app.process_request(request, self.parent_context))
        self.stream_tasks[event.stream_id] = loop.create_task(self.sending_loop(event.stream_id))
        t.add_done_callback(self._processing_done(env, event.stream_id))

    def window_opened(self, event: WindowUpdated):
        """
        Called when a control flow window has opened again.
        """
        if event.stream_id:
            self._locked[event.stream_id].set()
        else:
            for ev in self._locked.keys():
                ev.set()

    def receive_data(self, event: DataReceived):
        """
        Called when a request has data that has been received.
        """
        try:
            req = self.streams[event.stream_id]
        except KeyError:
            self.conn.reset_stream(event.stream_id, ErrorCodes.PROTOCOL_ERROR)
        else:
            req.insert_data(event.data)

    def stream_complete(self, event: StreamEnded):
        """
        Called when a stream is complete.

        This will invoke Kyoukai, which will handle the request.
        """
        try:
            req = self.streams[event.stream_id]
        except KeyError:
            self.conn.reset_stream(event.stream_id, ErrorCodes.PROTOCOL_ERROR)
            return
        else:
            req.insert_data(REQUEST_FINISHED)

    def close(self, error_code: int=0):
        """
        Called to terminate the connection for some reason.

        This will close the underlying transport.
        """
        self.conn.close_connection(error_code)
        self.raw_write(self.conn.data_to_send())
        self.transport.close()