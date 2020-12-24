# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/humberto/src/kytos/kytos-asyncio/kytos/core/tcp_server.py
# Compiled at: 2018-10-15 14:14:43
# Size of source mod 2**32: 6561 bytes
"""Basic TCP Server that will listen to port 6633."""
import logging
from socket import error as SocketError
from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn
from threading import current_thread
from kytos.core.connection import Connection, ConnectionState
from kytos.core.events import KytosEvent
__all__ = ('KytosServer', 'KytosRequestHandler')
LOG = logging.getLogger(__name__)

class KytosServer(ThreadingMixIn, TCPServer):
    __doc__ = 'Abstraction of a TCPServer to listen to packages from the network.\n\n    The KytosServer will listen on the specified port\n    for any new TCP request from the network and then instantiate the\n    specified RequestHandler to handle the new request.\n    It creates a new thread for each Handler.\n    '
    allow_reuse_address = True
    main_threads = {}

    def __init__(self, server_address, RequestHandlerClass, controller, protocol_name):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=False)
        self.controller = controller
        self.protocol_name = protocol_name

    def serve_forever(self, poll_interval=0.5):
        """Handle requests until an explicit shutdown() is called."""
        try:
            self.server_bind()
            self.server_activate()
            LOG.info('Kytos listening at %s:%s', self.server_address[0], self.server_address[1])
            super().serve_forever(poll_interval)
        except Exception:
            LOG.error('Failed to start Kytos TCP Server.')
            self.server_close()
            raise


class KytosRequestHandler(BaseRequestHandler):
    __doc__ = 'The socket/request handler class for our controller.\n\n    It is instantiated once per connection between each switch and the\n    controller.\n    The setup method will dispatch a KytosEvent (``kytos/core.connection.new``)\n    on the controller that will be processed by a Core App.\n    The finish method will close the connection and dispatch a KytosEvent\n    (``kytos/core.connection.closed``) on the controller.\n    '
    known_ports = {6633:'openflow', 
     6653:'openflow'}

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.connection = None

    def setup(self):
        """Create a new controller connection.

        This method builds a new controller Connection and places a
        ``kytos/core.connection.new`` KytosEvent in the app buffer.
        """
        self.addr = self.client_address[0]
        self.port = self.client_address[1]
        LOG.info('New connection from %s:%s', self.addr, self.port)
        self.connection = Connection(self.addr, self.port, self.request)
        server_port = self.server.server_address[1]
        if self.server.protocol_name:
            self.known_ports[server_port] = self.server.protocol_name
        elif server_port in self.known_ports:
            protocol_name = self.known_ports[server_port]
        else:
            protocol_name = f"{server_port:04d}"
        self.connection.protocol.name = protocol_name
        self.request.settimeout(70)
        self.exception = None
        event_name = f"kytos/core.{self.connection.protocol.name}.connection.new"
        event = KytosEvent(name=event_name, content={'source': self.connection})
        self.server.controller.buffers.app.put(event)

    def handle(self):
        """Handle each request and place its data in the raw event buffer.

        This method loops reading the binary data from the connection socket
        and placing a ``kytos/core.messages.new`` KytosEvent in the raw event
        buffer.
        """
        curr_thread = current_thread()
        max_size = 65536
        while True:
            try:
                new_data = self.request.recv(max_size)
            except (SocketError, OSError, InterruptedError, ConnectionResetError) as exception:
                try:
                    self.exception = exception
                    LOG.debug('Socket handler exception while reading: %s', exception)
                    break
                finally:
                    exception = None
                    del exception

            if new_data == b'':
                self.exception = 'Request closed by client.'
                break
            if not self.connection.is_alive():
                continue
            LOG.debug('New data from %s:%s at thread %s', self.addr, self.port, curr_thread.name)
            content = {'source':self.connection, 
             'new_data':new_data}
            event_name = f"kytos/core.{self.connection.protocol.name}.raw.in"
            event = KytosEvent(name=event_name, content=content)
            self.server.controller.buffers.raw.put(event)

    def finish(self):
        """Run when the client connection is finished.

        This method closes the connection socket and generates a
        ``kytos/core.connection.lost`` KytosEvent in the App buffer.
        """
        LOG.info('Connection lost with Client %s:%s. Reason: %s', self.addr, self.port, self.exception)
        self.connection.state = ConnectionState.FINISHED
        self.connection.close()
        content = {'source': self.connection}
        if self.exception:
            content['exception'] = self.exception
        event_name = f"kytos/core.{self.connection.protocol.name}.connection.lost"
        event = KytosEvent(name=event_name, content=content)
        self.server.controller.buffers.app.put(event)