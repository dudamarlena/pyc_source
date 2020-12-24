# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/optimizer/server.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
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