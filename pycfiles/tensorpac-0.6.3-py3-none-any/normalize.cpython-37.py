# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/normalize.py
# Compiled at: 2019-02-06 15:52:32
# Size of source mod 2**32: 1295 bytes
"""Normalize PAC by surrogates methods.

This file include the following methods :
- No normalization
- Substraction : substract the mean of surrogates
- Divide : divide by the mean of surrogates
- Substract then divide : substract then divide by the mean of surrogates
- Z-score : substract the mean and divide by the deviation of the
            surrogates
"""
__all__ = 'normalize'

def normalize(pac, s_mean, s_std, idn):
    """List of the normalization methods.

    Use a normalization to normalize the true cfc value by the surrogates.
    Here's the list of the normalization methods :
    - No normalization
    - Substraction : substract the mean of surrogates
    - Divide : divide by the mean of surrogates
    - Substract then divide : substract then divide by the mean of surrogates
    - Z-score : substract the mean and divide by the deviation of the
                surrogates

    The normalized method only return the normalized cfc.
    """
    if idn == 0:
        return pac
    elif idn == 1:
        pac -= s_mean
    else:
        if idn == 2:
            pac /= s_mean
        else:
            if idn == 3:
                pac -= s_mean
                pac /= s_mean
            else:
                if idn == 4:
                    pac -= s_mean
                    pac /= s_std