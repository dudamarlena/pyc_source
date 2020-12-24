# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_delta_GD.py
# Compiled at: 2019-10-25 07:26:23
# Size of source mod 2**32: 4682 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy.table import Table, Column, hstack
from copy import copy
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import apply_cosmology
cosmo = apply_cosmology.cosmo
if sys.version_info.major >= 3:
    long = int
else:

    def calc_deltaGD_from_metalZ_following_Leroy2011(metalZ):
        return np.power(10.0, 9.4 - 0.85 * metalZ)


    def calc_deltaGD_from_metalZ_following_Magdis2012(metalZ):
        return np.power(10.0, 10.54 - 0.99 * metalZ)


    def calc_deltaGD_from_metalZ_following_RemyRuyer2014a(metalZ):
        a = 2.21
        aH = 1.0
        b = 0.68
        aL = 3.08
        metaZ = metalZ
        metaZknee = 7.96
        metaZsolar = 8.69
        if not np.isscalar(metaZ):
            maskZ = metaZ > metaZknee
            GDR_ISM = metaZ * 0.0
            GDR_ISM[maskZ] = 10 ** (a + aH * (metaZsolar - metaZ[maskZ]))
            GDR_ISM[~maskZ] = 10 ** (b + aL * (metaZsolar - metaZ[(~maskZ)]))
        else:
            GDR_ISM = 10 ** (a + aH * (metaZsolar - metaZ)) if metaZ > 7.96 else 10 ** (b + aL * (metaZsolar - metaZ))
        return GDR_ISM


    def calc_deltaGD_from_metalZ_following_RemyRuyer2014b(metalZ):
        a = 2.21
        aH = 1.0
        b = 0.96
        aL = 3.1
        metaZ = metalZ
        metaZknee = 8.1
        metaZsolar = 8.69
        if not np.isscalar(metaZ):
            maskZ = metaZ > metaZknee
            GDR_ISM = metaZ * 0.0
            GDR_ISM[maskZ] = 10 ** (a + aH * (metaZsolar - metaZ[maskZ]))
            GDR_ISM[~maskZ] = 10 ** (b + aL * (metaZsolar - metaZ[(~maskZ)]))
        else:
            GDR_ISM = 10 ** (a + aH * (metaZsolar - metaZ)) if metaZ > 7.96 else 10 ** (b + aL * (metaZsolar - metaZ))
        return GDR_ISM


    def calc_deltaGD_from_metalZ_following_Genzel2015(metalZ):
        return calc_deltaGD_from_metalZ_following_Leroy2011(metalZ)