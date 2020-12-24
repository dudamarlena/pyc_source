# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cct\cct.py
# Compiled at: 2020-02-06 15:50:22
# Size of source mod 2**32: 36149 bytes
"""
cct: Module with functions related to correlated color temperature calculations
===============================================================================

 :_CCT_LUT_PATH: Folder with Look-Up-Tables (LUT) for correlated color 
                 temperature calculation followings Ohno's method.

 :_CCT_LUT: Dict with LUTs.
 
 :_CCT_LUT_CALC: Boolean determining whether to force LUT calculation, even if
                 the LUT can be fuond in ./data/cctluts/.

 :calculate_lut(): Function that calculates the LUT for the ccts stored in 
                   ./data/cctluts/cct_lut_cctlist.dat or given as input 
                   argument. Calculation is performed for CMF set specified in
                   cieobs. Adds a new (temprorary) field to the _CCT_LUT dict.

 :calculate_luts(): Function that recalculates (and overwrites) LUTs in 
                    ./data/cctluts/ for the ccts stored in 
                    ./data/cctluts/cct_lut_cctlist.dat or given as input 
                    argument. Calculation is performed for all CMF sets listed 
                    in _CMF['types'].

 :xyz_to_cct(): | Calculates CCT, Duv from XYZ 
                | wrapper for xyz_to_cct_ohno() & xyz_to_cct_search()

 :xyz_to_duv(): Calculates Duv, (CCT) from XYZ
                wrapper for xyz_to_cct_ohno() & xyz_to_cct_search()

 :cct_to_xyz(): Calculates xyz from CCT, Duv [100 K < CCT < 10**20]

 :xyz_to_cct_mcamy(): | Calculates CCT from XYZ using Mcamy model:
                      | `McCamy, Calvin S. (April 1992). 
                        Correlated color temperature as an explicit function of 
                        chromaticity coordinates. 
                        Color Research & Application. 17 (2): 142–144. 
                        <http://onlinelibrary.wiley.com/doi/10.1002/col.5080170211/abstract>`_

 :xyz_to_cct_HA(): | Calculate CCT from XYZ using Hernández-Andrés et al. model.
                   | `Hernández-Andrés, Javier; Lee, RL; Romero, J (September 20, 1999). 
                     Calculating Correlated Color Temperatures Across the 
                     Entire Gamut of Daylight and Skylight Chromaticities. 
                     Applied Optics. 38 (27): 5703–5709. PMID 18324081. 
                     <https://www.osapublishing.org/ao/abstract.cfm?uri=ao-38-27-5703>`_

 :xyz_to_cct_ohno(): | Calculates CCT, Duv from XYZ using a LUT following:
                     | `Ohno Y. (2014)
                       Practical use and calculation of CCT and Duv. 
                       Leukos. 2014 Jan 2;10(1):47-55.
                       <http://www.tandfonline.com/doi/abs/10.1080/15502724.2014.839020>`_

 :xyz_to_cct_search(): Calculates CCT, Duv from XYZ using brute-force search 
                       algorithm (between 1e2 K - 1e20 K on a log scale)

 :cct_to_mired(): Converts from CCT to Mired scale (or back).

===============================================================================
"""
from luxpy import np, pd, _PKG_PATH, _SEP, _EPS, _CMF, _CIEOBS, minimize, np2d, np2dT, getdata, dictkv, spd_to_xyz, cri_ref, blackbody, xyz_to_Yxy, xyz_to_Yuv, Yuv_to_xyz
_CCT_LUT_CALC = False
__all__ = ['_CCT_LUT_CALC']
__all__ += ['_CCT_LUT', '_CCT_LUT_PATH', 'calculate_luts', 'xyz_to_cct', 'xyz_to_duv', 'cct_to_xyz', 'cct_to_mired', 'xyz_to_cct_ohno', 'xyz_to_cct_search', 'xyz_to_cct_HA', 'xyz_to_cct_mcamy']
_CCT_LUT_PATH = _PKG_PATH + _SEP + 'data' + _SEP + 'cctluts' + _SEP
_CCT_LUT = {}

