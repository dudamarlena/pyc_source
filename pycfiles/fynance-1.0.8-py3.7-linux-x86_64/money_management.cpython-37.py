# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/tools/money_management.py
# Compiled at: 2019-05-24 07:06:05
# Size of source mod 2**32: 2026 bytes
""" Module with function to compute some money management coefficients. """
import numpy as np
from fynance.tools.momentums import ema
__all__ = [
 'iso_vol']

def iso_vol(series, target_vol=0.2, leverage=1.0, period=252, half_life=11):
    """ Make an iso-vol vector to apply to signal vector.

    Parameters
    ----------
    series : np.ndarray[ndim=1, dtype=np.float64]
        Series of price of underlying.
    target_vol : float (default 20 %)
        Volatility to target.
    leverage : float (default 1)
        Max leverage to use.
    period : int (default 250)
        Number of period per year.
    half_life : int (default 11)
        Half-life of exponential moving average used to compute volatility.

    Returns
    -------
    iv : np.ndarray[ndim=1, dtype=np.float64]
        Series of iso-vol coefficient.

    Examples
    --------
    >>> series = np.array([95, 100, 85, 105, 110, 90])
    >>> iso_vol(series, target_vol=0.5, leverage=2, period=12, half_life=3)
    array([1.        , 1.        , 2.        , 1.11289534, 0.88580571,
           1.20664917])

    """
    iv = np.ones([series.size])
    ret2 = np.square(series[:-1] / series[1:] - 1)
    vol = np.sqrt(period * ema(ret2, lags=half_life))
    vol[vol <= 0.0] = 1e-08
    iv[2:] = target_vol / vol[:-1]
    iv[iv > leverage] = leverage
    return iv