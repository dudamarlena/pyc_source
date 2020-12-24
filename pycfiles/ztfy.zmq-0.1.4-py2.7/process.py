# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/zmq/process.py
# Compiled at: 2014-05-12 03:31:21
import multiprocessing, signal, sys, zmq
from zmq.eventloop import ioloop, zmqstream
from ztfy.zmq.interfaces import IZMQProcess
from zope.interface import implements

class ZMQProcess(multiprocessing.Process):
    """
    This is the base for all processes and offers utility methods
    for setup and creating new streams.
    """
    implements(IZMQProcess)
    socket_type = zmq.REP

    def __init__(self, bind_addr, handler):
        super(ZMQProcess, self).__init__()
        self.context = None
        self.loop = None
        self.bind_addr = bind_addr
        self.rep_stream = None
        self.handler = handler
        return

    def setup(self):
        """Creates a :attr:`context` and an event :attr:`loop` for the process."""
        self.context = zmq.Context()
        self.loop = ioloop.IOLoop.instance()
        self.rep_stream, _ = self.stream(self.socket_type, self.bind_addr, bind=True)
        self.initStream()

    def initStream(self):
        """Initialize response stream"""
        self.rep_stream.on_recv(self.handler(self, self.rep_stream, self.stop))

    def run(self):
        """Sets up everything and starts the event loop."""
        signal.signal(signal.SIGTERM, self.exit)
        self.setup()
        self.loop.start()

    def stop(self):
        """Stops the event loop."""
        if self.loop is not None:
            self.loop.stop()
            self.loop = None
        return

    def exit(self, num, frame):
        self.stop()
        sys.exit()

    def stream(self, sock_type, addr, bind, callback=None, subscribe=''):
        u"""
        Creates a :class:`~zmq.eventloop.zmqstream.ZMQStream`.

        :param sock_type: The ØMQ socket type (e.g. ``zmq.REQ``)
        :param addr: Address to bind or connect to formatted as *host:port*,
                *(host, port)* or *host* (bind to random port).
                If *bind* is ``True``, *host* may be:

                - the wild-card ``*``, meaning all available interfaces,
                - the primary IPv4 address assigned to the interface, in its
                numeric representation or
                - the interface name as defined by the operating system.

                If *bind* is ``False``, *host* may be:

                - the DNS name of the peer or
                - the IPv4 address of the peer, in its numeric representation.

                If *addr* is just a host name without a port and *bind* is
                ``True``, the socket will be bound to a random port.
        :param bind: Binds to *addr* if ``True`` or tries to connect to it
                otherwise.
        :param callback: A callback for
                :meth:`~zmq.eventloop.zmqstream.ZMQStream.on_recv`, optional
        :param subscribe: Subscription pattern for *SUB* sockets, optional,
                defaults to ``b''``.
        :returns: A tuple containg the stream and the port number.

        """
        sock = self.context.socket(sock_type)
        if isinstance(addr, (str, unicode)):
            addr = addr.split(':')
        host, port = addr if len(addr) == 2 else (addr[0], None)
        if bind:
            if port:
                sock.bind('tcp://%s:%s' % (host, port))
            else:
                port = sock.bind_to_random_port('tcp://%s' % host)
        else:
            sock.connect('tcp://%s:%s' % (host, port))
        if sock_type == zmq.SUB:
            sock.setsockopt(zmq.SUBSCRIBE, subscribe)
        stream = zmqstream.ZMQStream(sock, self.loop)
        if callback:
            stream.on_recv(callback)
        return (stream, int(port))


def processExitFunc(process=None):
    if process is not None:
        if process.is_alive():
            process.terminate()
        process.join()
    return