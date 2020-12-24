# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/service.py
# Compiled at: 2018-03-15 14:27:52
# Size of source mod 2**32: 14283 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from datetime import timedelta
from abc import abstractmethod, ABCMeta
from threading import Event
import queue
from zmq import Context as ZMQContext
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
from wasp_general.verify import verify_type, verify_subclass
from wasp_general.config import WConfig
from wasp_general.network.transport import WNetworkNativeTransportProto

class WIOLoopServiceHandler(metaclass=ABCMeta):
    __doc__ = ' Represent service (or service client) handler that works with tornado IOLoop and do the work.\n\n\tTODO: rename to bla-bla-bla-Proto\n\t'

    @abstractmethod
    @verify_type(io_loop=IOLoop)
    def setup_handler(self, io_loop):
        """ Set up this handler with the specified IOLoop

                :param io_loop: service (or service client) loop to use with
                :return: None
                """
        raise NotImplementedError('This method is abstract')

    def loop_stopped(self):
        """ Method is called when previously set up loop was stopped

                :return: None
                """
        pass


class WIOLoopService(metaclass=ABCMeta):
    __doc__ = ' Represent service (or service client) that works over tornado IOLoop\n\t'

    @verify_type(handler=WIOLoopServiceHandler, loop=(IOLoop, None), timeout=(int, None))
    def __init__(self, handler, loop=None, timeout=None):
        """ Create new service (or service client)

                :param handler: handler that do the work
                :param loop: loop to use (or None for internal one)
                :param timeout: timeout after which this loop will be stopped
                """
        self._WIOLoopService__loop = IOLoop() if loop is None else loop
        self._WIOLoopService__handler = handler
        self._WIOLoopService__timeout = timeout

    def loop(self):
        """ Return service loop object

                :return: IOLoop
                """
        return self._WIOLoopService__loop

    def handler(self):
        """ Return service handler

                :return: WIOLoopServiceHandler
                """
        return self._WIOLoopService__handler

    def timeout(self):
        """ Return service timeout. (None for endless loop)

                :return: int or None
                """
        return self._WIOLoopService__timeout

    def start(self):
        """ Set up handler and start loop

                :return: None
                """
        timeout = self.timeout()
        if timeout is not None and timeout > 0:
            self._WIOLoopService__loop.add_timeout(timedelta(0, timeout), self.stop)
        self.handler().setup_handler(self.loop())
        self.loop().start()
        self.handler().loop_stopped()

    def stop(self):
        """ Stop loop

                :return: None
                """
        self.loop().stop()


class WNativeSocketIOHandler(metaclass=ABCMeta):
    __doc__ = ' Handler prototype for loops that work with :class:`.WNetworkNativeTransportProto` transports. It is used by\n\t:class:`.WBasicNativeSocketHandler` handler and do all the work for this class.\n\t'

    @abstractmethod
    def handler_fn(self, fd, event):
        """ Process (handle) specified event

                :param fd: integer file descriptor or a file-like object with a fileno() method
                :param event: IOLoop event
                :return: None
                """
        raise NotImplementedError('This method is abstract')


class WBasicNativeSocketHandler(WIOLoopServiceHandler, metaclass=ABCMeta):
    __doc__ = ' Basic :class:`.WIOLoopServiceHandler` implementation. Since some :class:`.WNetworkNativeTransportProto`\n\tmethods are required :class:`.WConfig` object, then that kind of object is required for this class\n\tinstantiation\n\t'

    @verify_type(transport=WNetworkNativeTransportProto, config=WConfig, io_handler=WNativeSocketIOHandler)
    def __init__(self, transport, config, io_handler):
        """ Create new socket handler

                :param transport: transport to use
                :param config: configuration to be used with transport
                :param io_handler: handler that do the real work
                """
        WIOLoopServiceHandler.__init__(self)
        self._WBasicNativeSocketHandler__transport = transport
        self._WBasicNativeSocketHandler__config = config
        self._WBasicNativeSocketHandler__io_handler = io_handler

    def transport(self):
        """ Return currently used transport
                :return: WNetworkNativeTransportProto
                """
        return self._WBasicNativeSocketHandler__transport

    def config(self):
        """ Return handler configuration

                :return: WConfig
                """
        return self._WBasicNativeSocketHandler__config

    def io_handler(self):
        """ Return IO-handler

                :return: WNativeSocketIOHandler
                """
        return self._WBasicNativeSocketHandler__io_handler