def calculate_lut(ccts=None, cieobs=None, add_to_lut=True):
    """
    Function that calculates LUT for the ccts stored in 
    ./data/cctluts/cct_lut_cctlist.dat or given as input argument.
    Calculation is performed for CMF set specified in cieobs. 
    Adds a new (temprorary) field to the _CCT_LUT dict.
    
    Args:
        :ccts: 
            | ndarray or str, optional
            | list of ccts for which to (re-)calculate the LUTs.
            | If str, ccts contains path/filename.dat to list.
        :cieobs: 
            | None or str, optional
            | str specifying cmf set.
            
    Returns:
        :returns: 
            | ndarray with cct and duv.
        
    Note:
        Function changes the global variable: _CCT_LUT!
    """
    if ccts is None:
        ccts = getdata('{}cct_lut_cctlist.dat'.format(_CCT_LUT_PATH))
    else:
        if isinstance(ccts, str):
            ccts = getdata(ccts)
    Yuv = np.ones((ccts.shape[0], 2)) * np.nan
    for i, cct in enumerate(ccts):
        Yuv[i, :] = xyz_to_Yuv(spd_to_xyz(blackbody(cct, wl3=[360, 830, 1]), cieobs=cieobs))[:, 1:3]

    u = Yuv[:, 0, None]
    v = 0.6666666666666666 * Yuv[:, 1, None]
    cctuv = np.hstack((ccts, u, v))
    if add_to_lut == True:
        _CCT_LUT[cieobs] = cctuv
    return cctuv


def calculate_luts(ccts=None):
    """
    Function that recalculates (and overwrites) LUTs in ./data/cctluts/ 
    for the ccts stored in ./data/cctluts/cct_lut_cctlist.dat or given as 
    input argument. Calculation is performed for all CMF sets listed 
    in _CMF['types'].
    
    Args:
        :ccts: 
            | ndarray or str, optional
            | List of ccts for which to (re-)calculate the LUTs.
            | If str, ccts contains path/filename.dat to list.
            
    Returns:
         | None
        
    Note:
        Function writes LUTs to ./data/cctluts/ folder!
    """
    for ii, cieobs in enumerate(sorted(_CMF['types'])):
        print('Calculating CCT LUT for CMF set: {}'.format(cieobs))
        cctuv = calculate_lut(ccts=ccts, cieobs=cieobs, add_to_lut=False)
        pd.DataFrame(cctuv).to_csv(('{}cct_lut_{}.dat'.format(_CCT_LUT_PATH, cieobs)), header=None, index=None, float_format='%1.9e')


if _CCT_LUT_CALC == True:
    calculate_luts()
try:
    _CCT_LUT = dictkv(keys=(sorted(_CMF['types'])), values=[getdata(('{}cct_lut_{}.dat'.format(_CCT_LUT_PATH, sorted(_CMF['types'])[i])), kind='np') for i in range(len(_CMF['types']))], ordered=False)
except:
    calculate_luts()
    _CCT_LUT = dictkv(keys=(sorted(_CMF['types'])), values=[getdata(('{}cct_lut_{}.dat'.format(_CCT_LUT_PATH, sorted(_CMF['types'])[i])), kind='np') for i in range(len(_CMF['types']))], ordered=False)

def xyz_to_cct_mcamy(xyzw):
    """
    Convert XYZ tristimulus values to correlated color temperature (CCT) using 
    the mccamy approximation.
    
    | Only valid for approx. 3000 < T < 9000, if < 6500, error < 2 K.
    
    Args:
        :xyzw: 
            | ndarray of tristimulus values
        
    Returns:
        :cct: 
            | ndarray of correlated color temperatures estimates
            
    References:
        1. `McCamy, Calvin S. (April 1992). 
        "Correlated color temperature as an explicit function of 
        chromaticity coordinates".
        Color Research & Application. 17 (2): 142–144.
        <http://onlinelibrary.wiley.com/doi/10.1002/col.5080170211/abstract>`_
         """
    Yxy = xyz_to_Yxy(xyzw)
    n = (Yxy[:, 1] - 0.332) / (Yxy[:, 2] - 0.1858)
    return np2d(-449.0 * n ** 3 + 3525.0 * n ** 2 - 6823.3 * n + 5520.33).T


