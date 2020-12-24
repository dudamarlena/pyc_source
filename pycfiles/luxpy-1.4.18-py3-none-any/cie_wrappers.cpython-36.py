# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cri\indices\cie_wrappers.py
# Compiled at: 2018-05-03 02:48:26
# Size of source mod 2**32: 3530 bytes
"""
Module with CIE 13.3-1995 Ra and CIE 224-2017 Rf color fidelity indices.
========================================================================
 
 :spd_to_ciera(): the 'ciera' color rendition (fidelity) metric (CIE 13.3-1995)    

 :spd_to_ciera_133_1995 = spd_to_ciera   

 :spd_to_cierf(): the 'cierf' color rendition (fidelity) metric (CIE224-2017). 

 :spd_to_cierf_224_2017 = spd_to_cierf
               
References:
    1. `CIE13.3-1995. Method of Measuring and Specifying 
    Colour Rendering Properties of Light Sources 
    (Vol. CIE13.3-19). Vienna, Austria: CIE. (1995).
    <http://www.cie.co.at/index.php/index.php?i_ca_id=303>`_
                
    2. `CIE224:2017. CIE 2017 Colour Fidelity Index for accurate scientific use. 
    Vienna, Austria: CIE. (2017).
    <http://www.cie.co.at/index.php?i_ca_id=1027>`_

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from ..utils.helpers import spd_to_cri
__all__ = [
 'spd_to_ciera', 'spd_to_cierf',
 'spd_to_ciera_133_1995', 'spd_to_cierf_224_2017']

def spd_to_ciera(SPD, out='Rf', wl=None):
    """
    Wrapper function the 'ciera' color rendition (fidelity) metric 
    (CIE 13.3-1995). 
    
    Args:
        :SPD: 
            | ndarray with spectral data 
              (can be multiple SPDs, first axis are the wavelengths)
        :wl: 
            | None, optional
            | Wavelengths (or [start, end, spacing]) to interpolate :SPD: to. 
            | None: default to no interpolation
        :out: 
            | 'Rf' or str, optional
            | Specifies requested output (e.g. 'Rf,Rfi,cct,duv') 
    
    Returns:
        :returns: 
            | float or ndarray with CIE13.3 Ra for :out: 'Rf'
            | Other output is also possible by changing the :out: str value.
    
    References:
        1. `CIE13.3-1995. Method of Measuring and Specifying 
        Colour Rendering Properties of Light Sources 
        (Vol. CIE13.3-19). Vienna, Austria: CIE. (1995).
        <http://www.cie.co.at/index.php/index.php?i_ca_id=303>`_

    """
    return spd_to_cri(SPD, cri_type='ciera', out=out, wl=wl)


def spd_to_cierf(SPD, out='Rf', wl=None):
    """
    Wrapper function the 'cierf' color rendition (fidelity) metric 
    (CIE224-2017). 
    
    Args:
        :SPD: 
            | ndarray with spectral data (can be multiple SPDs, 
              first axis are the wavelengths)
        :wl: 
            | None, optional
            | Wavelengths (or [start, end, spacing]) to interpolate :SPD: to.
            | None: default to no interpolation
        :out: 
            | 'Rf' or str, optional
            | Specifies requested output (e.g. 'Rf,Rfi,cct,duv') 
    
    Returns:
        :returns: 
            | float or ndarray with CIE224-2017 Rf for :out: 'Rf'
            | Other output is also possible by changing the :out: str value.
    References:
        1. `CIE224:2017. CIE 2017 Colour Fidelity Index for accurate scientific use. 
        Vienna, Austria: CIE. (2017).
        <http://www.cie.co.at/index.php?i_ca_id=1027>`_
    
    """
    return spd_to_cri(SPD, cri_type='cierf', out=out, wl=wl)


spd_to_ciera_133_1995 = spd_to_ciera
spd_to_cierf_224_2017 = spd_to_cierf