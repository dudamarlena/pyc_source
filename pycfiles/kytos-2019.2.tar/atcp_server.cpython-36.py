# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/humberto/src/kytos/kytos-asyncio/kytos/core/atcp_server.py
# Compiled at: 2019-10-18 15:36:22
# Size of source mod 2**32: 7116 bytes
"""AsyncIO TCP Server for Kytos."""
import asyncio, errno, logging
from kytos.core.connection import Connection
from kytos.core.events import KytosEvent
LOG = logging.getLogger(__name__)

def exception_handler(loop, context):
    """Exception handler to avoid tracebacks because of network timeouts."""
    exc = context.get('exception')
    transport = context.get('transport')
    if isinstance(exc, TimeoutError):
        LOG.info('Socket timeout: %r', transport)
    elif isinstance(exc, OSError):
        if exc.errno == errno.EBADF:
            LOG.info('Socket closed: %r', transport)
    else:
        loop.default_exception_handler(context)


class KytosServer:
    __doc__ = 'Abstraction of a TCP Server to listen to packages from the network.\n\n    The KytosServer will listen on the specified port\n    for any new TCP request from the network and then instantiate the\n    specified RequestHandler to handle the new request.\n    It creates a new thread for each Handler.\n    '

    def __init__(self, server_address, server_protocol, controller, protocol_name, loop=None):
        """Create the object without starting the server.

        Args:
            server_address (tuple): Address where the server is listening.
                example: ('127.0.0.1', 80)
            server_protocol (asyncio.Protocol):
                Class that will be instantiated to handle each request.
            controller (:class:`~kytos.core.controller.Controller`):
                An instance of Kytos Controller class.
            protocol_name (str): Southbound protocol name that will be used
        """
        self.server_address = server_address
        self.server_protocol = server_protocol
        self.controller = controller
        self.protocol_name = protocol_name
        self._server = None
        self.server_protocol.server = self
        self.loop = loop or asyncio.get_event_loop()
        self.loop.set_exception_handler(exception_handler)

    def serve_forever(self):
        """Handle requests until an explicit shutdown() is called."""
        addr, port = self.server_address[0], self.server_address[1]
        self._server = self.loop.create_server(self.server_protocol, addr, port)
        try:
            task = self.loop.create_task(self._server)
            LOG.info('Kytos listening at %s:%s', addr, port)
        except Exception:
            LOG.error('Failed to start Kytos TCP Server at %s:%s', addr, port)
            task.close()
            raise

    def shutdown(self):
        """Call .close() on underlying TCP server, closing client sockets."""
        self._server.close()


class KytosServerProtocol(asyncio.Protocol):
    __doc__ = "Kytos' main request handler.\n\n    It is instantiated once per connection between each switch and the\n    controller.\n    The setup method will dispatch a KytosEvent (``kytos/core.connection.new``)\n    on the controller, that will be processed by a Core App.\n    The finish method will close the connection and dispatch a KytosEvent\n    (``kytos/core.connection.closed``) on the controller.\n    "
    known_ports = {6633:'openflow', 
     6653:'openflow'}

    def __init__(self):
        """Initialize protocol and check if server attribute was set."""
        self._loop = asyncio.get_event_loop()
        self.connection = None
        self.transport = None
        self._rest = b''
        if not getattr(self, 'server'):
            self.server = None
        if not self.server:
            raise ValueError('server instance must be assigned before init')

    def connection_made(self, transport):
        """Handle new client connection, passing it to the controller.

        Build a new Kytos `Connection` and send a ``kytos/core.connection.new``
        KytosEvent through the app buffer.
        """
        self.transport = transport
        addr, port = transport.get_extra_info('peername')
        _, server_port = transport.get_extra_info('sockname')
        socket = transport.get_extra_info('socket')
        LOG.info('New connection from %s:%s', addr, port)
        self.connection = Connection(addr, port, socket)
        if self.server.protocol_name:
            self.known_ports[server_port] = self.server.protocol_name
        else:
            if server_port in self.known_ports:
                protocol_name = self.known_ports[server_port]
            else:
                protocol_name = f"{server_port:04d}"
        self.connection.protocol.name = protocol_name
        event_name = f"kytos/core.{protocol_name}.connection.new"
        event = KytosEvent(name=event_name, content={'source': self.connection})
        self._loop.create_task(self.server.controller.buffers.raw.aput(event))

    def data_received(self, data):
        """Handle each request and place its data in the raw event buffer.

        Sends the received binary data in a ``kytos/core.{protocol}.raw.in``
        event on the raw buffer.
        """
        data = self._rest + data
        LOG.debug('New data from %s:%s (%s bytes)', self.connection.address, self.connection.port, len(data))
        content = {'source':self.connection, 
         'new_data':data}
        event_name = f"kytos/core.{self.connection.protocol.name}.raw.in"
        event = KytosEvent(name=event_name, content=content)
        self._loop.create_task(self.server.controller.buffers.raw.aput(event))

    def connection_lost(self, exc):
        """Close the connection socket and generate connection lost event.

        Emits a ``kytos/core.{protocol}.connection.lost`` event through the
        App buffer.
        """
        reason = exc or 'Request closed by client'
        LOG.info('Connection lost with client %s:%s. Reason: %s', self.connection.address, self.connection.port, reason)
        self.connection.close()
        content = {'source': self.connection}
        if exc:
            content['exception'] = exc
        event_name = f"kytos/core.{self.connection.protocol.name}.connection.lost"
        event = KytosEvent(name=event_name, content=content)
        self._loop.create_task(self.server.controller.buffers.app.aput(event))