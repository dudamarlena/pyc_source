# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/server/TServer.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 11784 bytes
from six.moves import queue
import logging, os, threading
from thrift.protocol import TBinaryProtocol
from thrift.protocol.THeaderProtocol import THeaderProtocolFactory
from thrift.transport import TTransport
logger = logging.getLogger(__name__)

class TServer(object):
    __doc__ = 'Base interface for a server, which must have a serve() method.\n\n    Three constructors for all servers:\n    1) (processor, serverTransport)\n    2) (processor, serverTransport, transportFactory, protocolFactory)\n    3) (processor, serverTransport,\n        inputTransportFactory, outputTransportFactory,\n        inputProtocolFactory, outputProtocolFactory)\n    '

    def __init__(self, *args):
        if len(args) == 2:
            self.__initArgs__(args[0], args[1], TTransport.TTransportFactoryBase(), TTransport.TTransportFactoryBase(), TBinaryProtocol.TBinaryProtocolFactory(), TBinaryProtocol.TBinaryProtocolFactory())
        else:
            if len(args) == 4:
                self.__initArgs__(args[0], args[1], args[2], args[2], args[3], args[3])
            elif len(args) == 6:
                self.__initArgs__(args[0], args[1], args[2], args[3], args[4], args[5])

    def __initArgs__(self, processor, serverTransport, inputTransportFactory, outputTransportFactory, inputProtocolFactory, outputProtocolFactory):
        self.processor = processor
        self.serverTransport = serverTransport
        self.inputTransportFactory = inputTransportFactory
        self.outputTransportFactory = outputTransportFactory
        self.inputProtocolFactory = inputProtocolFactory
        self.outputProtocolFactory = outputProtocolFactory
        input_is_header = isinstance(self.inputProtocolFactory, THeaderProtocolFactory)
        output_is_header = isinstance(self.outputProtocolFactory, THeaderProtocolFactory)
        if any((input_is_header, output_is_header)):
            if input_is_header != output_is_header:
                raise ValueError('THeaderProtocol servers require that both the input and output protocols are THeaderProtocol.')

    def serve(self):
        pass


class TSimpleServer(TServer):
    __doc__ = 'Simple single-threaded server that just pumps around one transport.'

    def __init__(self, *args):
        (TServer.__init__)(self, *args)

    def serve(self):
        self.serverTransport.listen()
        while 1:
            client = self.serverTransport.accept()
            if not client:
                pass
            else:
                itrans = self.inputTransportFactory.getTransport(client)
                iprot = self.inputProtocolFactory.getProtocol(itrans)
                if isinstance(self.inputProtocolFactory, THeaderProtocolFactory):
                    otrans = None
                    oprot = iprot
                else:
                    otrans = self.outputTransportFactory.getTransport(client)
                    oprot = self.outputProtocolFactory.getProtocol(otrans)
                try:
                    while True:
                        self.processor.process(iprot, oprot)

                except TTransport.TTransportException:
                    pass
                except Exception as x:
                    logger.exception(x)

                itrans.close()
            if otrans:
                otrans.close()


class TThreadedServer(TServer):
    __doc__ = 'Threaded server that spawns a new thread per each connection.'

    def __init__(self, *args, **kwargs):
        (TServer.__init__)(self, *args)
        self.daemon = kwargs.get('daemon', False)

    def serve(self):
        self.serverTransport.listen()
        while True:
            try:
                client = self.serverTransport.accept()
                if not client:
                    continue
                t = threading.Thread(target=(self.handle), args=(client,))
                t.setDaemon(self.daemon)
                t.start()
            except KeyboardInterrupt:
                raise
            except Exception as x:
                logger.exception(x)

    def handle(self, client):
        itrans = self.inputTransportFactory.getTransport(client)
        iprot = self.inputProtocolFactory.getProtocol(itrans)
        if isinstance(self.inputProtocolFactory, THeaderProtocolFactory):
            otrans = None
            oprot = iprot
        else:
            otrans = self.outputTransportFactory.getTransport(client)
            oprot = self.outputProtocolFactory.getProtocol(otrans)
        try:
            while True:
                self.processor.process(iprot, oprot)

        except TTransport.TTransportException:
            pass
        except Exception as x:
            logger.exception(x)

        itrans.close()
        if otrans:
            otrans.close()