def xyz_to_cct_HA(xyzw):
    """
    Convert XYZ tristimulus values to correlated color temperature (CCT). 
    
    Args:
        :xyzw: 
            | ndarray of tristimulus values
        
    Returns:
        :cct: 
            | ndarray of correlated color temperatures estimates
    
    References:
        1. `Hernández-Andrés, Javier; Lee, RL; Romero, J (September 20, 1999). 
        Calculating Correlated Color Temperatures Across the Entire Gamut 
        of Daylight and Skylight Chromaticities.
        Applied Optics. 38 (27), 5703–5709. P
        <https://www.osapublishing.org/ao/abstract.cfm?uri=ao-38-27-5703>`_
            
    Notes: 
        According to paper small error from 3000 - 800 000 K, but a test with 
        Planckians showed errors up to 20% around 500 000 K; 
        e>0.05 for T>200 000, e>0.1 for T>300 000, ...
    """
    if len(xyzw.shape) > 2:
        raise Exception('xyz_to_cct_HA(): Input xyzw.ndim must be <= 2 !')
    out_of_range_code = np.nan
    xe = [0.3366, 0.3356]
    ye = [0.1735, 0.1691]
    A0 = [-949.86315, 36284.48953]
    A1 = [6253.80338, 0.00228]
    t1 = [0.92159, 0.07861]
    A2 = [28.70599, 5.4535e-36]
    t2 = [0.20039, 0.01543]
    A3 = [4e-05, 0.0]
    t3 = [0.07125, 1.0]
    cct_ranges = np.array([[3000.0, 50000.0], [50000.0, 800000.0]])
    Yxy = xyz_to_Yxy(xyzw)
    CCT = np.ones((1, Yxy.shape[0])) * out_of_range_code
    for i in range(2):
        n = (Yxy[:, 1] - xe[i]) / (Yxy[:, 2] - ye[i])
        CCT_i = np2d(np.array(A0[i] + A1[i] * np.exp(np.divide(-n, t1[i])) + A2[i] * np.exp(np.divide(-n, t2[i])) + A3[i] * np.exp(np.divide(-n, t3[i]))))
        p = (CCT_i >= (1.0 - 0.05 * (i == 0)) * cct_ranges[i][0]) & (CCT_i < (1.0 + 0.05 * (i == 0)) * cct_ranges[i][1])
        CCT[p] = CCT_i[p]
        p = CCT_i < 0.95 * cct_ranges[0][0]
        CCT[p] = -1

    if (np.isnan(CCT.sum()) == True) | np.any(CCT == -1):
        print("Warning: xyz_to_cct_HA(): one or more CCTs out of range! --> (CCT < 3 kK,  CCT >800 kK) coded as (-1, NaN) 's")
    return CCT.T


