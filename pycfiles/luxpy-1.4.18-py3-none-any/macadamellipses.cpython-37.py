# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\deltaE\macadamellipses.py
# Compiled at: 2019-04-19 16:19:10
# Size of source mod 2**32: 6162 bytes
"""
Module for MacAdam ellipses
==================================================================

 :get_macadam_ellipse(): Estimate n-step MacAdam ellipse at CIE x,y coordinates  
     

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, plt, math, cKDTree, plotSL, plot_chromaticity_diagram_colors, plotellipse
__all__ = [
 'get_macadam_ellipse']

def get_macadam_ellipse(xy=None, k_neighbours=3, nsteps=10, average_cik=True):
    """
    Estimate n-step MacAdam ellipse at CIE x,y coordinates xy by calculating 
    average inverse covariance ellipse of the k_neighbours closest ellipses.
    
    Args:
        :xy:
            | None or ndarray, optional
            | If None: output Macadam ellipses, if not None: xy are the 
            | CIE xy coordinates for which ellipses will be estimated.
            
        :k_neighbours:
            | 3, optional
            | Number of nearest ellipses to use to calculate ellipse at xy
        :nsteps:
            | 10, optional
            | Set number of MacAdam steps of ellipse.
        :average_cik:
            | True, optional
            | If True: take distance weighted average of inverse 
            |   'covariance ellipse' elements cik. 
            | If False: average major & minor axis lengths and 
            |   ellipse orientation angles directly.
            
    Returns:
        :v_mac_est:
            | estimated MacAdam ellipse(s) in v-format [Rmax,Rmin,xc,yc,theta]
            
    """
    v_mac = np.atleast_2d([
     [
      0.16, 0.057, 0.0085, 0.0035, 62.5],
     [
      0.187, 0.118, 0.022, 0.0055, 77],
     [
      0.253, 0.125, 0.025, 0.005, 55.5],
     [
      0.15, 0.68, 0.096, 0.023, 105],
     [
      0.131, 0.521, 0.047, 0.02, 112.5],
     [
      0.212, 0.55, 0.058, 0.023, 100],
     [
      0.258, 0.45, 0.05, 0.02, 92],
     [
      0.152, 0.365, 0.038, 0.019, 110],
     [
      0.28, 0.385, 0.04, 0.015, 75.5],
     [
      0.38, 0.498, 0.044, 0.012, 70],
     [
      0.16, 0.2, 0.021, 0.0095, 104],
     [
      0.228, 0.25, 0.031, 0.009, 72],
     [
      0.305, 0.323, 0.023, 0.009, 58],
     [
      0.385, 0.393, 0.038, 0.016, 65.5],
     [
      0.472, 0.399, 0.032, 0.014, 51],
     [
      0.527, 0.35, 0.026, 0.013, 20],
     [
      0.475, 0.3, 0.029, 0.011, 28.5],
     [
      0.51, 0.236, 0.024, 0.012, 29.5],
     [
      0.596, 0.283, 0.026, 0.013, 13],
     [
      0.344, 0.284, 0.023, 0.009, 60],
     [
      0.39, 0.237, 0.025, 0.01, 47],
     [
      0.441, 0.198, 0.028, 0.0095, 34.5],
     [
      0.278, 0.223, 0.024, 0.0055, 57.5],
     [
      0.3, 0.163, 0.029, 0.006, 54],
     [
      0.365, 0.153, 0.036, 0.0095, 40]])
    v_mac = v_mac[:, [2, 3, 0, 1, 4]]
    v_mac[:, -1] = v_mac[:, -1] * np.pi / 180
    v_mac[:, 0:2] = v_mac[:, 0:2] / 10 * nsteps
    if xy is not None:
        cik = math.v_to_cik(v_mac, inverse=True)
        if average_cik == True:
            cik_long = np.hstack((cik[:, 0, :], cik[:, 1, :]))
        else:
            tree = cKDTree((v_mac[:, 2:4]), copy_data=True)
            d, inds = tree.query(xy, k=k_neighbours)
            if k_neighbours > 1:
                pd = 1
                w = (1.0 / np.abs(d) ** pd)[:, :, None]
                if average_cik == True:
                    cik_long_est = np.sum((w * cik_long[inds, :]), axis=1) / np.sum(w, axis=1)
                else:
                    v_mac_est = np.sum((w * v_mac[inds, :]), axis=1) / np.sum(w, axis=1)
            else:
                v_mac_est = v_mac[inds, :].copy()
        if (average_cik == True) & (k_neighbours > 1):
            cik_est = np.dstack((cik_long_est[:, 0:2], cik_long_est[:, 2:4]))
            v_mac_est = math.cik_to_v(cik_est, inverse=True)
        v_mac_est[:, 2:4] = xy
    else:
        v_mac_est = v_mac
    return v_mac_est


if __name__ == '__main__':
    v_mac = get_macadam_ellipse(xy=None)
    xy_test = np.asarray([[0.5, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333]])
    v_mac_est = get_macadam_ellipse(xy_test)
    cspace = 'Yxy'
    axh = plotSL(cspace=cspace, cieobs='1931_2', show=False, diagram_colors=True)
    axh = plotellipse(v_mac, show=True, axh=axh, cspace_out=cspace, plot_center=False, center_color='r', out='axh', line_style=':', line_color='k', line_width=1.5)
    plotellipse(v_mac_est, show=True, axh=axh, cspace_out=cspace, line_color='k', plot_center=True, center_color='k')
    if cspace == 'Yuv':
        axh.set_xlim([0, 0.6])
        axh.set_ylim([0, 0.6])
    plt.plot(xy_test[:, 0], xy_test[:, 1], 'ro')