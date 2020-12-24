# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/engineio/asyncio_server.py
# Compiled at: 2019-08-30 19:22:57
# Size of source mod 2**32: 18704 bytes
import asyncio, six
from six.moves import urllib
from . import exceptions
from . import packet
from . import server
from . import asyncio_socket

class AsyncServer(server.Server):
    __doc__ = 'An Engine.IO server for asyncio.\n\n    This class implements a fully compliant Engine.IO web server with support\n    for websocket and long-polling transports, compatible with the asyncio\n    framework on Python 3.5 or newer.\n\n    :param async_mode: The asynchronous model to use. See the Deployment\n                       section in the documentation for a description of the\n                       available options. Valid async modes are "aiohttp",\n                       "sanic", "tornado" and "asgi". If this argument is not\n                       given, an async mode is chosen based on the installed\n                       packages.\n    :param ping_timeout: The time in seconds that the client waits for the\n                         server to respond before disconnecting.\n    :param ping_interval: The interval in seconds at which the client pings\n                          the server.\n    :param max_http_buffer_size: The maximum size of a message when using the\n                                 polling transport.\n    :param allow_upgrades: Whether to allow transport upgrades or not.\n    :param http_compression: Whether to compress packages when using the\n                             polling transport.\n    :param compression_threshold: Only compress messages when their byte size\n                                  is greater than this value.\n    :param cookie: Name of the HTTP cookie that contains the client session\n                   id. If set to ``None``, a cookie is not sent to the client.\n    :param cors_allowed_origins: List of origins that are allowed to connect\n                                 to this server. All origins are allowed by\n                                 default.\n    :param cors_credentials: Whether credentials (cookies, authentication) are\n                             allowed in requests to this server.\n    :param logger: To enable logging set to ``True`` or pass a logger object to\n                   use. To disable logging set to ``False``.\n    :param json: An alternative json module to use for encoding and decoding\n                 packets. Custom json modules must have ``dumps`` and ``loads``\n                 functions that are compatible with the standard library\n                 versions.\n    :param async_handlers: If set to ``True``, run message event handlers in\n                           non-blocking threads. To run handlers synchronously,\n                           set to ``False``. The default is ``True``.\n    :param kwargs: Reserved for future extensions, any additional parameters\n                   given as keyword arguments will be silently ignored.\n    '

    def is_asyncio_based(self):
        return True

    def async_modes(self):
        return [
         'aiohttp', 'sanic', 'tornado', 'asgi']

    def attach(self, app, engineio_path='engine.io'):
        """Attach the Engine.IO server to an application."""
        engineio_path = engineio_path.strip('/')
        self._async['create_route'](app, self, '/{}/'.format(engineio_path))

    async def send(self, sid, data, binary=None):
        """Send a message to a client.

        :param sid: The session id of the recipient client.
        :param data: The data to send to the client. Data can be of type
                     ``str``, ``bytes``, ``list`` or ``dict``. If a ``list``
                     or ``dict``, the data will be serialized as JSON.
        :param binary: ``True`` to send packet as binary, ``False`` to send
                       as text. If not given, unicode (Python 2) and str
                       (Python 3) are sent as text, and str (Python 2) and
                       bytes (Python 3) are sent as binary.

        Note: this method is a coroutine.
        """
        try:
            socket = self._get_socket(sid)
        except KeyError:
            self.logger.warning('Cannot send to sid %s', sid)
            return
        else:
            await socket.send(packet.Packet((packet.MESSAGE), data=data, binary=binary))

    async def get_session(self, sid):
        """Return the user session for a client.

        :param sid: The session id of the client.

        The return value is a dictionary. Modifications made to this
        dictionary are not guaranteed to be preserved. If you want to modify
        the user session, use the ``session`` context manager instead.
        """
        socket = self._get_socket(sid)
        return socket.session

    async def save_session(self, sid, session):
        """Store the user session for a client.

        :param sid: The session id of the client.
        :param session: The session dictionary.
        """
        socket = self._get_socket(sid)
        socket.session = session

    def session(self, sid):
        """Return the user session for a client with context manager syntax.

        :param sid: The session id of the client.

        This is a context manager that returns the user session dictionary for
        the client. Any changes that are made to this dictionary inside the
        context manager block are saved back to the session. Example usage::

            @eio.on('connect')
            def on_connect(sid, environ):
                username = authenticate_user(environ)
                if not username:
                    return False
                with eio.session(sid) as session:
                    session['username'] = username

            @eio.on('message')
            def on_message(sid, msg):
                async with eio.session(sid) as session:
                    print('received message from ', session['username'])
        """

        class _session_context_manager(object):

            def __init__(self, server, sid):
                self.server = server
                self.sid = sid
                self.session = None

            async def __aenter__(self):
                self.session = await self.server.get_session(sid)
                return self.session

            async def __aexit__(self, *args):
                await self.server.save_session(sid, self.session)

        return _session_context_manager(self, sid)

    async def disconnect(self, sid=None):
        """Disconnect a client.

        :param sid: The session id of the client to close. If this parameter
                    is not given, then all clients are closed.

        Note: this method is a coroutine.
        """
        if sid is not None:
            try:
                socket = self._get_socket(sid)
            except KeyError:
                pass
            else:
                await socket.close()
                del self.sockets[sid]
        else:
            await asyncio.wait([client.close() for client in six.itervalues(self.sockets)])
            self.sockets = {}

    async def handle_request(self, *args, **kwargs):
        """Handle an HTTP request from the client.

        This is the entry point of the Engine.IO application. This function
        returns the HTTP response to deliver to the client.

        Note: this method is a coroutine.
        """
        translate_request = self._async['translate_request']
        if asyncio.iscoroutinefunction(translate_request):
            environ = await translate_request(*args, **kwargs)
        else:
            environ = translate_request(*args, **kwargs)
        method = environ['REQUEST_METHOD']
        query = urllib.parse.parse_qs(environ.get('QUERY_STRING', ''))
        if 'j' in query:
            self.logger.warning('JSONP requests are not supported')
            r = self._bad_request()
        else:
            sid = query['sid'][0] if 'sid' in query else None
            b64 = False
            if 'b64' in query:
                if query['b64'][0] == '1' or query['b64'][0].lower() == 'true':
                    b64 = True
            if method == 'GET':
                if sid is None:
                    transport = query.get('transport', ['polling'])[0]
                    if transport != 'polling' and transport != 'websocket':
                        self.logger.warning('Invalid transport %s', transport)
                        r = self._bad_request()
                    else:
                        r = await self._handle_connect(environ, transport, b64)
                else:
                    if sid not in self.sockets:
                        self.logger.warning('Invalid session %s', sid)
                        r = self._bad_request()
                    else:
                        socket = self._get_socket(sid)
                        try:
                            packets = await socket.handle_get_request(environ)
                            if isinstance(packets, list):
                                r = self._ok(packets, b64=b64)
                            else:
                                r = packets
                        except exceptions.EngineIOError:
                            if sid in self.sockets:
                                await self.disconnect(sid)
                            r = self._bad_request()

                        if sid in self.sockets and self.sockets[sid].closed:
                            del self.sockets[sid]
            else:
                if method == 'POST':
                    if sid is None or sid not in self.sockets:
                        self.logger.warning('Invalid session %s', sid)
                        r = self._bad_request()
                    else:
                        socket = self._get_socket(sid)
                        try:
                            await socket.handle_post_request(environ)
                            r = self._ok()
                        except exceptions.EngineIOError:
                            if sid in self.sockets:
                                await self.disconnect(sid)
                            r = self._bad_request()
                        except:
                            self.logger.exception('post request handler error')
                            r = self._ok()

                else:
                    if method == 'OPTIONS':
                        r = self._ok()
                    else:
                        self.logger.warning('Method %s not supported', method)
                        r = self._method_not_found()
        if not isinstance(r, dict):
            if r is not None:
                return r
            return []
        else:
            if self.http_compression:
                if len(r['response']) >= self.compression_threshold:
                    encodings = [e.split(';')[0].strip() for e in environ.get('HTTP_ACCEPT_ENCODING', '').split(',')]
                    for encoding in encodings:
                        if encoding in self.compression_methods:
                            r['response'] = getattr(self, '_' + encoding)(r['response'])
                            r['headers'] += [('Content-Encoding', encoding)]
                            break

            else:
                cors_headers = self._cors_headers(environ)
                make_response = self._async['make_response']
                if asyncio.iscoroutinefunction(make_response):
                    response = await make_response(r['status'], r['headers'] + cors_headers, r['response'], environ)
                else:
                    response = make_response(r['status'], r['headers'] + cors_headers, r['response'], environ)
            return response

    def start_background_task(self, target, *args, **kwargs):
        """Start a background task using the appropriate async model.

        This is a utility function that applications can use to start a
        background task using the method that is compatible with the
        selected async mode.

        :param target: the target function to execute.
        :param args: arguments to pass to the function.
        :param kwargs: keyword arguments to pass to the function.

        The return value is a ``asyncio.Task`` object.
        """
        return asyncio.ensure_future(target(*args, **kwargs))

    async def sleep(self, seconds=0):
        """Sleep for the requested amount of time using the appropriate async
        model.

        This is a utility function that applications can use to put a task to
        sleep without having to worry about using the correct call for the
        selected async mode.

        Note: this method is a coroutine.
        """
        return await asyncio.sleep(seconds)

    def create_queue(self, *args, **kwargs):
        """Create a queue object using the appropriate async model.

        This is a utility function that applications can use to create a queue
        without having to worry about using the correct call for the selected
        async mode. For asyncio based async modes, this returns an instance of
        ``asyncio.Queue``.
        """
        return (asyncio.Queue)(*args, **kwargs)

    def get_queue_empty_exception(self):
        """Return the queue empty exception for the appropriate async model.

        This is a utility function that applications can use to work with a
        queue without having to worry about using the correct call for the
        selected async mode. For asyncio based async modes, this returns an
        instance of ``asyncio.QueueEmpty``.
        """
        return asyncio.QueueEmpty

    def create_event(self, *args, **kwargs):
        """Create an event object using the appropriate async model.

        This is a utility function that applications can use to create an
        event without having to worry about using the correct call for the
        selected async mode. For asyncio based async modes, this returns
        an instance of ``asyncio.Event``.
        """
        return (asyncio.Event)(*args, **kwargs)

    async def _handle_connect(self, environ, transport, b64=False):
        """Handle a client connection request."""
        if self.start_service_task:
            self.start_service_task = False
            self.start_background_task(self._service_task)
        else:
            sid = self._generate_id()
            s = asyncio_socket.AsyncSocket(self, sid)
            self.sockets[sid] = s
            pkt = packet.Packet(packet.OPEN, {'sid':sid,  'upgrades':self._upgrades(sid, transport), 
             'pingTimeout':int(self.ping_timeout * 1000), 
             'pingInterval':int(self.ping_interval * 1000)})
            await s.send(pkt)
            ret = await self._trigger_event('connect', sid, environ, run_async=False)
            if ret is False:
                del self.sockets[sid]
                self.logger.warning('Application rejected connection')
                return self._unauthorized()
            if transport == 'websocket':
                ret = await s.handle_get_request(environ)
                if s.closed:
                    del self.sockets[sid]
                return ret
            s.connected = True
            headers = None
            if self.cookie:
                headers = [
                 (
                  'Set-Cookie', self.cookie + '=' + sid)]
        try:
            return self._ok((await s.poll()), headers=headers, b64=b64)
        except exceptions.QueueEmpty:
            return self._bad_request()

    async def _trigger_event(self, event, *args, **kwargs):
        """Invoke an event handler."""
        run_async = kwargs.pop('run_async', False)
        ret = None
        if event in self.handlers:
            if asyncio.iscoroutinefunction(self.handlers[event]) is True:
                if run_async:
                    return (self.start_background_task)(self.handlers[event], *args)
                try:
                    ret = await (self.handlers[event])(*args)
                except asyncio.CancelledError:
                    pass
                except:
                    self.logger.exception(event + ' async handler error')
                    if event == 'connect':
                        return False

            else:
                if run_async:

                    async def async_handler():
                        return (self.handlers[event])(*args)

                    return self.start_background_task(async_handler)
                try:
                    ret = (self.handlers[event])(*args)
                except:
                    self.logger.exception(event + ' handler error')
                    if event == 'connect':
                        return False

        return ret

    async def _service_task(self):
        """Monitor connected clients and clean up those that time out."""
        while len(self.sockets) == 0:
            await self.sleep(self.ping_timeout)
            continue
            sleep_interval = self.ping_timeout / len(self.sockets)
            try:
                for socket in self.sockets.copy().values():
                    if not socket.closing:
                        if not socket.closed:
                            await socket.check_ping_timeout()
                    await self.sleep(sleep_interval)

            except (SystemExit, KeyboardInterrupt, asyncio.CancelledError):
                self.logger.info('service task canceled')
                break
            except:
                if asyncio.get_event_loop().is_closed():
                    self.logger.info('event loop is closed, exiting service task')
                    break
                self.logger.exception('service task exception')