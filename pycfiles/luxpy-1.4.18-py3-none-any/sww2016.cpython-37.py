# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cam\sww2016.py
# Compiled at: 2019-07-31 07:48:20
# Size of source mod 2**32: 17588 bytes
"""
Module with Smet, Webster and Whitehead 2016 CAM.
=================================================

 :_CAM_SWW16_AXES: dict with list[str,str,str] containing axis labels 
                   of defined cspaces.
                   
 :_CAM_SWW16_PARAMETERS: cam_sww16 model parameters.
 
 :cam_sww16(): A simple principled color appearance model based on a mapping 
               of the Munsell color system.

References:
    1. `Smet, K. A. G., Webster, M. A., & Whitehead, L. A. (2016). 
    A simple principled approach for modeling and understanding uniform color metrics. 
    Journal of the Optical Society of America A, 33(3), A319–A331. 
    <https://doi.org/10.1364/JOSAA.33.00A319>`_
    .. 
"""
from luxpy import np, math, _CIE_ILLUMINANTS, _MUNSELL, _CMF, np2d, put_args_in_db, spd_to_xyz, cie_interp, asplit, ajoin
_CAM_SWW16_AXES = {'lab_cam_sww16': ['L (lab_cam_sww16)', 'a (lab_cam_sww16)', 'b (lab_cam_sww16)']}
_CAM_SWW16_PARAMETERS = {'JOSA': {'cLMS':[1.0, 1.0, 1.0],  'lms0':[4985.0, 5032.0, 4761.0],  'Cc':0.252,  'Cf':-0.4,  'clambda':[0.5, 0.5, 0.0],  'calpha':[1.0, -1.0, 0.0],  'cbeta':[0.5, 0.5, -1.0],  'cga1':[26.1, 34.0],  'cgb1':[6.76, 10.9],  'cga2':[0.587],  'cgb2':[-0.952],  'cl_int':[14.0, 1.0],  'cab_int':[4.99, 65.8],  'cab_out':[-0.1, -1.0],  'Ccwb':None,  'Mxyz2lms':[[0.21701045, 0.83573367, -0.0435106], [-0.42997951, 1.2038895, 0.08621089], [0.0, 0.0, 0.46579234]]}}
_CAM_SWW16_PARAMETERS['best-fit-JOSA'] = {'cLMS':[1.0, 1.0, 1.0],  'lms0':[4208.0, 4447.0, 4199.0],  'Cc':0.243,  'Cf':-0.269,  'clambda':[0.5, 0.5, 0.0],  'calpha':[1.0, -1.0, 0.0],  'cbeta':[0.5, 0.5, -1.0],  'cga1':[22.38, 26.42],  'cgb1':[5.36, 9.61],  'cga2':[0.668],  'cgb2':[-1.214],  'cl_int':[15.0, 1.04],  'cab_int':[5.85, 65.86],  'cab_out':[-1.008, -1.037],  'Ccwb':0.8,  'Mxyz2lms':[[0.21701045, 0.83573367, -0.0435106], [-0.42997951, 1.2038895, 0.08621089], [0.0, 0.0, 0.46579234]]}
_CAM_SWW16_PARAMETERS['best-fit-all-Munsell'] = {'cLMS':[1.0, 1.0, 1.0],  'lms0':[5405.0, 5617.0, 5520.0],  'Cc':0.206,  'Cf':-0.128,  'clambda':[0.5, 0.5, 0.0],  'calpha':[1.0, -1.0, 0.0],  'cbeta':[0.5, 0.5, -1.0],  'cga1':[38.26, 43.35],  'cgb1':[8.97, 16.18],  'cga2':[0.512],  'cgb2':[-0.896],  'cl_int':[19.3, 0.99],  'cab_int':[5.87, 63.24],  'cab_out':[-0.545, -0.978],  'Ccwb':0.736,  'Mxyz2lms':[[0.21701045, 0.83573367, -0.0435106], [-0.42997951, 1.2038895, 0.08621089], [0.0, 0.0, 0.46579234]]}
__all__ = [
 '_CAM_SWW16_AXES', '_CAM_SWW16_PARAMETERS', 'cam_sww16', 'xyz_to_lab_cam_sww16', 'lab_cam_sww16_to_xyz']

