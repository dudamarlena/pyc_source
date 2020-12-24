# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cct\cctduv_ohno_CORM2011.py
# Compiled at: 2020-03-19 08:43:38
# Size of source mod 2**32: 3887 bytes
"""
Module implementing Ohno (2011) CCT&Duv calculation
===================================================

 :xyz_to_cct_ohno2011(): Calculate cct and Duv from CIE 1931 2° xyz following Ohno (CORM 2011).
 
References:
    1. Ohno, Y. (2011). Calculation of CCT and Duv and Practical Conversion Formulae. 
    CORM 2011 Conference, Gaithersburg, MD, May 3-5, 2011

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import xyz_to_Yuv
import numpy as np
__all__ = [
 'xyz_to_cct_ohno2011']
_KIJ = np.array([[-0.0037146, 0.0560614, -0.3307009, 0.9750013, -1.5008606, 1.115559, -0.177348],
 [
  -3.23255e-05, 0.0003570016, -0.001589747, 0.0036196568, -0.0043534788, 0.0021595434, 0.0005308409],
 [
  -0.0026653835, 0.0417781315, -0.273172022, 0.953570888, -1.873907584, 1.964980251, -0.858308927],
 [
  -23.52495, 271.83365, -1178.5121, 2511.70136, -2796.6888, 1492.84136, -232.75027],
 [
  -1731364.909, 27482732.935, -181749963.507, 640976356.945, -1271412909.56, 1344881606.14, -592685060.6],
 [
  -943.53083, 21046.8274, -195000.61, 960532.935, -2652991.38, 3895617.42, -2375815.8],
 [
  508.57956, -13210.07, 141015.38, -793406.005, 2485269.54, -4114369.58, 2815177.1]])

def xyz_to_cct_ohno2011(xyz):
    """
    Calculate cct and Duv from CIE 1931 2° xyz following Ohno (2011).
    
    Args:
        :xyz:
            | ndarray with CIE 1931 2° X,Y,Z tristimulus values
            
    Returns:
        :cct, duv:
            | ndarrays with correlated color temperatures and distance to blackbody locus in CIE 1960 uv
            
    References:
        1. Ohno, Y. (2011). Calculation of CCT and Duv and Practical Conversion Formulae. 
        CORM 2011 Conference, Gaithersburg, MD, May 3-5, 2011
    """
    uvp = xyz_to_Yuv(xyz)[..., 1:]
    uv = uvp * np.array([[1, 0.6666666666666666]])
    Lfp = ((uv[(Ellipsis, 0)] - 0.292) ** 2 + (uv[(Ellipsis, 1)] - 0.24) ** 2) ** 0.5
    a = np.arctan((uv[(Ellipsis, 1)] - 0.24) / (uv[(Ellipsis, 0)] - 0.292))
    a[a < 0] = a[(a < 0)] + np.pi
    Lbb = np.polyval(_KIJ[0, :], a)
    Duv = Lfp - Lbb
    T1 = 1 / np.polyval(_KIJ[1, :], a)
    T1[a >= 2.54] = 1 / np.polyval(_KIJ[2, :], a[(a >= 2.54)])
    dTc1 = np.polyval(_KIJ[3, :], a) * (Lbb + 0.01) / Lfp * Duv / 0.01
    dTc1[a >= 2.54] = 1 / np.polyval(_KIJ[4, :], a[(a >= 2.54)]) * (Lbb[(a >= 2.54)] + 0.01) / Lfp[(a >= 2.54)] * Duv[(a >= 2.54)] / 0.01
    T2 = T1 - dTc1
    c = np.log10(T2)
    dTc2 = np.polyval(_KIJ[5, :], c)
    dTc2[Duv < 0] = np.polyval(_KIJ[6, :], c[(Duv < 0)]) * np.abs(Duv[(Duv < 0)] / 0.03) ** 2
    Tfinal = T2 - dTc2
    return (Tfinal, Duv)


if __name__ == '__main__':
    import luxpy as lx
    xyz = lx.spd_to_xyz(np.vstack((lx._CIE_D65, lx._CIE_A[1:, :])))
    cct, duv = xyz_to_cct_ohno2011(xyz)
    print('cct: ', cct)
    print('Duv: ', duv)