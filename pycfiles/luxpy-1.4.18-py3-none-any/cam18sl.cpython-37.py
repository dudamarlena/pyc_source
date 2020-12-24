# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cam\cam18sl.py
# Compiled at: 2019-09-16 08:46:48
# Size of source mod 2**32: 19588 bytes
"""
Module with CAM18sl color appearance model
==========================================

 :_CAM_18SL_AXES: dict with list[str,str,str] containing axis labels 
                  of defined cspaces.
                  
 :_CAM18SL_PARAMETERS: database with CAM18sl model parameters.
 
 :_CAM18SL_UNIQUE_HUE_DATA: database of unique hues with corresponding 
                           Hue quadratures and eccentricity factors 
                           for cam18sl)
                              
 :_CAM18SL_NAKA_RUSHTON_PARAMETERS: | database with parameters 
                                     (n, sig, scaling and noise) 
                                     for the Naka-Rushton function: 
                                    | NK(x) = sign(x) * scaling * ((abs(x)**n) / ((abs(x)**n) + (sig**n))) + noise
                                       
 :cam18sl(): | calculates the output for the CAM18sl model for self-luminous related stimuli. 
             | `Hermans, S., Smet, K. A. G., & Hanselaer, P. (2018). 
               "Color appearance model for self-luminous stimuli."
               Journal of the Optical Society of America A, 35(12), 2000–2009. 
               <https://doi.org/10.1364/JOSAA.35.002000>`_
"""
from luxpy import np, _CMF, _CIE_ILLUMINANTS, _MUNSELL, np2d, spd_to_xyz, asplit, ajoin, cie_interp, getwlr, _WL3, np2dT
from luxpy.color.cam.colorappearancemodels import hue_angle, hue_quadrature, naka_rushton
_CAM18SL_WL3 = [
 390, 830, 1]
_CAM18SL_AXES = {'qabW_cam18sl': ['Q (cam18sl)', 'aW (cam18sl)', 'bW (cam18sl)']}
_CAM18SL_UNIQUE_HUE_DATA = {'hues':'red yellow green blue red'.split(), 
 'i':np.arange(5.0),  'hi':[20.14, 90.0, 164.25, 237.53, 380.14],  'ei':[0.8, 0.7, 1.0, 1.2, 0.8],  'Hi':[0.0, 100.0, 200.0, 300.0, 400.0]}
_CAM18SL_NAKA_RUSHTON_PARAMETERS = {'n':0.58, 
 'sig':lambda bg: 291.2 + 71.8 * bg ** 0.78,  'scaling':1,  'noise':0}
_CAM18SL_PARAMETERS = {'k':[
  676.7, 794.0, 1461.5], 
 'nakarushton':_CAM18SL_NAKA_RUSHTON_PARAMETERS, 
 'unique_hue_data':_CAM18SL_UNIQUE_HUE_DATA, 
 'cA':0.937, 
 'cAlms':[2.0, 1.0, 0.05],  'ca':0.63, 
 'calms':[1.0, -1.0909090909090908, 0.09090909090909091],  'cb':0.12, 
 'cblms':[1.0, 1.0, -2.0],  'cM':3260, 
 'cHK':[0.0024, 1.09],  'cW':[8.567511994516793e-05, 2.09],  'cfov':0.271}
__all__ = [
 'cam18sl', '_CAM18SL_AXES', '_CAM18SL_UNIQUE_HUE_DATA', '_CAM18SL_PARAMETERS', '_CAM18SL_NAKA_RUSHTON_PARAMETERS', '_CAM18SL_SURROUND_PARAMETERS']

