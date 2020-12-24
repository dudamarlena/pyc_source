# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_fmol.py
# Compiled at: 2019-10-25 06:30:11
# Size of source mod 2**32: 3156 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy.table import Table, Column, hstack
from copy import copy
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.27, Tcmb0=2.725)
if sys.version_info.major >= 3:
    long = int
else:

    def calc_fmol_from_metalZ_following_Krumholz2009(metalZOH):
        metalZ_solar = 8.69
        metalZ_ = 10 ** (metalZOH - metalZ_solar)
        Sigma_total_gas = 30.0
        ksi_KMT09 = 0.77 * (1.0 + 3.1 * np.power(metalZ_, 0.365))
        s_ = np.log(1.0 + 0.6 * ksi_KMT09) / (0.04 * Sigma_total_gas * metalZ_)
        delta_ = 0.0712 * (0.1 * s_ ** (-1) + 0.675) ** (-2.8)
        f_H2_to_total = 1.0 - np.power(1.0 + (0.75 * s_ / (1.0 + delta_)) ** (-5), -0.2)
        return f_H2_to_total


    def calc_fmol_from_metalZ_following_Dave2016(metalZOH):
        metalZ_solar = 8.69
        metalZ_ = 10 ** (metalZOH - metalZ_solar)
        Sigma_total_gas = 30.0
        ksi_KMT09 = 0.77 * (1.0 + 3.1 * np.power(metalZ_, 0.365))
        s_ = np.log(1.0 + 0.6 * ksi_KMT09 + 0.01 * ksi_KMT09 ** 2) / (0.0396 * metalZ_ * Sigma_total_gas)
        f_H2_to_total = 1.0 - 0.75 * s_ / (1.0 + 0.25 * s_)
        return f_H2_to_total


    def calc_fmol_from_metalZ_following_Popping2014(metalZOH, U_MW=None):
        metalZ_solar = 8.69
        if U_MW is None:
            U_MW = 10 ** (5.0 * (metalZOH - metalZ_solar))
            U_MW[U_MW < 1.0] = 1.0
        if np.isscalar(U_MW):
            U_MW = np.array([U_MW] * len(metalZOH))
        D_MW = 10 ** (metalZOH - metalZ_solar)
        D_star = 0.0015 * np.log(1.0 + np.power(3.0 * U_MW, 1.7))
        alpha_ = 5.0 * (U_MW / 2.0) / (1.0 + (U_MW / 2.0) ** 2)
        s_ = 0.04 / (D_star + D_MW)
        g_ = (1.0 + alpha_ * s_ + s_ ** 2) / (1.0 + s_)
        Gamma_ = np.log(1.0 + g_ * np.power(D_MW, 0.42857142857142855) * np.power(U_MW / 15.0, 0.5714285714285714))
        Sigma_tide = 20.0 * np.power(Gamma_, 0.5714285714285714) / D_MW / np.sqrt(1.0 + U_MW * D_MW ** 2)
        Sigma_total_gas_r = 10.0
        f_H2_r = (1.0 + Sigma_tide / Sigma_total_gas_r) ** (-2)
        f_H2_to_total = f_H2_r
        print('-----')
        for i in range(len(f_H2_to_total)):
            print('metalZ 12+log10(O/H) %0.3f, f_H2_to_total %0.6f, D_star %0.6f, D_MW %0.6f, U_MW %0.6f' % (metalZOH[i], f_H2_to_total[i], D_star[i], D_MW[i], U_MW[i]))

        return f_H2_to_total