# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cri\indices\cri2012.py
# Compiled at: 2018-05-03 02:48:37
# Size of source mod 2**32: 6239 bytes
"""
Module with CRI2012 color fidelity index.
=========================================
    
 :spd_to_cri2012(): the 'cri2012' color rendition (fidelity) metric
                    with the spectally uniform HL17 mathematical sampleset. 
                    
 :spd_to_cri2012_hl17(): the 'cri2012' color rendition (fidelity) metric
                    with the spectally uniform HL17 mathematical sampleset.  
                    
 :spd_to_cri2012_hl1000(): the 'cri2012' color rendition (fidelity) metric
                           with the spectally uniform HL1000 sampleset. 
                    
 :spd_to_cri2012(): the 'cri2012' color rendition (fidelity) metric
                    with the Real-210 sampleset. 
                    (normally for special color rendering indices)
                    
Reference:
    1. `Smet, K., Schanda, J., Whitehead, L., & Luo, R. (2013). 
    CRI2012: A proposal for updating the CIE colour rendering index. 
    Lighting Research and Technology, 45, 689–709. 
    <http://lrt.sagepub.com/content/45/6/689>`_                    

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from ..utils.helpers import spd_to_cri
__all__ = [
 'spd_to_cri2012', 'spd_to_cri2012_hl17', 'spd_to_cri2012_hl1000', 'spd_to_cri2012_real210']

def spd_to_cri2012(SPD, out='Rf', wl=None):
    """
    Wrapper function for the 'cri2012' color rendition (fidelity) metric
    with the spectally uniform HL17 mathematical sampleset.

    Args:
        :SPD: 
            | ndarray with spectral data (can be multiple SPDs, 
              first axis are the wavelengths)
        :wl: 
            | None, optional
            | Wavelengths (or [start, end, spacing]) to interpolate the SPDs to. 
            | None: default to no interpolation
        :out:
            | 'Rf' or str, optional
            | Specifies requested output (e.g. 'Rf,Rfi,cct,duv') 
    
    Returns:
        :returns:
            | float or ndarray with CRI2012 Rf for :out: 'Rf'
            | Other output is also possible by changing the :out: str value.
            
    References:
        ..[1] Smet, K., Schanda, J., Whitehead, L., & Luo, R. (2013). 
            CRI2012: A proposal for updating the CIE colour rendering index. 
            Lighting Research and Technology, 45, 689–709. 
            Retrieved from http://lrt.sagepub.com/content/45/6/689
    """
    return spd_to_cri(SPD, cri_type='cri2012', out=out, wl=wl)


def spd_to_cri2012_hl17(SPD, out='Rf', wl=None):
    """
    Wrapper function for the 'cri2012' color rendition (fidelity) metric
    with the spectally uniform HL17 mathematical sampleset.
    
    Args:
        :SPD: ndarray with spectral data (can be multiple SPDs, 
              first axis are the wavelengths)
        :wl: None, optional
            Wavelengths (or [start, end, spacing]) to interpolate the SPDs to. 
            None: default to no interpolation
        :out:  'Rf' or str, optional
            Specifies requested output (e.g. 'Rf,Rfi,cct,duv') 
    
    Returns:
        :returns: float or ndarray with CRI2012 Rf for :out: 'Rf'
            Other output is also possible by changing the :out: str value.
    
    Reference:
        1. `Smet, K., Schanda, J., Whitehead, L., & Luo, R. (2013). 
        CRI2012: A proposal for updating the CIE colour rendering index. 
        Lighting Research and Technology, 45, 689–709. 
        <http://lrt.sagepub.com/content/45/6/689>`_
    """
    return spd_to_cri(SPD, cri_type='cri2012-hl17', out=out, wl=wl)


def spd_to_cri2012_hl1000(SPD, out='Rf', wl=None):
    """
    Wrapper function for the 'cri2012' color rendition (fidelity) metric
    with the spectally uniform Hybrid HL1000 sampleset.
    
    Args:
        :SPD: ndarray with spectral data (can be multiple SPDs, 
              first axis are the wavelengths)
        :wl: None, optional
            Wavelengths (or [start, end, spacing]) to interpolate the SPDs to. 
            None: default to no interpolation
        :out:  'Rf' or str, optional
            Specifies requested output (e.g. 'Rf,Rfi,cct,duv') 
    
    Returns:
        :returns: float or ndarray with CRI2012 Rf for :out: 'Rf'
            Other output is also possible by changing the :out: str value.
    
    Reference:
        1. `Smet, K., Schanda, J., Whitehead, L., & Luo, R. (2013). 
        CRI2012: A proposal for updating the CIE colour rendering index. 
        Lighting Research and Technology, 45, 689–709. 
        <http://lrt.sagepub.com/content/45/6/689>`_
    """
    return spd_to_cri(SPD, cri_type='cri2012-hl1000', out=out, wl=wl)


def spd_to_cri2012_real210(SPD, out='Rf', wl=None):
    """
    Wrapper function the 'cri2012' color rendition (fidelity) metric 
    with the Real-210 sampleset (normally for special color rendering indices).
    
    Args:
        :SPD: ndarray with spectral data (can be multiple SPDs, 
              first axis are the wavelengths)
        :wl: None, optional
            Wavelengths (or [start, end, spacing]) to interpolate the SPDs to. 
            None: default to no interpolation
        :out:  'Rf' or str, optional
            Specifies requested output (e.g. 'Rf,Rfi,cct,duv') 
    
    Returns:
        :returns: float or ndarray with CRI2012 Rf for :out: 'Rf'
            Other output is also possible by changing the :out: str value.
    
    Reference:
        1. `Smet, K., Schanda, J., Whitehead, L., & Luo, R. (2013). 
        CRI2012: A proposal for updating the CIE colour rendering index. 
        Lighting Research and Technology, 45, 689–709. 
        <http://lrt.sagepub.com/content/45/6/689>`_
    
    """
    return spd_to_cri(SPD, cri_type='cri2012-real210', out=out, wl=wl)