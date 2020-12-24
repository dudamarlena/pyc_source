# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_cosmic_star_formation_rate_density.py
# Compiled at: 2019-10-24 23:33:00
# Size of source mod 2**32: 2282 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy.table import Table, Column, hstack
from copy import copy
from numpy import log10, power as pow
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=73, Om0=0.27, Tcmb0=2.725)
if sys.version_info.major >= 3:
    long = int
else:

    def convert_age_to_z(cosmoAge):
        if type(cosmoAge) is list:
            cosmoAge = np.array(cosmoAge)
        spl_opz_log10 = np.linspace((np.log10(1.0)), (np.log10(10000.0)), num=1000, endpoint=True)
        spl_z = 10 ** spl_opz_log10 - 1.0
        spl_cosmoAge = cosmo.age(spl_z).value
        spl_cosmoAge_log10 = np.log10(spl_cosmoAge)
        spl_cosmoAge_log10 = spl_cosmoAge_log10[::-1]
        spl_opz_log10 = spl_opz_log10[::-1]
        tmp_opz_log10 = np.interp(np.log10(cosmoAge), spl_cosmoAge_log10, spl_opz_log10)
        z = 10 ** tmp_opz_log10 - 1.0
        return z


    def calc_cosmic_star_formation_rate_density_MadauDickinson2014(z):
        rho_SFR = 0.015 * (1 + z) ** 2.7 / (1.0 + ((1 + z) / 2.9) ** 5.6) / 1.64
        return rho_SFR


    def calc_CSFRD_Madau2014(z):
        return calc_cosmic_star_formation_rate_density_MadauDickinson2014(z)


    def calc_cosmic_star_formation_rate_density_Liu2018(z, shape='double-powerlaw'):
        if shape.startswith('double'):
            rho_SFR = 0.00587 * (1 + z) ** 3.0 / (1.0 + ((1 + z) / 2.9) ** 5.6)
        else:
            if shape.startswith('log'):
                A0 = 0.575
                tau = 0.66
                T0 = 1.5
                t = cosmo.age(z).value
                rho_SFR = A0 / (t * np.sqrt(2.0 * np.pi * tau ** 2)) * np.exp(-(np.log(t) - T0) ** 2 / (2.0 * tau ** 2))
            else:
                raise ValueError('Error! The input shape %s is not allowed by the called function calc_cosmic_star_formation_rate_density_Liu2018()!' % shape)
        return rho_SFR


    def calc_CSFRD_Liu2018(z, shape='double-powerlaw'):
        return calc_cosmic_star_formation_rate_density_Liu2018(z, shape=shape)