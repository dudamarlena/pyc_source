# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cam\cam_02_X.py
# Compiled at: 2019-10-24 08:26:08
# Size of source mod 2**32: 63732 bytes
"""

cam_02_X: Module with CIECAM02-type color appearance models
===========================================================

 :_CAM_02_X_UNIQUE_HUE_DATA: database of unique hues with corresponding 
                             Hue quadratures and eccentricity factors 
                             for ciecam02, cam16, ciecam97s)

 :_CAM_02_X_SURROUND_PARAMETERS: database of surround param. c, Nc, F and FLL 
                                 for ciecam02, cam16, ciecam97s.

 :_CAM_02_X_NAKA_RUSHTON_PARAMETERS: | database with parameters 
                                       (n, sig, scaling and noise) 
                                       for the Naka-Rushton function: 
                                     | NK(x) = sign(x) * scaling * ((abs(x)**n) / ((abs(x)**n) + (sig**n))) + noise

 :_CAM_02_X_UCS_PARAMETERS: | database with parameters specifying the conversion 
                              from ciecam02/cam16 to:
                            |    cam[x]ucs (uniform color space), 
                            |    cam[x]lcd (large color diff.), 
                            |    cam[x]scd (small color diff).

 :_CAM_02_X_DEFAULT_WHITE_POINT: Default internal reference white point (xyz)

 :_CAM_02_X_DEFAULT_TYPE: Default CAM type str specifier.

 : _CAM_02_X_DEFAULT_MCAT: Default MCAT specifier.

 :_CAM_02_X_DEFAULT_CONDITIONS: Default CAM model parameters for model 
                                in cam._CAM_02_X_DEFAULT_TYPE

 :_CAM_02_X_AXES: dict with list[str,str,str] containing axis labels 
                  of defined cspaces.

 :deltaH(): Compute a hue difference, dH = 2*C1*C2*sin(dh/2)

 :naka_rushton(): applies a Naka-Rushton function to the input
 
 :hue_angle(): calculates a positive hue angle

 :hue_quadrature(): calculates the Hue quadrature from the hue.

 :cam_structure_ciecam02_cam16(): | basic structure of ciecam02 and cam16 models.
                                  | Has 'forward' (xyz --> color attributes) 
                                    and 'inverse' (color attributes --> xyz) modes.

 :ciecam02(): | calculates ciecam02 output 
              | (wrapper for cam_structure_ciecam02_cam16 with specifics 
                of ciecam02): 
              | `N. Moroney, M. D. Fairchild, R. W. G. Hunt, C. Li, M. R. Luo, and T. Newman, 
                “The CIECAM02 color appearance model,” 
                IS&T/SID Tenth Color Imaging Conference. p. 23, 2002. <http://rit-mcsl.org/fairchild/PDFs/PRO19.pdf>`_

 :cam16(): | calculates cam16 output 
           | (wrapper for cam_structure_ciecam02_cam16 with specifics 
             of cam16):  
           | `C. Li, Z. Li, Z. Wang, Y. Xu, M. R. Luo, G. Cui, M. Melgosa, M. H. Brill, and M. Pointer, 
             “Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS,” 
             Color Res. Appl., p. n/a–n/a. <http://onlinelibrary.wiley.com/doi/10.1002/col.22131/abstract>`_

 :camucs_structure(): basic structure to go to ucs, lcd and scd color spaces 
                      (forward + inverse available)

 :cam02ucs(): | calculates ucs (or lcd, scd) output based on ciecam02 
                (forward + inverse available)
              |  `M. R. Luo, G. Cui, and C. Li, 
                 Uniform colour spaces based on CIECAM02 colour appearance model, 
                 Color Research & Application, 31(4), pp. 320–330, 2006.
                 <http://onlinelibrary.wiley.com/doi/10.1002/col.20227/abstract>`_

 :cam16ucs(): | calculates ucs (or lcd, scd) output based on cam16 
                (forward + inverse available)
              | `C. Li, Z. Li, Z. Wang, Y. Xu, M. R. Luo, G. Cui, M. Melgosa, M. H. Brill, and M. Pointer, 
                “Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS,” 
                Color Res. Appl., p. n/a–n/a. <http://onlinelibrary.wiley.com/doi/10.1002/col.22131/abstract>`_

 :specific_wrappers_in_the_'xyz_to_cspace()' and 'cpsace_to_xyz()' format:
      | 'xyz_to_jabM_ciecam02', 'jabM_ciecam02_to_xyz',
      | 'xyz_to_jabC_ciecam02', 'jabC_ciecam02_to_xyz',
      | 'xyz_to_jabM_cam16', 'jabM_cam16_to_xyz',
      | 'xyz_to_jabC_cam16', 'jabC_cam16_to_xyz',
      | 'xyz_to_jab_cam02ucs', 'jab_cam02ucs_to_xyz', 
      | 'xyz_to_jab_cam02lcd', 'jab_cam02lcd_to_xyz',
      | 'xyz_to_jab_cam02scd', 'jab_cam02scd_to_xyz', 
      | 'xyz_to_jab_cam16ucs', 'jab_cam16ucs_to_xyz',
      | 'xyz_to_jab_cam16lcd', 'jab_cam16lcd_to_xyz',
      | 'xyz_to_jab_cam16scd', 'jab_cam16scd_to_xyz'

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, math, cat, _CIEOBS, _CIE_ILLUMINANTS, np2d, np2dT, np3d, put_args_in_db, spd_to_xyz, asplit, ajoin
__all__ = [
 '_CAM_02_X_AXES', '_CAM_02_X_UNIQUE_HUE_DATA', '_CAM_02_X_SURROUND_PARAMETERS', '_CAM_02_X_NAKA_RUSHTON_PARAMETERS', '_CAM_02_X_UCS_PARAMETERS']
__all__ += ['_CAM_02_X_DEFAULT_TYPE', '_CAM_02_X_DEFAULT_WHITE_POINT', '_CAM_02_X_DEFAULT_MCAT', '_CAM_02_X_DEFAULT_CONDITIONS']
__all__ += ['deltaH', 'hue_angle', 'hue_quadrature', 'naka_rushton',
 'cam_structure_ciecam02_cam16', 'camucs_structure',
 'ciecam02', 'cam16', 'cam02ucs', 'cam16ucs']
__all__ += ['xyz_to_jabM_ciecam02', 'jabM_ciecam02_to_xyz',
 'xyz_to_jabC_ciecam02', 'jabC_ciecam02_to_xyz',
 'xyz_to_jabM_cam16', 'jabM_cam16_to_xyz',
 'xyz_to_jabC_cam16', 'jabC_cam16_to_xyz',
 'xyz_to_jab_cam02ucs', 'jab_cam02ucs_to_xyz',
 'xyz_to_jab_cam02lcd', 'jab_cam02lcd_to_xyz',
 'xyz_to_jab_cam02scd', 'jab_cam02scd_to_xyz',
 'xyz_to_jab_cam16ucs', 'jab_cam16ucs_to_xyz',
 'xyz_to_jab_cam16lcd', 'jab_cam16lcd_to_xyz',
 'xyz_to_jab_cam16scd', 'jab_cam16scd_to_xyz']
_CAM_02_X_AXES = {'jabM_ciecam02': ['J (ciecam02)', 'aM (ciecam02)', 'bM (ciecam02)']}
_CAM_02_X_AXES['jabC_ciecam02'] = ['J (ciecam02)', 'aC (ciecam02)', 'bC (ciecam02)']
_CAM_02_X_AXES['jabM_cam16'] = ['J (cam16)', 'aM (cam16)', 'bM (cam16)']
_CAM_02_X_AXES['jabC_cam16'] = ['J (cam16)', 'aC (cam16)', 'bC (cam16)']
_CAM_02_X_AXES['jab_cam02ucs'] = ["J' (cam02ucs)", "a' (cam02ucs)", "b' (cam02ucs)"]
_CAM_02_X_AXES['jab_cam02lcd'] = ["J' (cam02lcd)", "a' (cam02lcd)", "b' (cam02lcd)"]
_CAM_02_X_AXES['jab_cam02scd'] = ["J' (cam02scd)", "a' (cam02scd)", "b' (cam02scd)"]
_CAM_02_X_UNIQUE_HUE_DATA = {'parameters': 'hues i hi ei Hi'.split()}
_CAM_02_X_UNIQUE_HUE_DATA['models'] = 'ciecam97s ciecam02 cam16'.split()
_CAM_02_X_UNIQUE_HUE_DATA['ciecam97s'] = {'hues':'red yellow green blue red'.split(),  'i':np.arange(5.0),  'hi':[20.14, 90.0, 164.25, 237.53, 380.14],  'ei':[0.8, 0.7, 1.0, 1.2, 0.8],  'Hi':[0.0, 100.0, 200.0, 300.0, 400.0]}
_CAM_02_X_UNIQUE_HUE_DATA['ciecam02'] = _CAM_02_X_UNIQUE_HUE_DATA['ciecam97s']
_CAM_02_X_UNIQUE_HUE_DATA['cam16'] = {'hues':'red yellow green blue red'.split(),  'i':np.arange(5.0),  'hi':[20.14, 90.0, 164.25, 237.53, 380.14],  'ei':[0.8, 0.7, 1.0, 1.2, 0.8],  'Hi':[0.0, 100.0, 200.0, 300.0, 400.0]}
_UNIQUE_HUE_DATA = _CAM_02_X_UNIQUE_HUE_DATA
_CAM_02_X_SURROUND_PARAMETERS = {'parameters': 'c Nc F FLL'.split()}
_CAM_02_X_SURROUND_PARAMETERS['models'] = 'ciecam97s ciecam02 cam16'.split()
_CAM_02_X_SURROUND_PARAMETERS['ciecam97s'] = {'surrounds':['avg', 'avg,stim>4°', 'dim', 'dark', 'cutsheet'],  'avg':{'c':0.69,  'Nc':1.0,  'F':1.0,  'FLL':1.0},  'avg,stim>4°':{'c':0.69,  'Nc':1.0,  'F':1.0,  'FLL':0.0},  'dim':{'c':0.59,  'Nc':1.1,  'F':0.9,  'FLL':1.0},  'dark':{'c':0.525,  'Nc':0.8,  'F':0.9,  'FLL':1.0},  'cutsheet':{'c':0.41,  'Nc':0.8,  'F':0.9,  'FLL':1.0}}
_CAM_02_X_SURROUND_PARAMETERS['ciecam02'] = {'surrounds':['avg', 'dim', 'dark'],  'avg':{'c':0.69,  'Nc':1.0,  'F':1.0,  'FLL':1.0},  'dim':{'c':0.59,  'Nc':0.9,  'F':0.9,  'FLL':1.0},  'dark':{'c':0.525,  'Nc':0.8,  'F':0.8,  'FLL':1.0}}
_CAM_02_X_SURROUND_PARAMETERS['cam16'] = {'surrounds':['avg', 'dim', 'dark'],  'avg':{'c':0.69,  'Nc':1.0,  'F':1.0,  'FLL':1.0},  'dim':{'c':0.59,  'Nc':0.9,  'F':0.9,  'FLL':1.0},  'dark':{'c':0.525,  'Nc':0.8,  'F':0.8,  'FLL':1.0}}
_CAM_02_X_NAKA_RUSHTON_PARAMETERS = {'parameters': 'n sig scaling noise'.split()}
_CAM_02_X_NAKA_RUSHTON_PARAMETERS['models'] = 'ciecam02 ciecam97s cam15u cam16'.split()
_CAM_02_X_NAKA_RUSHTON_PARAMETERS['ciecam02'] = {'n':0.42,  'sig':2588.068098016295,  'scaling':400.0,  'noise':0.1}
_CAM_02_X_NAKA_RUSHTON_PARAMETERS['ciecam97s'] = {'n':0.73,  'sig':2.584460250810935,  'scaling':40.0,  'noise':1.0}
_CAM_02_X_NAKA_RUSHTON_PARAMETERS['cam16'] = {'n':0.42,  'sig':2588.068098016295,  'scaling':400.0,  'noise':0.1}
_NAKA_RUSHTON_PARAMETERS = _CAM_02_X_NAKA_RUSHTON_PARAMETERS
_CAM_02_X_UCS_PARAMETERS = {'ciecam02': {'none':{'KL':1.0,  'c1':0,  'c2':0},  'ucs':{'KL':1.0,  'c1':0.007,  'c2':0.0228},  'lcd':{'KL':0.77,  'c1':0.007,  'c2':0.0053},  'scd':{'KL':1.24,  'c1':0.007,  'c2':0.0363}}}
_CAM_02_X_UCS_PARAMETERS['cam16'] = {'none':{'KL':1.0,  'c1':0,  'c2':0},  'ucs':{'KL':1.0,  'c1':0.007,  'c2':0.0228},  'lcd':{'KL':0.77,  'c1':0.007,  'c2':0.0053},  'scd':{'KL':1.24,  'c1':0.007,  'c2':0.0363}}
_CAM_02_X_DEFAULT_TYPE = 'ciecam02'
_CAM_02_X_DEFAULT_WHITE_POINT = np2d([100.0, 100.0, 100.0])
_CAM_02_X_DEFAULT_CONDITIONS = {'La':100.0,  'Yb':20.0,  'surround':'avg',  'D':1.0,  'Dtype':None}
_CAM_02_X_DEFAULT_MCAT = 'cat02'

def naka_rushton(data, sig=2.0, n=0.73, scaling=1.0, noise=0.0, cam=None, direction='forward'):
    """
    Apply a Naka-Rushton response compression (n) and an adaptive shift (sig).
    
    | NK(x) = sign(x) * scaling * ((abs(x)**n) / ((abs(x)**n) + (sig**n))) + noise
    
    Args:
        :data:
            | float or ndarray
        :sig: 
            | 2.0, optional
            | Semi-saturation constant. Value for which NK(:data:) is 1/2
        :n: 
            | 0.73, optional
            | Compression power.
        :scaling:
            | 1.0, optional
            | Maximum value of NK-function.
        :noise:
            | 0.0, optional
            | Cone excitation noise.
        :cam: 
            | None or str, optional
            | Use NK parameters values specific to the color appearance model.
            | See .cam._NAKA_RUSHTON_PARAMETERS['models'] for supported types.
        :direction:
            | 'forward' or 'inverse', optional
            | Perform either NK(x) or NK(x)**(-1).
    
    Returns:
        :returns: 
            | float or ndarray with NK-(de)compressed input :x:        
    """
    if cam is not None:
        n = _NAKA_RUSHTON_PARAMETERS[cam]['n']
        sig = _NAKA_RUSHTON_PARAMETERS[cam]['sig']
        scaling = _NAKA_RUSHTON_PARAMETERS[cam]['scaling']
        noise = _NAKA_RUSHTON_PARAMETERS[cam]['noise']
    else:
        if direction == 'forward':
            return np.sign(data) * scaling * (np.abs(data) ** n / (np.abs(data) ** n + sig ** n)) + noise
        else:
            if direction == 'inverse':
                Ip = sig * (np.abs(np.abs(data) - noise) / (scaling - np.abs(np.abs(data) - noise))) ** (1 / n)
                p = np.isscalar(Ip) or np.where(np.abs(data) < noise)
                Ip[p] = -Ip[p]
            elif np.abs(data) < noise:
                Ip = -Ip
            return Ip


def hue_angle(a, b, htype='deg'):
    """
    Calculate positive hue angle (0°-360° or 0 - 2*pi rad.) 
    from opponent signals a and b.
    
    Args:
        :a: 
            | ndarray of a-coordinates
        :b: 
            | ndarray of b-coordinates
        :htype: 
            | 'deg' or 'rad', optional
            |   - 'deg': hue angle between 0° and 360°
            |   - 'rad': hue angle between 0 and 2pi radians
    Returns:
        :returns:
            | ndarray of positive hue angles.
    """
    return math.positive_arctan(a, b, htype=htype)


def hue_quadrature(h, unique_hue_data=None):
    """
    Get hue quadrature H from h.
    
    Args:
        :h: 
            | float or ndarray [(N,) or (N,1)] with hue data in degrees (!).
        :unique_hue data:
            | None or str or dict, optional
            |   - None: H = h.
            |   - str: CAM specifier that gets parameters from .cam._UNIQUE_HUE_DATA
            |          (For supported models, see .cam._UNIQUE_HUE_DATA['models'])
            |   - dict: user specified unique hue data 
            |          (see luxpy.cam._UNIQUE_HUE_DATA for expected structure)
    
    Returns:
        :H: 
            | ndarray of Hue quadrature value(s).
    """
    if unique_hue_data is None:
        return h
    else:
        if isinstance(unique_hue_data, str):
            unique_hue_data = _UNIQUE_HUE_DATA[unique_hue_data]
        else:
            changed_number_to_array = False
            if isinstance(h, float) | isinstance(h, int):
                h = np.atleast_1d(h)
                changed_number_to_array = True
            squeezed = False
            if h.ndim > 1:
                if h.shape[0] == 1:
                    h = np.squeeze(h, axis=0)
                    squeezed = True
            hi = unique_hue_data['hi']
            Hi = unique_hue_data['Hi']
            ei = unique_hue_data['ei']
            h[(h < hi[0])] += 360.0
            h_tmp = np.atleast_2d(h)
            if h_tmp.shape[0] == 1:
                h_tmp = h_tmp.T
            h_hi = np.repeat(h_tmp, repeats=(len(hi)), axis=1)
            hi_h = np.repeat((np.atleast_2d(hi)), repeats=(h.shape[0]), axis=0)
            d = h_hi - hi_h
            d[d < 0] = 1000.0
            p = d.argmin(axis=1)
            p[p == len(hi) - 1] = 0
            H = np.array([Hi[pi] + 100.0 * (h[i] - hi[pi]) / ei[pi] / ((h[i] - hi[pi]) / ei[pi] + (hi[(pi + 1)] - h[i]) / ei[(pi + 1)]) for i, pi in enumerate(p)])
            if changed_number_to_array:
                H = H[0]
            if squeezed:
                H = np.expand_dims(H, axis=0)
        return H


def deltaH(h1, C1, h2=None, C2=None, htype='deg'):
    """
    Compute a hue difference, dH = 2*C1*C2*sin(dh/2)
    
    Args:
        :h1:
            | hue for sample 1 (or hue difference if h2 is None)
        :C1: 
            | chroma of sample 1 (or prod C1*C2 if C2 is None)
        :h2: 
            | hue angle of sample 2 (if None, then h1 contains a hue difference)
        :C2: 
            | chroma of sample 2
        :htype: 
            | 'deg' or 'rad', optional
            |   - 'deg': hue angle between 0° and 360°
            |   - 'rad': hue angle between 0 and 2pi radians
    
    Returns:
        :returns:
            | ndarray of deltaH values.
    """
    if htype == 'deg':
        r2d = np.pi / 180
    else:
        r2d = 1.0
    if h2 is not None:
        deltah = h1 - h2
    else:
        deltah = h1
    if C2 is not None:
        Cprod = C1 * C2
    else:
        Cprod = C1
    return 2 * Cprod ** 0.5 * np.sin(r2d * deltah / 2)


def cam_structure_ciecam02_cam16(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, camtype=_CAM_02_X_DEFAULT_TYPE, mcat=None, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, direction='forward', outin='J,aM,bM', yellowbluepurplecorrect=False):
    """
    Convert between XYZ tristsimulus values and 
    ciecam02 /cam16 color appearance correlates.
    
    Args:
        :data: 
            | ndarray with input tristimulus values or 
              input color appearance correlates
            | Can be of shape: (N [, xM], x 3), whereby 
              N refers to samples, M to light sources.
        :xyzw:
            | _CAM_02_X_DEFAULT_WHITE_POINT or ndarray with tristimulus values
              of white point(s), optional
            | Can be multiple by specifying a Mx3 ndarray, instead of 1x3.
        :Yw: 
            | None, optional
            | Luminance factor of white point.
            | If None: xyz (in data) and xyzw are entered as relative tristimulus values 
            | (normalized to Yw = 100). 
            | If not None: input tristimulus are absolute and Yw is used to
            | rescale the absolute values to relative ones (relative to a 
            | reference perfect white diffuser with Ywr = 100). 
            | Yw can be < 100 for e.g. paper as white point. If Yw is None, it 
            | assumed that the relative Y-tristimulus value in xyzw represents 
            | the luminance factor Yw.
        :camtype: 
            | luxpy.cam._CAM_02_X_DEFAULT_TYPE, optional
            | Str specifier for CAM type to use, options: 'ciecam02' or 'cam16'.
        :mcat:
            | None or str or ndarray, optional
            | Specifies CAT sensor space.
            |   - None defaults to the one native to the camtype 
            |      (others e.g. 'cat02-bs', 'cat02-jiang',
            |      all trying to correct gamut problems of original cat02 matrix)
            |   - str: see see luxpy.cat._MCATS.keys() for options 
            |    (details on type, ?luxpy.cat)
            |   - ndarray: matrix with sensor primaries
        :condition:
            | luxpy.cam._CAM_02_X_DEFAULT_CONDITIONS, optional
            | Dict with condition parameters, D, La, surround ([c,Nc,F]), Yb
            | Can be user defined, but dict must have same structure.
        :direction:
            | 'forward' or 'inverse', optional
            |   -'forward': xyz -> ciecam02 / cam16
            |   -'inverse': ciecam02 / cam16 -> xyz 
            |    (input data must be:
            |         (J or Q, aM, bM) or 
            |         (J or Q, aC,bC) or 
            |         (J or Q, aS, bS) !!)
        :outin: 
            | 'J,aM,bM' or str, optional
            | Str specifying the type of 
            |   input (:direction: == 'inverse') and 
            |   output (:direction: == 'forward')
        :yellowbluepurplecorrect:
            | True or False, optional
            | Correct for yellow-blue and purple problems in ciecam02 
              (Is not used in cam16 because cat16 solves issues)
    
    Returns:
        :returns: 
            | ndarray with color appearance correlates (:direction: == 'forward')
            |   or 
            | XYZ tristimulus values (:direction: == 'inverse')
    
    References:
        1. `N. Moroney, M. D. Fairchild, R. W. G. Hunt, C. Li, M. R. Luo, and T. Newman, (2002), 
        "The CIECAM02 color appearance model,” 
        IS&T/SID Tenth Color Imaging Conference. p. 23, 2002.
        <http://rit-mcsl.org/fairchild/PDFs/PRO19.pdf>`_
        2. `C. Li, Z. Li, Z. Wang, Y. Xu, M. R. Luo, G. Cui, M. Melgosa, M. H. Brill, and M. Pointer, (2017), 
        “Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS,” 
        Color Res. Appl., p. n/a–n/a.
        <http://onlinelibrary.wiley.com/doi/10.1002/col.22131/abstract>`_

    """
    outin = outin.split(',')
    data = np2d(data)
    data_original_shape = data.shape
    if data.ndim == 2:
        data = data[:, None]
    else:
        if Yw is not None:
            Yw = np.atleast_2d(Yw)
            if Yw.shape[0] == 1:
                Yw = np.repeat(Yw, data.shape[1])
        else:
            Yw = xyzw[..., 1:2]
            if Yw.shape[0] == 1:
                Yw = np.repeat(Yw, data.shape[1])
            if xyzw.ndim < 3:
                if xyzw.shape[0] == 1:
                    xyzw = (xyzw * np.ones(data.shape[1:]))[None]
                else:
                    if xyzw.shape[0] == data.shape[1]:
                        xyzw = xyzw[None]
                    else:
                        xyzw = xyzw[:, None]
            if isinstance(conditions, dict):
                conditions = np.repeat(conditions, data.shape[1])
            dshape = list(data.shape)
            dshape[-1] = len(outin)
            camout = np.nan * np.ones(dshape)
            if camtype == 'ciecam02':
                if (mcat is None) | (mcat == 'cat02'):
                    mcat = cat._MCATS['cat02']
                    if yellowbluepurplecorrect == 'brill-suss':
                        mcat = cat._MCATS['cat02-bs']
                    else:
                        if yellowbluepurplecorrect == 'jiang-luo':
                            mcat = cat._MCATS['cat02-jiang-luo']
                else:
                    if isinstance(mcat, str):
                        mcat = cat._MCATS[mcat]
                invmcat = np.linalg.inv(mcat)
                mhpe = cat._MCATS['hpe']
                mhpe_x_invmcat = np.dot(mhpe, invmcat)
                if direction == 'inverse':
                    mcat_x_invmhpe = np.dot(mcat, np.linalg.inv(mhpe))
            else:
                if camtype == 'cam16':
                    if mcat is None:
                        mcat = cat._MCATS['cat16']
                    else:
                        if isinstance(mcat, str):
                            mcat = cat._MCATS[mcat]
                    invmcat = np.linalg.inv(mcat)
                else:
                    raise Exception('.cam.cam_structure_ciecam02_cam16(): Unrecognized camtype')
    for i in range(xyzw.shape[1]):
        D, Dtype, La, Yb, surround = [conditions[i][x] for x in sorted(conditions[i].keys())]
        if isinstance(surround, str):
            surround = _CAM_02_X_SURROUND_PARAMETERS[camtype][surround]
        F, FLL, Nc, c = [surround[x] for x in sorted(surround.keys())]
        k = 1.0 / (5.0 * La + 1.0)
        FL = 0.2 * k ** 4.0 * (5.0 * La) + 0.1 * (1.0 - k ** 4.0) ** 2.0 * (5.0 * La) ** 0.3333333333333333
        n = Yb / Yw[i]
        Nbb = 0.725 * (1 / n) ** 0.2
        Ncb = Nbb
        z = 1.48 + FLL * n ** 0.5
        yw = xyzw[:, i, 1, None]
        xyzwi = Yw[i] * xyzw[:, i] / yw
        if D is None:
            D = F * (1.0 - 0.2777777777777778 * np.exp((-La - 42.0) / 92.0))
        rgbw = np.dot(mcat, xyzwi.T)
        rgbwc = (D * Yw[i].T / rgbw + (1 - D)) * rgbw
        if camtype == 'ciecam02':
            rgbwp = np.dot(mhpe_x_invmcat, rgbwc).T
        else:
            if camtype == 'cam16':
                rgbwp = rgbwc.T
        pw = np.where(rgbwp < 0)
        if (yellowbluepurplecorrect == 'brill-suss') & (camtype == 'ciecam02'):
            rgbwp[pw] = 0.0
        rgbwpa = naka_rushton((FL * rgbwp / 100.0), cam=camtype)
        rgbwpa[pw] = 0.1 - (naka_rushton((FL * np.abs(rgbwp[pw]) / 100.0), cam=camtype) - 0.1)
        rwpa, gwpa, bwpa = asplit(rgbwpa)
        Aw = (2.0 * rwpa + gwpa + 0.05 * bwpa - 0.305) * Nbb
        if direction == 'forward':
            xyzi = Yw[i] * data[:, i] / yw
            rgb = np.dot(mcat, xyzi.T)
            rgbc = (Yw[i] * D / rgbw + (1 - D)) * rgb
            if camtype == 'ciecam02':
                rgbp = np.dot(mhpe_x_invmcat, rgbc).T
            else:
                if camtype == 'cam16':
                    rgbp = rgbc.T
                else:
                    p = np.where(rgbp < 0)
                    if (yellowbluepurplecorrect == 'brill-suss') & (camtype == 'ciecam02'):
                        rgbp[p] = 0.0
                    rgbpa = naka_rushton((FL * rgbp / 100.0), cam=camtype)
                    rgbpa[p] = 0.1 - (naka_rushton((FL * np.abs(rgbp[p]) / 100.0), cam=camtype) - 0.1)
                    rpa, gpa, bpa = asplit(rgbpa)
                    a = rpa - 12.0 * gpa / 11.0 + bpa / 11.0
                    b = 0.1111111111111111 * (rpa + gpa - 2.0 * bpa)
                    h = hue_angle(a, b, htype='deg')
                    et = 0.25 * (np.cos(h * np.pi / 180.0 + 2.0) + 3.8)
                    if 'H' in outin:
                        H = hue_quadrature(h, unique_hue_data=camtype)
                    else:
                        H = None
                    A = (2.0 * rpa + gpa + 0.05 * bpa - 0.305) * Nbb
                    if ('J' in outin) | ('Q' in outin) | ('C' in outin) | ('M' in outin) | ('s' in outin) | ('aS' in outin) | ('aC' in outin) | ('aM' in outin):
                        J = 100.0 * (A / Aw) ** (c * z)
                    if ('Q' in outin) | ('s' in outin) | ('aS' in outin):
                        Q = 4.0 / c * (J / 100.0) ** 0.5 * (Aw + 4.0) * FL ** 0.25
                    if ('C' in outin) | ('M' in outin) | ('s' in outin) | ('aS' in outin) | ('aC' in outin) | ('aM' in outin):
                        t = 3846.153846153846 * Nc * Ncb * et * (a ** 2.0 + b ** 2.0) ** 0.5 / (rpa + gpa + 1.05 * bpa)
                        C = t ** 0.9 * (J / 100.0) ** 0.5 * (1.64 - 0.29 ** n) ** 0.73
                    if ('M' in outin) | ('s' in outin) | ('aM' in outin) | ('aS' in outin):
                        M = C * FL ** 0.25
                    if ('s' in outin) | ('aS' in outin):
                        s = 100.0 * (M / Q) ** 0.5
                    if 'aS' in outin:
                        aS = s * np.cos(h * np.pi / 180.0)
                        bS = s * np.sin(h * np.pi / 180.0)
                    if 'aC' in outin:
                        aC = C * np.cos(h * np.pi / 180.0)
                        bC = C * np.sin(h * np.pi / 180.0)
                    if 'aM' in outin:
                        aM = M * np.cos(h * np.pi / 180.0)
                        bM = M * np.sin(h * np.pi / 180.0)
                if outin != ['J', 'aM', 'bM']:
                    out_i = eval('ajoin((' + ','.join(outin) + '))')
                else:
                    out_i = ajoin((J, aM, bM))
            camout[:, i] = out_i
        else:
            if direction == 'inverse':
                J, aMCs, bMCs = asplit(data[:, i])
                h = hue_angle(aMCs, bMCs, htype='deg')
                MCs = (aMCs ** 2.0 + bMCs ** 2.0) ** 0.5
                if 'Q' in outin:
                    Q = J.copy()
                    J = 100.0 * (Q / ((Aw + 4.0) * FL ** 0.25 * (4.0 / c))) ** 2.0
                if 'aS' in outin:
                    Q = 4.0 / c * (J / 100.0) ** 0.5 * (Aw + 4.0) * FL ** 0.25
                    M = Q * (MCs / 100.0) ** 2.0
                    C = M / FL ** 0.25
                if 'aM' in outin:
                    C = MCs / FL ** 0.25
                if 'aC' in outin:
                    C = MCs
                t = (C / ((J / 100.0) ** 0.5 * (1.64 - 0.29 ** n) ** 0.73)) ** 1.1111111111111112
                et = (np.cos(h * np.pi / 180.0 + 2.0) + 3.8) / 4.0
                A = Aw * (J / 100.0) ** (1.0 / (c * z))
                at = np.cos(h * np.pi / 180.0)
                bt = np.sin(h * np.pi / 180.0)
                p1 = 3846.153846153846 * Nc * Ncb * et / t
                p2 = A / Nbb + 0.305
                p3 = 1.05
                p4 = p1 / bt
                p5 = p1 / at
                q = np.where(np.abs(bt) < np.abs(at))[0]
                b = p2 * (2.0 + p3) * 0.32786885245901637 / (p4 + (2.0 + p3) * 0.15680684248039914 * (at / bt) - 0.01924447612259444 + p3 * 4.490377761938703)
                a = b * (at / bt)
                a[q] = p2[q] * (2.0 + p3) * 0.32786885245901637 / (p5[q] + (2.0 + p3) * 0.15680684248039914 - (0.01924447612259444 - p3 * 4.490377761938703) * (bt[q] / at[q]))
                b[q] = a[q] * (bt[q] / at[q])
                rpa = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0
                gpa = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0
                bpa = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0
                rgbpa = ajoin((rpa, gpa, bpa))
                rgbp = 100.0 / FL * naka_rushton(rgbpa, cam=camtype, direction='inverse')
                if (yellowbluepurplecorrect == 'brill-suss') & (camtype == 'ciecam02'):
                    p = np.where(rgbp < 0.0)
                    rgbp[p] = 0.0
                if camtype == 'ciecam02':
                    rgbc = np.dot(mcat_x_invmhpe, rgbp.T)
                else:
                    if camtype == 'cam16':
                        rgbc = rgbp.T
                rgb = rgbc / (Yw[i] * D / rgbw + (1.0 - D))
                xyzi = np.dot(invmcat, rgb).T
                xyzi = xyzi * yw / Yw[i]
                camout[:, i] = xyzi

    if len(data_original_shape) == 2:
        camout = camout[:, 0]
    return camout


def ciecam02(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, mcat='cat02', Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, direction='forward', outin='J,aM,bM', yellowbluepurplecorrect=False):
    """
    Convert between XYZ tristsimulus values and ciecam02 color appearance correlates.
    
    | Wrapper for luxpy.cam.cam_structure_ciecam02_cam16() designed specifically 
      for camtype = 'ciecam02.
    
    Args:
        :data: 
            | ndarray with input tristimulus values or 
              input color appearance correlates
            | Can be of shape: (N [, xM], x 3), whereby 
              N refers to samples, M to light sources.
        :xyzw:
            | _CAM_02_X_DEFAULT_WHITE_POINT or ndarray with tristimulus values
              of white point(s), optional
            | Can be multiple by specifying a Mx3 ndarray, instead of 1x3.
        :Yw: 
            | None, optional
            | Luminance factor of white point.
            | If None: xyz (in data) and xyzw are entered as relative tristimulus values 
            | (normalized to Yw = 100). 
            | If not None: input tristimulus are absolute and Yw is used to
            | rescale the absolute values to relative ones (relative to a 
            | reference perfect white diffuser with Ywr = 100). 
            | Yw can be < 100 for e.g. paper as white point. If Yw is None, it 
            | assumed that the relative Y-tristimulus value in xyzw represents 
            | the luminance factor Yw.       
        :mcat:
            | 'cat02' or str or ndarray, optional
            | Specifies CAT sensor space.
            |   - None defaults to the one native to the camtype 
            |      (others e.g. 'cat02-bs', 'cat02-jiang',
            |      all trying to correct gamut problems of original cat02 matrix)
            |   - str: see see luxpy.cat._MCATS.keys() for options 
            |    (details on type, ?luxpy.cat)
            |   - ndarray: matrix with sensor primaries
        :condition:
            | luxpy.cam._CAM_02_X_DEFAULT_CONDITIONS, optional
            | Dict with condition parameters, D, La, surround ([c,Nc,F]), Yb
            | Can be user defined, but dict must have same structure.
        :direction:
            | 'forward' or 'inverse', optional
            |   -'forward': xyz -> ciecam02 
            |   -'inverse': ciecam02 -> xyz 
            |    (input data must be:
            |         (J or Q, aM, bM) or 
            |         (J or Q, aC,bC) or 
            |         (J or Q, aS, bS) !!)
        :outin: 
            | 'J,aM,bM' or str, optional
            | Str specifying the type of 
            |   input (:direction: == 'inverse') and 
            |   output (:direction: == 'forward')
        :yellowbluepurplecorrect:
            | True or False, optional
            | Correct for yellow-blue and purple problems in ciecam02 
              (Is not used in cam16 because cat16 solves issues)
    
    Returns:
        :returns: 
            | ndarray with color appearance correlates (:direction: == 'forward') 
            |  or 
            | XYZ tristimulus values (:direction: == 'inverse')
    
    References:
        1. `N. Moroney, M. D. Fairchild, R. W. G. Hunt, C. Li, M. R. Luo, and T. Newman, (2002), 
        "The CIECAM02 color appearance model,” 
        IS&T/SID Tenth Color Imaging Conference. p. 23, 2002.
        <http://rit-mcsl.org/fairchild/PDFs/PRO19.pdf>`_
    
    """
    return cam_structure_ciecam02_cam16(data, xyzw, camtype='ciecam02', mcat=mcat, Yw=Yw, conditions=conditions, direction=direction, outin=outin, yellowbluepurplecorrect=yellowbluepurplecorrect)


def cam16(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, mcat='cat16', Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, direction='forward', outin='J,aM,bM'):
    """
    Convert between XYZ tristsimulus values and cam16 color appearance correlates.
    
   | Wrapper for luxpy.cam.cam_structure_ciecam02_cam16() designed specifically 
     for camtype = 'cam16'.
    
    Args:
        :data: 
            | ndarray with input tristimulus values or 
              input color appearance correlates
            | Can be of shape: (N [, xM], x 3), whereby 
              N refers to samples, M to light sources.
        :xyzw:
            | _CAM_02_X_DEFAULT_WHITE_POINT or ndarray with tristimulus values
              of white point(s), optional
            | Can be multiple by specifying a Mx3 ndarray, instead of 1x3.
        :Yw: 
            | None, optional
            | Luminance factor of white point.
            | If None: xyz (in data) and xyzw are entered as relative tristimulus values 
            | (normalized to Yw = 100). 
            | If not None: input tristimulus are absolute and Yw is used to
            | rescale the absolute values to relative ones (relative to a 
            | reference perfect white diffuser with Ywr = 100). 
            | Yw can be < 100 for e.g. paper as white point. If Yw is None, it 
            | assumed that the relative Y-tristimulus value in xyzw represents 
            | the luminance factor Yw.        
        :mcat:
            | 'cat16' or str or ndarray, optional
            | Specifies CAT sensor space.
            |   - None defaults back to 'cat02!'. 
            |      (others e.g. 'cat02-bs', 'cat02-jiang',
            |      all trying to correct gamut problems of original cat02 matrix)
            |   - str: see see luxpy.cat._MCATS.keys() for options 
            |    (details on type, ?luxpy.cat)
            |   - ndarray: matrix with sensor primaries
        :condition:
            | luxpy.cam._CAM_02_X_DEFAULT_CONDITIONS, optional
            | Dict with condition parameters, D, La, surround ([c,Nc,F]), Yb
            | Can be user defined, but dict must have same structure.
        :direction:
            | 'forward' or 'inverse', optional
            |   -'forward': xyz -> cam16
            |   -'inverse': cam16 -> xyz 
            |    (input data must be:
            |         (J or Q, aM, bM) or 
            |         (J or Q, aC,bC) or 
            |         (J or Q, aS, bS) !!)
        :outin: 
            | 'J,aM,bM' or str, optional
            | Str specifying the type of 
            |   input (:direction: == 'inverse') and 
            |   output (:direction: == 'forward')
    
    Returns:
        :returns: 
            | ndarray with color appearance correlates (:direction: == 'forward') 
            |  or 
            | XYZ tristimulus values (:direction: == 'inverse')
    
    References:
        ..[1] C. Li, Z. Li, Z. Wang, Y. Xu, M. R. Luo, G. Cui, M. Melgosa, M. H. Brill, and M. Pointer, 
            “Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS,” 
            Color Res. Appl., p. n/a–n/a.
 
    """
    return cam_structure_ciecam02_cam16(data, xyzw, camtype='cam16', mcat=mcat, Yw=Yw, conditions=conditions, direction=direction, outin=outin, yellowbluepurplecorrect=False)


def camucs_structure(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, camtype=_CAM_02_X_DEFAULT_TYPE, mcat=None, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, direction='forward', outin='J,aM,bM', ucstype='ucs', yellowbluepurplecorrect=False):
    """
    Convert between XYZ tristsimulus values 
    and camucs type color appearance correlates.
    
    | Wrapper for luxpy.cam.cam_structure_ciecam02_cam16() with additional 
      compression of color attributes
      for the following case:
    |    - 'none': original cam space
    |    - 'ucs': for uniform color space
    |    - 'lcd': for large color differences
    |    - 'scd': for small color differences
    
    Args:
        :data: 
            | ndarray with input tristimulus values or 
              input color appearance correlates
            | Can be of shape: (N [, xM], x 3), whereby 
              N refers to samples, M to light sources.
        :xyzw:
            | _CAM_02_X_DEFAULT_WHITE_POINT or ndarray with tristimulus values
              of white point(s), optional
            | Can be multiple by specifying a Mx3 ndarray, instead of 1x3.
        :Yw: 
            | None, optional
            | Luminance factor of white point.
            | If None: xyz (in data) and xyzw are entered as relative tristimulus values 
            | (normalized to Yw = 100). 
            | If not None: input tristimulus are absolute and Yw is used to
            | rescale the absolute values to relative ones (relative to a 
            | reference perfect white diffuser with Ywr = 100). 
            | Yw can be < 100 for e.g. paper as white point. If Yw is None, it 
            | assumed that the relative Y-tristimulus value in xyzw represents 
            | the luminance factor Yw.      
        :camtype: 
            | luxpy.cam._CAM_02_X_DEFAULT_TYPE, optional
            | Str specifier for CAM type to use, options: 'ciecam02' or 'cam16'.
        :mcat:
            | None or str or ndarray, optional
            | Specifies CAT sensor space.
            |   - None defaults to the one native to the camtype 
            |      (others e.g. 'cat02-bs', 'cat02-jiang',
            |      all trying to correct gamut problems of original cat02 matrix)
            |   - str: see see luxpy.cat._MCATS.keys() for options 
            |    (details on type, ?luxpy.cat)
            |   - ndarray: matrix with sensor primaries
        :condition:
            | luxpy.cam._CAM_02_X_DEFAULT_CONDITIONS, optional
            | Dict with condition parameters, D, La, surround ([c,Nc,F]), Yb
            | Can be user defined, but dict must have same structure.
        :direction:
            | 'forward' or 'inverse', optional
            |   -'forward': xyz -> camucs
            |   -'inverse': camucs -> xyz 
            |    (input data must be:
            |         (J or Q, aM, bM) or 
            |         (J or Q, aC,bC) or 
            |         (J or Q, aS, bS) !!)
        :outin: 
            | 'J,aM,bM' or str, optional
            | Str specifying the type of 
            |   input (:direction: == 'inverse') and 
            |   output (:direction: == 'forward')
        :yellowbluepurplecorrect:
            | True or False, optional
            | Correct for yellow-blue and purple problems in ciecam02 
              (Is not used in cam16 because cat16 solves issues)
        :ucstype: 
            |'ucs' or 'lcd' or 'scd', optional
            | Str specifier for which type of color attribute compression 
            | parameters to use:
            |     -'ucs': uniform color space, 
            |     -'lcd', large color differences, 
            |     -'scd': small color differences
                         
    Returns:
        :returns: 
            | ndarray with color appearance correlates (:direction: == 'forward') 
            |  or 
            | XYZ tristimulus values (:direction: == 'inverse')
    
    References:
        1. `C. Li, Z. Li, Z. Wang, Y. Xu, M. R. Luo, G. Cui, M. Melgosa, M. H. Brill, and M. Pointer, (2017), 
        “Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS,” 
        Color Res. Appl., p. n/a–n/a.
        <http://onlinelibrary.wiley.com/doi/10.1002/col.22131/abstract>`_
    
    """
    if mcat == None:
        if camtype == 'ciecam02':
            mcat = 'cat02'
        elif camtype == 'cam16':
            mcat = 'cat16'
    else:
        KL, c1, c2 = [_CAM_02_X_UCS_PARAMETERS[camtype][ucstype][x] for x in sorted(_CAM_02_X_UCS_PARAMETERS[camtype][ucstype].keys())]
        if direction == 'forward':
            J, aM, bM = asplit(cam_structure_ciecam02_cam16(data, xyzw=xyzw, camtype=camtype, Yw=Yw, conditions=conditions, direction='forward', outin=outin, yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat))
            M = (aM ** 2.0 + bM ** 2.0) ** 0.5
            h = np.arctan2(bM, aM)
            Jp = (1.0 + 100.0 * c1) * J / (1.0 + c1 * J)
            if c2 == 0:
                Mp = M
            else:
                Mp = 1.0 / c2 * np.log(1.0 + c2 * M)
            aMp = Mp * np.cos(h)
            bMp = Mp * np.sin(h)
            return ajoin((Jp, aMp, bMp))
        if direction == 'inverse':
            Jp, aMp, bMp = asplit(data)
            h = np.arctan2(bMp, aMp)
            Mp = (aMp ** 2.0 + bMp ** 2.0) ** 0.5
            M = (np.exp(c2 * Mp) - 1.0) / c2
            aM = M * np.cos(h)
            bM = M * np.sin(h)
            J = Jp / (1.0 + (100.0 - Jp) * c1)
            data = ajoin((J, aM, bM))
            return cam_structure_ciecam02_cam16(data, xyzw=xyzw, camtype=camtype, Yw=Yw, conditions=conditions, direction='inverse', outin='J,aM,bM', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def cam02ucs(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, direction='forward', ucstype='ucs', yellowbluepurplecorrect=False, mcat='cat02'):
    """
    Convert between XYZ tristsimulus values 
    and cam02ucs type color appearance correlates.
    
    | Wrapper for luxpy.cam.camucs_structure() specifically 
      designed for 'ciecam02' + 'ucs'
    
    Args:
        :data: 
            | ndarray with input tristimulus values or 
              input color appearance correlates
            | Can be of shape: (N [, xM], x 3), whereby 
              N refers to samples, M to light sources.
        :xyzw:
            | _CAM_02_X_DEFAULT_WHITE_POINT or ndarray with tristimulus values
              of white point(s), optional
            | Can be multiple by specifying a Mx3 ndarray, instead of 1x3.
        :Yw: 
            | None, optional
            | Luminance factor of white point.
            | If None: xyz (in data) and xyzw are entered as relative tristimulus values 
            | (normalized to Yw = 100). 
            | If not None: input tristimulus are absolute and Yw is used to
            | rescale the absolute values to relative ones (relative to a 
            | reference perfect white diffuser with Ywr = 100). 
            | Yw can be < 100 for e.g. paper as white point. If Yw is None, it 
            | assumed that the relative Y-tristimulus value in xyzw represents 
            | the luminance factor Yw.        
        :mcat:
            | 'cat02' or str or ndarray, optional
            | Specifies CAT sensor space.
            |   - None defaults to the one native to the camtype 
            |      (others e.g. 'cat02-bs', 'cat02-jiang',
            |      all trying to correct gamut problems of original cat02 matrix)
            |   - str: see see luxpy.cat._MCATS.keys() for options 
            |     (details on type, ?luxpy.cat)
            |   - ndarray: matrix with sensor primaries
        :condition:
            | luxpy.cam._CAM_02_X_DEFAULT_CONDITIONS, optional
            | Dict with condition parameters, D, La, surround ([c,Nc,F]), Yb
            | Can be user defined, but dict must have same structure.
        :direction:
            | 'forward' or 'inverse', optional
            |   -'forward': xyz -> cam02ucs
            |   -'inverse': cam02ucs -> xyz 
            |    (input data must be:
            |         (J or Q, aM, bM) or 
            |         (J or Q, aC,bC) or 
            |         (J or Q, aS, bS) !!)
        :outin: 
            | 'J,aM,bM' or str, optional
            | Str specifying the type of 
            |   input (:direction: == 'inverse') and 
            |   output (:direction: == 'forward')
        :yellowbluepurplecorrect:
            | True or False, optional
            | Correct for yellow-blue and purple problems in ciecam02 
              (Is not used in cam16 because cat16 solves issues)
        :ucstype: 
            | 'ucs' or 'lcd' or 'scd', optional
            | Str specifier for which type of color attribute compression 
            | parameters to use:
            |     -'ucs': uniform color space, 
            |     -'lcd', large color differences, 
            |     -'scd': small color differences
                         
    Returns:
        :returns: 
            | ndarray with color appearance correlates (:direction: == 'forward') 
            |  or 
            | XYZ tristimulus values (:direction: == 'inverse')
     
    References:
        1. `M.R. Luo, G. Cui, and C. Li, 
        'Uniform colour spaces based on CIECAM02 colour appearance model,' 
        Color Res. Appl., vol. 31, no. 4, pp. 320–330, 2006.
        <http://onlinelibrary.wiley.com/doi/10.1002/col.20227/abstract)>`_
    """
    return camucs_structure(data, xyzw=xyzw, camtype='ciecam02', mcat=mcat, Yw=Yw, conditions=conditions, direction=direction, ucstype=ucstype, yellowbluepurplecorrect=yellowbluepurplecorrect)


def cam16ucs(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, direction='forward', ucstype='ucs', mcat='cat16'):
    """
    Convert between XYZ tristsimulus values and cam16ucs type color appearance correlates.
    
    | Wrapper for luxpy.cam.camucs_structure() 
      specifically designed for 'cam16' + 'ucs'
    
    Args:
        :data: 
            | ndarray with input tristimulus values or 
              input color appearance correlates
            | Can be of shape: (N [, xM], x 3), whereby 
              N refers to samples, M to light sources.
        :xyzw:
            | _CAM_02_X_DEFAULT_WHITE_POINT or ndarray with tristimulus values
              of white point(s), optional
            | Can be multiple by specifying a Mx3 ndarray, instead of 1x3.
        :Yw: 
            | None, optional
            | Luminance factor of white point.
            | If None: xyz (in data) and xyzw are entered as relative tristimulus values 
            | (normalized to Yw = 100). 
            | If not None: input tristimulus are absolute and Yw is used to
            | rescale the absolute values to relative ones (relative to a 
            | reference perfect white diffuser with Ywr = 100). 
            | Yw can be < 100 for e.g. paper as white point. If Yw is None, it 
            | assumed that the relative Y-tristimulus value in xyzw represents 
            | the luminance factor Yw.        .
        :mcat:
            | 'cat16' or str or ndarray, optional
            | Specifies CAT sensor space.
            |   - None defaults to 'cat02'!
            |      (others e.g. 'cat02-bs', 'cat02-jiang',
            |      all trying to correct gamut problems of original cat02 matrix)
            |   - str: see see luxpy.cat._MCATS.keys() for options 
            |    (details on type, ?luxpy.cat)
            |   - ndarray: matrix with sensor primaries
        :condition:
            | luxpy.cam._CAM_02_X_DEFAULT_CONDITIONS, optional
            | Dict with condition parameters, D, La, surround ([c,Nc,F]), Yb
            | Can be user defined, but dict must have same structure.
        :direction:
            | 'forward' or 'inverse', optional
            |   -'forward': xyz -> cam16ucs
            |   -'inverse': cam16ucs -> xyz 
            |    (input data must be:
            |         (J or Q, aM, bM) or 
            |         (J or Q, aC,bC) or 
            |         (J or Q, aS, bS) !!)
        :outin: 
            | 'J,aM,bM' or str, optional
            | Str specifying the type of 
            |   input (:direction: == 'inverse') and 
            |   output (:direction: == 'forward')
        :yellowbluepurplecorrect:
            | True or False, optional
            | Correct for yellow-blue and purple problems in ciecam02 
              (Is not used in cam16 because cat16 solves issues)
        :ucstype: 
            | 'ucs' or 'lcd' or 'scd', optional
            | Str specifier for which type of color attribute compression 
            | parameters to use:
            |     -'ucs': uniform color space, 
            |     -'lcd', large color differences, 
            |     -'scd': small color differences
                         
    Returns:
        :returns: 
            | ndarray with color appearance correlates (:direction: == 'forward') 
            |  or 
            | XYZ tristimulus values (:direction: == 'inverse')
     
    References:
        1. `M. R. Luo, G. Cui, and C. Li, (2006),
        “Uniform colour spaces based on CIECAM02 colour appearance model,” 
        Color Res. Appl., vol. 31, no. 4, pp. 320–330.
        <http://onlinelibrary.wiley.com/doi/10.1002/col.20227/abstract)>`_
        2. `C. Li, Z. Li, Z. Wang, Y. Xu, M. R. Luo, G. Cui, M. Melgosa, M. H. Brill, and M. Pointer, (2017), 
        “Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS,” 
        Color Res. Appl., p. n/a–n/a.
        <http://onlinelibrary.wiley.com/doi/10.1002/col.22131/abstract)>`_
     """
    return camucs_structure(data, xyzw=xyzw, camtype='cam16', mcat=mcat, Yw=Yw, conditions=conditions, direction=direction, ucstype=ucstype, yellowbluepurplecorrect=False)


def xyz_to_jabM_ciecam02(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for ciecam02 forward mode with J,aM,bM output.
    
    | For help on parameter details: ?luxpy.cam.ciecam02 
    """
    return ciecam02(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', outin='J,aM,bM', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def jabM_ciecam02_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for ciecam02 inverse mode with J,aM,bM input.
    
    | For help on parameter details: ?luxpy.cam.ciecam02 
    """
    return ciecam02(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', outin='J,aM,bM', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def xyz_to_jabC_ciecam02(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for ciecam02 forward mode with J,aC,bC output.
    
    | For help on parameter details: ?luxpy.cam.ciecam02 
    """
    return ciecam02(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', outin='J,aC,bC', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def jabC_ciecam02_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for ciecam02 inverse mode with J,aC,bC input.
    
    | For help on parameter details: ?luxpy.cam.ciecam02 
    """
    return ciecam02(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', outin='J,aC,bC', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def xyz_to_jab_cam02ucs(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for cam02ucs forward mode with J,aM,bM output.
    
    | For help on parameter details: ?luxpy.cam.cam02ucs 
    """
    return cam02ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', ucstype='ucs', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def jab_cam02ucs_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for cam02ucs inverse mode with J,aM,bM input.
    
    | For help on parameter details: ?luxpy.cam.cam02ucs 
    """
    return cam02ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', ucstype='ucs', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def xyz_to_jab_cam02lcd(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for cam02ucs forward mode with J,aMp,bMp output and ucstype = lcd.
    
    | For help on parameter details: ?luxpy.cam.cam02ucs 
    """
    return cam02ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', ucstype='lcd', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def jab_cam02lcd_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for cam02ucs inverse mode with J,aMp,bMp input and ucstype = lcd.
    
    | For help on parameter details: ?luxpy.cam.cam02ucs 
    """
    return cam02ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', ucstype='lcd', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def xyz_to_jab_cam02scd(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for cam02ucs forward mode with J,aMp,bMp output and ucstype = scd.
    
    | For help on parameter details: ?luxpy.cam.cam02ucs 
    """
    return cam02ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', ucstype='scd', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def jab_cam02scd_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, yellowbluepurplecorrect=None, mcat='cat02', **kwargs):
    """
    Wrapper function for cam02ucs inverse mode with J,aMp,bMp input and ucstype = scd.
    
    | For help on parameter details: ?luxpy.cam.cam02ucs 
    """
    return cam02ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', ucstype='scd', yellowbluepurplecorrect=yellowbluepurplecorrect, mcat=mcat)


def xyz_to_jabM_cam16(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16 forward mode with J,aM,bM output.
    
    | For help on parameter details: ?luxpy.cam.cam16 
    """
    return cam16(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', outin='J,aM,bM', mcat=mcat)


def jabM_cam16_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16 inverse mode with J,aM,bM input.
    
    | For help on parameter details: ?luxpy.cam.cam16 
    """
    return cam16(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', outin='J,aM,bM', mcat=mcat)


def xyz_to_jabC_cam16(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16 forward mode with J,aC,bC output.
    
    | For help on parameter details: ?luxpy.cam.cam16 
    """
    return cam16(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', outin='J,aC,bC', mcat=mcat)


def jabC_cam16_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16 inverse mode with J,aC,bC input.
    
    | For help on parameter details: ?luxpy.cam.cam16 
    """
    return cam16(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', outin='J,aC,bC', mcat=mcat)


def xyz_to_jab_cam16ucs(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16ucs forward mode with J,aM,bM output and ucstype = 'ucs'.
    
    | For help on parameter details: ?luxpy.cam.cam16ucs 
    """
    return cam16ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', ucstype='ucs', mcat=mcat)


def jab_cam16ucs_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16ucs inverse mode with J,aM,bM input and ucstype = 'ucs'.
    
    | For help on parameter details: ?luxpy.cam.cam16ucs 
    """
    return cam16ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', ucstype='ucs', mcat=mcat)


def xyz_to_jab_cam16lcd(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16ucs forward mode with J,aM,bM output and ucstype = 'lcd'.
    
    | For help on parameter details: ?luxpy.cam.cam16ucs 
    """
    return cam16ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', ucstype='lcd', mcat=mcat)


def jab_cam16lcd_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16ucs inverse mode with J,aM,bM input and ucstype = 'lcd'.
    
    | For help on parameter details: ?luxpy.cam.cam16ucs 
    """
    return cam16ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', ucstype='lcd', mcat=mcat)


def xyz_to_jab_cam16scd(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16ucs forward mode with J,aM,bM output and ucstype = 'scd'.
    
    | For help on parameter details: ?luxpy.cam.cam16ucs 
    """
    return cam16ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='forward', ucstype='scd', mcat=mcat)


def jab_cam16scd_to_xyz(data, xyzw=_CAM_02_X_DEFAULT_WHITE_POINT, Yw=None, conditions=_CAM_02_X_DEFAULT_CONDITIONS, mcat='cat16', **kwargs):
    """
    Wrapper function for cam16ucs inverse mode with J,aM,bM input  and ucstype = 'scd'. 
    
    | For help on parameter details: ?luxpy.cam.cam16ucs 
    """
    return cam16ucs(data, xyzw=xyzw, Yw=Yw, conditions=conditions, direction='inverse', ucstype='scd', mcat=mcat)