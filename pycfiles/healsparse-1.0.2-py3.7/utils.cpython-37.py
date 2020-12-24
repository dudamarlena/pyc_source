# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healsparse/utils.py
# Compiled at: 2020-04-09 13:59:38
# Size of source mod 2**32: 3230 bytes
import numpy as np, healpy as hp, warnings, numbers
WIDE_NBIT = 8
WIDE_MASK = np.uint8

def reduce_array(x, reduction='mean', axis=2):
    """
    Auxiliary method to perform one of the following operations:
    nanmean, nanmax, nanmedian, nanmin, nanstd

    Args:
    ----
    x: `ndarray`
        input array in which to perform the operation
    reduction: `str`
        reduction method. Valid options: mean, median, std, max, min
        (default: mean).
    axis: `int`
        axis in which to perform the operation (default: 2)

    Returns:
    --------
    out: `ndarray`.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        if reduction == 'mean':
            ret = np.nanmean(x, axis=2).flatten()
        else:
            if reduction == 'median':
                ret = np.nanmedian(x, axis=2).flatten()
            else:
                if reduction == 'std':
                    ret = np.nanstd(x, axis=2).flatten()
                else:
                    if reduction == 'max':
                        ret = np.nanmax(x, axis=2).flatten()
                    else:
                        if reduction == 'min':
                            ret = np.nanmin(x, axis=2).flatten()
                        else:
                            raise ValueError('Reduction method %s not recognized.' % reduction)
    return ret


def check_sentinel(type, sentinel):
    """
    Check if the sentinel value works for the given dtype.

    Parameters
    ----------
    type: `type`
    sentinel: `int`, `float`, or None

    Returns
    -------
    Default sentinel if input is None.

    Raises
    ------
    ValueError if sentinel is of wrong type
    """
    if issubclass(type, np.floating):
        if sentinel is None:
            return hp.UNSEEN
        if isinstance(sentinel, numbers.Real):
            return sentinel
        raise ValueError('Sentinel not of floating type')
    else:
        if issubclass(type, np.integer):
            if sentinel is None:
                return np.iinfo(type).min
            if is_integer_value(sentinel) and not sentinel < np.iinfo(type).min:
                if sentinel > np.iinfo(type).max:
                    raise ValueError('Sentinel out of range of type')
                return sentinel
                raise ValueError('Sentinel not of integer type')


def is_integer_value(value):
    """
    Check if a value is an integer type

    Parameters
    ----------
    value : 'Object`
       A value of any type

    Returns
    -------
    is_integer : `bool`
       `True` if is a numpy or python integer.  False otherwise.
    """
    if isinstance(value, numbers.Integral):
        return True
    return False


def _get_field_and_bitval(bit):
    """
    Get the associated field and shifted bit value for a wide mask

    Parameters
    ----------
    bit : `int`
       Bit position

    Returns
    -------
    field : `int`
       Field index for the shifted bit
    bitval : `healsparse.WIDE_MASK`
       Shifted bit value in its field
    """
    field = bit // WIDE_NBIT
    bitval = WIDE_MASK(np.left_shift(1, bit - field * WIDE_NBIT))
    return (
     field, bitval)