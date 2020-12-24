# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\toolboxes\photbiochem\cie_tn003_2015.py
# Compiled at: 2019-01-25 08:32:14
# Size of source mod 2**32: 9393 bytes
"""
Module for calculating CIE (TN003:2015) photobiological quantities
==================================================================
(Eesc, Eemc, Eelc, Eez, Eer and Esc, Emc, Elc, Ez, Er)

+---------------+----------------+---------------------+---------------------+----------+-------------+
| Photoreceptor |  Photopigment  | Spectral efficiency | Quantity            | Q-symbol | Unit symbol |
|               |  (label, α)    | sα(λ)               | (α-opic irradiance) | (Ee,α)   |             |
+===============+================+=====================+=====================+==========+=============+
|    s-cone     | photopsin (sc) |       cyanolabe     |      cyanopic       |   Ee,sc  |    W.m−2    |
+---------------+----------------+---------------------+---------------------+----------+-------------+
|    m-cone     | photopsin (mc) |       chlorolabe    |      chloropic      |   Ee,mc  |    W.m−2    |
+---------------+----------------+---------------------+---------------------+----------+-------------+
|    l-cone     | photopsin (lc) |       erythrolabe   |      erythropic     |   Ee,lc  |    W.m−2    |
+---------------+----------------+---------------------+---------------------+----------+-------------+
|    ipRGC      | melanopsin (z) |       melanopic     |      melanopic      |   Ee,z   |    W.m−2    |
+---------------+----------------+---------------------+---------------------+----------+-------------+
|    rod        | rhodopsin (r)  |       rhodopic      |      rhodopic       |   Ee,r   |    W.m−2    |
+---------------+----------------+---------------------+---------------------+----------+-------------+

| CIE recommends that the α-opic irradiance is determined by convolving the spectral
| irradiance, Ee,λ(λ) (W⋅m−2), for each wavelength, with the action spectrum, sα(λ), 
| where sα(λ) is normalized to one at its peak:
| 
|    Ee,α = ∫ Ee,λ(λ) sα(λ) dλ 
|
| where the corresponding units are W⋅m−2 in each case. 
| 
| The equivalent luminance is calculated as:
|     
|     E,α = Km ⋅ ∫ Ee,λ(λ) sα(λ) dλ ⋅ ∫ V(λ) dλ / ∫ sα(λ) dλ
| 
| To avoid ambiguity, the weighting function used must be stated, so, for example, 
| cyanopic refers to the cyanopic irradiance weighted using 
| the s-cone or ssc(λ) spectral efficiency function.

 :_PHOTORECEPTORS: ['l-cone', 'm-cone','s-cone', 'rod', 'iprgc']
 :_Ee_SYMBOLS: ['Ee,lc','Ee,mc', 'Ee,sc','Ee,r',  'Ee,z']
 :_E_SYMBOLS: ['E,lc','E,mc', 'E,sc','E,r',  'E,z']
 :_Q_SYMBOLS: ['Q,lc','Q,mc', 'Q,sc','Q,r',  'Q,z']
 :_Ee_UNITS: ['W⋅m−2'] * 5
 :_E_UNITS: ['lux'] * 5
 :_Q_UNITS: ['photons/m2/s'] * 5 
 :_QUANTITIES: | list with actinic types of irradiance, illuminance
               | ['erythropic', 
               |  'chloropic',
               |  'cyanopic',
               |  'rhodopic',
               |  'melanopic'] 
 
 :_ACTIONSPECTRA: ndarray with alpha-actinic action spectra. (stored in file:
                  './data/cie_tn003_2015_SI_action_spectra.dat')

 :spd_to_aopicE(): Calculate alpha-opic irradiance (Ee,α) and equivalent 
                   luminance (Eα) values for the l-cone, m-cone, s-cone, 
                   rod and iprgc (α) photoreceptor cells following 
                   CIE technical note TN 003:2015.
References:
      1. `CIE-TN003:2015 (2015). 
      Report on the first international workshop on 
      circadian and neurophysiological photometry, 2013 
      (Vienna, Austria).
      <http://www.cie.co.at/publications/report-first-international-workshop-circadian-and-neurophysiological-photometry-2013>`_
      (http://files.cie.co.at/785_CIE_TN_003-2015.pdf)

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, _PKG_PATH, _SEP, _CIEOBS, _BB, spd, getdata, getwld, vlbar, spd_to_power, spd_normalize
__all__ = [
 '_PHOTORECEPTORS', '_QUANTITIES', '_ACTIONSPECTRA', 'Km_correction_factor',
 '_Ee_SYMBOLS', '_E_SYMBOLS', '_Q_SYMBOLS',
 '_Ee_UNITS', '_E_UNITS', '_Q_UNITS',
 'spd_to_aopicE']
_PHOTORECEPTORS = [
 'l-cone', 'm-cone', 's-cone', 'rod', 'iprgc']
_Ee_SYMBOLS = ['Ee,lc', 'Ee,mc', 'Ee,sc', 'Ee,r', 'Ee,z']
_E_SYMBOLS = ['E,lc', 'E,mc', 'E,sc', 'E,r', 'E,z']
_Q_SYMBOLS = ['Q,lc', 'Q,mc', 'Q,sc', 'Q,r', 'Q,z']
_Ee_UNITS = ['W⋅m−2', 'W⋅m−2', 'W⋅m−2', 'W⋅m−2', 'W⋅m−2']
_E_UNITS = ['lux', 'lux', 'lux', 'lux', 'lux']
_Q_UNITS = ['photons/m2/s', 'photons/m2/s', 'photons/m2/s', 'photons/m2/s', 'photons/m2/s']
_QUANTITIES = ['erythropic', 'chloropic', 'cyanopic', 'rhodopic', 'melanopic']
_ACTIONSPECTRA = getdata((_PKG_PATH + _SEP + 'toolboxes' + _SEP + 'photbiochem' + _SEP + 'data' + _SEP + 'cie_tn003_2015_SI_action_spectra.dat'), header='infer', kind='np', verbosity=0).T
na = _BB['na']
c = _BB['c']
lambdad = c / (na * 54 * 10000000000000.0) / 1e-09
Km_correction_factor = 1 / (1 - 0.00014329999999995735 * (lambdad - 555))

def spd_to_aopicE(sid, Ee=None, E=None, Q=None, cieobs=_CIEOBS, sid_units='W/m2', out='Eeas,Eas'):
    """
    Calculate alpha-opic irradiance (Ee,α) and equivalent luminance (Eα) values
    for the l-cone, m-cone, s-cone, rod and iprgc (α) photoreceptor cells 
    following CIE technical note TN 003:2015.
    
    Args:
        :sid: 
            | numpy.ndarray with retinal spectral irradiance in :sid_units: 
            | (if 'uW/cm2', sid will be converted to SI units 'W/m2')
        :Ee: 
            | None, optional
            | If not None: normalize :sid: to an irradiance of :Ee:
        :E: 
            | None, optional
            | If not None: normalize :sid: to an illuminance of :E:
            | Note that E is calculate using a Km factor corrected to standard air.
        :Q: 
            | None, optional
            | If not None: nNormalize :sid: to a quantal energy of :Q:
        :cieobs:
            | _CIEOBS or str, optional
            | Type of cmf set to use for photometric units.
        :sid_units:
            | 'W/m2', optional
            | Other option 'uW/m2', input units of :sid:
        :out: 
            | 'Eeas, Eas' or str, optional
            | Determines values to return.
            
    Returns:
        :returns: 
            | (Eeas, Eas) with Eeas and Eas resp. numpy.ndarrays with the 
              α-opic irradiance and equivalent illuminance values 
              of all spectra in :sid: in SI-units. 
         
            | (other choice can be set using :out:)
    """
    outlist = out.split(',')
    if sid_units == 'uW/cm2':
        sid[1:] = sid[1:] / 100
    else:
        if sid_units == 'W/m2':
            pass
        else:
            raise Exception('spd_to_aopicE(): {} unsupported units for SID.'.format(sid_units))
        if Ee is not None:
            sid = spd_normalize(sid, norm_type='ru', norm_f=Ee)
        else:
            if E is not None:
                sid = spd_normalize(sid, norm_type='pusa', norm_f=E)
            else:
                if Q is not None:
                    sid = spd_normalize(sid, norm_type='qu', norm_f=Q)
        if 'Ee' in outlist:
            Ee = spd_to_power(sid, cieobs=cieobs, ptype='ru')
        if 'E' in outlist:
            E = spd_to_power(sid, cieobs=cieobs, ptype='pusa')
        if 'Q' in outlist:
            Q = spd_to_power(sid, cieobs=cieobs, ptype='qu')
        sa = spd(_ACTIONSPECTRA, wl=(sid[0]), interpolation='cmf', norm_type='max')
        dl = getwld(sid[0])
        Eeas = np.dot(sa[1:] * dl, sid[1:].T).T
        Vl, Km = vlbar(cieobs=cieobs, wl_new=(sid[0]), out=2)
        Eas = Km * Km_correction_factor * Eeas * (Vl[1].sum() / sa[1:].sum(axis=1))
        if out == 'Eeas,Eas':
            return (
             Eeas, Eas)
        if out == 'Eeas':
            return Eeas
        if out == 'Eas':
            return Eas
        eval(out)