def cam18sl(data, datab=None, Lb=[100], fov=10.0, inputtype='xyz', direction='forward', outin='Q,aW,bW', parameters=None):
    """
    Convert between CIE 2006 10°  XYZ tristimulus values (or spectral data) 
    and CAM18sl color appearance correlates.
    
    Args:
        :data: 
            | ndarray of CIE 2006 10°  absolute XYZ tristimulus values or spectral data
              or color appearance attributes of stimulus
        :datab: 
            | ndarray of CIE 2006 10°  absolute XYZ tristimulus values or spectral data
              of stimulus background
        :Lb: 
            | [100], optional
            | Luminance (cd/m²) value(s) of background(s) calculated using the CIE 2006 10° CMFs 
            | (only used in case datab == None and the background is assumed to be an Equal-Energy-White)
        :fov: 
            | 10.0, optional
            | Field-of-view of stimulus (for size effect on brightness)
        :inputtpe:
            | 'xyz' or 'spd', optional
            | Specifies the type of input: 
            |     tristimulus values or spectral data for the forward mode.
        :direction:
            | 'forward' or 'inverse', optional
            |   -'forward': xyz -> cam18sl
            |   -'inverse': cam18sl -> xyz 
        :outin:
            | 'Q,aW,bW' or str, optional
            | 'Q,aW,bW' (brightness and opponent signals for amount-of-neutral)
            |  other options: 'Q,aM,bM' (colorfulness) and 'Q,aS,bS' (saturation)
            | Str specifying the type of 
            |     input (:direction: == 'inverse') and 
            |     output (:direction: == 'forward')
        :parameters:
            | None or dict, optional
            | Set of model parameters.
            |   - None: defaults to luxpy.cam._CAM18SL_PARAMETERS 
            |    (see references below)
    
    Returns:
        :returns: 
            | ndarray with color appearance correlates (:direction: == 'forward')
            |  or 
            | XYZ tristimulus values (:direction: == 'inverse')
            
    Notes:
        | * Instead of using the CIE 1964 10° CMFs in some places of the model,
        |   the CIE 2006 10° CMFs are used througout, making it more self_consistent.
        |   This has an effect on the k scaling factors (now different those in CAM15u) 
        |   and the illuminant E normalization for use in the chromatic adaptation transform.
        |   (see future erratum to Hermans et al., 2018)
        | * The paper also used an equation for the amount of white W, which is
        |   based on a Q value not expressed in 'bright' ('cA' = 0.937 instead of 123). 
        |   This has been corrected for in the luxpy version of the model, i.e.
        |   _CAM18SL_PARAMETERS['cW'][0] has been changed from 2.29 to 1/11672.
        |   (see future erratum to Hermans et al., 2018)

    References: 
        1. `Hermans, S., Smet, K. A. G., & Hanselaer, P. (2018). 
        "Color appearance model for self-luminous stimuli."
        Journal of the Optical Society of America A, 35(12), 2000–2009. 
        <https://doi.org/10.1364/JOSAA.35.002000>`_ 
     """
    if parameters is None:
        parameters = _CAM18SL_PARAMETERS
    else:
        outin = outin.split(',')
        cA, cAlms, cHK, cM, cW, ca, calms, cb, cblms, cfov, k, naka, unique_hue_data = [parameters[x] for x in sorted(parameters.keys())]
        Mlms2xyz = np.linalg.inv(_CMF['2006_10']['M'])
        MAab = np.array([cAlms, calms, cblms])
        invMAab = np.linalg.inv(MAab)
        if datab is not None:
            if inputtype != 'xyz':
                Lb = spd_to_xyz(datab, cieobs='2006_10', relative=False)[..., 1:2]
            else:
                Lb = datab[..., 1:2]
        elif isinstance(Lb, list):
            Lb = np2dT(Lb)
        if inputtype == 'xyz':
            wlr = getwlr(_CAM18SL_WL3)
        else:
            if datab is None:
                wlr = data[0]
            else:
                wlr = datab[0]
        datar = np.vstack((wlr, np.ones((Lb.shape[0], wlr.shape[0]))))
        xyzr = spd_to_xyz(datar, cieobs='2006_10', relative=False)
        datar[1:] = datar[1:] / xyzr[..., 1:2] * Lb
        if datab is None:
            if inputtype != 'xyz':
                datab = datar.copy()
            else:
                datab = spd_to_xyz(datar, cieobs='2006_10', relative=False)
                datar = datab.copy()
        if data.ndim == 2:
            data = np.expand_dims(data, axis=1)
        if inputtype == 'xyz':
            if datab.shape[0] == 1:
                datab = np.repeat(datab, (data.shape[1]), axis=0)
                datar = np.repeat(datar, (data.shape[1]), axis=0)
        elif datab.shape[0] == 2:
            datab = np.vstack((datab[0], np.repeat((datab[1:]), (data.shape[1]), axis=0)))
        if datar.shape[0] == 2:
            datar = np.vstack((datar[0], np.repeat((datar[1:]), (data.shape[1]), axis=0)))
    data = np.transpose(data, axes=(1, 0, 2))
    dshape = list(data.shape)
    dshape[-1] = len(outin)
    if (inputtype != 'xyz') & (direction == 'forward'):
        dshape[-2] = dshape[(-2)] - 1
    camout = np.nan * np.ones(dshape)
    for i in range(data.shape[0]):
        if inputtype != 'xyz':
            xyzb = spd_to_xyz((np.vstack((datab[0], datab[i + 1:i + 2, :]))), cieobs='2006_10', relative=False)
            xyzr = spd_to_xyz((np.vstack((datar[0], datar[i + 1:i + 2, :]))), cieobs='2006_10', relative=False)
        else:
            xyzb = datab[i:i + 1, :]
            xyzr = datar[i:i + 1, :]
        lmsb = np.dot(_CMF['2006_10']['M'], xyzb.T).T
        rgbb = lmsb / _CMF['2006_10']['K'] * k
        rgbr = np.ones(xyzr.shape) * Lb[i]
        if direction == 'forward':
            if inputtype != 'xyz':
                xyz = spd_to_xyz((data[i]), cieobs='2006_10', relative=False)
            else:
                if inputtype == 'xyz':
                    xyz = data[i]
                else:
                    lms = np.dot(_CMF['2006_10']['M'], xyz.T).T
                    rgb = lms / _CMF['2006_10']['K'] * k
                    if (rgbb == 0).any():
                        Mcat = np.eye(3)
                    else:
                        Mcat = np.diag((rgbr / rgbb)[0])
                    rgba = np.dot(Mcat, rgb.T).T
                    rgbc = naka_rushton(rgba, n=(naka['n']), sig=(naka['sig'](rgbr.mean())), noise=(naka['noise']), scaling=(naka['scaling']))
                    Aab = np.dot(MAab, rgbc.T).T
                    A, a, b = asplit(Aab)
                    a = ca * a
                    b = cb * b
                    M = cM * (a ** 2.0 + b ** 2.0) ** 0.5
                    Q = cA * (A + cHK[0] * M ** cHK[1])
                    s = M / Q
                    W = 1 / (1.0 + cW[0] * s ** cW[1])
                    Q = Q * (fov / 10.0) ** cfov
                    h = hue_angle(a, b, htype='deg')
                    if 'H' in outin:
                        H = hue_quadrature(h, unique_hue_data=unique_hue_data)
                    else:
                        H = None
                if 'aM' in outin:
                    aM = M * np.cos(h * np.pi / 180.0)
                    bM = M * np.sin(h * np.pi / 180.0)
                if 'aS' in outin:
                    aS = s * np.cos(h * np.pi / 180.0)
                    bS = s * np.sin(h * np.pi / 180.0)
                if 'aW' in outin:
                    aW = W * np.cos(h * np.pi / 180.0)
                    bW = W * np.sin(h * np.pi / 180.0)
            if outin != ['Q', 'aW', 'bW']:
                camout[i] = eval('ajoin((' + ','.join(outin) + '))')
            else:
                camout[i] = ajoin((Q, aW, bW))
        elif direction == 'inverse':
            if 'aW' in outin:
                Q, a, b = asplit(data[i])
                Q = Q / (fov / 10.0) ** cfov
                W = (a ** 2.0 + b ** 2.0) ** 0.5
                s = ((1.0 / W - 1.0) / cW[0]) ** (1.0 / cW[1])
                M = s * Q
            elif 'aM' in outin:
                Q, a, b = asplit(data[i])
                Q = Q / (fov / 10.0) ** cfov
                M = (a ** 2.0 + b ** 2.0) ** 0.5
            else:
                if 'aS' in outin:
                    Q, a, b = asplit(data[i])
                    Q = Q / (fov / 10.0) ** cfov
                    s = (a ** 2.0 + b ** 2.0) ** 0.5
                    M = s * Q
                if 'h' in outin:
                    Q, WsM, h = asplit(data[i])
                    Q = Q / (fov / 10.0) ** cfov
                    if 'W' in outin:
                        s = ((1.0 / WsM - 1.0) / cW[0]) ** (1.0 / cW[1])
                        M = s * Q
                    else:
                        if 's' in outin:
                            M = WsM * Q
                        else:
                            if 'M' in outin:
                                M = WsM
            A = Q / cA - cHK[0] * M ** cHK[1]
            h = hue_angle(a, b, htype='rad')
            a = M / cM * np.cos(h)
            b = M / cM * np.sin(h)
            a = a / ca
            b = b / cb
            Aab = ajoin((A, a, b))
            rgbc = np.dot(invMAab, Aab.T).T
            rgba = naka_rushton(rgbc, n=(naka['n']), sig=(naka['sig'](rgbr.mean())), noise=(naka['noise']), scaling=(naka['scaling']), direction='inverse')
            rgb = np.dot(np.diag((rgbb / rgbr)[0]), rgba.T).T
            lms = rgb / k * _CMF['2006_10']['K']
            xyz = np.dot(Mlms2xyz, lms.T).T
            camout[i] = xyz

    if camout.shape[0] == 1:
        camout = np.squeeze(camout, axis=0)
    return camout


