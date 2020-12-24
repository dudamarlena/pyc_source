# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_gas_fraction.py
# Compiled at: 2019-08-28 23:59:32
# Size of source mod 2**32: 11334 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, copy, numpy as np
from astropy.table import Table, Column, hstack
from numpy import log10, power as pow
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import apply_cosmology
cosmo = apply_cosmology.cosmo
if sys.version_info.major >= 3:
    long = int
else:

    def calc_gas_fraction_Scoville2017(z, lgMstar=10.5, DeltaMS=0.0):
        Ratio_M_molgas_M_star = 0.71 * (1 + z) ** 1.84 * 10 ** DeltaMS ** 0.32 * 10 ** (lgMstar - 10.0) ** (-0.7)
        return Ratio_M_molgas_M_star


    def calc_gas_fraction_Tacconi2018_beta_2(z, lgMstar=10.5, DeltaMS=0.0):
        A = 0.12
        B = -3.62
        F = 0.66
        beta = 2.0
        C = 0.53
        D = -0.35
        E = 0.11
        DeltaRe = 0.0
        log10_Ratio_M_molgas_M_star = A + B * (np.log10(1 + z) - F) ** beta + C * DeltaMS + D * (lgMstar - 10.7) + E * DeltaRe
        Ratio_M_molgas_M_star = 10 ** log10_Ratio_M_molgas_M_star
        return Ratio_M_molgas_M_star


    def calc_gas_fraction_Tacconi2018(z, lgMstar=10.5, DeltaMS=0.0):
        return calc_gas_fraction_Tacconi2018_beta_2(z, lgMstar, DeltaMS)


    def calc_gas_fraction_A3COSMOS(cosmic_age=None, z=None, lgMstar=10.5, DeltaMS=0.0):
        popt = [
         0.4195381171312362, -0.6906526862112656, -0.1542557899746253, 0.9339052286147904, 0.11949845461785102, 0.03204158046196248]
        a, b, c, d, ak, ck = popt
        if z is None and cosmic_age is None:
            print('Error! Please input either z or cosmic_age')
            sys.exit()
        else:
            if cosmic_age is not None:
                cosmoAge = cosmic_age
            else:
                cosmoAge = cosmo.age(z).value
        log10_Ratio_M_molgas_M_star = (a + ak * (lgMstar - 10.0)) * DeltaMS + b * (lgMstar - 10.0) + (c + ck * (lgMstar - 10.0)) * cosmoAge + d
        Ratio_M_molgas_M_star = 10 ** log10_Ratio_M_molgas_M_star
        return Ratio_M_molgas_M_star


    def calc_gas_fraction_A3COSMOS_with_Leslie2019_MS(cosmic_age=None, z=None, lgMstar=10.5, DeltaMS=0.0):
        popt = [
         0.3781725710882265, -0.8360054443744662, -0.1557707273000366, 1.0923711580061433, 0.09940673198827188, 0.03940816266321434]
        a, b, c, d, ak, ck = popt
        if z is None and cosmic_age is None:
            print('Error! Please input either z or cosmic_age')
            sys.exit()
        else:
            if cosmic_age is not None:
                cosmoAge = cosmic_age
            else:
                cosmoAge = cosmo.age(z).value
        log10_Ratio_M_molgas_M_star = (a + ak * (lgMstar - 10.0)) * DeltaMS + b * (lgMstar - 10.0) + (c + ck * (lgMstar - 10.0)) * cosmoAge + d
        Ratio_M_molgas_M_star = 10 ** log10_Ratio_M_molgas_M_star
        return Ratio_M_molgas_M_star


    def calc_gas_fraction_A3COSMOS_with_Scoville2017_MS(cosmic_age=None, z=None, lgMstar=10.5, DeltaMS=0.0):
        popt = [
         0.42803584038283427, -1.0941775869942276, -0.168209612312487, 1.207999567254241, 0.08377200755981207, 0.06373985587594078]
        a, b, c, d, ak, ck = popt
        if z is None and cosmic_age is None:
            print('Error! Please input either z or cosmic_age')
            sys.exit()
        else:
            if cosmic_age is not None:
                cosmoAge = cosmic_age
            else:
                cosmoAge = cosmo.age(z).value
        log10_Ratio_M_molgas_M_star = (a + ak * (lgMstar - 10.0)) * DeltaMS + b * (lgMstar - 10.0) + (c + ck * (lgMstar - 10.0)) * cosmoAge + d
        Ratio_M_molgas_M_star = 10 ** log10_Ratio_M_molgas_M_star
        return Ratio_M_molgas_M_star


    def func_deltaGas_dzliu_log(pars, a, b, c, d, e):
        if type(pars) is dict:
            for t in ('tauDepl', 'DeltaMS', 'lgMstar', 'lgSFR', 'cosmoAge', 'z'):
                if t in pars:
                    locals()[t] = copy.copy(pars[t])

        else:
            tauDepl, DeltaMS, lgMstar, lgSFR, cosmoAge, z = pars
        deltaGas_model_log = np.log10(tauDepl) * 0.0 + a * DeltaMS + (lgSFR - 2.0) * 0.0 + (b + c * cosmoAge) * (lgMstar - 10.0) + d * cosmoAge + e
        return deltaGas_model_log


    def func_deltaGas_dzliu(pars, a, b, c, d, e):
        if type(pars) is dict:
            deltaGas_model_log = func_deltaGas_dzliu_log(pars, a, b, c, d, e)
        else:
            tauDepl, DeltaMS, lgMstar, lgSFR, cosmoAge, z = pars
            deltaGas_model_log = func_deltaGas_dzliu_log((tauDepl, DeltaMS, lgMstar, lgSFR, cosmoAge, z), a, b, c, d, e)
        deltaGas_model = numpy.power(10, deltaGas_model_log)
        return deltaGas_model


    def func_deltaGas_Tacconi2018_log(pars, a, b, c, d):
        DeltaMS, lgMstar, z = pars
        deltaGas_model_log = a * DeltaMS + b * (lgMstar - 10.7) + c * (numpy.log10(1 + z) - 0.66) ** 2 + d
        return deltaGas_model_log


    def func_deltaGas_Tacconi2018(pars):
        DeltaMS, lgMstar, z = pars
        deltaGas_model_log = func_deltaGas_Tacconi2018_log((DeltaMS, lgMstar, z), 0.53, -0.35, -3.62, 0.12)
        deltaGas_model = numpy.power(10, deltaGas_model_log)
        return deltaGas_model


    def func_deltaGas_Scoville2017_log(pars, a, b, c, d):
        DeltaMS, lgMstar, z = pars
        deltaGas_model_log = a * DeltaMS + b * (lgMstar - 10.0) + c * numpy.log10(1 + z) + d
        return deltaGas_model_log


    def func_deltaGas_Scoville2017(pars):
        DeltaMS, lgMstar, z = pars
        deltaGas_model_log = func_deltaGas_Scoville2017_log((DeltaMS, lgMstar, z), 0.32, -0.7, 1.84, numpy.log10(0.71))
        deltaGas_model = numpy.power(10, deltaGas_model_log)
        return deltaGas_model