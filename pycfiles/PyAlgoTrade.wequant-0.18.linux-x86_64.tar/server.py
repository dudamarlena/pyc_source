# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/optimizer/server.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import pyalgotrade.logger
from pyalgotrade.optimizer import base
from pyalgotrade.optimizer import xmlrpcserver
logger = pyalgotrade.logger.getLogger(__name__)

class Results(object):
    """The results of the strategy executions."""

    def __init__(self, parameters, result):
        self.__parameters = parameters
        self.__result = result

    def getParameters(self):
        """Returns a sequence of parameter values."""
        return self.__parameters

    def getResult(self):
        """Returns the result for a given set of parameters."""
        return self.__result


def serve(barFeed, strategyParameters, address, port):
    """Executes a server that will provide bars and strategy parameters for workers to use.

    :param barFeed: The bar feed that each worker will use to backtest the strategy.
    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`.
    :param strategyParameters: The set of parameters to use for backtesting. An iterable object where **each element is a tuple that holds parameter values**.
    :param address: The address to listen for incoming worker connections.
    :type address: string.
    :param port: The port to listen for incoming worker connections.
    :type port: int.
    :rtype: A :class:`Results` instance with the best results found or None if no results were obtained.
    """
    paramSource = base.ParameterSource(strategyParameters)
    resultSinc = base.ResultSinc()
    s = xmlrpcserver.Server(paramSource, resultSinc, barFeed, address, port)
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