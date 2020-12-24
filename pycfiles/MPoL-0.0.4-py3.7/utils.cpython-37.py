# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mpol/utils.py
# Compiled at: 2020-02-03 01:02:18
# Size of source mod 2**32: 1236 bytes
import numpy as np, torch
from mpol.constants import *

def get_Jy_arcsec2(T_b, nu=230000000000.0):
    r"""
    Calculate specific intensity from the brightness temperature, using the Rayleigh-Jeans definition.

    Args:
        T_b : brightness temperature in [:math:`K`]
        nu : frequency (in Hz)

    Returns:
        float: specific intensity (in [:math:`\mathrm{Jy}\, \mathrm{arcsec}^2]`)
    """
    I_nu = T_b * 2 * nu ** 2 * kB / cc ** 2
    Jy_ster = I_nu * 1e+23
    Jy_arcsec2 = Jy_ster * arcsec ** 2
    return Jy_arcsec2


def fftshift(x, axes=None):
    """
    `fftshift <https://docs.scipy.org/doc/numpy/reference/generated/numpy.fft.fftshift.html>`_ the input array along each axis. For even-length arrays, fftshift and ifftshift are equivalent operations. 

    Args:
        x : a torch tensor 
        axes : tuple selecting which axes to shift over. Default is all.

    Returns:
        x : an fftshift-ed tensor
    """
    if axes is None:
        axes = range(0, len(x.size()))
    for dim in axes:
        x = torch.roll(x, (x.size(dim) // 2), dims=dim)

    return x