# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/dev/series.py
# Compiled at: 2019-05-23 12:20:00
# Size of source mod 2**32: 7722 bytes
import numpy as np

class TimeSeries:
    __doc__ = ' TimeSeries is a 1 dimensional array of floating numbers.\n\n    Attributes\n    ----------\n    series : np.ndarray[ndim=1, dtype=np.float64]\n        The series of values.\n    time_index : np.ndarray[ndim, dtype=int or str or datetime]\n        Time index of series.\n    T : int\n        Size of the `series`.\n\n    Methods\n    -------\n\n    '

    def __init__(self, series, index=None, kind_returns='raw', signal=None):
        """ """
        self.series = np.asarray(series).flatten()
        self.T = self.series.size
        if index is None:
            self.index = range(len(series))
        else:
            self.index = index


class FySeries(TimeSeries):
    __doc__ = " FySeries is a 1 dimensional array of floating number. It's can be a\n    series of prices of an asset or index values or performances.\n\n    Attributes\n    ----------\n    series : np.ndarray[ndim=1, dtype=np.float64]\n        The series of values.\n    time_index : np.ndarray[ndim=1, dtype=int or str or datetime]\n        Time index of the series.\n    returns : np.ndarray[ndim=1, dtype=np.float64]\n        Returns of the series.\n    T : int\n        Size of the `series`.\n    kind_returns : str\n        Design the method to compute returns: 'raw' is the first difference,\n        'log' is logarithmic returns and 'perc' is returns in percentage.\n\n    Methods\n    -------\n\n    "

    def __init__(self, series, index=None, kind_returns='raw'):
        """ """
        self.series = np.asarray(series, dtype=(np.float64)).flatten()
        self.T = self.series.size
        if index is None:
            self.index = np.arange((len(series)), dtype=int)
        else:
            self.index = index
        self.kind_returns = kind_returns
        self.returns = _comp_returns(series, kind_returns=kind_returns)

    def __get__(self, i_0, i_T, i=1):
        return self.series[i_0:i_T:i]

    def get_ret(self, i_0):
        pass


class StratSeries(FySeries):
    __doc__ = " StratSeries is a 1 dimensional array of floating number. performances\n    or index values of a financial strategy.\n\n    Attributes\n    ----------\n    series : np.ndarray[ndim=1, dtype=np.float64]\n        The series of values.\n    time_index : np.ndarray[ndim=1, dtype=int or str or datetime]\n        Time index of the series.\n    returns : np.ndarray[ndim=1, dtype=np.float64]\n        Returns of the series.\n    signal : np.ndarray[ndim=1, dtype=np.float64]\n        Signal of strategy.\n    T : int\n        Size of the `series`.\n    kind_returns : str\n        Design the method to compute returns: 'raw' is the first difference,\n        'log' is logarithmic returns and 'perc' is returns in percentage.\n\n    Methods\n    -------\n\n    "

    def __init__(self, series, index=None, kind_returns='raw', signal=None):
        """ """
        self.series = np.asarray(series).flatten()
        self.T = self.series.size
        if index is None:
            self.index = range(len(series))
        else:
            self.index = index
        self.kind_returns = kind_returns
        self.returns = _comp_returns(series, kind_returns=kind_returns)
        if signal is None:
            self.signal = np.ones([])


def _comp_returns(series, kind_returns='raw'):
    returns = np.zeros([len(series)])
    if kind_returns == 'raw':
        returns[1:] = series[1:] - series[:-1]
    else:
        if kind_returns == 'log':
            returns[1:] = np.log(series[1:] / series[:-1])
        else:
            if kind_returns == 'perc':
                returns[1:] = series[1:] / series[:-1] - 1
            else:
                raise ValueError(str(kind_returns) + ' not allowed.')
    return returns


def comp_returns(series, kind_returns='raw'):
    """ Compute returns for one period of series of prices or performances or
    index values.

    Parameters
    ----------
    series: np.ndarray[ndim=1, dtype=np.float64]
        Time-series of prices, performances or index values.
    kind_returns : str, optional
        Kind of returns TODO : available parameters.

    Returns
    -------
    out : np.ndarray[ndim=1, dtype=np.float64]
        Time-series of returns for one period.

    Examples
    --------
    TODO

    See Also
    --------
    TODO

    """
    if (series[:-1] <= 0).any():
        if kind_returns != 'raw':
            description_error = 'Series containing null or negative numbers not '
            description_error += 'allowed with log and percentage kind of returns.'
            raise ValueError(description_error)
    return _comp_returns(series, kind_returns=kind_returns)


class farray:
    __doc__ = ' This object is a financial array.\n\n    Attributes\n    ----------\n    series : np.ndarray[ndim=1, dtype=np.float64]\n        A time-series of prices, performances or index values.\n    returns : np.array[ndim=1, dtype=np.float64]\n        A time-series of returns on one period of `series`.\n\n    Methods\n    -------\n    __getitem__ : Return a slice of `series` or `returns`.\n    __repr__ : Display series and returns.\n\n    '

    def __init__(self, series):
        """ Set a financial array.

        Parameters
        ----------
        series : np.ndarray[ndim=1, dtype=np.float64]
            A time-series of prices, performances or index values.

        """
        self.series = np.asarray(series, dtype=(np.float64))
        self.returns = np.zeros(series.shape)
        self.returns[1:] = series[1:] - series[:-1]

    def __getitem__(self, keys):
        """ Return a slice of `series` or `returns`.

        Parameters
        ----------
        keys : int, slice, or tuple of int, slice or str
            If int or slice return the corresponding part of `series`. If
            tuple first parameters must be slice or int, and last one must
            be a string.

        Returns
        -------
        out : np.ndarray[ndim=1, dtype=np.float64]
            `series` or `returns`

        Examples
        --------
        >>> a = farray([100, 80, 120, 150, 120, 130])
        >>> a[:]
        array([100., 80., 120., 150., 120., 130.])
        >>> a[:, 'ret']
        array([0., -20., 40., 30., -30., 10.])
        >>> a
        Series:
        array([100., 80., 120., 150., 120., 130.])
        Returns:
        array([0., -20., 40., 30., -30., 10.])

        """
        if isinstance(keys, slice) or isinstance(keys, int):
            return self.series[keys]
        if isinstance(keys, tuple):
            if keys[(-1)] == 'ret':
                return self.returns[keys[:-1]]
            raise ValueError(str(kind) + ' not allowed')
        else:
            raise IndexError(str(type(keys)) + ' type not allowed')

    def __repr__(self):
        """ Display series and returns.

        Returns
        -------
        out : str
            Values of `series` and `returns`.

        """
        txt = 'Series:\n'
        txt += str(self.series)
        txt += '\nReturns:\n'
        txt += str(self.returns)
        return txt