def xyz_to_cct_search(xyzw, cieobs=_CIEOBS, out='cct', wl=None, accuracy=0.1, upper_cct_max=1e+20, approx_cct_temp=True):
    """
    Convert XYZ tristimulus values to correlated color temperature (CCT) and 
    Duv(distance above (> 0) or below ( < 0) the Planckian locus) by a 
    brute-force search. 

    | The algorithm uses an approximate cct_temp (HA approx., see xyz_to_cct_HA) 
      as starting point or uses the middle of the allowed cct-range 
      (1e2 K - 1e20 K, higher causes overflow) on a log-scale, then constructs 
      a 4-step section of the blackbody (Planckian) locus on which to find the
      minimum distance to the 1960 uv chromaticity of the test source.

    Args:
        :xyzw: 
            | ndarray of tristimulus values
        :cieobs: 
            | luxpy._CIEOBS, optional
            | CMF set used to calculated xyzw.
        :out: 
            | 'cct' (or 1), optional
            | Determines what to return.
            | Other options: 'duv' (or -1), 'cct,duv'(or 2), "[cct,duv]" (or -2)
        :wl: 
            | None, optional
            | Wavelengths used when calculating Planckian radiators.
        :accuracy: 
            | float, optional
            | Stop brute-force search when cct :accuracy: is reached.
        :upper_cct_max: 
            | 10.0**20, optional
            | Limit brute-force search to this cct.
        :approx_cct_temp: 
            | True, optional
            | If True: use xyz_to_cct_HA() to get a first estimate of cct to 
              speed up search.

    Returns:
        :returns: 
            | ndarray with:
            |    cct: out == 'cct' (or 1)
            |    duv: out == 'duv' (or -1)
            |    cct, duv: out == 'cct,duv' (or 2)
            |    [cct,duv]: out == "[cct,duv]" (or -2) 
    
    Notes:
        This program is more accurate, but slower than xyz_to_cct_ohno!
        Note that cct must be between 1e3 K - 1e20 K 
        (very large cct take a long time!!!)
    """
    xyzw = np2d(xyzw)
    if len(xyzw.shape) > 2:
        raise Exception('xyz_to_cct_search(): Input xyzw.shape must be <= 2 !')
    else:
        Yuvt = xyz_to_Yuv(np.squeeze(xyzw))
        ut = Yuvt[:, 1, None]
        vt = 0.6666666666666666 * Yuvt[:, 2, None]
        ccts = np.ones((xyzw.shape[0], 1)) * np.nan
        duvs = ccts.copy()
        if approx_cct_temp == True:
            ccts_est = xyz_to_cct_HA(xyzw)
            procent_estimates = np.array([[3000.0, 100000.0, 0.05], [100000.0, 200000.0, 0.1], [200000.0, 300000.0, 0.25], [300000.0, 400000.0, 0.4], [400000.0, 600000.0, 0.4], [600000.0, 800000.0, 0.4], [800000.0, np.inf, 0.25]])
        else:
            upper_cct = np.array(upper_cct_max)
        lower_cct = np.array(100.0)
        cct_scale_fun = lambda x: np.log10(x)
        cct_scale_ifun = lambda x: np.power(10.0, x)
        dT = (cct_scale_fun(upper_cct) - cct_scale_fun(lower_cct)) / 2
        ccttemp = np.array([cct_scale_ifun(cct_scale_fun(lower_cct) + dT)])
        ccts_est = np2d(ccttemp * np.ones((xyzw.shape[0], 1)))
        dT_approx_cct_False = dT.copy()
    for i in range(xyzw.shape[0]):
        cct = np.nan
        duv = np.nan
        ccttemp = ccts_est[i].copy()
        approx_cct_temp_temp = approx_cct_temp
        if approx_cct_temp == True:
            cct_scale_fun = lambda x: x
            cct_scale_ifun = lambda x: x
            if (ccttemp != -1) & (np.isnan(ccttemp) == False):
                for ii in range(procent_estimates.shape[0]):
                    if (ccttemp >= (1.0 - 0.05 * (ii == 0)) * procent_estimates[(ii, 0)]) & (ccttemp < (1.0 + 0.05 * (ii == 0)) * procent_estimates[(ii, 1)]):
                        procent_estimate = procent_estimates[(ii, 2)]
                        break

                dT = np.multiply(ccttemp, procent_estimate)
            else:
                if (ccttemp == -1) & (np.isnan(ccttemp) == False):
                    ccttemp = np.array([procent_estimates[(0, 0)] / 2])
                    procent_estimate = 1
                    dT = np.multiply(ccttemp, procent_estimate)
                else:
                    if np.isnan(ccttemp) == True:
                        upper_cct = np.array(upper_cct_max)
                        lower_cct = np.array(100.0)
                        cct_scale_fun = lambda x: np.log10(x)
                        cct_scale_ifun = lambda x: np.power(10.0, x)
                        dT = (cct_scale_fun(upper_cct) - cct_scale_fun(lower_cct)) / 2
                        ccttemp = np.array([cct_scale_ifun(cct_scale_fun(lower_cct) + dT)])
                        approx_cct_temp = False
        else:
            dT = dT_approx_cct_False
        nsteps = 3
        signduv = 1.0
        ccttemp = ccttemp[0]
        delta_cct = dT
        while delta_cct > accuracy:
            ccts_i = cct_scale_ifun(np.linspace(cct_scale_fun(ccttemp) - dT, cct_scale_fun(ccttemp) + dT, nsteps + 1))
            ccts_i[ccts_i < 100.0] = 100.0
            BB = cri_ref(ccts_i, wl3=wl, ref_type=['BB'], cieobs=cieobs)
            xyz = spd_to_xyz(BB, cieobs=cieobs)
            Yuv = xyz_to_Yuv(np.squeeze(xyz))
            u = Yuv[:, 1, None]
            v = 0.6666666666666666 * Yuv[:, 2, None]
            dc = ((ut[i] - u) ** 2 + (vt[i] - v) ** 2) ** 0.5
            if np.isnan(dc.min()) == False:
                q = dc.argmin()
                if np.size(q) > 1:
                    cct = np.median(ccts[q])
                    duv = np.median(dc[q])
                    q = np.median(q)
                    q = int(q)
                else:
                    cct = ccts_i[q]
                    duv = dc[q]
                if q == 0:
                    ccttemp = cct_scale_ifun(np.array(cct_scale_fun([cct])) + 2 * dT / nsteps)
                    continue
                if q == np.size(ccts_i):
                    ccttemp = cct_scale_ifun(np.array(cct_scale_fun([cct])) - 2 * dT / nsteps)
                else:
                    if (q > 0) & (q < np.size(ccts_i) - 1):
                        dT = 2 * dT / nsteps
                        d_p1m1 = ((u[(q + 1)] - u[(q - 1)]) ** 2.0 + (v[(q + 1)] - v[(q - 1)]) ** 2.0) ** 0.5
                        x = (dc[(q - 1)] ** 2.0 - dc[(q + 1)] ** 2.0 + d_p1m1 ** 2.0) / 2.0 * d_p1m1
                        vBB = v[(q - 1)] + (v[(q + 1)] - v[(q - 1)]) * (x / d_p1m1)
                        signduv = np.sign(vt[i] - vBB)
                    delta_cct = abs(cct - ccttemp)
                    ccttemp = np.array(cct)
                    approx_cct_temp = approx_cct_temp_temp
            else:
                ccttemp = np.nan
                cct = np.nan
                duv = np.nan

        duvs[i] = signduv * abs(duv)
        ccts[i] = cct

    if (out == 'cct') | (out == 1):
        return np2d(ccts)
    if (out == 'duv') | (out == -1):
        return np2d(duvs)
    if (out == 'cct,duv') | (out == 2):
        return (
         np2d(ccts), np2d(duvs))
    if (out == '[cct,duv]') | (out == -2):
        return np.vstack((ccts, duvs)).T


