# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/server/TProcessPoolServer.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 4054 bytes
import logging
from multiprocessing import Process, Value, Condition
from .TServer import TServer
from thrift.transport.TTransport import TTransportException
logger = logging.getLogger(__name__)

class TProcessPoolServer(TServer):
    __doc__ = "Server with a fixed size pool of worker subprocesses to service requests\n\n    Note that if you need shared state between the handlers - it's up to you!\n    Written by Dvir Volk, doat.com\n    "

    def __init__(self, *args):
        (TServer.__init__)(self, *args)
        self.numWorkers = 10
        self.workers = []
        self.isRunning = Value('b', False)
        self.stopCondition = Condition()
        self.postForkCallback = None

    def setPostForkCallback(self, callback):
        if not callable(callback):
            raise TypeError('This is not a callback!')
        self.postForkCallback = callback

    def setNumWorkers(self, num):
        """Set the number of worker threads that should be created"""
        self.numWorkers = num

    def workerProcess(self):
        """Loop getting clients from the shared queue and process them"""
        if self.postForkCallback:
            self.postForkCallback()
        while self.isRunning.value:
            try:
                client = self.serverTransport.accept()
                if not client:
                    continue
                self.serveClient(client)
            except (KeyboardInterrupt, SystemExit):
                return 0
            except Exception as x:
                logger.exception(x)

    def serveClient(self, client):
        """Process input/output from a client for as long as possible"""
        itrans = self.inputTransportFactory.getTransport(client)
        otrans = self.outputTransportFactory.getTransport(client)
        iprot = self.inputProtocolFactory.getProtocol(itrans)
        oprot = self.outputProtocolFactory.getProtocol(otrans)
        try:
            while True:
                self.processor.process(iprot, oprot)

        except TTransportException:
            pass
        except Exception as x:
            logger.exception(x)

        itrans.close()
        otrans.close()

    def serve(self):
        """Start workers and put into queue"""
        self.isRunning.value = True
        self.serverTransport.listen()
        for i in range(self.numWorkers):
            try:
                w = Process(target=(self.workerProcess))
                w.daemon = True
                w.start()
                self.workers.append(w)
            except Exception as x:
                logger.exception(x)

        while True:
            self.stopCondition.acquire()
            try:
                self.stopCondition.wait()
                break
            except (SystemExit, KeyboardInterrupt):
                break
            except Exception as x:
                logger.exception(x)

        self.isRunning.value = False

    def stop(self):
        self.isRunning.value = False
        self.stopCondition.acquire()
        self.stopCondition.notify()
        self.stopCondition.release()