def cam_sww16(data, dataw=None, Yb=20.0, Lw=400.0, Ccwb=None, relative=True, parameters=None, inputtype='xyz', direction='forward', cieobs='2006_10'):
    """
    A simple principled color appearance model based on a mapping 
    of the Munsell color system.
    
    | This function implements the JOSA A (parameters = 'JOSA') published model. 
    
    Args:
        :data: 
            | ndarray with input tristimulus values 
            | or spectral data 
            | or input color appearance correlates
            | Can be of shape: (N [, xM], x 3), whereby: 
            | N refers to samples and M refers to light sources.
            | Note that for spectral input shape is (N x (M+1) x wl) 
        :dataw: 
            | None or ndarray, optional
            | Input tristimulus values or spectral data of white point.
            | None defaults to the use of CIE illuminant C.
        :Yb: 
            | 20.0, optional
            | Luminance factor of background (perfect white diffuser, Yw = 100)
        :Lw:
            | 400.0, optional
            | Luminance (cd/m²) of white point.
        :Ccwb:
            | None,  optional
            | Degree of cognitive adaptation (white point balancing)
            | If None: use [..,..] from parameters dict.
        :relative:
            | True or False, optional
            | True: xyz tristimulus values are relative (Yw = 100)
        :parameters:
            | None or str or dict, optional
            | Dict with model parameters.
            |    - None: defaults to luxpy.cam._CAM_SWW_2016_PARAMETERS['JOSA']
            |    - str: 'best-fit-JOSA' or 'best-fit-all-Munsell'
            |    - dict: user defined model parameters 
            |            (dict should have same structure)
        :inputtype:
            | 'xyz' or 'spd', optional
            | Specifies the type of input: 
            |     tristimulus values or spectral data for the forward mode.
        :direction:
            | 'forward' or 'inverse', optional
            |   -'forward': xyz -> cam_sww_2016
            |   -'inverse': cam_sww_2016 -> xyz 
        :cieobs:
            | '2006_10', optional
            | CMF set to use to perform calculations where spectral data 
              is involved (inputtype == 'spd'; dataw = None)
            | Other options: see luxpy._CMF['types']
    
    Returns:
        :returns: 
            | ndarray with color appearance correlates (:direction: == 'forward')
            |  or 
            | XYZ tristimulus values (:direction: == 'inverse')
    
    Notes:
        | This function implements the JOSA A (parameters = 'JOSA') 
          published model. 
        | With:
        |    1. A correction for the parameter 
        |         in Eq.4 of Fig. 11: 0.952 --> -0.952 
        |         
        |     2. The delta_ac and delta_bc white-balance shifts in Eq. 5e & 5f 
        |         should be: -0.028 & 0.821 
        |  
        |     (cfr. Ccwb = 0.66 in: 
        |         ab_test_out = ab_test_int - Ccwb*ab_gray_adaptation_field_int))
             
    References:
        1. `Smet, K. A. G., Webster, M. A., & Whitehead, L. A. (2016). 
        A simple principled approach for modeling and understanding uniform color metrics. 
        Journal of the Optical Society of America A, 33(3), A319–A331. 
        <https://doi.org/10.1364/JOSAA.33.00A319>`_

    """
    args = locals().copy()
    if parameters is None:
        parameters = _CAM_SWW16_PARAMETERS['JOSA']
    if isinstance(parameters, str):
        parameters = _CAM_SWW16_PARAMETERS[parameters]
    else:
        parameters = put_args_in_db(parameters, args)
        Cc, Ccwb, Cf, Mxyz2lms, cLMS, cab_int, cab_out, calpha, cbeta, cga1, cga2, cgb1, cgb2, cl_int, clambda, lms0 = [parameters[x] for x in sorted(parameters.keys())]
        if dataw is None:
            dataw = _CIE_ILLUMINANTS['C'].copy()
            xyzw = spd_to_xyz(dataw, cieobs=cieobs, relative=False)
            if relative == False:
                dataw[1:] = Lw * dataw[1:] / xyzw[:, 1:2]
            else:
                dataw = dataw
            if inputtype == 'xyz':
                dataw = spd_to_xyz(dataw, cieobs=cieobs, relative=relative)
        else:
            Mxyz2lms = np.dot(np.diag(cLMS), math.normalize_3x3_matrix(Mxyz2lms, np.array([[1, 1, 1]])))
            invMxyz2lms = np.linalg.inv(Mxyz2lms)
            MAab = np.array([clambda, calpha, cbeta])
            invMAab = np.linalg.inv(MAab)
            data = np2d(data).copy()
            dataw = np2d(dataw).copy()
            if data.ndim == 2:
                data = np.expand_dims(data, axis=1)
            if inputtype == 'xyz':
                if dataw.shape[0] == 1:
                    dataw = np.repeat(dataw, (data.shape[1]), axis=0)
            elif dataw.shape[0] == 2:
                dataw = np.vstack((dataw[0], np.repeat((dataw[1:]), (data.shape[1]), axis=0)))
    data = np.transpose(data, axes=(1, 0, 2))
    dshape = list(data.shape)
    dshape[-1] = 3
    if (inputtype != 'xyz') & (direction == 'forward'):
        dshape[-2] = dshape[(-2)] - 1
    camout = np.nan * np.ones(dshape)
    for i in range(data.shape[0]):
        if inputtype != 'xyz':
            if relative == True:
                xyzw_abs = spd_to_xyz((np.vstack((dataw[0], dataw[(i + 1)]))), cieobs=cieobs, relative=False)
                dataw[i + 1] = Lw * dataw[(i + 1)] / xyzw_abs[(0, 1)]
            else:
                xyzw = spd_to_xyz((np.vstack((dataw[0], dataw[(i + 1)]))), cieobs=cieobs, relative=False)
                lmsw = 683.0 * np.dot(Mxyz2lms, xyzw.T).T / _CMF[cieobs]['K']
                lmsf = Yb / 100.0 * lmsw
                if direction == 'forward':
                    if relative == True:
                        data[i, 1:, :] = Lw * data[i, 1:, :] / xyzw_abs[(0, 1)]
                    xyzt = spd_to_xyz((data[i]), cieobs=cieobs, relative=False) / _CMF[cieobs]['K']
                    lmst = 683.0 * np.dot(Mxyz2lms, xyzt.T).T
                else:
                    lmst = lmsf
        else:
            if inputtype == 'xyz':
                if relative == True:
                    dataw[i] = Lw * dataw[i] / 100.0
                else:
                    lmsw = 683.0 * np.dot(Mxyz2lms, dataw[i].T).T / _CMF[cieobs]['K']
                    lmsf = Yb / 100.0 * lmsw
                    if direction == 'forward':
                        if relative == True:
                            data[i] = Lw * data[i] / 100.0
                        lmst = 683.0 * np.dot(Mxyz2lms, data[i].T).T / _CMF[cieobs]['K']
                    else:
                        lmst = lmsf
            else:
                lmstp = math.erf(Cc * (np.log(lmst / lms0) + Cf * np.log(lmsf / lms0)))
                lmsfp = math.erf(Cc * (np.log(lmsf / lms0) + Cf * np.log(lmsf / lms0)))
                lmstp = np.vstack((lmsfp, lmstp))
                lstar, alph, bet = asplit(np.dot(MAab, lmstp.T).T)
                alphp = cga1[0] * alph
                alphp[alph < 0] = cga1[1] * alph[(alph < 0)]
                betp = cgb1[0] * bet
                betp[bet < 0] = cgb1[1] * bet[(bet < 0)]
                alphpp = cga2[0] * (alphp + betp)
                betpp = cgb2[0] * (alphp - betp)
                lstar_int = cl_int[0] * (lstar + cl_int[1])
                alph_int = cab_int[0] * (np.cos(cab_int[1] * np.pi / 180.0) * alphpp - np.sin(cab_int[1] * np.pi / 180.0) * betpp)
                bet_int = cab_int[0] * (np.sin(cab_int[1] * np.pi / 180.0) * alphpp + np.cos(cab_int[1] * np.pi / 180.0) * betpp)
                lstar_out = lstar_int
                if direction == 'forward':
                    if Ccwb is None:
                        alph_out = alph_int - cab_out[0]
                        bet_out = bet_int - cab_out[1]
                    else:
                        Ccwb = Ccwb * np.ones(2)
                        Ccwb[Ccwb < 0.0] = 0.0
                        Ccwb[Ccwb > 1.0] = 1.0
                        alph_out = alph_int - Ccwb[0] * alph_int[0]
                        bet_out = bet_int - Ccwb[1] * bet_int[0]
                    camout[i] = np.vstack((lstar_out[1:], alph_out[1:], bet_out[1:])).T
        if direction == 'inverse':
            labf_int = np.hstack((lstar_int[0], alph_int[0], bet_int[0]))
            lstar_out, alph_out, bet_out = asplit(data[i])
            if Ccwb is None:
                alph_int = alph_out + cab_out[0]
                bet_int = bet_out + cab_out[1]
            else:
                Ccwb = Ccwb * np.ones(2)
                Ccwb[Ccwb < 0.0] = 0.0
                Ccwb[Ccwb > 1.0] = 1.0
                alph_int = alph_out + Ccwb[0] * alph_int[0]
                bet_int = bet_out + Ccwb[1] * bet_int[0]
            lstar_int = lstar_out
            alphpp = 1.0 / cab_int[0] * (np.cos(-cab_int[1] * np.pi / 180.0) * alph_int - np.sin(-cab_int[1] * np.pi / 180.0) * bet_int)
            betpp = 1.0 / cab_int[0] * (np.sin(-cab_int[1] * np.pi / 180.0) * alph_int + np.cos(-cab_int[1] * np.pi / 180.0) * bet_int)
            lstar_int = lstar_out
            lstar = lstar_int / cl_int[0] - cl_int[1]
            alphp = 0.5 * (alphpp / cga2[0] + betpp / cgb2[0])
            betp = 0.5 * (alphpp / cga2[0] - betpp / cgb2[0])
            alph = alphp / cga1[0]
            bet = betp / cgb1[0]
            sa = np.sign(cga1[1])
            sb = np.sign(cgb1[1])
            alph[sa * alphp < 0.0] = alphp[(sa * alphp < 0)] / cga1[1]
            bet[sb * betp < 0.0] = betp[(sb * betp < 0)] / cgb1[1]
            lab = ajoin((lstar, alph, bet))
            lmstp = np.dot(invMAab, lab.T).T
            lmstp[lmstp < -1.0] = -1.0
            lmstp[lmstp > 1.0] = 1.0
            lmstp = math.erfinv(lmstp) / Cc - Cf * np.log(lmsf / lms0)
            lmst = np.exp(lmstp) * lms0
            xyzt = np.dot(invMxyz2lms, lmst.T).T
            if relative == True:
                xyzt = 100.0 / Lw * xyzt
            camout[i] = xyzt

    camout = np.transpose(camout, axes=(1, 0, 2))
    if camout.shape[0] == 1:
        camout = np.squeeze(camout, axis=0)
    return camout