def xyz_to_cct_ohno(xyzw, cieobs=_CIEOBS, out='cct', wl=None, accuracy=0.1, force_out_of_lut=True, upper_cct_max=1e+20, approx_cct_temp=True):
    """
    Convert XYZ tristimulus values to correlated color temperature (CCT) and 
    Duv (distance above (>0) or below (<0) the Planckian locus) 
    using Ohno's method. 
    
    Args:
        :xyzw: 
            | ndarray of tristimulus values
        :cieobs: 
            | luxpy._CIEOBS, optional
            | CMF set used to calculated xyzw.
        :out: 
            | 'cct' (or 1), optional
            | Determines what to return.
            | Other options: 'duv' (or -1), 'cct,duv'(or 2), "[cct,duv]" (or -2)
        :wl: 
            | None, optional
            | Wavelengths used when calculating Planckian radiators.
        :accuracy: 
            | float, optional
            | Stop brute-force search when cct :accuracy: is reached.
        :upper_cct_max: 
            | 10.0**20, optional
            | Limit brute-force search to this cct.
        :approx_cct_temp: 
            | True, optional
            | If True: use xyz_to_cct_HA() to get a first estimate of cct 
              to speed up search.
        :force_out_of_lut: 
            | True, optional
            | If True and cct is out of range of the LUT, then switch to 
              brute-force search method, else return numpy.nan values.
        
    Returns:
        :returns: 
            | ndarray with:
            |    cct: out == 'cct' (or 1)
            |    duv: out == 'duv' (or -1)
            |    cct, duv: out == 'cct,duv' (or 2)
            |    [cct,duv]: out == "[cct,duv]" (or -2) 
            
    Note:
        LUTs are stored in ./data/cctluts/
        
    Reference:
        1. `Ohno Y. Practical use and calculation of CCT and Duv. 
        Leukos. 2014 Jan 2;10(1):47-55.
        <http://www.tandfonline.com/doi/abs/10.1080/15502724.2014.839020>`_
    """
    xyzw = np2d(xyzw)
    if len(xyzw.shape) > 2:
        raise Exception('xyz_to_cct_ohno(): Input xyzwa.ndim must be <= 2 !')
    Yuv = xyz_to_Yuv(xyzw)
    axis_of_v3 = len(Yuv.shape) - 1
    u = Yuv[:, 1, None]
    v = 0.6666666666666666 * Yuv[:, 2, None]
    uv = np2d(np.concatenate((u, v), axis=axis_of_v3))
    if cieobs not in _CCT_LUT:
        _CCT_LUT[cieobs] = calculate_lut(ccts=None, cieobs=cieobs, add_to_lut=False)
    cct_LUT = _CCT_LUT[cieobs][:, 0, None]
    uv_LUT = _CCT_LUT[cieobs][:, 1:3]
    CCT = np.ones(uv.shape[0]) * np.nan
    Duv = CCT.copy()
    idx_m = 0
    idx_M = uv_LUT.shape[0] - 1
    for i in range(uv.shape[0]):
        out_of_lut = False
        delta_uv = ((uv_LUT - uv[i]) ** 2.0).sum(axis=1) ** 0.5
        idx_min = delta_uv.argmin()
        if idx_min == idx_m:
            idx_min_m1 = idx_min
            out_of_lut = True
        else:
            idx_min_m1 = idx_min - 1
        if idx_min == idx_M:
            idx_min_p1 = idx_min
            out_of_lut = True
        else:
            idx_min_p1 = idx_min + 1
        if (out_of_lut == True) & (force_out_of_lut == True):
            cct_i, Duv_i = xyz_to_cct_search((xyzw[i]), cieobs=cieobs, wl=wl, accuracy=accuracy, out='cct,duv', upper_cct_max=upper_cct_max, approx_cct_temp=approx_cct_temp)
            CCT[i] = cct_i
            Duv[i] = Duv_i
            continue
        else:
            if (out_of_lut == True) & (force_out_of_lut == False):
                CCT[i] = np.nan
                Duv[i] = np.nan
            cct_m1 = cct_LUT[idx_min_m1]
            delta_uv_m1 = delta_uv[idx_min_m1]
            uv_m1 = uv_LUT[idx_min_m1]
            cct_p1 = cct_LUT[idx_min_p1]
            delta_uv_p1 = delta_uv[idx_min_p1]
            uv_p1 = uv_LUT[idx_min_p1]
            cct_0 = cct_LUT[idx_min]
            delta_uv_0 = delta_uv[idx_min]
            delta_uv_p1m1 = ((uv_p1[0] - uv_m1[0]) ** 2.0 + (uv_p1[1] - uv_m1[1]) ** 2.0) ** 0.5
            x = (delta_uv_m1 ** 2 - delta_uv_p1 ** 2 + delta_uv_p1m1 ** 2) / (2 * delta_uv_p1m1)
            Tx = cct_m1 + (cct_p1 - cct_m1) * (x / delta_uv_p1m1)
            vBB = uv_m1[1] + (uv_p1[1] - uv_m1[1]) * (x / delta_uv_p1m1)
            Tx_corrected_triangular = Tx * 0.99991
            signDuv = np.sign(uv[i][1] - vBB)
            Duv_triangular = signDuv * np.atleast_1d((delta_uv_m1 ** 2.0 - x ** 2.0) ** 0.5)
            a = delta_uv_m1 / (cct_m1 - cct_0 + _EPS) / (cct_m1 - cct_p1 + _EPS)
            b = delta_uv_0 / (cct_0 - cct_m1 + _EPS) / (cct_0 - cct_p1 + _EPS)
            c = delta_uv_p1 / (cct_p1 - cct_0 + _EPS) / (cct_p1 - cct_m1 + _EPS)
            A = a + b + c
            B = -(a * (cct_p1 + cct_0) + b * (cct_p1 + cct_m1) + c * (cct_0 + cct_m1))
            C = a * cct_p1 * cct_0 + b * cct_p1 * cct_m1 + c * cct_0 * cct_m1
            Tx = -B / (2 * A + _EPS)
            Tx_corrected_parabolic = Tx * 0.99991
            Duv_parabolic = signDuv * (A * np.power(Tx_corrected_parabolic, 2) + B * Tx_corrected_parabolic + C)
            Threshold = 0.002
            if Duv_triangular < Threshold:
                CCT[i] = Tx_corrected_triangular
                Duv[i] = Duv_triangular
            else:
                CCT[i] = Tx_corrected_parabolic
                Duv[i] = Duv_parabolic

    if (out == 'cct') | (out == 1):
        return np2dT(CCT)
    if (out == 'duv') | (out == -1):
        return np2dT(Duv)
    if (out == 'cct,duv') | (out == 2):
        return (
         np2dT(CCT), np2dT(Duv))
    if (out == '[cct,duv]') | (out == -2):
        return np.vstack((CCT, Duv)).T


