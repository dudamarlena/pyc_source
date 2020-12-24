# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\optimizer\server.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 2813 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import pyalgotrade.logger
from pyalgotrade.optimizer import base
from pyalgotrade.optimizer import xmlrpcserver
logger = pyalgotrade.logger.getLogger(__name__)

class Results(object):
    __doc__ = 'The results of the strategy executions.'

    def __init__(self, parameters, result):
        self._Results__parameters = parameters
        self._Results__result = result

    def getParameters(self):
        """Returns a sequence of parameter values."""
        return self._Results__parameters

    def getResult(self):
        """Returns the result for a given set of parameters."""
        return self._Results__result


def serve(barFeed, strategyParameters, address, port, batchSize=200):
    """Executes a server that will provide bars and strategy parameters for workers to use.

    :param barFeed: The bar feed that each worker will use to backtest the strategy.
    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`.
    :param strategyParameters: The set of parameters to use for backtesting. An iterable object where **each element is a tuple that holds parameter values**.
    :param address: The address to listen for incoming worker connections.
    :type address: string.
    :param port: The port to listen for incoming worker connections.
    :type port: int.
    :param batchSize: The number of strategy executions that are delivered to each worker.
    :type batchSize: int.
    :rtype: A :class:`Results` instance with the best results found or None if no results were obtained.
    """
    paramSource = base.ParameterSource(strategyParameters)
    resultSinc = base.ResultSinc()
    s = xmlrpcserver.Server(paramSource, resultSinc, barFeed, address, port, batchSize=batchSize)
    logger.info('Starting server')
    s.serve()
    logger.info('Server finished')
    ret = None
    bestResult, bestParameters = resultSinc.getBest()
    if bestResult is not None:
        logger.info('Best final result %s with parameters %s' % (bestResult, bestParameters.args))
        ret = Results(bestParameters.args, bestResult)
    else:
        logger.error('No results. All jobs failed or no jobs were processed.')
    return ret