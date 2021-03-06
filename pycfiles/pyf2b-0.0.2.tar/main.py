# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/station/main.py
# Compiled at: 2015-06-25 18:18:03
import traceback
from twisted.internet.protocol import ServerFactory
from twisted.protocols import basic
from twisted.internet.threads import deferToThread
from simplejson import loads
from pyf.transport.packets import encode_packet_flow
import Queue
from pyf.transport import decode_packet_flow, Packet
import logging
logger = logging.getLogger('pyf.station')

class BadFlowEnding(Exception):
    pass


class ServerError(Exception):
    pass


class PacketGeneratorAdapter(object):

    def __init__(self, generator):
        self.generator = iter(generator)
        self.inited = False

    def __iter__(self):
        return self

    def next(self):
        if self.inited:
            return self.adapted_generator.next()
        else:
            self.header_str = self.generator.next()
            self.header = Packet(data=loads(self.header_str), data_type='serialized')
            self.adapted_generator = decode_packet_flow(self.generator, decompress=self.header.get('compressed', False), pure_flow=True)
            self.inited = True
            return self.header


class GeneratorAdapter(object):

    def __init__(self, client):
        self.client = client

    def __iter__(self):
        queue = self.client.data_queue
        i = 0
        while True:
            if self.client.data_queue.empty() and self.client.data_queue.finished:
                if self.client.data_queue.complete:
                    raise StopIteration
                else:
                    raise BadFlowEnding('Bad ending in flow. Corrupted connection ?')
            item = queue.get()
            yield item
            i += 1


class FlowReceiver(basic.LineReceiver):
    delimiter = '\r\n\x00'


class DataFlowQueue(Queue.Queue):

    def __init__(self, *args, **kwargs):
        Queue.Queue.__init__(self, *args, **kwargs)
        self.finished = False
        self.complete = False


class FlowProtocol(FlowReceiver):
    go = Packet(dict(message='go', type='control'))
    nogo = Packet(dict(message='nogo', type='control', detail='error in initialization'))
    good = 'good.'
    ok = Packet(dict(message='ok', type='info'))

    def lineReceived(self, line):
        if line == self.good:
            self.data_queue.finished = True
            self.data_queue.complete = True
        else:
            self.data_queue.put(line)

    def message(self, message):
        if isinstance(message, Packet):
            for v in encode_packet_flow([message], separator=self.delimiter):
                self.transport.write(v)

        else:
            self.transport.write(message + self.delimiter)

    def data_handler_wrapper(self, data_handler, flow, client):
        """we don't catch errors here because we are in a thread.
        The ErrBack of our deferToThread caller will catch them

        This wrapper accepts either a class or a callable as a data
        handler.

        If we receive a class it will be instanciated with flow and client
        as its args. And we will then call the handle_data() method on it
        without arguments

        If we receive a callable we will call it with flow and client as
        arguments.
        """
        if isinstance(data_handler, type):
            d = data_handler(flow, client)
            d.handle_data()
        else:
            data_handler(flow=flow, client=client)

    def data_handler_error(self, err):
        """an ErrBack used by the deferToThread of connectionMade
        to send errors back to the client.
        """
        logger.warning('Error sent to client: %r' % err)
        self.error(traceback.format_exc())

    def connectionMade(self):
        try:
            self.factory.numProtocols = self.factory.numProtocols + 1
            self.factory.clients.append(self)
            self.data_queue = DataFlowQueue(maxsize=self.factory.max_items)
            if self.factory.numProtocols > self.factory.max_clients:
                self.error(ServerError('Too many connections. Try again later.'))
            else:
                flow = PacketGeneratorAdapter(GeneratorAdapter(self))
                d = deferToThread(self.data_handler_wrapper, self.factory.data_handler, flow, self)
                d.addErrback(self.data_handler_error)
                self.message(self.go)
        except Exception as e:
            self.transport.loseConnection()
            raise e

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        self.factory.numProtocols = self.factory.numProtocols - 1
        self.data_queue.finished = True

    def error(self, error):
        self.message(Packet(dict(type='error', message=repr(error), error_type=type(error).__name__)))
        self.transport.loseConnection()

    def success(self, message):
        self.message(Packet(dict(type='success', message=message)))
        self.transport.loseConnection()


class FlowServer(ServerFactory):
    """ The flow server factory.

    Example use:

    >>> factory = FlowServer(my_handler)
    # handler is a function receiving a flow
    # and a "client" keyword argument
    # client being a FlowProtocol instance.
    >>> reactor.listenTCP(8000, factory)
    >>> reactor.run()

    """
    protocol = FlowProtocol

    def __init__(self, data_handler, max_items=1000, max_clients=100):
        self.max_items = max_items
        self.max_clients = max_clients
        self.data_handler = data_handler
        self.numProtocols = 0
        self.clients = list()


def launch_server():
    from twisted.internet import reactor

    def toto_plouf(flow, client=None):
        for i, item in enumerate(flow):
            pass

        client.success('Done')

    factory = FlowServer(toto_plouf)
    reactor.listenTCP(8000, factory)
    reactor.run()
    return


if __name__ == '__main__':
    launch_server()