def cct_to_xyz(ccts, duv=None, cieobs=_CIEOBS, wl=None, mode='lut', out=None, accuracy=0.1, force_out_of_lut=True, upper_cct_max=200.0, approx_cct_temp=True):
    """
    Convert correlated color temperature (CCT) and Duv (distance above (>0) or 
    below (<0) the Planckian locus) to XYZ tristimulus values.
    
    | Finds xyzw_estimated by minimization of:
    |    
    |    F = numpy.sqrt(((100.0*(cct_min - cct)/(cct))**2.0) 
    |         + (((duv_min - duv)/(duv))**2.0))
    |    
    | with cct,duv the input values and cct_min, duv_min calculated using 
    | luxpy.xyz_to_cct(xyzw_estimated,...).
    
    Args:
        :ccts: 
            | ndarray of cct values
        :duv: 
            | None or ndarray of duv values, optional
            | Note that duv can be supplied together with cct values in :ccts: 
              as ndarray with shape (N,2)
        :cieobs: 
            | luxpy._CIEOBS, optional
            | CMF set used to calculated xyzw.
        :mode: 
            | 'lut' or 'search', optional
            | Determines what method to use.
        :out: 
            | None (or 1), optional
            | If not None or 1: output a ndarray that contains estimated 
              xyz and minimization results: 
            | (cct_min, duv_min, F_min (objective fcn value))
        :wl: 
            | None, optional
            | Wavelengths used when calculating Planckian radiators.
        :accuracy: 
            | float, optional
            | Stop brute-force search when cct :accuracy: is reached.
        :upper_cct_max: 
            | 10.0**20, optional
            | Limit brute-force search to this cct.
        :approx_cct_temp: 
            | True, optional
            | If True: use xyz_to_cct_HA() to get a first estimate of cct to 
              speed up search.
        :force_out_of_lut: 
            | True, optional
            | If True and cct is out of range of the LUT, then switch to 
              brute-force search method, else return numpy.nan values.
        
    Returns:
        :returns: 
            | ndarray with estimated XYZ tristimulus values
    
    Note:
        If duv is not supplied (:ccts:.shape is (N,1) and :duv: is None), 
        source is assumed to be on the Planckian locus.
         """
    if isinstance(ccts, list):
        ccts = np2dT(np.array(ccts))
    else:
        ccts = np2d(ccts)
    if len(ccts.shape) > 2:
        raise Exception('cct_to_xyz(): Input ccts.shape must be <= 2 !')
    cct = np2d(ccts[:, 0, None])
    if (duv is None) & (ccts.shape[1] == 2):
        duv = np2d(ccts[:, 1, None])
    else:
        if duv is not None:
            duv = np2d(duv)
    BB = cri_ref(ccts=cct, wl3=wl, ref_type=['BB'])
    xyz_est = spd_to_xyz(data=BB, cieobs=cieobs, out=1)
    results = np.ones([ccts.shape[0], 3]) * np.nan
    if duv is not None:

        def objfcn(uv_offset, uv0, cct, duv, out=1):
            uv0 = np2d(uv0 + uv_offset)
            Yuv0 = np.concatenate((np2d([100.0]), uv0), axis=1)
            cct_min, duv_min = xyz_to_cct((Yuv_to_xyz(Yuv0)), cieobs=cieobs, out='cct,duv', wl=wl, mode=mode, accuracy=accuracy, force_out_of_lut=force_out_of_lut, upper_cct_max=upper_cct_max, approx_cct_temp=approx_cct_temp)
            F = np.sqrt((100.0 * (cct_min[0] - cct[0]) / cct[0]) ** 2.0 + ((duv_min[0] - duv[0]) / duv[0]) ** 2.0)
            if out == 'F':
                return F
            else:
                return np.concatenate((cct_min, duv_min, np2d(F)), axis=1)

        for i in range(xyz_est.shape[0]):
            xyz0 = xyz_est[i]
            cct_i = cct[i]
            duv_i = duv[i]
            cct_min, duv_min = xyz_to_cct(xyz0, cieobs=cieobs, out='cct,duv', wl=wl, mode=mode, accuracy=accuracy, force_out_of_lut=force_out_of_lut, upper_cct_max=upper_cct_max, approx_cct_temp=approx_cct_temp)
            if np.abs(duv[i]) > _EPS:
                Yuv0 = xyz_to_Yuv(xyz0)
                uv0 = Yuv0[0][1:3]
                OptimizeResult = minimize(fun=objfcn, x0=(np.zeros((1, 2))), args=(uv0, cct_i, duv_i, 'F'), method='Nelder-Mead', options={'maxiter':np.inf,  'maxfev':np.inf,  'xatol':1e-06,  'fatol':1e-06})
                betas = OptimizeResult['x']
                if out is not None:
                    results[i] = objfcn(betas, uv0, cct_i, duv_i, out=3)
                uv0 = np2d(uv0 + betas)
                Yuv0 = np.concatenate((np2d([100.0]), uv0), axis=1)
                xyz_est[i] = Yuv_to_xyz(Yuv0)
            else:
                xyz_est[i] = xyz0

    if (out is None) | (out == 1):
        return xyz_est
    else:
        return np.concatenate((xyz_est, results), axis=1)


