# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/optimizer/worker.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import xmlrpclib, pickle, time, socket, random, multiprocessing, pyalgotrade.logger
from pyalgotrade import barfeed

def call_function(function, *args, **kwargs):
    return function(*args, **kwargs)


def call_and_retry_on_network_error(function, retryCount, *args, **kwargs):
    ret = None
    while retryCount > 0:
        retryCount -= 1
        try:
            ret = call_function(function, *args, **kwargs)
            return ret
        except socket.error:
            time.sleep(random.randint(1, 3))

    ret = call_function(function, *args, **kwargs)
    return ret


class Worker(object):

    def __init__(self, address, port, workerName=None):
        url = 'http://%s:%s/PyAlgoTradeRPC' % (address, port)
        self.__server = xmlrpclib.ServerProxy(url, allow_none=True)
        self.__logger = pyalgotrade.logger.getLogger(workerName)
        if workerName is None:
            self.__workerName = socket.gethostname()
        else:
            self.__workerName = workerName
        return

    def getLogger(self):
        return self.__logger

    def getInstrumentsAndBars(self):
        ret = call_and_retry_on_network_error(self.__server.getInstrumentsAndBars, 10)
        ret = pickle.loads(ret)
        return ret

    def getBarsFrequency(self):
        ret = call_and_retry_on_network_error(self.__server.getBarsFrequency, 10)
        ret = int(ret)
        return ret

    def getNextJob(self):
        ret = call_and_retry_on_network_error(self.__server.getNextJob, 10)
        ret = pickle.loads(ret)
        return ret

    def pushJobResults(self, jobId, result, parameters):
        jobId = pickle.dumps(jobId)
        result = pickle.dumps(result)
        parameters = pickle.dumps(parameters)
        workerName = pickle.dumps(self.__workerName)
        call_and_retry_on_network_error(self.__server.pushJobResults, 10, jobId, result, parameters, workerName)

    def __processJob(self, job, barsFreq, instruments, bars):
        bestResult = None
        parameters = job.getNextParameters()
        bestParams = parameters
        while parameters is not None:
            feed = barfeed.OptimizerBarFeed(barsFreq, instruments, bars)
            self.getLogger().info('Running strategy with parameters %s' % str(parameters))
            result = None
            try:
                result = self.runStrategy(feed, *parameters)
            except Exception as e:
                self.getLogger().exception('Error running strategy with parameters %s: %s' % (str(parameters), e))

            self.getLogger().info('Result %s' % result)
            if bestResult is None or result > bestResult:
                bestResult = result
                bestParams = parameters
            parameters = job.getNextParameters()

        assert bestParams is not None
        self.pushJobResults(job.getId(), bestResult, bestParams)
        return

    def runStrategy(self, feed, parameters):
        raise Exception('Not implemented')

    def run(self):
        try:
            self.getLogger().info('Started running')
            instruments, bars = self.getInstrumentsAndBars()
            barsFreq = self.getBarsFrequency()
            job = self.getNextJob()
            while job is not None:
                self.__processJob(job, barsFreq, instruments, bars)
                job = self.getNextJob()

            self.getLogger().info('Finished running')
        except Exception as e:
            self.getLogger().exception('Finished running with errors: %s' % e)

        return


def worker_process(strategyClass, address, port, workerName):

    class MyWorker(Worker):

        def runStrategy(self, barFeed, *args, **kwargs):
            strat = strategyClass(barFeed, *args, **kwargs)
            strat.run()
            return strat.getResult()

    w = MyWorker(address, port, workerName)
    w.run()


def run(strategyClass, address, port, workerCount=None, workerName=None):
    """Executes one or more worker processes that will run a strategy with the bars and parameters supplied by the server.

    :param strategyClass: The strategy class.
    :param address: The address of the server.
    :type address: string.
    :param port: The port where the server is listening for incoming connections.
    :type port: int.
    :param workerCount: The number of worker processes to run. If None then as many workers as CPUs are used.
    :type workerCount: int.
    :param workerName: A name for the worker. A name that identifies the worker. If None, the hostname is used.
    :type workerName: string.
    """
    assert workerCount is None or workerCount > 0
    if workerCount is None:
        workerCount = multiprocessing.cpu_count()
    workers = []
    for i in range(workerCount):
        workers.append(multiprocessing.Process(target=worker_process, args=(strategyClass, address, port, workerName)))

    for process in workers:
        process.start()

    for process in workers:
        process.join()

    return