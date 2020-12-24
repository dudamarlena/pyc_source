# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/util/common.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 979 bytes
""" Obtained from Keras GitHub repository: https://github.com/keras-team/keras/blob/master/keras/backend/common.py

"""
_FLOATX = 'float32'

def floatx():
    """Returns the default float type, as a string.  (e.g. float16, float32, float64).

    Returns:
        String: the current default float type.

    Example:
        >>> inf.floatx()
        'float32'

    """
    global _FLOATX
    return _FLOATX


def set_floatx(floatx):
    """ Sets the default float type.

    Args:
        floatx: String, 'float16', 'float32', or 'float64'.

    Example:
        >>> from keras import backend as K
        >>> inf.floatx()
        'float32'
        >>> inf.set_floatx('float16')
        >>> inf..floatx()
        'float16'

    """
    global _FLOATX
    if floatx not in frozenset({'float32', 'float64', 'float16'}):
        raise ValueError('Unknown floatx type: ' + str(floatx))
    _FLOATX = str(floatx)


def is_float(dtype):
    return dtype == 'float16' or dtype == 'float32' or dtype == 'float64'