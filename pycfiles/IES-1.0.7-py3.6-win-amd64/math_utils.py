# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\math_utils.py
# Compiled at: 2018-01-14 22:14:26
# Size of source mod 2**32: 2446 bytes
from decimal import Decimal
import math
from numpy import isnan

def tolerant_equals(a, b, atol=1e-06, rtol=1e-06, equal_nan=False):
    """Check if a and b are equal with some tolerance.

    Parameters
    ----------
    a, b : float
        The floats to check for equality.
    atol : float, optional
        The absolute tolerance.
    rtol : float, optional
        The relative tolerance.
    equal_nan : bool, optional
        Should NaN compare equal?

    See Also
    --------
    numpy.isclose

    Notes
    -----
    This function is just a scalar version of numpy.isclose for performance.
    See the docstring of ``isclose`` for more information about ``atol`` and
    ``rtol``.
    """
    if equal_nan:
        if isnan(a):
            if isnan(b):
                return True
    return math.fabs(a - b) <= atol + rtol * math.fabs(b)


try:
    import bottleneck as bn
    nanmean = bn.nanmean
    nanstd = bn.nanstd
    nansum = bn.nansum
    nanmax = bn.nanmax
    nanmin = bn.nanmin
    nanargmax = bn.nanargmax
    nanargmin = bn.nanargmin
except ImportError:
    import numpy as np
    nanmean = np.nanmean
    nanstd = np.nanstd
    nansum = np.nansum
    nanmax = np.nanmax
    nanmin = np.nanmin
    nanargmax = np.nanargmax
    nanargmin = np.nanargmin

def round_if_near_integer(a, epsilon=0.0001):
    """
    Round a to the nearest integer if that integer is within an epsilon
    of a.
    """
    if abs(a - round(a)) <= epsilon:
        return round(a)
    else:
        return a


def number_of_decimal_places(n):
    """
    Compute the number of decimal places in a number.

    Examples
    --------
    >>> number_of_decimal_places(1)
    0
    >>> number_of_decimal_places(3.14)
    2
    >>> number_of_decimal_places('3.14')
    2
    """
    decimal = Decimal(str(n))
    return -decimal.as_tuple().exponent