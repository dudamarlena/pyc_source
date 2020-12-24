# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\toolboxes\photbiochem\ASNZS_1680_2_5_1997_COI.py
# Compiled at: 2019-01-25 08:33:02
# Size of source mod 2**32: 5086 bytes
"""
Module for calculation of cyanosis index (AS/NZS 1680.2.5:1997)
===============================================================
 
 :_COI_OBS: Default CMF set for calculations
 :_COI_CSPACE: Default color space (CIELAB)
 :_COI_RFL_BLOOD: ndarray with reflectance spectra of 100% and 50% 
                   oxygenated blood
 :spd_to_COI_ASNZS1680: Calculate the Cyanosis Observartion Index (COI) 
                        [ASNZS 1680.2.5-1995] 

Reference:
    AS/NZS1680.2.5 (1997). INTERIOR LIGHTING PART 2.5: HOSPITAL AND MEDICAL TASKS.

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, deltaE, _PKG_PATH, _SEP, _CIE_ILLUMINANTS, getdata, spd_to_xyz, blackbody, xyz_to_cct
__all__ = [
 '_COI_RFL_BLOOD', '_COI_CIEOBS', '_COI_CSPACE', 'spd_to_COI_ASNZS1680']
_COI_RFL_BLOOD = getdata((_PKG_PATH + _SEP + 'toolboxes' + _SEP + 'photbiochem' + _SEP + 'data' + _SEP + 'ASNZS_1680.2.5_1997_cyanosisindex_100_50.dat'), header=None, kind='np', verbosity=0).T
_COI_CIEOBS = '1931_2'
_COI_CSPACE = 'lab'
_COI_REF = blackbody(4000)

def spd_to_COI_ASNZS1680(S=None, tf=_COI_CSPACE, cieobs=_COI_CIEOBS, out='COI,cct', extrapolate_rfl=False):
    """
    Calculate the Cyanosis Observation Index (COI) [ASNZS 1680.2.5-1995].
    
    Args:
        :S:
            | ndarray with light source spectrum (first column are wavelengths).
        :tf:
            | _COI_CSPACE, optional
            | Color space in which to calculate the COI.
            | Default is CIELAB.
        :cieobs: 
            | _COI_CIEOBS, optional
            | CMF set to use. 
            | Default is '1931_2'.
        :out: 
            | 'COI,cct' or str, optional
            | Determines output.
        :extrapolate_rfl:
            | False, optional
            | If False: 
            |  limit the wavelength range of the source to that of the standard
            |  reflectance spectra for the 50% and 100% oxygenated blood.
            
    Returns:
        :COI:
            | ndarray with cyanosis indices for input sources.
        :cct:
            | ndarray with correlated color temperatures.
            
    Note:
        Clause 7.2 of the ASNZS 1680.2.5-1995. standard mentions the properties
        demanded of the light source used in region where visual conditions 
        suitable to the detection of cyanosis should be provided:
        
            1. The correlated color temperature (CCT) of the source should be from 
            3300 to 5300 K.
                
            2. The cyanosis observation index should not exceed 3.3

    """
    if S is None:
        S = _CIE_ILLUMINANTS['F4']
    else:
        if extrapolate_rfl == False:
            wl_min = _COI_RFL_BLOOD[0].min()
            wl_max = _COI_RFL_BLOOD[0].max()
            S = S[:, np.where((S[0] >= wl_min) & (S[0] <= wl_max))[0]]
        Sr = blackbody(4000, wl3=(S[0]))
        xyzt, xyzwt = spd_to_xyz(S, rfl=_COI_RFL_BLOOD, relative=True, cieobs=cieobs, out=2)
        xyzr, xyzwr = spd_to_xyz(Sr, rfl=_COI_RFL_BLOOD, relative=True, cieobs=cieobs, out=2)
        DEi = deltaE.DE_cspace(xyzt, xyzr, xyzwt=xyzwt, xyzwr=xyzwr, tf=tf)
        COI = np.nanmean(DEi, axis=0)[:, None]
        if 'cct' in out.split(','):
            cct, duv = xyz_to_cct(xyzwt, cieobs=cieobs, out=2)
    if out == 'COI':
        return COI
    else:
        if out == 'COI,cct':
            return (
             COI, cct)
        return eval(out)


if __name__ == '__main__':
    S = np.vstack((_CIE_ILLUMINANTS['A'], _CIE_ILLUMINANTS['F4'][1:], _CIE_ILLUMINANTS['F5'][1:]))
    coi, cct = spd_to_COI_ASNZS1680(S, extrapolate_rfl=True)