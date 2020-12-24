# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/astrocalc/__init__.py
# Compiled at: 2020-05-02 07:37:04
from __future__ import division
from . import cl_utils
from past.utils import old_div

def luminosity_to_flux(lumErg_S, dist_Mpc):
    """
    *Convert luminosity to a flux*

    **Key Arguments**

    - ``lumErg_S`` -- luminosity in ergs/sec
    - ``dist_Mpc`` -- distance in Mpc

    **Return**

    - ``fluxErg_cm2_S`` -- flux in ergs/cm2/s

    """
    import numpy as np, math
    distCm = dist_Mpc * MPC_2_CMS
    fluxErg_cm2_S = old_div(lumErg_S, 4 * np.pi * distCm ** 2)
    return fluxErg_cm2_S


if __name__ == '__main__':
    main()