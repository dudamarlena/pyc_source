# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\optimizer\xmlrpcserver.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5752 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import threading, time
from six.moves import xmlrpc_server
import pyalgotrade.logger
from pyalgotrade.optimizer import base
from pyalgotrade.optimizer import serialization
logger = pyalgotrade.logger.getLogger(__name__)

class AutoStopThread(threading.Thread):

    def __init__(self, server):
        super(AutoStopThread, self).__init__()
        self._AutoStopThread__server = server

    def run(self):
        while self._AutoStopThread__server.jobsPending():
            time.sleep(1)

        self._AutoStopThread__server.stop()


class Job(object):

    def __init__(self, strategyParameters):
        self._Job__strategyParameters = strategyParameters
        self._Job__bestResult = None
        self._Job__bestParameters = None
        self._Job__id = id(self)

    def getId(self):
        return self._Job__id

    def getNextParameters(self):
        ret = None
        if len(self._Job__strategyParameters):
            ret = self._Job__strategyParameters.pop()
        return ret


class RequestHandler(xmlrpc_server.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/PyAlgoTradeRPC', )


class Server(xmlrpc_server.SimpleXMLRPCServer):

    def __init__(self, paramSource, resultSinc, barFeed, address, port, autoStop=True, batchSize=200):
        if not batchSize > 0:
            raise AssertionError('Invalid batch size')
        else:
            xmlrpc_server.SimpleXMLRPCServer.__init__(self,
              (address, port), requestHandler=RequestHandler, logRequests=False, allow_none=True)
            self._Server__batchSize = batchSize
            self._Server__paramSource = paramSource
            self._Server__resultSinc = resultSinc
            self._Server__barFeed = barFeed
            self._Server__instrumentsAndBars = None
            self._Server__barsFreq = None
            self._Server__activeJobs = {}
            self._Server__lock = threading.Lock()
            self._Server__startedServingEvent = threading.Event()
            self._Server__forcedStop = False
            self._Server__bestResult = None
            if autoStop:
                self._Server__autoStopThread = AutoStopThread(self)
            else:
                self._Server__autoStopThread = None
        self.register_introspection_functions()
        self.register_function(self.getInstrumentsAndBars, 'getInstrumentsAndBars')
        self.register_function(self.getBarsFrequency, 'getBarsFrequency')
        self.register_function(self.getNextJob, 'getNextJob')
        self.register_function(self.pushJobResults, 'pushJobResults')

    def getInstrumentsAndBars(self):
        return self._Server__instrumentsAndBars

    def getBarsFrequency(self):
        return str(self._Server__barsFreq)

    def getNextJob(self):
        ret = None
        with self._Server__lock:
            params = [p.args for p in self._Server__paramSource.getNext(self._Server__batchSize)]
            if len(params):
                ret = Job(params)
                self._Server__activeJobs[ret.getId()] = ret
        return serialization.dumps(ret)

    def jobsPending(self):
        if self._Server__forcedStop:
            return False
        with self._Server__lock:
            jobsPending = not self._Server__paramSource.eof()
            activeJobs = len(self._Server__activeJobs) > 0
        return jobsPending or activeJobs

    def pushJobResults(self, jobId, result, parameters, workerName):
        jobId = serialization.loads(jobId)
        result = serialization.loads(result)
        parameters = serialization.loads(parameters)
        with self._Server__lock:
            try:
                del self._Server__activeJobs[jobId]
            except KeyError:
                return
            else:
                if self._Server__bestResult is None or result > self._Server__bestResult:
                    logger.info('Best result so far %s with parameters %s' % (result, parameters))
                    self._Server__bestResult = result
        self._Server__resultSinc.push(result, (base.Parameters)(*parameters))

    def waitServing(self, timeout=None):
        return self._Server__startedServingEvent.wait(timeout)

    def stop(self):
        self.shutdown()

    def serve(self):
        try:
            logger.info('Loading bars')
            loadedBars = []
            for dateTime, bars in self._Server__barFeed:
                loadedBars.append(bars)

            instruments = self._Server__barFeed.getRegisteredInstruments()
            self._Server__instrumentsAndBars = serialization.dumps((instruments, loadedBars))
            self._Server__barsFreq = self._Server__barFeed.getFrequency()
            if self._Server__autoStopThread:
                self._Server__autoStopThread.start()
            logger.info('Started serving')
            self._Server__startedServingEvent.set()
            self.serve_forever()
            logger.info('Finished serving')
            if self._Server__autoStopThread:
                self._Server__autoStopThread.join()
        finally:
            self._Server__forcedStop = True