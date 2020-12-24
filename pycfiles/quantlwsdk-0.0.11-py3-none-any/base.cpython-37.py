# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\optimizer\base.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 3313 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import threading, six

class Parameters(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class ParameterSource(object):
    __doc__ = '\n    Source for backtesting parameters. This class is thread safe.\n    '

    def __init__(self, params):
        self._ParameterSource__iter = iter(params)
        self._ParameterSource__lock = threading.Lock()

    def getNext(self, count):
        """
        Returns the next parameters to use in a backtest.
        If there are no more parameters to try then an empty list is returned.

        :param count: The max number of parameters to return.
        :type count: int
        :rtype: list of Parameters.
        """
        assert count > 0, 'Invalid number of parameters'
        ret = []
        with self._ParameterSource__lock:
            if self._ParameterSource__iter is not None:
                try:
                    while count > 0:
                        params = six.next(self._ParameterSource__iter)
                        if not isinstance(params, Parameters):
                            params = Parameters(*params)
                        ret.append(params)
                        count -= 1

                except StopIteration:
                    self._ParameterSource__iter = None

        return ret

    def eof(self):
        with self._ParameterSource__lock:
            return self._ParameterSource__iter is None


class ResultSinc(object):
    __doc__ = '\n    Sinc for backtest results. This class is thread safe.\n    '

    def __init__(self):
        self._ResultSinc__lock = threading.Lock()
        self._ResultSinc__bestResult = None
        self._ResultSinc__bestParameters = None

    def push(self, result, parameters):
        """
        Push strategy results obtained by running the strategy with the given parameters.

        :param result: The result obtained by running the strategy with the given parameters.
        :type result: float
        :param parameters: The parameters that yield the given result.
        :type parameters: Parameters
        """
        with self._ResultSinc__lock:
            self.onNewResult(result, parameters)
            if result is not None:
                if self._ResultSinc__bestResult is None or result > self._ResultSinc__bestResult:
                    self._ResultSinc__bestResult = result
                    self._ResultSinc__bestParameters = parameters
                    self.onNewBestResult(result, parameters)

    def getBest(self):
        with self._ResultSinc__lock:
            ret = (
             self._ResultSinc__bestResult, self._ResultSinc__bestParameters)
        return ret

    def onNewResult(self, result, parameters):
        pass

    def onNewBestResult(self, result, parameters):
        pass