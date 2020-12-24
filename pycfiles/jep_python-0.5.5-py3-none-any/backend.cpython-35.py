# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\jep_py\backend.py
# Compiled at: 2016-01-04 11:02:19
# Size of source mod 2**32: 10585 bytes
"""Framework independent PEP backend implementation."""
import datetime, enum, logging, socket, select
from jep_py.config import TIMEOUT_SELECT_SEC, BUFFER_LENGTH, TIMEOUT_LAST_MESSAGE
from jep_py.content import ContentMonitor, SynchronizationResult
from jep_py.protocol import MessageSerializer
from jep_py.schema import Shutdown, BackendAlive, ContentSync, OutOfSync, StaticSyntaxList, StaticSyntax
from jep_py.syntax import SyntaxFileSet, SyntaxFile
_logger = logging.getLogger(__name__)
PORT_RANGE = (9001, 9100)
LISTEN_QUEUE_LENGTH = 3
TIMEOUT_BACKEND_ALIVE = datetime.timedelta(minutes=1)

class NoPortFoundError(Exception):
    pass


@enum.unique
class State(enum.Enum):
    Stopped = 1
    Running = 2
    ShutdownPending = 3


class FrontendListener:
    __doc__ = 'API to listen to messages from frontend, communicated via backend.'

    def on_shutdown(self, context):
        return NotImplemented

    def on_content_sync(self, content_sync, context):
        return NotImplemented

    def on_completion_request(self, completion_request, context):
        return NotImplemented

    def on_completion_invocation(self, completion_invocation, context):
        return NotImplemented

    def on_static_syntax_request(self, format, fileExtensions, context):
        return NotImplemented


