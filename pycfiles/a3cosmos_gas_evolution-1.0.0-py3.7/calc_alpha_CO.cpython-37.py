# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_alpha_CO.py
# Compiled at: 2019-07-18 22:30:15
# Size of source mod 2**32: 5123 bytes
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

    def calc_alphaCO_from_metalZ_following_Wilson1995(metalZ):
        metalZ_solar_old = 8.88
        metalZ_solar_new = 8.69
        XCO_Galactic = 3e+20
        alphaCO_Galactic = 6.449999999999999
        return np.power(10.0, 5.95 - 0.67 * (metalZ - metalZ_solar_new + metalZ_solar_old)) * alphaCO_Galactic


    def calc_alphaCO_from_metalZ_following_Magdis2012(metalZ):
        return np.power(10.0, 12.8 - 1.39 * metalZ)


    def calc_alphaCO_from_metalZ_following_Genzel2012(metalZ):
        return np.power(10.0, 12.0 - 1.3 * metalZ)


    def calc_alphaCO_from_metalZ_following_Genzel2015a(metalZ, metalZ_solar=8.67, alphaCO_MilkyWay=4.36):
        return 0.67 * np.exp(0.36 * np.power(10.0, -(metalZ - metalZ_solar))) * alphaCO_MilkyWay


    def calc_alphaCO_from_metalZ_following_Genzel2015b(metalZ, metalZ_solar=8.67, alphaCO_MilkyWay=4.36):
        return np.power(10.0, -1.27 * (metalZ - metalZ_solar)) * alphaCO_MilkyWay


    def calc_alphaCO_from_metalZ_following_Genzel2015(metalZ, metalZ_solar=8.67, alphaCO_MilkyWay=4.36):
        return calc_alphaCO_from_metalZ_following_Genzel2015a(metalZ, metalZ_solar=metalZ_solar, alphaCO_MilkyWay=alphaCO_MilkyWay)


    def calc_alphaCO_from_metalZ_following_Bolatto2013(metalZ, Sigma_total, Sigma_GMC_100=1.0, metalZ_solar=8.67, alphaCO_MilkyWay=4.36):
        if np.isscalar(Sigma_total):
            if Sigma_total >= 100.0:
                t_gamma = 0.5
            else:
                t_gamma = 0.0
        else:
            t_gamma = np.array(Sigma_total) * 0.0
            t_gamma[Sigma_total >= 100.0] = 0.5
        return 2.9 * np.exp(0.4 / (np.power(10.0, metalZ - metalZ_solar) * Sigma_GMC_100)) * np.power(Sigma_total / 100.0, -t_gamma)


    def calc_alphaCO_from_metalZ_following_Accurso2017(metalZ, DeltaMS=0.0):
        return np.power(10.0, 14.752 - 1.623 * metalZ + 0.062 * DeltaMS)


    def calc_alphaCO_from_metalZ_following_Bertemes2018(metalZ):
        alphaCO_G12 = np.power(10.0, -1.27 * (metalZ - 8.67))
        alphaCO_B13 = 0.67 * np.exp(0.36 * -(metalZ - 8.67))
        alphaCO_MW = 3.2
        alphaCO_combined = alphaCO_MW * np.sqrt(alphaCO_G12 * alphaCO_B13) * 1.36
        return alphaCO_combined


    def calc_alphaCO_from_metalZ_following_Tacconi2018(metalZ):
        alphaCO_G12 = np.power(10.0, -1.27 * (metalZ - 8.67))
        alphaCO_B13 = 0.67 * np.exp(0.36 * -(metalZ - 8.67))
        alphaCO_MW = 4.36
        alphaCO_combined = alphaCO_MW * np.sqrt(alphaCO_G12 * alphaCO_B13)
        return alphaCO_combined


    def calc_alphaCO_from_metalZ_following_Boselli2014(lgL_Hband):
        X_CO = np.power(10.0, -0.38 * lgL_Hband + 24.23)
        alphaCO = X_CO / 2e+20 * 4.3
        return alphaCO