class WNativeSocketDirectIOHandler(WNativeSocketIOHandler, metaclass=ABCMeta):
    __doc__ = ' This type of IO-handler has access to low-level socket object\n\t'

    def __init__(self):
        """ Create new IO-handler

                """
        WNativeSocketIOHandler.__init__(self)
        self._WNativeSocketDirectIOHandler__transport_socket = None

    def transport_socket(self, new_socket=None):
        """ Save and/or return currently used socket object

                :param new_socket: new socket to save
                :return: socket object (any type, None if socket wasn't set)
                """
        if new_socket is not None:
            self._WNativeSocketDirectIOHandler__transport_socket = new_socket
        return self._WNativeSocketDirectIOHandler__transport_socket


class WNativeSocketHandler(WBasicNativeSocketHandler):
    __doc__ = " Enhanced variant of :class:`.WBasicNativeSocketHandler` class. This class support 'server_mode' flag and\n\tis capable to set up the specified IO-handler with :class:`.WIOLoopService` service\n\t"

    @verify_type('paranoid', transport=WNetworkNativeTransportProto, config=WConfig)
    @verify_type('paranoid', io_handler=WNativeSocketIOHandler)
    @verify_type(server_mode=bool)
    def __init__(self, transport, config, io_handler, server_mode):
        """ Create new loop-handler

                :param transport: transport to use
                :param config: configuration to use (in the most cases it is used by transport object only)
                :param io_handler: io-handler to use
                :param server_mode: set 'server_mode' flag for correct transport configuration
                """
        WBasicNativeSocketHandler.__init__(self, transport, config, io_handler)
        self._WNativeSocketHandler__server_mode = server_mode

    def server_mode(self):
        """ Return current mode. True if this handler works as a server, otherwise - False

                :return: bool
                """
        return self._WNativeSocketHandler__server_mode

    @verify_type(io_loop=IOLoop)
    def setup_handler(self, io_loop):
        """ :meth:`.WIOLoopServiceHandler.setup_handler` implementation.
                If :class:`.WNativeSocketDirectIOHandler` is used as a io-handler, then socket object is saved
                to this handler before loop starting

                :param io_loop: io_loop to use
                :return: None
                """
        if self.server_mode() is True:
            s = self.transport().server_socket(self.config())
        else:
            s = self.transport().client_socket(self.config())
        io_handler = self.io_handler()
        if isinstance(io_handler, WNativeSocketDirectIOHandler) is True:
            io_handler.transport_socket(s)
        io_loop.add_handler(s.fileno(), io_handler.handler_fn, io_loop.READ)

    def loop_stopped(self):
        """ Terminate socket connection because of stopping loop

                :return: None
                """
        transport = self.transport()
        if self.server_mode() is True:
            transport.close_server_socket(self.config())
        else:
            transport.close_client_socket(self.config())


class WZMQHandler(WIOLoopServiceHandler, metaclass=ABCMeta):

    class SocketOption:

        def __init__(self, name, value):
            self.name = name
            self.value = value

    class SetupAgent:

        @verify_type(socket_type=int, connection=str)
        def __init__(self, socket_type, connection, *socket_options):
            self._SetupAgent__socket_type = socket_type
            self._SetupAgent__connection = connection
            for option in socket_options:
                if isinstance(option, WZMQHandler.SocketOption) is False:
                    raise TypeError('Invalid socket option')

            self._SetupAgent__socket_options = socket_options if len(socket_options) > 0 else tuple()

        def socket_type(self):
            return self._SetupAgent__socket_type

        def connection(self):
            return self._SetupAgent__connection

        def socket_options(self):
            return self._SetupAgent__socket_options

        def create_socket(self, handler):
            if isinstance(handler, WZMQHandler) is False:
                raise TypeError('Invalid handler type')
            context = handler.context()
            for option in self.socket_options():
                context.setsockopt(option.name, option.value)

            return context.socket(self.socket_type())

        @verify_type(io_loop=IOLoop)
        def setup_handler(self, handler, io_loop):
            if isinstance(handler, WZMQHandler) is False:
                raise TypeError('Invalid handler type')
            s = self.create_socket(handler)
            return ZMQStream(s, io_loop=io_loop)

        def setup_receiver(self, handler, receive_agent):
            if isinstance(handler, WZMQHandler) is False:
                raise TypeError('Invalid handler type')
            if isinstance(receive_agent, WZMQHandler.ReceiveAgent) is False:
                raise TypeError('Invalid receive agent type')
            stream = handler.stream()
            if stream is None:
                raise RuntimeError("Handler stream wasn't set")

            def callback(msg):
                receive_agent.on_receive(handler, msg)

            receive_agent.setup_receiver(handler)
            stream.on_recv(callback)

    class BindSetupAgent(SetupAgent):

        def create_socket(self, handler):
            socket = WZMQHandler.SetupAgent.create_socket(self, handler)
            socket.bind(self.connection())
            return socket

    class ConnectSetupAgent(SetupAgent):

        def create_socket(self, handler):
            socket = WZMQHandler.SetupAgent.create_socket(self, handler)
            socket.connect(self.connection())
            return socket

    class SendAgent:

        @verify_type(data=bytes)
        def send(self, handler, data):
            if isinstance(handler, WZMQHandler) is False:
                raise TypeError('Invalid handler type')
            stream = handler.stream()
            if stream is None:
                raise RuntimeError("Handler stream wasn't set")
            stream.send(data)
            stream.flush()

    class ReceiveAgent:

        @abstractmethod
        def on_receive(self, handler, msg):
            raise NotImplementedError('This method is abstract')

        def setup_receiver(self, handler):
            pass

    @verify_type(context=(ZMQContext, None))
    def __init__(self, context=None):
        self._WZMQHandler__context = context if context is not None else ZMQContext()
        self._WZMQHandler__stream = None
        self._WZMQHandler__setup_agent = None
        self._WZMQHandler__receive_agent = None

    def context(self):
        return self._WZMQHandler__context

    def stream(self):
        return self._WZMQHandler__stream

    def setup_agent(self):
        return self._WZMQHandler__setup_agent

    def receive_agent(self):
        return self._WZMQHandler__receive_agent

    def configure(self, setup_agent, receive_agent=None):
        if self._WZMQHandler__setup_agent is not None:
            raise RuntimeError('Unable to configure handler multiple time')
        self._WZMQHandler__setup_agent = setup_agent
        self._WZMQHandler__receive_agent = receive_agent

    @verify_type(io_loop=IOLoop)
    def setup_handler(self, io_loop):
        setup_agent = self.setup_agent()
        self._WZMQHandler__stream = setup_agent.setup_handler(self, io_loop)
        receive_agent = self.receive_agent()
        if receive_agent is not None:
            setup_agent.setup_receiver(self, receive_agent)


