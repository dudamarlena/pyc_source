# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\optimizer\worker.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5995 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import socket, multiprocessing, retrying
from six.moves import xmlrpc_client
import pyalgotrade.logger
from pyalgotrade import barfeed
from pyalgotrade.optimizer import serialization
wait_exponential_multiplier = 500
wait_exponential_max = 10000
stop_max_delay = 10000

def any_exception(exception):
    return True


@retrying.retry(wait_exponential_multiplier=wait_exponential_multiplier, wait_exponential_max=wait_exponential_max, stop_max_delay=stop_max_delay, retry_on_exception=any_exception)
def retry_on_network_error(function, *args, **kwargs):
    return function(*args, **kwargs)


class Worker(object):

    def __init__(self, address, port, workerName=None):
        url = 'http://%s:%s/PyAlgoTradeRPC' % (address, port)
        self._Worker__logger = pyalgotrade.logger.getLogger(workerName)
        self._Worker__server = xmlrpc_client.ServerProxy(url, allow_none=True)
        if workerName is None:
            self._Worker__workerName = socket.gethostname()
        else:
            self._Worker__workerName = workerName

    def getLogger(self):
        return self._Worker__logger

    def getInstrumentsAndBars(self):
        ret = retry_on_network_error(self._Worker__server.getInstrumentsAndBars)
        ret = serialization.loads(ret)
        return ret

    def getBarsFrequency(self):
        ret = retry_on_network_error(self._Worker__server.getBarsFrequency)
        ret = int(ret)
        return ret

    def getNextJob(self):
        ret = retry_on_network_error(self._Worker__server.getNextJob)
        ret = serialization.loads(ret)
        return ret

    def pushJobResults(self, jobId, result, parameters):
        jobId = serialization.dumps(jobId)
        result = serialization.dumps(result)
        parameters = serialization.dumps(parameters)
        workerName = serialization.dumps(self._Worker__workerName)
        retry_on_network_error(self._Worker__server.pushJobResults, jobId, result, parameters, workerName)

    def __processJob(self, job, barsFreq, instruments, bars):
        bestResult = None
        parameters = job.getNextParameters()
        bestParams = parameters
        while parameters is not None:
            feed = barfeed.OptimizerBarFeed(barsFreq, instruments, bars)
            self.getLogger().info('Running strategy with parameters %s' % str(parameters))
            result = None
            try:
                result = (self.runStrategy)(feed, *parameters)
            except Exception as e:
                try:
                    self.getLogger().exception('Error running strategy with parameters %s: %s' % (str(parameters), e))
                finally:
                    e = None
                    del e

            self.getLogger().info('Result %s' % result)
            if bestResult is None or result > bestResult:
                bestResult = result
                bestParams = parameters
            parameters = job.getNextParameters()

        assert bestParams is not None
        self.pushJobResults(job.getId(), bestResult, bestParams)

    def runStrategy(self, feed, parameters):
        raise Exception('Not implemented')

    def run(self):
        try:
            self.getLogger().info('Started running')
            instruments, bars = self.getInstrumentsAndBars()
            barsFreq = self.getBarsFrequency()
            job = self.getNextJob()
            while job is not None:
                self._Worker__processJob(job, barsFreq, instruments, bars)
                job = self.getNextJob()

            self.getLogger().info('Finished running')
        except Exception as e:
            try:
                self.getLogger().exception('Finished running with errors: %s' % e)
            finally:
                e = None
                del e


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
    if not workerCount is None:
        assert workerCount > 0
    if workerCount is None:
        workerCount = multiprocessing.cpu_count()
    workers = []
    for i in range(workerCount):
        workers.append(multiprocessing.Process(target=worker_process, args=(strategyClass, address, port, workerName)))

    for process in workers:
        process.start()

    for process in workers:
        process.join()