def xyz_to_cct(xyzw, cieobs=_CIEOBS, out='cct', mode='lut', wl=None, accuracy=0.1, force_out_of_lut=True, upper_cct_max=1e+20, approx_cct_temp=True):
    """
    Convert XYZ tristimulus values to correlated color temperature (CCT) and
    Duv (distance above (>0) or below (<0) the Planckian locus)
    using either the brute-force search method or Ohno's method. 
    
    | Wrapper function for use with luxpy.colortf().
    
    Args:
        :xyzw:
            | ndarray of tristimulus values
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set used to calculated xyzw.
        :mode: 
            | 'lut' or 'search', optional
            | Determines what method to use.
        :out: 
            | 'cct' (or 1), optional
            | Determines what to return.
            | Other options: 'duv' (or -1), 'cct,duv'(or 2), "[cct,duv]" (or -2)
        :wl: 
            | None, optional
            | Wavelengths used when calculating Planckian radiators.
        :accuracy:
            | float, optional
            | Stop brute-force search when cct :accuracy: is reached.
        :upper_cct_max: 
            | 10.0**20, optional
            | Limit brute-force search to this cct.
        :approx_cct_temp: 
            | True, optional
            | If True: use xyz_to_cct_HA() to get a first estimate of cct to 
              speed up search.
        :force_out_of_lut: 
            | True, optional
            | If True and cct is out of range of the LUT, then switch to 
              brute-force search method, else return numpy.nan values.
        
    Returns:
        :returns: 
            | ndarray with:
            |   cct: out == 'cct' (or 1)
            | Optional: 
            |     duv: out == 'duv' (or -1), 
            |    cct, duv: out == 'cct,duv' (or 2), 
            |    [cct,duv]: out == "[cct,duv]" (or -2)
    """
    if (mode == 'lut') | (mode == 'ohno'):
        return xyz_to_cct_ohno(xyzw=xyzw, cieobs=cieobs, out=out, accuracy=accuracy, force_out_of_lut=force_out_of_lut)
    if mode == 'search':
        return xyz_to_cct_search(xyzw=xyzw, cieobs=cieobs, out=out, wl=wl, accuracy=accuracy, upper_cct_max=upper_cct_max, approx_cct_temp=approx_cct_temp)