class TThreadPoolServer(TServer):
    __doc__ = 'Server with a fixed size pool of threads which service requests.'

    def __init__(self, *args, **kwargs):
        (TServer.__init__)(self, *args)
        self.clients = queue.Queue()
        self.threads = 10
        self.daemon = kwargs.get('daemon', False)

    def setNumThreads(self, num):
        """Set the number of worker threads that should be created"""
        self.threads = num

    def serveThread(self):
        """Loop around getting clients from the shared queue and process them."""
        while True:
            try:
                client = self.clients.get()
                self.serveClient(client)
            except Exception as x:
                logger.exception(x)

    def serveClient(self, client):
        """Process input/output from a client for as long as possible"""
        itrans = self.inputTransportFactory.getTransport(client)
        iprot = self.inputProtocolFactory.getProtocol(itrans)
        if isinstance(self.inputProtocolFactory, THeaderProtocolFactory):
            otrans = None
            oprot = iprot
        else:
            otrans = self.outputTransportFactory.getTransport(client)
            oprot = self.outputProtocolFactory.getProtocol(otrans)
        try:
            while True:
                self.processor.process(iprot, oprot)

        except TTransport.TTransportException:
            pass
        except Exception as x:
            logger.exception(x)

        itrans.close()
        if otrans:
            otrans.close()

    def serve(self):
        """Start a fixed number of worker threads and put client into a queue"""
        for i in range(self.threads):
            try:
                t = threading.Thread(target=(self.serveThread))
                t.setDaemon(self.daemon)
                t.start()
            except Exception as x:
                logger.exception(x)

        self.serverTransport.listen()
        while True:
            try:
                client = self.serverTransport.accept()
                if not client:
                    continue
                self.clients.put(client)
            except Exception as x:
                logger.exception(x)


class TForkingServer(TServer):
    __doc__ = 'A Thrift server that forks a new process for each request\n\n    This is more scalable than the threaded server as it does not cause\n    GIL contention.\n\n    Note that this has different semantics from the threading server.\n    Specifically, updates to shared variables will no longer be shared.\n    It will also not work on windows.\n\n    This code is heavily inspired by SocketServer.ForkingMixIn in the\n    Python stdlib.\n    '

    def __init__(self, *args):
        (TServer.__init__)(self, *args)
        self.children = []

    def serve(self):

        def try_close(file):
            try:
                file.close()
            except IOError as e:
                logger.warning(e, exc_info=True)

        self.serverTransport.listen()
        while True:
            client = self.serverTransport.accept()
            if not client:
                pass
            else:
                try:
                    pid = os.fork()
                    if pid:
                        self.children.append(pid)
                        self.collect_children()
                        itrans = self.inputTransportFactory.getTransport(client)
                        otrans = self.outputTransportFactory.getTransport(client)
                        try_close(itrans)
                        try_close(otrans)
                    else:
                        itrans = self.inputTransportFactory.getTransport(client)
                        iprot = self.inputProtocolFactory.getProtocol(itrans)
                        if isinstance(self.inputProtocolFactory, THeaderProtocolFactory):
                            otrans = None
                            oprot = iprot
                        else:
                            otrans = self.outputTransportFactory.getTransport(client)
                            oprot = self.outputProtocolFactory.getProtocol(otrans)
                        ecode = 0
                        try:
                            try:
                                while True:
                                    self.processor.process(iprot, oprot)

                            except TTransport.TTransportException:
                                pass
                            except Exception as e:
                                logger.exception(e)
                                ecode = 1

                        finally:
                            try_close(itrans)
                            if otrans:
                                try_close(otrans)

                        os._exit(ecode)
                except TTransport.TTransportException:
                    pass
                except Exception as x:
                    logger.exception(x)

    def collect_children(self):
        while self.children:
            try:
                pid, status = os.waitpid(0, os.WNOHANG)
            except os.error:
                pid = None

            if pid:
                self.children.remove(pid)
            else:
                break