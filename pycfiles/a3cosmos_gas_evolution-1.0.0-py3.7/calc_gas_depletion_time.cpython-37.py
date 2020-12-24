# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_gas_depletion_time.py
# Compiled at: 2019-07-23 04:37:53
# Size of source mod 2**32: 7903 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy.table import Table, Column, hstack
from numpy import log10, power as pow
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import apply_cosmology
cosmo = apply_cosmology.cosmo
if sys.version_info.major >= 3:
    long = int
else:

    def calc_gas_depletion_time_Scoville2017(z, lgMstar=10.5, DeltaMS=0.0):
        Ratio_M_molgas_SFR = 3.23 * (1 + z) ** (-1.04) * 10 ** DeltaMS ** (-0.7) * 10 ** (lgMstar - 10.0) ** (-0.01)
        return Ratio_M_molgas_SFR


    def calc_gas_depletion_time_Tacconi2018(z, lgMstar=10.5, DeltaMS=0.0):
        A = 0.09
        B = -0.62
        C = -0.44
        D = 0.09
        E = 0.11
        DeltaRe = 0.0
        log10_Ratio_M_molgas_SFR = A + B * np.log10(1 + z) + C * DeltaMS + D * (lgMstar - 10.7) + E * DeltaRe
        Ratio_M_molgas_SFR = 10 ** log10_Ratio_M_molgas_SFR
        return Ratio_M_molgas_SFR


    def calc_gas_depletion_time_A3COSMOS(z=None, cosmic_age=None, lgMstar=10.5, DeltaMS=0.0):
        popt = [
         -0.5816185208613138, -0.5338752260098323, -0.0038228411346192814, 0.040738011277865915, 0.12494331865991803, 0.05914760529893037]
        a, b, c, d, ak, ck = popt
        if z is None and cosmic_age is None:
            print('Error! Please input either z or cosmic_age')
            sys.exit()
        else:
            if cosmic_age is not None:
                cosmoAge = cosmic_age
            else:
                cosmoAge = cosmo.age(z).value
        log10_Ratio_M_molgas_SFR = (a + ak * (lgMstar - 10.0)) * DeltaMS + b * (lgMstar - 10.0) + (c + ck * (lgMstar - 10.0)) * cosmoAge + d
        Ratio_M_molgas_SFR = 10 ** log10_Ratio_M_molgas_SFR
        return Ratio_M_molgas_SFR


    def func_tauDepl_dzliu_log(pars, a, b, c, d, e):
        deltaGas, DeltaMS, lgMstar, lgSFR, cosmoAge, z = pars
        tauDepl_model_log = a * np.log10(deltaGas) * 0.0 + b * DeltaMS + 10 ** lgSFR * 0.0 + c * np.log10(1 + z) + lgMstar * 0.0 + d * cosmoAge * 0.0 + e
        return tauDepl_model_log


    def func_tauDepl_dzliu(pars, a, b, c, d, e):
        deltaGas, DeltaMS, lgMstar, lgSFR, cosmoAge, z = pars
        tauDepl_model_log = func_tauDepl_dzliu_log((deltaGas, DeltaMS, lgMstar, lgSFR, cosmoAge, z), a, b, c, d, e)
        tauDepl_model = np.power(10, tauDepl_model_log)
        return tauDepl_model


    def func_tauDepl_Tacconi2018_log(pars, a, b, c, d):
        DeltaMS, lgMstar, z = pars
        tauDepl_model_log = a * DeltaMS + b * (lgMstar - 10.7) + c * np.log10(1 + z) + d
        return tauDepl_model_log


    def func_tauDepl_Tacconi2018(pars):
        DeltaMS, lgMstar, z = pars
        tauDepl_model_log = func_tauDepl_Tacconi2018_log((DeltaMS, lgMstar, z), -0.44, 0.09, -0.62, 0.09)
        tauDepl_model = np.power(10, tauDepl_model_log)
        return tauDepl_model


    def func_tauDepl_Scoville2017_log(pars, a, b, c, d):
        DeltaMS, lgMstar, z = pars
        tauDepl_model_log = a * DeltaMS + b * (lgMstar - 10.0) + c * np.log10(1 + z) + d
        return tauDepl_model_log


    def func_tauDepl_Scoville2017(pars):
        DeltaMS, lgMstar, z = pars
        tauDepl_model_log = func_tauDepl_Scoville2017_log((DeltaMS, lgMstar, z), -0.7, -0.01, -1.04, np.log10(3.23))
        tauDepl_model = np.power(10, tauDepl_model_log)
        return tauDepl_model