class WZMQService(WIOLoopService):

    @verify_type('paranoid', setup_agent=WZMQHandler.SetupAgent, loop=(IOLoop, None))
    @verify_type('paranoid', receive_agent=(WZMQHandler.ReceiveAgent, None), timeout=(int, None))
    @verify_type(handler=(WZMQHandler, None))
    def __init__(self, setup_agent, loop=None, handler=None, receive_agent=None, timeout=None):
        if handler is None:
            handler = WZMQHandler()
        handler.configure(setup_agent, receive_agent)
        WIOLoopService.__init__(self, handler, loop=loop, timeout=timeout)

    def discard_queue_messages(self):
        """ Sometimes it is necessary to drop undelivered messages. These messages may be stored in different
                caches, for example in a zmq socket queue. With different zmq flags we can tweak zmq sockets and
                contexts no to keep those messages. But inside ZMQStream class there is a queue that can not be
                cleaned other way then the way it does in this method. So yes, it is dirty to access protected
                members, and yes it can be broken at any moment. And yes without correct locking procedure there
                is a possibility of unpredicted behaviour. But still - there is no other way to drop undelivered
                messages

                Discussion of the problem: https://github.com/zeromq/pyzmq/issues/1095

                :return: None
                """
        zmq_stream_queue = self.handler().stream()._send_queue
        while not zmq_stream_queue.empty():
            try:
                zmq_stream_queue.get(False)
            except queue.Empty:
                continue

            zmq_stream_queue.task_done()


class WLoglessIOLoop(IOLoop):

    def _setup_logging(self):
        pass


class WZMQSyncAgent(WZMQHandler.ReceiveAgent):

    @verify_type(timeout=(int, float, None))
    def __init__(self, timeout=None):
        self._WZMQSyncAgent__timeout = timeout
        self._WZMQSyncAgent__threaded_event = Event()
        self._WZMQSyncAgent__data = None
        self._WZMQSyncAgent__handler = None

    def timeout(self):
        return self._WZMQSyncAgent__timeout

    def event(self):
        return self._WZMQSyncAgent__threaded_event

    def data(self):
        data = self._WZMQSyncAgent__data
        self._WZMQSyncAgent__data = None
        self._WZMQSyncAgent__threaded_event.clear()
        return data

    def handler(self):
        return self._WZMQSyncAgent__handler

    def on_receive(self, handler, msg):
        if self._WZMQSyncAgent__data is not None:
            raise RuntimeError('Multiple responses for a single request')
        self._WZMQSyncAgent__data = msg
        self._WZMQSyncAgent__threaded_event.set()

    @verify_type(handler=WZMQHandler)
    def setup_receiver(self, handler):
        if self._WZMQSyncAgent__handler is None:
            self._WZMQSyncAgent__handler = handler
        else:
            raise RuntimeError('Unable to setup receive agent multiple times')

    def receive(self):
        status = self.event().wait(self.timeout())
        if status is True:
            return self.data()
        raise TimeoutError('Request timeout reached')