class Backend(FrontendListener):
    __doc__ = 'Synchronous JEP backend service.'

    def __init__(self, listeners=None, *, syntax_fileset=None):
        self.listeners = listeners or []
        self.syntax_fileset = syntax_fileset or SyntaxFileSet()
        self.sockets = []
        self.state = State.Stopped
        self.ts_alive_sent = None
        self.BACKEND_ALIVE_DATA = MessageSerializer().serialize(BackendAlive())
        self.connection = dict()

    @property
    def serversocket(self):
        if self.sockets:
            return self.sockets[0]

    def start(self):
        """Starts listening for front-ends to connect."""
        assert self.state is State.Stopped
        _logger.info('Starting backend.')
        self._listen()
        self._run()
        _logger.info('Backend stopped.')
        assert self.state is State.Stopped
        assert not self.sockets, 'Unexpected active sockets after shutdown.'
        assert not self.connection, 'Unexpected frontend connectors after shutdown.'

    def stop(self):
        _logger.debug('Received request to shut down.')
        self.state = State.ShutdownPending

    def register_static_syntax(self, name, path, fileformat, *extensions):
        """Adds a new static syntax file to the backend's registry for pickup by the frontend.

        Should usually be called before the backend is started and connections are made.
        """
        self.syntax_fileset.add_syntax_file(name, path, fileformat, extensions)

    def _listen(self):
        """Set up server socket to listen for incoming connections."""
        self.sockets = [
         socket.socket()]
        port = PORT_RANGE[0]
        while self.state is not State.Running and port < PORT_RANGE[1]:
            try:
                self.serversocket.bind(('localhost', port))
                self.serversocket.listen(LISTEN_QUEUE_LENGTH)
                self.state = State.Running
            except OSError:
                _logger.debug('Port %d not available.' % port)
                port += 1

        if self.state is not State.Running:
            _logger.error('Could not bind to any available port in range [%d,%d]. Startup failed.' % PORT_RANGE)
            raise NoPortFoundError()
        print('JEP service, listening on port %d' % port, flush=True)

    def _run(self):
        """Process connections and messages. This is the main loop of the server."""
        while self.state is State.Running:
            readable, *_ = select.select(self.sockets, [], [], TIMEOUT_SELECT_SEC)
            for sock in readable:
                if sock is self.serversocket:
                    self._accept()
                else:
                    self._receive(sock)

            self._cyclic()

        if self.state == State.ShutdownPending:
            for sock in self.sockets.copy():
                self._close(sock)

            self.state = State.Stopped

    def _accept(self):
        """Blocking accept of incoming connection."""
        clientsocket, *_ = self.serversocket.accept()
        clientsocket.setblocking(0)
        self.sockets.append(clientsocket)
        self.connection[clientsocket] = FrontendConnection(self, clientsocket)
        _logger.info('Frontend %d connected.' % id(clientsocket))

    def _receive(self, clientsocket):
        """Read of client data on given socket."""
        frontend_connector = self.connection[clientsocket]
        cycles = 0
        try:
            while True:
                data = clientsocket.recv(BUFFER_LENGTH)
                cycles += 1
                if data:
                    _logger.debug('Received data: %s' % data)
                    frontend_connector.ts_last_data_received = datetime.datetime.now()
                    frontend_connector.serializer.enque_data(data)
                else:
                    _logger.debug('Socket closed by frontend.')
                    raise ConnectionAbortedError()

        except ConnectionAbortedError:
            _logger.debug('Closing connection to frontend due to closed socket.')
            self._close(clientsocket)
        except BlockingIOError as e:
            pass

        _logger.debug('Read data in %d cycles.' % cycles)
        for msg in frontend_connector.serializer:
            _logger.debug('Received message: %s' % msg)
            msg.invoke(self, frontend_connector)
            for listener in self.listeners:
                msg.invoke(listener, frontend_connector)

    def _close(self, sock):
        _logger.info('Socket %d disconnected.' % id(sock))
        sock.close()
        self.sockets.remove(sock)
        self.connection.pop(sock, None)

    def _cyclic(self):
        """Cyclic processing of service level tasks."""
        now = datetime.datetime.now()
        num_frontends = len(self.sockets) - 1
        if num_frontends > 0:
            if not self.ts_alive_sent or now - self.ts_alive_sent >= TIMEOUT_BACKEND_ALIVE:
                _logger.debug('Sending alive message to %d frontend(s).' % num_frontends)
                for sock in self.sockets[1:]:
                    self._send_data(sock, self.BACKEND_ALIVE_DATA)

                self.ts_alive_sent = now
            for sock in self.sockets[1:].copy():
                if now - self.connection[sock].ts_last_data_received >= TIMEOUT_LAST_MESSAGE:
                    _logger.debug('Disconnecting frontend after timeout.')
                    self._close(sock)

    def send_message(self, connection, msg):
        """Message used by MessageContext only to delegate send."""
        _logger.debug('Sending message: %s.' % msg)
        serialized = self.connection[connection.sock].serializer.serialize(msg)
        _logger.debug('Sending data: %s.' % serialized)
        self._send_data(connection.sock, serialized)

    @classmethod
    def _send_data(cls, sock, data):
        sock.send(data)

    def on_shutdown(self, context):
        self.stop()

    def on_content_sync(self, content_sync: ContentSync, context):
        """Keeps track of file content through data sent by frontend."""
        result = context.content_monitor.synchronize(content_sync.file, content_sync.data, content_sync.start, content_sync.end)
        if result == SynchronizationResult.OutOfSync:
            context.send_message(OutOfSync(content_sync.file))

    def on_static_syntax_request(self, format, fileExtensions, context):
        """Handle requests for static syntax definitions, expected to be in normalized form."""
        if fileExtensions:
            _logger.debug('Received syntax request in format {} for extensions {}.'.format(format, ', '.join(fileExtensions)))
        else:
            _logger.debug('Received syntax request in format {} for all available extensions.'.format(format))
        filtered = self.syntax_fileset.filtered(format, fileExtensions)
        if filtered:
            msg = StaticSyntaxList(format, [StaticSyntax(sf.name, sf.extensions, sf.definition) for sf in filtered])
            _logger.debug('Returning {} matching syntax definitions.'.format(len(msg.syntaxes)))
            context.send_message(msg)
        else:
            _logger.debug('Did not find any matching syntax definition.')


class FrontendConnection:
    __doc__ = 'Connection to frontend instance.'

    def __init__(self, service, sock, *, serializer=None, content_monitor=None):
        self.service = service
        self.sock = sock
        self.ts_last_data_received = datetime.datetime.now()
        self.serializer = serializer or MessageSerializer()
        self.content_monitor = content_monitor or ContentMonitor()

    def send_message(self, msg):
        self.service.send_message(self, msg)