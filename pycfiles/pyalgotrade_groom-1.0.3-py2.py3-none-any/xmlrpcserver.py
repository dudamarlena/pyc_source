# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/optimizer/xmlrpcserver.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import SimpleXMLRPCServer, pickle, threading, time, pyalgotrade.logger
from pyalgotrade.optimizer import base
logger = pyalgotrade.logger.getLogger(__name__)

class AutoStopThread(threading.Thread):

    def __init__(self, server):
        super(AutoStopThread, self).__init__()
        self.__server = server

    def run(self):
        while self.__server.jobsPending():
            time.sleep(1)

        self.__server.stop()


class Job(object):

    def __init__(self, strategyParameters):
        self.__strategyParameters = strategyParameters
        self.__bestResult = None
        self.__bestParameters = None
        self.__id = id(self)
        return

    def getId(self):
        return self.__id

    def getNextParameters(self):
        ret = None
        if len(self.__strategyParameters):
            ret = self.__strategyParameters.pop()
        return ret


class RequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/PyAlgoTradeRPC', )


class Server(SimpleXMLRPCServer.SimpleXMLRPCServer):
    defaultBatchSize = 200

    def __init__(self, paramSource, resultSinc, barFeed, address, port, autoStop=True):
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self, (address, port), requestHandler=RequestHandler, logRequests=False, allow_none=True)
        self.__paramSource = paramSource
        self.__resultSinc = resultSinc
        self.__barFeed = barFeed
        self.__instrumentsAndBars = None
        self.__barsFreq = None
        self.__activeJobs = {}
        self.__activeJobsLock = threading.Lock()
        self.__forcedStop = False
        self.__bestResult = None
        if autoStop:
            self.__autoStopThread = AutoStopThread(self)
        else:
            self.__autoStopThread = None
        self.register_introspection_functions()
        self.register_function(self.getInstrumentsAndBars, 'getInstrumentsAndBars')
        self.register_function(self.getBarsFrequency, 'getBarsFrequency')
        self.register_function(self.getNextJob, 'getNextJob')
        self.register_function(self.pushJobResults, 'pushJobResults')
        return

    def getInstrumentsAndBars(self):
        return self.__instrumentsAndBars

    def getBarsFrequency(self):
        return str(self.__barsFreq)

    def getNextJob(self):
        ret = None
        params = self.__paramSource.getNext(self.defaultBatchSize)
        params = map(lambda p: p.args, params)
        if len(params):
            ret = Job(params)
            with self.__activeJobsLock:
                self.__activeJobs[ret.getId()] = ret
        return pickle.dumps(ret)

    def jobsPending(self):
        if self.__forcedStop:
            return False
        jobsPending = not self.__paramSource.eof()
        with self.__activeJobsLock:
            activeJobs = len(self.__activeJobs) > 0
        return jobsPending or activeJobs

    def pushJobResults(self, jobId, result, parameters, workerName):
        jobId = pickle.loads(jobId)
        result = pickle.loads(result)
        parameters = pickle.loads(parameters)
        with self.__activeJobsLock:
            try:
                del self.__activeJobs[jobId]
            except KeyError:
                return

        if result is None or result > self.__bestResult:
            logger.info('Best result so far %s with parameters %s' % (result, parameters))
            self.__bestResult = result
        self.__resultSinc.push(result, base.Parameters(*parameters))
        return

    def stop(self):
        self.shutdown()

    def serve(self):
        try:
            logger.info('Loading bars')
            loadedBars = []
            for dateTime, bars in self.__barFeed:
                loadedBars.append(bars)

            instruments = self.__barFeed.getRegisteredInstruments()
            self.__instrumentsAndBars = pickle.dumps((instruments, loadedBars))
            self.__barsFreq = self.__barFeed.getFrequency()
            if self.__autoStopThread:
                self.__autoStopThread.start()
            logger.info('Waiting for workers')
            self.serve_forever()
            if self.__autoStopThread:
                self.__autoStopThread.join()
        finally:
            self.__forcedStop = True