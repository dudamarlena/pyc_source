# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/param/utilities.py
# Compiled at: 2020-03-22 18:42:45
# Size of source mod 2**32: 2283 bytes
from numpy.random.mtrand import normal, uniform
from pandas import DataFrame
from astropy.units import Unit, R_jup, R_sun
from numpy import sqrt
from pytransit.utils.eclipses import Teq
from pytransit.orbits import as_from_rhop, i_from_ba, d_from_pkaiews

def derive_qois(data: DataFrame, rstar: tuple=None, teff: tuple=None, distance_unit: Unit=R_jup):
    df = data.copy()
    ns = df.shape[0]
    df['period'] = period = df.p.values if 'p' in df else df.pr.values
    if 'k2_true' in df:
        df['k_true'] = sqrt(df.k2_true)
    if 'k2_app' in df:
        df['k_app'] = sqrt(df.k2_app)
    else:
        if 'k2_true' in df:
            if 'k2_app' in df:
                df['cnt'] = 1.0 - df.k2_app / df.k2_true
        if 'g' in df:
            if 'k' in df:
                df['b'] = df.g * (1 + df.k)
            else:
                if 'k_true' in df:
                    df['b'] = df.g * (1 + df.k_true)
    df['a'] = as_from_rhop(df.rho.values, period)
    df['inc'] = i_from_ba(df.b.values, df.a.values)
    df['t14'] = d_from_pkaiews(period, df.k_true.values, df.a.values, df.inc.values, 0.0, 0.0, 1)
    df['t14_h'] = 24 * df.t14
    if rstar is not None:
        from astropy.units import R_sun
        rstar_d = (normal(*rstar, **{'size': ns}) * R_sun).to(distance_unit).value
        df['r_app'] = df.k_app.values * rstar_d
        df['r_true'] = df.k_true.values * rstar_d
        df['a_au'] = df.a * (rstar_d * distance_unit).to(AU)
    if teff is not None:
        df['teq_p'] = Teq(normal(*teff, **{'size': ns}), df.a, uniform(0.25, 0.5, ns), uniform(0, 0.4, ns))
    return df