def xyz_to_duv(xyzw, cieobs=_CIEOBS, out='duv', mode='lut', wl=None, accuracy=0.1, force_out_of_lut=True, upper_cct_max=1e+20, approx_cct_temp=True):
    """
    Convert XYZ tristimulus values to Duv (distance above (>0) or below (<0) 
    the Planckian locus) and correlated color temperature (CCT) values
    using either the brute-force search method or Ohno's method. 
    
    | Wrapper function for use with luxpy.colortf().
    
    Args:
        :xyzw: 
            | ndarray of tristimulus values
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set used to calculated xyzw.
        :mode: 
            | 'lut' or 'search', optional
            | Determines what method to use.
        :out: 
            | 'duv' (or 1), optional
            | Determines what to return.
            | Other options: 'duv' (or -1), 'cct,duv'(or 2), "[cct,duv]" (or -2)
        :wl: 
            | None, optional
            | Wavelengths used when calculating Planckian radiators.
        :accuracy: 
            | float, optional
            | Stop brute-force search when cct :accuracy: is reached.
        :upper_cct_max: 
            | 10.0**20, optional
            | Limit brute-force search to this cct.
        :approx_cct_temp:
            | True, optional
            | If True: use xyz_to_cct_HA() to get a first estimate of cct 
              to speed up search.
        :force_out_of_lut: 
            | True, optional
            | If True and cct is out of range of the LUT, then switch to 
              brute-force search method, else return numpy.nan values.
        
    Returns:
        :returns:
            | ndarray with:
            |   duv: out == 'duv' (or -1)
            | Optional: 
            |     duv: out == 'duv' (or -1), 
            |     cct, duv: out == 'cct,duv' (or 2), 
            |     [cct,duv]: out == "[cct,duv]" (or -2)
    """
    if (mode == 'lut') | (mode == 'ohno'):
        return xyz_to_cct_ohno(xyzw=xyzw, cieobs=cieobs, out=out, accuracy=accuracy, force_out_of_lut=force_out_of_lut)
    if mode == 'search':
        return xyz_to_cct_search(xyzw=xyzw, cieobs=cieobs, out=out, wl=wl, accuracy=accuracy, upper_cct_max=upper_cct_max, approx_cct_temp=approx_cct_temp)


def cct_to_mired(data):
    """
    Convert cct to Mired scale (or back). 

    Args:
        :data: 
            | ndarray with cct or Mired values.

    Returns:
        :returns: 
            | ndarray ((10**6) / data)
    """
    return np.divide(1000000, data)