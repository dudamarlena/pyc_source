# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\deltaE\frieleellipses.py
# Compiled at: 2020-03-19 04:29:00
# Size of source mod 2**32: 12012 bytes
"""
Module for Modified Friele discrimination ellipses
==================================================
 :get_gij_fmc(): Get gij matrices describing the discrimination ellipses for Yxy using FMC-1 or FMC-2.

 :get_fmc_discrimination_ellipse(): Get n-step discrimination ellipse(s) in v-format (R,r, xc, yc, theta) for Yxy using FMC-1 or FMC-2.

References:
    1. Chickering, K.D. (1967), Optimization of the MacAdam-Modified 1965 Friele Color-Difference Formula, 57(4), p.537-541
    2. Chickering, K.D. (1971), FMC Color-Difference Formulas: Clarification Concerning Usage, 61(1), p.118-122
 
.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, plt, math, Yxy_to_xyz, plotSL, plot_chromaticity_diagram_colors, plotellipse
_M_XYZ_TO_PQS = np.array([[0.724, 0.382, -0.098], [-0.48, 1.37, 0.1276], [0, 0, 0.686]])
__all__ = [
 'get_gij_fmc', 'get_fmc_discrimination_ellipse']

def _dot_M_xyz(M, xyz):
    """
    Perform matrix multiplication between M and xyz (M*xyz) using einsum.
    
    Args:
        :xyz:
            | 2D or 3D ndarray
        :M:
            | 2D or 3D ndarray
            | if 2D: use same matrix M for each xyz, 
            | if 3D: use M[i] for xyz[i,:] (2D xyz) or xyz[:,i,:] (3D xyz)
            
    Returns:
        :M*xyz:
            | ndarray with same shape as xyz containing dot product of M and xyz.
    """
    if np.ndim(M) == 2:
        if len(xyz.shape) == 3:
            return np.einsum('ij,klj->kli', M, xyz)
        else:
            return np.einsum('ij,lj->li', M, xyz)
    else:
        if len(xyz.shape) == 3:
            return np.concatenate([np.einsum('ij,klj->kli', M[i], xyz[:, i:i + 1, :]) for i in range(M.shape[0])], axis=1)
        else:
            return np.concatenate([np.einsum('ij,lj->li', M[i], xyz[i:i + 1, :]) for i in range(M.shape[0])], axis=0)


def _xyz_to_pqs(xyz):
    """
    Calculate pqs from xyz.
    """
    return _dot_M_xyz(_M_XYZ_TO_PQS, xyz)


def _transpose_02(C):
    if C.ndim == 3:
        C = np.transpose(C, (2, 0, 1))
    else:
        C = C[(None, Ellipsis)]
    return C


def _cij_to_gij(xyz, C):
    """ Convert from matrix elements describing the discrimination ellipses from Cij (XYZ) to gij (Yxy)"""
    SIG = xyz[(Ellipsis, 0)] + xyz[(Ellipsis, 1)] + xyz[(Ellipsis, 2)]
    M1 = np.array([SIG, -SIG * xyz[(Ellipsis, 0)] / xyz[(Ellipsis, 1)], xyz[(Ellipsis, 0)] / xyz[(Ellipsis, 1)]])
    M2 = np.array([np.zeros_like(SIG), np.zeros_like(SIG), np.ones_like(SIG)])
    M3 = np.array([-SIG, -SIG * (xyz[(Ellipsis, 1)] + xyz[(Ellipsis, 2)]) / xyz[(Ellipsis, 1)], xyz[(Ellipsis, 2)] / xyz[(Ellipsis, 1)]])
    M = np.array((M1, M2, M3))
    M = _transpose_02(M)
    C = _transpose_02(C)
    AM = np.einsum('ij,kjl->kil', _M_XYZ_TO_PQS, M)
    CAM = np.einsum('kij,kjl->kil', C, AM)
    gij = np.einsum('kij,kjl->kil', np.transpose(AM, (0, 2, 1)), CAM)
    gij = np.roll(np.roll(gij, 1, axis=2), 1, axis=1)
    return gij


def _get_gij_fmc_1(xyz, cspace='Yxy'):
    """
    Get gij matrices describing the discrimination ellipses for xyz using FMC-1.
    
    Reference:
        Chickering, K.D. (1967), Optimization of the MacAdam-Modified 1965 Friele Color-Difference Formula, 57(4), p.537-541
    """
    pqs = _xyz_to_pqs(xyz)
    D2 = pqs[(Ellipsis, 0)] ** 2 + pqs[(Ellipsis, 1)] ** 2
    b2 = 0.0003098 * (pqs[(Ellipsis, 2)] ** 2 + 0.2015 * xyz[(Ellipsis, 1)] ** 2)
    A2 = 57780 * (1 + 2.73 * (pqs[(Ellipsis, 0)] * pqs[(Ellipsis, 1)]) ** 2 / (pqs[(Ellipsis,
                                                                                    0)] ** 4 + pqs[(Ellipsis,
                                                                                                    1)] ** 4))
    C11 = (A2 * (0.0778 * pqs[(Ellipsis, 0)] ** 2 + pqs[(Ellipsis, 1)] ** 2) + (pqs[(Ellipsis,
                                                                                     0)] * pqs[(Ellipsis,
                                                                                                2)]) ** 2 / b2) / D2 ** 2
    C12 = (-0.9222 * A2 * pqs[(Ellipsis, 0)] * pqs[(Ellipsis, 1)] + pqs[(Ellipsis,
                                                                         0)] * pqs[(Ellipsis,
                                                                                    1)] * pqs[(Ellipsis,
                                                                                               2)] ** 2 / b2) / D2 ** 2
    C22 = (A2 * (pqs[(Ellipsis, 0)] ** 2 + 0.0778 * pqs[(Ellipsis, 1)] ** 2) + (pqs[(Ellipsis,
                                                                                     1)] * pqs[(Ellipsis,
                                                                                                2)]) ** 2 / b2) / D2 ** 2
    C13 = -pqs[(Ellipsis, 0)] * pqs[(Ellipsis, 2)] / (b2 * D2)
    C33 = 1 / b2
    C23 = pqs[(Ellipsis, 1)] * C13 / pqs[(Ellipsis, 0)]
    C = np.array([[C11, C12, C13], [C12, C22, C23], [C13, C23, C33]])
    if cspace == 'Yxy':
        return _cij_to_gij(xyz, C)
    else:
        return C


def _get_gij_fmc_2(xyz, cspace='Yxy'):
    """
    Get gij matrices describing the discrimination ellipses for xyz using FMC-1.
    
    Reference:
        Chickering, K.D. (1971), FMC Color-Difference Formulas: Clarification Concerning Usage, 61(1), p.118-122
    """
    pqs = _xyz_to_pqs(xyz)
    D = (pqs[(Ellipsis, 0)] ** 2 + pqs[(Ellipsis, 1)] ** 2) ** 0.5
    a = (1.73e-05 * D ** 2 / (1 + 2.73 * (pqs[(Ellipsis, 0)] * pqs[(Ellipsis, 1)]) ** 2 / (pqs[(Ellipsis,
                                                                                                0)] ** 4 + pqs[(Ellipsis,
                                                                                                                1)] ** 4))) ** 0.5
    b = (0.0003098 * (pqs[(Ellipsis, 2)] ** 2 + 0.2015 * xyz[(Ellipsis, 1)] ** 2)) ** 0.5
    K1 = 0.55669 + xyz[(Ellipsis, 1)] * (0.049434 + xyz[(Ellipsis, 1)] * (-0.00082575 + xyz[(Ellipsis,
                                                                                             1)] * (7.9172e-06 - 3.0087e-08 * xyz[(Ellipsis,
                                                                                                                                   1)])))
    K2 = 0.17548 + xyz[(Ellipsis, 1)] * (0.027556 + xyz[(Ellipsis, 1)] * (-0.00057262 + xyz[(Ellipsis,
                                                                                             1)] * (6.3893e-06 - 2.6731e-08 * xyz[(Ellipsis,
                                                                                                                                   1)])))
    e1 = K1 * pqs[(Ellipsis, 2)] / (b * D ** 2)
    e2 = K1 / b
    e3 = 0.279 * K2 / (a * D)
    e4 = K1 / (a * D)
    C11 = (e1 ** 2 + e3 ** 2) * pqs[(Ellipsis, 0)] ** 2 + e4 ** 2 * pqs[(Ellipsis,
                                                                         1)] ** 2
    C12 = (e1 ** 2 + e3 ** 2 - e4 ** 2) * pqs[(Ellipsis, 0)] * pqs[(Ellipsis, 1)]
    C22 = (e1 ** 2 + e3 ** 2) * pqs[(Ellipsis, 1)] ** 2 + e4 ** 2 * pqs[(Ellipsis,
                                                                         0)] ** 2
    C13 = -e1 * e2 * pqs[(Ellipsis, 0)]
    C23 = -e1 * e2 * pqs[(Ellipsis, 1)]
    C33 = e2 ** 2
    C = np.array([[C11, C12, C13], [C12, C22, C23], [C13, C23, C33]])
    if cspace == 'Yxy':
        return _cij_to_gij(xyz, C)
    else:
        return C


def get_gij_fmc(Yxy, etype='fmc2', ellipsoid=True, Y=None, cspace='Yxy'):
    """
    Get gij matrices describing the discrimination ellipses/ellipsoids for Yxy or xyz using FMC-1 or FMC-2.
    
    Args:
        :Yxy:
            | 2D ndarray with [Y,]x,y coordinate centers. 
            | If Yxy.shape[-1]==2: Y is added using the value from the Y-input argument.
        :etype:
            | 'fmc2', optional
            | Type of FMC color discrimination equations to use (see references below).
            | options: 'fmc1', fmc2'
        :Y:
            | None, optional
            | Only affects FMC-2 (see note below).
            | If not None: Y = 10.69 and overrides values in Yxy. 
        :ellipsoid:
            | True, optional
            | If True: return ellipsoids, else return ellipses (only if cspace == 'Yxy')!
        :cspace:
            | 'Yxy', optional
            | Return coefficients for Yxy-ellipses/ellipsoids ('Yxy') or XYZ ellipsoids ('xyz')
    
    Note:
        1. FMC-2 is almost identical to FMC-1 is Y = 10.69!; see [2]
    
    References:
        1. Chickering, K.D. (1967), Optimization of the MacAdam-Modified 1965 Friele Color-Difference Formula, 57(4), p.537-541
        2. Chickering, K.D. (1971), FMC Color-Difference Formulas: Clarification Concerning Usage, 61(1), p.118-122
    """
    if Yxy.shape[(-1)] == 2:
        Yxy = np.hstack((100 * np.ones((Yxy.shape[0], 1)), Yxy))
    else:
        if Y is not None:
            Yxy[(Ellipsis, 0)] = Y
        xyz = Yxy_to_xyz(Yxy)
        if etype == 'fmc2':
            gij = _get_gij_fmc_2(xyz, cspace=cspace)
        else:
            gij = _get_gij_fmc_1(xyz, cspace=cspace)
    if ellipsoid == True:
        return gij
    else:
        if cspace.lower() == 'xyz':
            return gij
        return gij[:, 1:, 1:]


def get_fmc_discrimination_ellipse(Yxy=np.array([[100, 0.3333333333333333, 0.3333333333333333]]), etype='fmc2', Y=None, nsteps=10):
    """
    Get discrimination ellipse(s) in v-format (R,r, xc, yc, theta) for Yxy using FMC-1 or FMC-2.
    
    Args:
        :Yxy:
            | 2D ndarray with [Y,]x,y coordinate centers. 
            | If Yxy.shape[-1]==2: Y is added using the value from the Y-input argument.
        :etype:
            | 'fmc2', optional
            | Type of FMC color discrimination equations to use (see references below).
            | options: 'fmc1', fmc2'
        :Y:
            | None, optional
            | Only affects FMC-2 (see note below).
            | If not None: Y = 10.69 and overrides values in Yxy. 
        :nsteps:
            | 10, optional
            | Set multiplication factor for ellipses 
            | (nsteps=1 corresponds to approximately 1 MacAdam step, 
            | for FMC-2, Y also has to be 10.69, see note below).
    
    Note:
        1. FMC-2 is almost identical to FMC-1 is Y = 10.69!; see [2]
    
    References:
        1. Chickering, K.D. (1967), Optimization of the MacAdam-Modified 1965 Friele Color-Difference Formula, 57(4), p.537-541
        2. Chickering, K.D. (1971), FMC Color-Difference Formulas: Clarification Concerning Usage, 61(1), p.118-122
    """
    gij = get_gij_fmc(Yxy, etype=etype, ellipsoid=False, Y=Y, cspace='Yxy')
    if Yxy.shape[(-1)] == 2:
        xyc = Yxy
    else:
        xyc = Yxy[..., 1:]
    v = math.cik_to_v(gij, xyc=xyc)
    v[:, 0:2] = v[:, 0:2] * nsteps
    return v


if __name__ == '__main__':
    from macadamellipses import get_macadam_ellipse
    Yxy1 = np.array([[100, 0.3333333333333333, 0.3333333333333333]])
    Yxy2 = np.array([[100, 0.3333333333333333, 0.3333333333333333], [50, 0.3333333333333333, 0.3333333333333333]])
    gij_11 = get_gij_fmc(Yxy1, etype='fmc1', ellipsoid=False)
    gij_12 = get_gij_fmc(Yxy2, etype='fmc1', ellipsoid=False)
    v_mac = get_macadam_ellipse(xy=None)
    xys = v_mac[:, 2:4]
    v_mac_1 = get_fmc_discrimination_ellipse(Yxy=xys, etype='fmc1', nsteps=10)
    v_mac_2 = get_fmc_discrimination_ellipse(Yxy=xys, etype='fmc2', nsteps=10, Y=10.69)
    cspace = 'Yxy'
    axh = plotSL(cspace=cspace, cieobs='1931_2', show=False, diagram_colors=False)
    axh = plotellipse(v_mac, show=True, axh=axh, cspace_in=None, cspace_out=cspace, plot_center=False, center_color='r', out='axh', line_style=':', line_color='r', line_width=1.5)
    plotellipse(v_mac_1, show=True, axh=axh, cspace_in=None, cspace_out=cspace, line_color='b', line_style=':', plot_center=True, center_color='k')
    plotellipse(v_mac_2, show=True, axh=axh, cspace_in=None, cspace_out=cspace, line_color='g', line_style='--', plot_center=True, center_color='k')
    axh.set_xlim([0, 0.75])
    axh.set_ylim([0, 0.85])