def xyz_to_qabW_cam18sl(xyz, xyzb=None, Lb=[100], fov=10.0, parameters=None, **kwargs):
    """
    Wrapper function for cam18sl forward mode with 'Q,aW,bW' output.
    
    | For help on parameter details: ?luxpy.cam.cam18sl
    """
    return cam18sl(xyz, datab=xyzb, Lb=Lb, fov=fov, direction='forward', inputtype='xyz', outin='Q,aW,bW', parameters=parameters)


def qabW_cam18sl_to_xyz(qab, xyzb=None, Lb=[100], fov=10.0, parameters=None, **kwargs):
    """
    Wrapper function for cam18sl inverse mode with 'Q,aW,bW' input.
    
    | For help on parameter details: ?luxpy.cam.cam18sl
    """
    return cam18sl(qab, datab=xyzb, Lb=Lb, fov=fov, direction='inverse', inputtype='xyz', outin='Q,aW,bW', parameters=parameters)


def xyz_to_qabM_cam18sl(xyz, xyzb=None, Lb=[100], fov=10.0, parameters=None, **kwargs):
    """
    Wrapper function for cam18sl forward mode with 'Q,aM,bM' output.
    
    | For help on parameter details: ?luxpy.cam.cam18sl
    """
    return cam18sl(xyz, datab=xyzb, Lb=Lb, fov=fov, direction='forward', inputtype='xyz', outin='Q,aM,bM', parameters=parameters)


