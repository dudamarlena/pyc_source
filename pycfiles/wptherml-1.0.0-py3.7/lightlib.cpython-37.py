# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wptherml/lightlib.py
# Compiled at: 2019-08-20 10:28:22
# Size of source mod 2**32: 1422 bytes
"""
Created on Thu Oct 11 12:32:14 2018

@author: varnerj

This function passed the following tests:
    Predicted luminous efficiency of 14% for a blackbody at 6,600 K in 
    agreement with http://www.ccri.edu/physics/keefe/light.htm
    
    Wikipedia has tabulated values of various standards for Luminous Efficiency and Luminous Efficacy:
    https://en.wikipedia.org/wiki/Luminous_efficacy

"""
import wptherml.numlib as numlib
import wptherml.datalib as datalib
import numpy as np

def Lum_efficiency(lam, TE):
    upper = np.amax(lam)
    ph = datalib.PhLum(lam)
    num = ph * TE
    numerator = numlib.Integrate(num, lam, 0, upper)
    den = TE
    denominator = numlib.Integrate(den, lam, 0, upper)
    return numerator / denominator


def normalized_power(lam, TE, BB):
    upper = np.amax(lam)
    ph = datalib.PhLum(lam)
    num = ph * TE
    den = ph * BB
    numerator = numlib.Integrate(num, lam, 0, upper)
    denominator = numlib.Integrate(den, lam, 0, upper)
    return numerator / denominator


def Lum_efficacy(lam, TE):
    le = Lum_efficiency(lam, TE)
    efficacy = 683 * le
    return efficacy


def IdealSource(lam, T):
    rho = datalib.BB(lam, T)
    ph = datalib.PhLum(lam)
    TE_ideal = ph * rho
    return TE_ideal