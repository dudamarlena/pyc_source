# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\optimizer\local.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5229 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import logging, multiprocessing, os, random, socket, threading, time
from pyalgotrade.optimizer import base
from pyalgotrade.optimizer import server
from pyalgotrade.optimizer import worker
from pyalgotrade.optimizer import xmlrpcserver
logger = logging.getLogger(__name__)

class ServerThread(threading.Thread):

    def __init__(self, server):
        super(ServerThread, self).__init__()
        self._ServerThread__server = server

    def run(self):
        self._ServerThread__results = self._ServerThread__server.serve()


def worker_process(strategyClass, port, logLevel):

    class Worker(worker.Worker):

        def runStrategy(self, barFeed, *args, **kwargs):
            strat = strategyClass(barFeed, *args, **kwargs)
            strat.run()
            return strat.getResult()

    try:
        name = 'worker-%s' % os.getpid()
        w = Worker('localhost', port, name)
        w.getLogger().setLevel(logLevel)
        w.run()
    except Exception as e:
        try:
            w.getLogger().exception('Failed to run worker: %s' % e)
        finally:
            e = None
            del e


def find_port():
    while True:
        ret = random.randint(1025, 65536)
        try:
            s = socket.socket()
            s.bind(('localhost', ret))
            s.close()
            return ret
        except socket.error:
            pass


def stop_process(p):
    timeout = 3
    p.join(timeout)
    while p.is_alive():
        logger.info('Stopping process %s' % p.pid)
        p.terminate()
        p.join(timeout)


def run_impl(strategyClass, barFeed, strategyParameters, batchSize, workerCount=None, logLevel=logging.ERROR, resultSinc=None):
    if workerCount is None:
        workerCount = multiprocessing.cpu_count()
    assert workerCount > 0, 'No workers'
    ret = None
    workers = []
    port = find_port()
    if port is None:
        raise Exception('Failed to find a port to listen')
    paramSource = base.ParameterSource(strategyParameters)
    if resultSinc is None:
        resultSinc = base.ResultSinc()
    logger.info('Starting server on port %s' % port)
    srv = xmlrpcserver.Server(paramSource, resultSinc, barFeed, 'localhost', port, autoStop=False, batchSize=batchSize)
    serverThread = ServerThread(srv)
    serverThread.start()
    logger.info('Waiting for the server to be ready')
    srv.waitServing()
    try:
        logger.info('Starting %s workers' % workerCount)
        for i in range(workerCount):
            workers.append(multiprocessing.Process(target=worker_process,
              args=(
             strategyClass, port, logLevel)))

        for process in workers:
            process.start()

        while srv.jobsPending():
            time.sleep(1)

    finally:
        for process in workers:
            stop_process(process)

        logger.info('Stopping server')
        srv.stop()
        serverThread.join()
        bestResult, bestParameters = resultSinc.getBest()
        if bestResult is not None:
            ret = server.Results(bestParameters.args, bestResult)

    return ret


def run(strategyClass, barFeed, strategyParameters, workerCount=None, logLevel=logging.ERROR, batchSize=200):
    """Executes many instances of a strategy in parallel and finds the parameters that yield the best results.

    :param strategyClass: The strategy class.
    :param barFeed: The bar feed to use to backtest the strategy.
    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`.
    :param strategyParameters: The set of parameters to use for backtesting. An iterable object where **each element is
        a tuple that holds parameter values**.
    :param workerCount: The number of strategies to run in parallel. If None then as many workers as CPUs are used.
    :type workerCount: int.
    :param logLevel: The log level. Defaults to **logging.ERROR**.
    :param batchSize: The number of strategy executions that are delivered to each worker.
    :type batchSize: int.
    :rtype: A :class:`Results` instance with the best results found.
    """
    return run_impl(strategyClass, barFeed, strategyParameters, batchSize, workerCount=workerCount, logLevel=logLevel)