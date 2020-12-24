# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\deltaE\discriminationellipses.py
# Compiled at: 2020-03-19 05:50:53
# Size of source mod 2**32: 9865 bytes
"""
Module for discrimination ellipses
==================================================
 :get_macadam_ellipse(): Estimate n-step MacAdam ellipse at CIE x,y coordinates  
 
 :get_gij_fmc(): Get gij matrices describing the discrimination ellipses for Yxy using FMC-1 or FMC-2.

 :get_fmc_discrimination_ellipse(): Get n-step discrimination ellipse(s) in v-format (R,r, xc, yc, theta) for Yxy using FMC-1 or FMC-2.

 :discrimination_hotelling_t2(): Check significance of difference using Hotelling's T2 test on the centers Yxy1 and Yxy2 and their associate FMC-1/2 discrimination ellipses.

 
References:
    1. MacAdam DL. Visual Sensitivities to Color Differences in Daylight*. J Opt Soc Am. 1942;32(5):247-274.
    2. Chickering, K.D. (1967), Optimization of the MacAdam-Modified 1965 Friele Color-Difference Formula, 57(4):537-541
    3. Chickering, K.D. (1971), FMC Color-Difference Formulas: Clarification Concerning Usage, 61(1):118-122
    
.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import sp, np, plt, math, Yxy_to_xyz, plotSL, plot_chromaticity_diagram_colors, plotellipse
from .macadamellipses import get_macadam_ellipse
from .frieleellipses import get_gij_fmc, get_fmc_discrimination_ellipse
__all__ = [
 'get_discrimination_ellipse', 'get_macadam_ellipse', 'get_gij_fmc', 'get_fmc_discrimination_ellipse', 'discrimination_hotelling_t2']

def get_discrimination_ellipse(Yxy=np.array([[100, 0.3333333333333333, 0.3333333333333333]]), etype='fmc2', nsteps=10, k_neighbours=3, average_cik=True, Y=None):
    """
    Get discrimination ellipse(s) in v-format (R,r, xc, yc, theta) for Yxy using an interpolation of the MacAdam ellipses or using FMC-1 or FMC-2.
    
    Args:
        :Yxy:
            | 2D ndarray with [Y,]x,y coordinate centers. 
            | If Yxy.shape[-1]==2: Y is added using the value from the Y-input argument.
        :etype:
            | 'fmc2', optional
            | Type color discrimination ellipse estimation to use.
            | options: 'macadam', 'fmc1', 'fmc2' 
            |  - 'macadam': interpolate covariance matrices of closest MacAdam ellipses (see: get_macadam_ellipse?).
            |  - 'fmc1': use FMC-1 from ref 2 (see get_fmc_discrimination_ellipse?).
            |  - 'fmc2': use FMC-1 from ref 3 (see get_fmc_discrimination_ellipse?).
        :nsteps:
            | 10, optional
            | Set multiplication factor for ellipses 
            | (nsteps=1 corresponds to approximately 1 MacAdam step, 
            | for FMC-2, Y also has to be 10.69, see note below).
        :k_neighbours:
            | 3, optional
            | Only for option 'macadam'.
            | Number of nearest ellipses to use to calculate ellipse at xy 
        :average_cik:
            | True, optional
            | Only for option 'macadam'.
            | If True: take distance weighted average of inverse 
            |   'covariance ellipse' elements cik. 
            | If False: average major & minor axis lengths and 
            |   ellipse orientation angles directly.
        :Y:
            | None, optional
            | Only for option 'fmc2'(see note below).
            | If not None: Y = 10.69 and overrides values in Yxy. 
    
    Note:
        1. FMC-2 is almost identical to FMC-1 is Y = 10.69!; see [3]
    
    References:
       1. MacAdam DL. Visual Sensitivities to Color Differences in Daylight*. J Opt Soc Am. 1942;32(5):247-274.
       2. Chickering, K.D. (1967), Optimization of the MacAdam-Modified 1965 Friele Color-Difference Formula, 57(4):537-541
       3. Chickering, K.D. (1971), FMC Color-Difference Formulas: Clarification Concerning Usage, 61(1):118-122
    """
    if Yxy.shape[(-1)] == 2:
        Yxy = np.hstack((100 * np.ones((Yxy.shape[0], 1)), Yxy))
    if Y is not None:
        Yxy[(Ellipsis, 0)] = Y
    if etype == 'macadam':
        return get_macadam_ellipse(xy=(Yxy[..., 1:]), k_neighbours=k_neighbours, nsteps=nsteps, average_cik=average_cik)
    else:
        return get_fmc_discrimination_ellipse(Yxy=Yxy, etype=etype, nsteps=nsteps, Y=Y)


def discrimination_hotelling_t2(Yxy1, Yxy2, etype='fmc2', ellipsoid=True, Y1=None, Y2=None, cspace='Yxy'):
    """
    Check 'significance' of difference using Hotelling's T2 test on the centers Yxy1 and Yxy2 and their associate FMC-1/2 discrimination ellipses.
    
    Args:
        :Yxy1, Yxy2:
            | 2D ndarrays with [Y,]x,y coordinate centers. 
            | If Yxy.shape[-1]==2: Y is added using the value from the Y-input argument.
        :etype:
            | 'fmc2', optional
            | Type of FMC color discrimination equations to use (see references below).
            | options: 'fmc1', fmc2'
        :Y1, Y2:
            | None, optional
            | Only affects FMC-2 (see note below).
            | If not None: Yi = 10.69 and overrides values in Yxyi. 
        :ellipsoid:
            | True, optional
            | If True: return ellipsoids, else return ellipses (only if cspace == 'Yxy')!
        :cspace:
            | 'Yxy', optional
            | Return coefficients for Yxy-ellipses/ellipsoids ('Yxy') or XYZ ellipsoids ('xyz')

    Returns:
        :p:
            | Chi-square based p-value
        :T2:
            | T2 test statistic (= mahalanobis distance on summed standard error cov. matrices)
    
    Steps:
        1. For each center coordinate, the standard error covariance matrix gij^-1 = Si/ni
        is determined using the FMC-1 or FMC-2 equations (see refs. 1 & 2).
        2. Calculate sum of covariance matrices: SIG = S1/n1 + S2/n2 = gij1^-1 + gij2^-1
        3. These are then used in Hotelling's T2 test: T2 = (xy1 - xy2).T*(SIG^-1)*(xy1_xy2)
        4. The T2 statistic is then tested against a Chi-square distribution with 2 or 3 degrees of freedom.
    
    References:
       1. Chickering, K.D. (1967), Optimization of the MacAdam-Modified 1965 Friele Color-Difference Formula, 57(4):537-541
       2. Chickering, K.D. (1971), FMC Color-Difference Formulas: Clarification Concerning Usage, 61(1):118-122

    """
    if Yxy1.shape[(-1)] == 2:
        Yxy1 = np.hstack((100 * np.ones((Yxy1.shape[0], 1)), Yxy1))
    else:
        if Y1 is not None:
            Yxy1[(Ellipsis, 0)] = Y1
        if Yxy2.shape[(-1)] == 2:
            Yxy2 = np.hstack((100 * np.ones((Yxy2.shape[0], 1)), Yxy2))
        if Y2 is not None:
            Yxy2[(Ellipsis, 0)] = Y2
    gij1 = get_gij_fmc(Yxy1, etype=etype, ellipsoid=ellipsoid, Y=Y1, cspace=cspace)
    gij2 = get_gij_fmc(Yxy2, etype=etype, ellipsoid=ellipsoid, Y=Y2, cspace=cspace)
    df = gij1.shape[1]
    D12 = Yxy1[..., 3 - df:] - Yxy2[..., 3 - df:]
    SIG12 = np.linalg.inv(np.linalg.inv(gij1) + np.linalg.inv(gij2))
    T2 = np.einsum('ki,ki->k', D12, np.einsum('kij,kj->ki', SIG12, D12))
    p = sp.stats.distributions.chi2.sf(T2, df)
    return (
     p, T2)


if __name__ == '__main__':
    Yxy1 = np.array([[100, 0.3333333333333333, 0.3333333333333333]])
    Yxy2 = np.array([[100, 0.3333333333333333, 0.3333333333333333], [50, 0.3333333333333333, 0.3333333333333333]])
    gij_11 = get_gij_fmc(Yxy1, etype='fmc1', ellipsoid=False)
    gij_12 = get_gij_fmc(Yxy2, etype='fmc1', ellipsoid=False)
    Yxy1 = np.array([[100, 0.3333333333333333, 0.3333333333333333]])
    Yxy2 = np.array([[100, 0.3333333333333333, 0.3333333333333333], [50, 0.3333333333333333, 0.3406333333333333]])
    p, T2 = discrimination_hotelling_t2(Yxy1, Yxy2, Y1=10.69, Y2=10.69, etype='fmc2', ellipsoid=False, cspace='Yxy')
    print('p-value, Chi2:', p, T2)
    v_mac = get_macadam_ellipse(xy=None)
    xys = v_mac[:, 2:4]
    v_mac_0 = get_fmc_discrimination_ellipse(Yxy=xys, etype='macadam', nsteps=10)
    v_mac_1 = get_discrimination_ellipse(Yxy=xys, etype='fmc1', nsteps=10)
    v_mac_2 = get_discrimination_ellipse(Yxy=xys, etype='fmc2', nsteps=10, Y=10.69)
    cspace = 'Yxy'
    axh = plotSL(cspace=cspace, cieobs='1931_2', show=False, diagram_colors=False)
    axh = plotellipse(v_mac_0, show=True, axh=axh, cspace_in=None, cspace_out=cspace, plot_center=False, center_color='r', out='axh', line_style=':', line_color='r', line_width=1.5)
    plotellipse(v_mac_1, show=True, axh=axh, cspace_in=None, cspace_out=cspace, line_color='b', line_style=':', plot_center=True, center_color='k')
    plotellipse(v_mac_2, show=True, axh=axh, cspace_in=None, cspace_out=cspace, line_color='g', line_style='--', plot_center=True, center_color='k')
    if cspace == 'Yuv':
        axh.set_xlim([0, 0.6])
        axh.set_ylim([0, 0.6])
    plt.plot(xys[:, 0], xys[:, 1], 'r.')