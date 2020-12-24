# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/pacstr.py
# Compiled at: 2019-06-19 05:13:22
# Size of source mod 2**32: 1590 bytes
"""Simply get the name of defined methods."""
__all__ = 'pacstr'

def pacstr(idpac):
    """Return correspond methods string."""
    if idpac[0] == 1:
        method = 'Mean Vector Length (MVL, Canolty, 2006)'
    else:
        if idpac[0] == 2:
            method = 'Kullback-Leiber Distance (KLD, Tort, 2010)'
        else:
            if idpac[0] == 3:
                method = 'Heights ratio (HR, Lakatos, 2005)'
            else:
                if idpac[0] == 4:
                    method = 'ndPac (Ozkurt, 2012)'
                else:
                    if idpac[0] == 5:
                        method = 'Phase-Synchrony (Cohen, 2008; Penny, 2008)'
                    else:
                        if idpac[0] == 6:
                            method = 'Gaussian Copula PAC'
                        else:
                            raise ValueError('No corresponding pac method.')
    if idpac[1] == 0:
        suro = 'No surrogates'
    else:
        if idpac[1] == 1:
            suro = 'Swap phase/amplitude across trials'
        else:
            if idpac[1] == 2:
                suro = 'Swap amplitude blocks across time'
            else:
                if idpac[1] == 3:
                    suro = 'Time lag'
                else:
                    raise ValueError('No corresponding surrogate method.')
    if idpac[2] == 0:
        norm = 'No normalization'
    else:
        if idpac[2] == 1:
            norm = 'Substract the mean of surrogates'
        else:
            if idpac[2] == 2:
                norm = 'Divide by the mean of surrogates'
            else:
                if idpac[2] == 3:
                    norm = 'Substract then divide by the mean of surrogates'
                else:
                    if idpac[2] == 4:
                        norm = 'Substract the mean and divide by the deviation of the surrogates'
                    else:
                        raise ValueError('No corresponding normalization method.')
    return (
     method, suro, norm)