def xyz_to_lab_cam_sww16(xyz, xyzw=None, Yb=20.0, Lw=400.0, Ccwb=None, relative=True, parameters=None, inputtype='xyz', cieobs='2006_10', **kwargs):
    """
    Wrapper function for cam_sww16 forward mode with 'xyz' input.
    
    | For help on parameter details: ?luxpy.cam.cam_sww16
    """
    return cam_sww16(xyz, dataw=xyzw, Yb=Yb, Lw=Lw, relative=relative, parameters=parameters, inputtype='xyz', direction='forward', cieobs=cieobs)


def lab_cam_sww16_to_xyz(lab, xyzw=None, Yb=20.0, Lw=400.0, Ccwb=None, relative=True, parameters=None, inputtype='xyz', cieobs='2006_10', **kwargs):
    """
    Wrapper function for cam_sww16 inverse mode with 'xyz' input.
    
    | For help on parameter details: ?luxpy.cam.cam_sww16
    """
    return cam_sww16(lab, dataw=xyzw, Yb=Yb, Lw=Lw, relative=relative, parameters=parameters, inputtype='xyz', direction='inverse', cieobs=cieobs)


if __name__ == '__main___':
    C = _CIE_ILLUMINANTS['C'].copy()
    C = np.vstack((C, cie_interp((_CIE_ILLUMINANTS['D65']), (C[0]), kind='spd')[1:]))
    M = _MUNSELL.copy()
    rflM = M['R']
    cieobs = '2006_10'
    Lw = 400
    Yb = 20
    xyzw2 = spd_to_xyz(C, cieobs=cieobs, relative=False)
    for i in range(C.shape[0] - 1):
        C[i + 1] = Lw * C[(i + 1)] / xyzw2[(i, 1)]

    xyz, xyzw = spd_to_xyz(C, cieobs=cieobs, relative=True, rfl=rflM, out=2)
    lab = cam_sww16(xyzw, dataw=xyzw, Yb=Yb, Lw=Lw, Ccwb=1, relative=True, parameters=None,
      inputtype='xyz',
      direction='forward',
      cieobs=cieobs)
    lab2 = cam_sww16(C, dataw=C, Yb=Yb, Lw=Lw, Ccwb=1, relative=True, parameters=None,
      inputtype='spd',
      direction='forward',
      cieobs=cieobs)
    xyz_ = cam_sww16(lab, dataw=xyzw, Yb=Yb, Lw=Lw, Ccwb=1, relative=True, parameters=None,
      inputtype='xyz',
      direction='inverse',
      cieobs=cieobs)
    xyz_2 = cam_sww16(lab2, dataw=C, Yb=Yb, Lw=Lw, Ccwb=1, relative=True, parameters=None,
      inputtype='spd',
      direction='inverse',
      cieobs=cieobs)