def qabM_cam18sl_to_xyz(qab, xyzb=None, Lb=[100], fov=10.0, parameters=None, **kwargs):
    """
    Wrapper function for cam18sl inverse mode with 'Q,aM,bM' input.
    
    | For help on parameter details: ?luxpy.cam.cam18sl
    """
    return cam18sl(qab, datab=xyzb, Lb=Lb, fov=fov, direction='inverse', inputtype='xyz', outin='Q,aM,bM', parameters=parameters)


def xyz_to_qabS_cam18sl(xyz, xyzb=None, Lb=[100], fov=10.0, parameters=None, **kwargs):
    """
    Wrapper function for cam18sl forward mode with 'Q,aS,bS' output.
    
    | For help on parameter details: ?luxpy.cam.cam18sl
    """
    return cam18sl(xyz, datab=xyzb, Lb=Lb, fov=fov, direction='forward', inputtype='xyz', outin='Q,aS,bS', parameters=parameters)


def qabS_cam18sl_to_xyz(qab, xyzb=None, Lb=[100], fov=10.0, parameters=None, **kwargs):
    """
    Wrapper function for cam18sl inverse mode with 'Q,aS,bS' input.
    
    | For help on parameter details: ?luxpy.cam.cam18sl
    """
    return cam18sl(qab, datab=xyzb, Lb=Lb, fov=fov, direction='inverse', inputtype='xyz', outin='Q,aS,bS', parameters=parameters)


if __name__ == '__main__':
    C = _CIE_ILLUMINANTS['C'].copy()
    C = np.vstack((C, cie_interp((_CIE_ILLUMINANTS['D65']), (C[0]), kind='spd')[1:]))
    M = _MUNSELL.copy()
    rflM = M['R']
    cieobs = '2006_10'
    Lw = 100
    xyzw2 = spd_to_xyz(C, cieobs=cieobs, relative=False)
    for i in range(C.shape[0] - 1):
        C[i + 1] = Lw * C[(i + 1)] / xyzw2[(i, 1)]

    xyz, xyzw = spd_to_xyz(C, cieobs=cieobs, relative=True, rfl=rflM, out=2)
    qab = xyz_to_qabW_cam18sl(xyzw, xyzb=None, Lb=[100], fov=10.0)
    print('qab: ', qab)
    qab2 = cam18sl(C, datab=None, Lb=[100], fov=10.0, direction='forward', inputtype='spd', outin='Q,aW,bW', parameters=None)
    print('qab2: ', qab2)
    xyz_ = qabW_cam18sl_to_xyz(qab, xyzb=None, Lb=[100], fov=10.0)
    print('delta: ', xyzw - xyz_)
    cieobs = '2006_10'
    Lb = np2d([100])
    wlr = getwlr(_CAM18SL_WL3)
    EEW = np.vstack((wlr, np.ones((Lb.shape[1], wlr.shape[0]))))
    E = cie_interp((_CIE_ILLUMINANTS['E']), (EEW[0]), kind='spd')
    D65 = cie_interp((_CIE_ILLUMINANTS['D65']), (EEW[0]), kind='spd')
    A = cie_interp((_CIE_ILLUMINANTS['A']), (EEW[0]), kind='spd')
    C = cie_interp((_CIE_ILLUMINANTS['C']), (EEW[0]), kind='spd')
    STIM = np.vstack((EEW, E[1:], C[1:], D65[1, :], A[1:]))
    xyz = spd_to_xyz(STIM, cieobs=cieobs, relative=False)
    STIM[1:] = STIM[1:] / xyz[..., 1:2] * Lw
    xyz = spd_to_xyz(STIM, cieobs=cieobs, relative=False)
    BG = EEW
    qab = cam18sl(EEW, datab=EEW, Lb=[100], fov=10.0, direction='forward', inputtype='spd', outin='Q,aW,bW', parameters=None)
    print('test 2 qab: ', qab)