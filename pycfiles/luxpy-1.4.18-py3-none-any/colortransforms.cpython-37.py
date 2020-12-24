# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\ctf\colortransforms.py
# Compiled at: 2019-10-04 02:12:05
# Size of source mod 2**32: 41915 bytes
"""
Module with functions related to basic colorimetry
==================================================

Note
----

  Note that colorimetric data is always located in the last axis
  of the data arrays. (See also xyz specification in __doc__ string
  of luxpy.spd_to_xyz())

colortransforms.py
------------------

 :_CSPACE_AXES: dict with list[str,str,str] containing axis labels
                of defined cspaces
 :_IPT_M: Conversion matrix for IPT color space
  
 :_COLORTF_DEFAULT_WHITE_POINT : default white point for colortf (set at Illuminant E)

Supported chromaticity / colorspace functions:
  | * xyz_to_Yxy(), Yxy_to_xyz(): (X,Y,Z) <-> (Y,x,y);
  | * xyz_to_Yuv(), Yuv_to_Yxy(): (X,Y,Z) <-> CIE 1976 (Y,u',v');
  | * xyz_to_xyz(), lms_to_xyz(): (X,Y,Z) <-> (X,Y,Z); for use with colortf()
  | * xyz_to_lms(), lms_to_xyz(): (X,Y,Z) <-> (L,M,S) cone fundamental responses
  | * xyz_to_lab(), lab_to_xyz(): (X,Y,Z) <-> CIE 1976 (L*a*b*)
  | * xyz_to_luv(), luv_to_xyz(): (X,Y,Z) <-> CIE 1976 (L*u*v*)
  | * xyz_to_Vrb_mb(),Vrb_mb_to_xyz(): (X,Y,Z) <-> (V,r,b); [Macleod & Boyton, 1979]
  | * xyz_to_ipt(), ipt_to_xyz(): (X,Y,Z) <-> (I,P,T); (Ebner et al, 1998)
  | * xyz_to_Ydlep(), Ydlep_to_xyz(): (X,Y,Z) <-> (Y,dl, ep); 
  |                   Y, dominant wavelength (dl) and excitation purity (ep)
  | * xyz_to_srgb(), srgb_to_xyz(): (X,Y,Z) <-> sRGB; (IEC:61966 sRGB)
  | * xyz_to_jabz(), jabz_to_xyz(): (X,Y,Z) <-> (Jz,az,bz) (Safdar et al, 2017)

References
----------
    1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_
    2. `Ebner F, and Fairchild MD (1998).
       Development and testing of a color space (IPT) with improved hue uniformity.
       In IS&T 6th Color Imaging Conference, (Scottsdale, Arizona, USA), pp. 8–13.
       <http://www.ingentaconnect.com/content/ist/cic/1998/00001998/00000001/art00003?crawler=true>`_
    3. `MacLeod DI, and Boynton RM (1979).
       Chromaticity diagram showing cone excitation by stimuli of equal luminance.
       J. Opt. Soc. Am. 69, 1183–1186.
       <https://www.osapublishing.org/josa/abstract.cfm?uri=josa-69-8-1183>`_
    4. `Safdar, M., Cui, G., Kim,Y. J., and  Luo,M. R. (2017).
       Perceptually uniform color space for image signals including high dynamic range and wide gamut.
       Opt. Express, vol. 25, no. 13, pp. 15131–15151, Jun. 2017.
       <https://www.opticsexpress.org/abstract.cfm?URI=oe-25-13-15131>`_

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)

Created on Wed Jun 28 22:48:09 2017
"""
from luxpy import np, _CMF, _CIE_ILLUMINANTS, _CIEOBS, _CSPACE, math, spd_to_xyz, np2d, np2dT, np3d, todim, asplit, ajoin
__all__ = [
 '_CSPACE_AXES', '_IPT_M', 'xyz_to_Yxy', 'Yxy_to_xyz', 'xyz_to_Yuv', 'Yuv_to_xyz',
 'xyz_to_wuv', 'wuv_to_xyz', 'xyz_to_xyz', 'xyz_to_lms', 'lms_to_xyz', 'xyz_to_lab', 'lab_to_xyz', 'xyz_to_luv', 'luv_to_xyz',
 'xyz_to_Vrb_mb', 'Vrb_mb_to_xyz', 'xyz_to_ipt', 'ipt_to_xyz', 'xyz_to_Ydlep', 'Ydlep_to_xyz', 'xyz_to_srgb', 'srgb_to_xyz']
_CSPACE_AXES = {'Yxy': ['Y / L (cd/m²)', 'x', 'y']}
_CSPACE_AXES['Yuv'] = ['Y / L (cd/m²)', "u'", "v'"]
_CSPACE_AXES['xyz'] = ['X', 'Y', 'Z']
_CSPACE_AXES['lms'] = ['L', 'M', 'S']
_CSPACE_AXES['lab'] = ['L*', 'a*', 'b*']
_CSPACE_AXES['luv'] = ['L*', 'u*', 'v*']
_CSPACE_AXES['ipt'] = ['I', 'P', 'T']
_CSPACE_AXES['wuv'] = ['W*', 'U*', 'V*']
_CSPACE_AXES['Vrb_mb'] = ['V (Macleod-Boyton)', 'r (Macleod-Boyton)', 'b (Macleod-Boyton)']
_CSPACE_AXES['cct'] = ['', 'cct', 'duv']
_CSPACE_AXES['srgb'] = ['sR', 'sG', 'sB']
_IPT_M = {'lms2ipt':np.array([[0.4, 0.4, 0.2], [4.455, -4.851, 0.396], [0.8056, 0.3572, -1.1628]]), 
 'xyz2lms':{x:math.normalize_3x3_matrix(_CMF[x]['M'], spd_to_xyz((_CIE_ILLUMINANTS['D65']), cieobs=x)) for x in sorted(_CMF['types'])}}
_COLORTF_DEFAULT_WHITE_POINT = np.array([100.0, 100.0, 100.0])

def xyz_to_Yxy(xyz, **kwargs):
    """
    Convert XYZ tristimulus values CIE Yxy chromaticity values.

    Args:
        :xyz: 
            | ndarray with tristimulus values

    Returns:
        :Yxy: 
            | ndarray with Yxy chromaticity values
              (Y value refers to luminance or luminance factor)
    """
    xyz = np2d(xyz)
    Yxy = np.empty(xyz.shape)
    sumxyz = xyz[(Ellipsis, 0)] + xyz[(Ellipsis, 1)] + xyz[(Ellipsis, 2)]
    Yxy[(Ellipsis, 0)] = xyz[(Ellipsis, 1)]
    Yxy[(Ellipsis, 1)] = xyz[(Ellipsis, 0)] / sumxyz
    Yxy[(Ellipsis, 2)] = xyz[(Ellipsis, 1)] / sumxyz
    return Yxy


def Yxy_to_xyz(Yxy, **kwargs):
    """
    Convert CIE Yxy chromaticity values to XYZ tristimulus values.

    Args:
        :Yxy: 
            | ndarray with Yxy chromaticity values
              (Y value refers to luminance or luminance factor)

    Returns:
        :xyz: 
            | ndarray with tristimulus values
    """
    Yxy = np2d(Yxy)
    xyz = np.empty(Yxy.shape)
    xyz[(Ellipsis, 1)] = Yxy[(Ellipsis, 0)]
    xyz[(Ellipsis, 0)] = Yxy[(Ellipsis, 0)] * Yxy[(Ellipsis, 1)] / Yxy[(Ellipsis, 2)]
    xyz[(Ellipsis, 2)] = Yxy[(Ellipsis, 0)] * (1.0 - Yxy[(Ellipsis, 1)] - Yxy[(Ellipsis,
                                                                               2)]) / Yxy[(Ellipsis,
                                                                                           2)]
    return xyz


def xyz_to_Yuv(xyz, **kwargs):
    """
    Convert XYZ tristimulus values CIE 1976 Yu'v' chromaticity values.

    Args:
        :xyz: 
            | ndarray with tristimulus values

    Returns:
        :Yuv: 
            | ndarray with CIE 1976 Yu'v' chromaticity values
              (Y value refers to luminance or luminance factor)
    """
    xyz = np2d(xyz)
    Yuv = np.empty(xyz.shape)
    denom = xyz[(Ellipsis, 0)] + 15.0 * xyz[(Ellipsis, 1)] + 3.0 * xyz[(Ellipsis, 2)]
    Yuv[(Ellipsis, 0)] = xyz[(Ellipsis, 1)]
    Yuv[(Ellipsis, 1)] = 4.0 * xyz[(Ellipsis, 0)] / denom
    Yuv[(Ellipsis, 2)] = 9.0 * xyz[(Ellipsis, 1)] / denom
    return Yuv


def Yuv_to_xyz(Yuv, **kwargs):
    """
    Convert CIE 1976 Yu'v' chromaticity values to XYZ tristimulus values.

    Args:
        :Yuv: 
            | ndarray with CIE 1976 Yu'v' chromaticity values
              (Y value refers to luminance or luminance factor)

    Returns:
        :xyz: 
            | ndarray with tristimulus values
    """
    Yuv = np2d(Yuv)
    xyz = np.empty(Yuv.shape)
    xyz[(Ellipsis, 1)] = Yuv[(Ellipsis, 0)]
    xyz[(Ellipsis, 0)] = Yuv[(Ellipsis, 0)] * (9.0 * Yuv[(Ellipsis, 1)]) / (4.0 * Yuv[(Ellipsis,
                                                                                       2)])
    xyz[(Ellipsis, 2)] = Yuv[(Ellipsis, 0)] * (12.0 - 3.0 * Yuv[(Ellipsis, 1)] - 20.0 * Yuv[(Ellipsis,
                                                                                             2)]) / (4.0 * Yuv[(Ellipsis,
                                                                                                                2)])
    return xyz


def xyz_to_wuv(xyz, xyzw=_COLORTF_DEFAULT_WHITE_POINT, **kwargs):
    """
    Convert XYZ tristimulus values CIE 1964 U*V*W* color space.

    Args:
        :xyz: 
            | ndarray with tristimulus values
        :xyzw: 
            | ndarray with tristimulus values of white point, optional
              (Defaults to luxpy._COLORTF_DEFAULT_WHITE_POINT)

    Returns:
        :wuv: 
            | ndarray with W*U*V* values
    """
    Yuv = xyz_to_Yuv(np2d(xyz))
    Yuvw = xyz_to_Yuv(np2d(xyzw))
    wuv = np.empty(xyz.shape)
    wuv[(Ellipsis, 0)] = 25.0 * Yuv[(Ellipsis, 0)] ** 0.3333333333333333 - 17.0
    wuv[(Ellipsis, 1)] = 13.0 * wuv[(Ellipsis, 0)] * (Yuv[(Ellipsis, 1)] - Yuvw[(Ellipsis,
                                                                                 1)])
    wuv[(Ellipsis, 2)] = 13.0 * wuv[(Ellipsis, 0)] * (Yuv[(Ellipsis, 2)] - Yuvw[(Ellipsis,
                                                                                 2)]) * 0.6666666666666666
    return wuv


def wuv_to_xyz(wuv, xyzw=_COLORTF_DEFAULT_WHITE_POINT, **kwargs):
    """
    Convert CIE 1964 U*V*W* color space coordinates to XYZ tristimulus values.

    Args:
        :wuv: 
            | ndarray with W*U*V* values
        :xyzw: 
            | ndarray with tristimulus values of white point, optional
              (Defaults to luxpy._COLORTF_DEFAULT_WHITE_POINT)

    Returns:
        :xyz: 
            | ndarray with tristimulus values
         """
    wuv = np2d(wuv)
    Yuvw = xyz_to_Yuv(xyzw)
    Yuv = np.empty(wuv.shape)
    Yuv[(Ellipsis, 0)] = ((wuv[(Ellipsis, 0)] + 17.0) / 25.0) ** 3.0
    Yuv[(Ellipsis, 1)] = Yuvw[(Ellipsis, 1)] + wuv[(Ellipsis, 1)] / (13.0 * wuv[(Ellipsis,
                                                                                 0)])
    Yuv[(Ellipsis, 2)] = Yuvw[(Ellipsis, 2)] + wuv[(Ellipsis, 2)] / (13.0 * wuv[(Ellipsis,
                                                                                 0)]) * 1.5
    return Yuv_to_xyz(Yuv)


def xyz_to_xyz(xyz, **kwargs):
    """
    Convert XYZ tristimulus values to XYZ tristimulus values.

    Args:
        :xyz: 
            | ndarray with tristimulus values

    Returns:
        :xyz: 
            | ndarray with tristimulus values
    """
    return np2d(xyz)


def xyz_to_lms(xyz, cieobs=_CIEOBS, M=None, **kwargs):
    """
    Convert XYZ tristimulus values to LMS cone fundamental responses.

    Args:
        :xyz: 
            | ndarray with tristimulus values
        :cieobs: 
            | _CIEOBS or str, optional
        :M: 
            | None, optional
            | Conversion matrix for xyz to lms.
            |   If None: use the one defined by :cieobs:

    Returns:
        :lms: 
            | ndarray with LMS cone fundamental responses
    """
    xyz = np2d(xyz)
    if M is None:
        M = _CMF[cieobs]['M']
    elif len(xyz.shape) == 3:
        lms = np.einsum('ij,klj->kli', M, xyz)
    else:
        lms = np.einsum('ij,lj->li', M, xyz)
    return lms


def lms_to_xyz(lms, cieobs=_CIEOBS, M=None, **kwargs):
    """
    Convert LMS cone fundamental responses to XYZ tristimulus values.

    Args:
        :lms: 
            | ndarray with LMS cone fundamental responses
        :cieobs:
            | _CIEOBS or str, optional
        :M: 
            | None, optional
            | Conversion matrix for xyz to lms.
            |   If None: use the one defined by :cieobs:

    Returns:
        :xyz: 
            | ndarray with tristimulus values
    """
    lms = np2d(lms)
    if M is None:
        M = _CMF[cieobs]['M']
    elif len(lms.shape) == 3:
        xyz = np.einsum('ij,klj->kli', np.linalg.inv(M), lms)
    else:
        xyz = np.einsum('ij,lj->li', np.linalg.inv(M), lms)
    return xyz


def xyz_to_lab(xyz, xyzw=None, cieobs=_CIEOBS, **kwargs):
    """
    Convert XYZ tristimulus values to CIE 1976 L*a*b* (CIELAB) coordinates.

    Args:
        :xyz: 
            | ndarray with tristimulus values
        :xyzw:
            | None or ndarray with tristimulus values of white point, optional
            | None defaults to xyz of CIE D65 using the :cieobs: observer.
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set to use when calculating xyzw.

    Returns:
        :lab: 
            | ndarray with CIE 1976 L*a*b* (CIELAB) color coordinates
    """
    xyz = np2d(xyz)
    if xyzw is None:
        xyzw = spd_to_xyz((_CIE_ILLUMINANTS['D65']), cieobs=cieobs)
    XYZr = xyz / xyzw
    fXYZr = XYZr ** 0.3333333333333333
    pqr = XYZr <= 0.008856451679035631
    fXYZr[pqr] = 7.787037037037037 * XYZr[pqr] + 0.13793103448275862
    Lab = np.empty(xyz.shape)
    Lab[(Ellipsis, 0)] = 116.0 * fXYZr[(Ellipsis, 1)] - 16.0
    Lab[(pqr[(Ellipsis, 1)], 0)] = 903.3 * XYZr[(pqr[(Ellipsis, 1)], 1)]
    Lab[(Ellipsis, 1)] = 500.0 * (fXYZr[(Ellipsis, 0)] - fXYZr[(Ellipsis, 1)])
    Lab[(Ellipsis, 2)] = 200.0 * (fXYZr[(Ellipsis, 1)] - fXYZr[(Ellipsis, 2)])
    return Lab


def lab_to_xyz(lab, xyzw=None, cieobs=_CIEOBS, **kwargs):
    """
    Convert CIE 1976 L*a*b* (CIELAB) color coordinates to XYZ tristimulus values.

    Args:
        :lab: 
            | ndarray with CIE 1976 L*a*b* (CIELAB) color coordinates
        :xyzw:
            | None or ndarray with tristimulus values of white point, optional
            | None defaults to xyz of CIE D65 using the :cieobs: observer.
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set to use when calculating xyzw.

    Returns:
        :xyz: 
            | ndarray with tristimulus values
    """
    lab = np2d(lab)
    if xyzw is None:
        xyzw = spd_to_xyz((_CIE_ILLUMINANTS['D65']), cieobs=cieobs)
    xyzw = xyzw * np.ones(lab.shape)
    fXYZ = np.empty(lab.shape)
    fXYZ[(Ellipsis, 1)] = (lab[(Ellipsis, 0)] + 16.0) / 116.0
    fXYZ[(Ellipsis, 0)] = lab[(Ellipsis, 1)] / 500.0 + fXYZ[(Ellipsis, 1)]
    fXYZ[(Ellipsis, 2)] = fXYZ[(Ellipsis, 1)] - lab[(Ellipsis, 2)] / 200.0
    xyz = fXYZ ** 3.0 * xyzw
    pqr = fXYZ <= 0.20689655172413793
    xyz[pqr] = np.squeeze(xyzw[pqr] * ((fXYZ[pqr] - 0.13793103448275862) / 7.787037037037037))
    return xyz


def xyz_to_luv(xyz, xyzw=None, cieobs=_CIEOBS, **kwargs):
    """
    Convert XYZ tristimulus values to CIE 1976 L*u*v* (CIELUV) coordinates.

    Args:
        :xyz: 
            | ndarray with tristimulus values
        :xyzw:
            | None or ndarray with tristimulus values of white point, optional
            | None defaults to xyz of CIE D65 using the :cieobs: observer.
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set to use when calculating xyzw.

    Returns:
        :luv: 
            | ndarray with CIE 1976 L*u*v* (CIELUV) color coordinates
    """
    xyz = np2d(xyz)
    if xyzw is None:
        xyzw = spd_to_xyz((_CIE_ILLUMINANTS['D65']), cieobs=cieobs)
    Yuv = xyz_to_Yuv(xyz)
    Yuvw = xyz_to_Yuv(todim(xyzw, xyz.shape))
    luv = np.empty(xyz.shape)
    YdivYw = Yuv[(Ellipsis, 0)] / Yuvw[(Ellipsis, 0)]
    luv[(Ellipsis, 0)] = 116.0 * YdivYw ** 0.3333333333333333 - 16.0
    p = np.where(YdivYw <= 0.008856451679035631)
    luv[(Ellipsis, 0)][p] = 903.2962962962961 * YdivYw[p]
    luv[(Ellipsis, 1)] = 13.0 * luv[(Ellipsis, 0)] * (Yuv[(Ellipsis, 1)] - Yuvw[(Ellipsis,
                                                                                 1)])
    luv[(Ellipsis, 2)] = 13.0 * luv[(Ellipsis, 0)] * (Yuv[(Ellipsis, 2)] - Yuvw[(Ellipsis,
                                                                                 2)])
    return luv


def luv_to_xyz(luv, xyzw=None, cieobs=_CIEOBS, **kwargs):
    """
    Convert CIE 1976 L*u*v* (CIELUVB) coordinates to XYZ tristimulus values.

    Args:
        :luv: 
            | ndarray with CIE 1976 L*u*v* (CIELUV) color coordinates
        :xyzw:
            | None or ndarray with tristimulus values of white point, optional
            | None defaults to xyz of CIE D65 using the :cieobs: observer.
        :cieobs: 
            | luxpy._CIEOBS, optional
            | CMF set to use when calculating xyzw.

    Returns:
        :xyz: 
            | ndarray with tristimulus values
    """
    luv = np2d(luv)
    if xyzw is None:
        xyzw = spd_to_xyz((_CIE_ILLUMINANTS['D65']), cieobs=cieobs)
    Yuvw = todim((xyz_to_Yuv(xyzw)), (luv.shape), equal_shape=True)
    Yuv = np.empty(luv.shape)
    Yuv[..., 1:3] = luv[..., 1:3] / (13 * luv[(Ellipsis, 0)]) + Yuvw[..., 1:3]
    Yuv[Yuv[(Ellipsis, 0)] == 0, 1:3] = 0
    Yuv[(Ellipsis, 0)] = Yuvw[(Ellipsis, 0)] * ((luv[(Ellipsis, 0)] + 16.0) / 116.0) ** 3.0
    p = np.where(Yuv[(Ellipsis, 0)] / Yuvw[(Ellipsis, 0)] < 0.008856451679035631)
    Yuv[(Ellipsis, 0)][p] = Yuvw[(Ellipsis, 0)][p] * (luv[(Ellipsis, 0)][p] / 903.2962962962961)
    return Yuv_to_xyz(Yuv)


def xyz_to_Vrb_mb(xyz, cieobs=_CIEOBS, scaling=[1, 1], M=None, **kwargs):
    """
    Convert XYZ tristimulus values to V,r,b (Macleod-Boynton) color coordinates.

    | Macleod Boynton: V = R+G, r = R/V, b = B/V
    | Note that R,G,B ~ L,M,S

    Args:
        :xyz: 
            | ndarray with tristimulus values
        :cieobs: 
            | luxpy._CIEOBS, optional
            | CMF set to use when getting the default M, which is
              the xyz to lms conversion matrix.
        :scaling:
            | list of scaling factors for r and b dimensions.
        :M: 
            | None, optional
            | Conversion matrix for going from XYZ to RGB (LMS)
            |   If None, :cieobs: determines the M (function does inversion)

    Returns:
        :Vrb: 
            | ndarray with V,r,b (Macleod-Boynton) color coordinates

    Reference:
        1. `MacLeod DI, and Boynton RM (1979).
           Chromaticity diagram showing cone excitation by stimuli of equal luminance.
           J. Opt. Soc. Am. 69, 1183–1186.
           <https://www.osapublishing.org/josa/abstract.cfm?uri=josa-69-8-1183>`_
    """
    xyz = np2d(xyz)
    if M is None:
        M = _CMF[cieobs]['M']
    elif len(xyz.shape) == 3:
        RGB = np.einsum('ij,klj->kli', M, xyz)
    else:
        RGB = np.einsum('ij,lj->li', M, xyz)
    Vrb = np.empty(xyz.shape)
    Vrb[(Ellipsis, 0)] = RGB[(Ellipsis, 0)] + RGB[(Ellipsis, 1)]
    Vrb[(Ellipsis, 1)] = RGB[(Ellipsis, 0)] / Vrb[(Ellipsis, 0)] * scaling[0]
    Vrb[(Ellipsis, 2)] = RGB[(Ellipsis, 2)] / Vrb[(Ellipsis, 0)] * scaling[1]
    return Vrb


def Vrb_mb_to_xyz(Vrb, cieobs=_CIEOBS, scaling=[1, 1], M=None, Minverted=False, **kwargs):
    """
    Convert V,r,b (Macleod-Boynton) color coordinates to XYZ tristimulus values.

    | Macleod Boynton: V = R+G, r = R/V, b = B/V
    | Note that R,G,B ~ L,M,S

    Args:
        :Vrb: 
            | ndarray with V,r,b (Macleod-Boynton) color coordinates
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set to use when getting the default M, which is
              the xyz to lms conversion matrix.
        :scaling:
            | list of scaling factors for r and b dimensions.
        :M: 
            | None, optional
            | Conversion matrix for going from XYZ to RGB (LMS)
            |   If None, :cieobs: determines the M (function does inversion)
        :Minverted:
            | False, optional
            | Bool that determines whether M should be inverted.

    Returns:
        :xyz: 
            | ndarray with tristimulus values

    Reference:
        1. `MacLeod DI, and Boynton RM (1979).
           Chromaticity diagram showing cone excitation by stimuli of equal luminance.
           J. Opt. Soc. Am. 69, 1183–1186.
           <https://www.osapublishing.org/josa/abstract.cfm?uri=josa-69-8-1183>`_
    """
    Vrb = np2d(Vrb)
    RGB = np.empty(Vrb.shape)
    RGB[(Ellipsis, 0)] = Vrb[(Ellipsis, 1)] * Vrb[(Ellipsis, 0)] / scaling[0]
    RGB[(Ellipsis, 2)] = Vrb[(Ellipsis, 2)] * Vrb[(Ellipsis, 0)] / scaling[1]
    RGB[(Ellipsis, 1)] = Vrb[(Ellipsis, 0)] - RGB[(Ellipsis, 0)]
    if M is None:
        M = _CMF[cieobs]['M']
    if Minverted == False:
        M = np.linalg.inv(M)
    if len(RGB.shape) == 3:
        return np.einsum('ij,klj->kli', M, RGB)
    return np.einsum('ij,lj->li', M, RGB)


def xyz_to_ipt(xyz, cieobs=_CIEOBS, xyzw=None, M=None, **kwargs):
    """
    Convert XYZ tristimulus values to IPT color coordinates.

    | I: Lightness axis, P, red-green axis, T: yellow-blue axis.

    Args:
        :xyz: 
            | ndarray with tristimulus values
        :xyzw: 
            | None or ndarray with tristimulus values of white point, optional
            | None defaults to xyz of CIE D65 using the :cieobs: observer.
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set to use when calculating xyzw for rescaling M
              (only when not None).
        :M: | None, optional
            | None defaults to xyz to lms conversion matrix determined by :cieobs:

    Returns:
        :ipt: 
            | ndarray with IPT color coordinates

    Note:
        :xyz: is assumed to be under D65 viewing conditions! If necessary 
              perform chromatic adaptation !

    Reference:
        1. `Ebner F, and Fairchild MD (1998).
           Development and testing of a color space (IPT) with improved hue uniformity.
           In IS&T 6th Color Imaging Conference, (Scottsdale, Arizona, USA), pp. 8–13.
           <http://www.ingentaconnect.com/content/ist/cic/1998/00001998/00000001/art00003?crawler=true>`_
    """
    xyz = np2d(xyz)
    if M is None:
        M = _IPT_M['xyz2lms'][cieobs].copy()
        if xyzw is None:
            xyzw = spd_to_xyz((_CIE_ILLUMINANTS['D65']), cieobs=cieobs, out=1)[0] / 100.0
        else:
            xyzw = xyzw / 100.0
        M = math.normalize_3x3_matrix(M, xyzw)
    else:
        xyz = xyz / 100.0
        if np.ndim(M) == 2:
            if len(xyz.shape) == 3:
                lms = np.einsum('ij,klj->kli', M, xyz)
            else:
                lms = np.einsum('ij,lj->li', M, xyz)
        elif len(xyz.shape) == 3:
            lms = np.concatenate([np.einsum('ij,klj->kli', M[i], xyz[:, i:i + 1, :]) for i in range(M.shape[0])], axis=1)
        else:
            lms = np.concatenate([np.einsum('ij,lj->li', M[i], xyz[i:i + 1, :]) for i in range(M.shape[0])], axis=0)
        lmsp = lms ** 0.43
        p = np.where(lms < 0.0)
        lmsp[p] = -np.abs(lms[p]) ** 0.43
        if len(xyz.shape) == 3:
            ipt = np.einsum('ij,klj->kli', _IPT_M['lms2ipt'], lmsp)
        else:
            ipt = np.einsum('ij,lj->li', _IPT_M['lms2ipt'], lmsp)
    return ipt


def ipt_to_xyz(ipt, cieobs=_CIEOBS, xyzw=None, M=None, **kwargs):
    """
    Convert XYZ tristimulus values to IPT color coordinates.

    | I: Lightness axis, P, red-green axis, T: yellow-blue axis.

    Args:
        :ipt: 
            | ndarray with IPT color coordinates
        :xyzw:
            | None or ndarray with tristimulus values of white point, optional
            | None defaults to xyz of CIE D65 using the :cieobs: observer.
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set to use when calculating xyzw for rescaling Mxyz2lms
              (only when not None).
        :M: | None, optional
            | None defaults to xyz to lms conversion matrix determined by:cieobs:

    Returns:
        :xyz: 
            | ndarray with tristimulus values

    Note:
        :xyz: is assumed to be under D65 viewing conditions! If necessary 
              perform chromatic adaptation !

    Reference:
        1. `Ebner F, and Fairchild MD (1998).
           Development and testing of a color space (IPT) with improved hue uniformity.
           In IS&T 6th Color Imaging Conference, (Scottsdale, Arizona, USA), pp. 8–13.
           <http://www.ingentaconnect.com/content/ist/cic/1998/00001998/00000001/art00003?crawler=true>`_
    """
    ipt = np2d(ipt)
    if M is None:
        M = _IPT_M['xyz2lms'][cieobs].copy()
        if xyzw is None:
            xyzw = spd_to_xyz((_CIE_ILLUMINANTS['D65']), cieobs=cieobs, out=1)[0] / 100.0
        else:
            xyzw = xyzw / 100.0
        M = math.normalize_3x3_matrix(M, xyzw)
    else:
        if len(ipt.shape) == 3:
            lmsp = np.einsum('ij,klj->kli', np.linalg.inv(_IPT_M['lms2ipt']), ipt)
        else:
            lmsp = np.einsum('ij,lj->li', np.linalg.inv(_IPT_M['lms2ipt']), ipt)
        lms = lmsp ** 2.3255813953488373
        p = np.where(lmsp < 0.0)
        lms[p] = -np.abs(lmsp[p]) ** 2.3255813953488373
        if np.ndim(M) == 2:
            if len(ipt.shape) == 3:
                xyz = np.einsum('ij,klj->kli', np.linalg.inv(M), lms)
            else:
                xyz = np.einsum('ij,lj->li', np.linalg.inv(M), lms)
        else:
            if len(ipt.shape) == 3:
                xyz = np.concatenate([np.einsum('ij,klj->kli', np.linalg.inv(M[i]), lms[:, i:i + 1, :]) for i in range(M.shape[0])], axis=1)
            else:
                xyz = np.concatenate([np.einsum('ij,lj->li', np.linalg.inv(M[i]), lms[i:i + 1, :]) for i in range(M.shape[0])], axis=0)
    xyz = xyz * 100.0
    xyz[np.where(xyz < 0.0)] = 0.0
    return xyz


def xyz_to_Ydlep(xyz, cieobs=_CIEOBS, xyzw=_COLORTF_DEFAULT_WHITE_POINT, flip_axes=False, **kwargs):
    """
    Convert XYZ tristimulus values to Y, dominant (complementary) wavelength
    and excitation purity.

    Args:
        :xyz:
            | ndarray with tristimulus values
        :xyzw:
            | None or ndarray with tristimulus values of a single (!) native white point, optional
            | None defaults to xyz of CIE D65 using the :cieobs: observer.
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set to use when calculating spectrum locus coordinates.
        :flip_axes:
            | False, optional
            | If True: flip axis 0 and axis 1 in Ydelep to increase speed of loop in function.
            |          (single xyzw with is not flipped!)
    Returns:
        :Ydlep: 
            | ndarray with Y, dominant (complementary) wavelength
              and excitation purity
    """
    xyz3 = np3d(xyz).copy().astype(np.float)
    if (xyz3.shape[0] < xyz3.shape[1]) & (flip_axes == True):
        axes12flipped = True
        xyz3 = xyz3.transpose((1, 0, 2))
    else:
        axes12flipped = False
    Yxy = xyz_to_Yxy(xyz3)
    Yxyw = xyz_to_Yxy(xyzw)
    SL = _CMF[cieobs]['bar']
    wlsl = SL[0]
    Yxysl = xyz_to_Yxy(SL[1:4].T)[:, None]
    Yxy = Yxy - Yxyw
    Yxysl = Yxysl - Yxyw
    Yxyw = Yxyw - Yxyw
    Y, x, y = asplit(Yxy)
    Yw, xw, yw = asplit(Yxyw)
    Ysl, xsl, ysl = asplit(Yxysl)
    h = math.positive_arctan(x, y, htype='deg')
    hsl = math.positive_arctan(xsl, ysl, htype='deg')
    hsl_max = hsl[0]
    hsl_min = hsl[(-1)]
    dominantwavelength = np.empty(Y.shape)
    purity = np.empty(Y.shape)
    for i in range(xyz3.shape[1]):
        pc = np.where((h[:, i] >= hsl_max) & (h[:, i] <= hsl_min + 360.0))
        h[:, i][pc] = h[:, i][pc] - np.sign(h[:, i][pc] - 180.0) * 180.0
        hib, hslb = np.meshgrid(h[:, i:i + 1], hsl)
        dh = np.abs(hslb - hib)
        q1 = dh.argmin(axis=0)
        dh[q1] = 1000.0
        q2 = dh.argmin(axis=0)
        dominantwavelength[:, i] = wlsl[q1] + np.divide(np.multiply(wlsl[q2] - wlsl[q1], h[:, i] - hsl[(q1, 0)]), hsl[(q2, 0)] - hsl[(q1, 0)])
        dominantwavelength[:, i][pc] = -dominantwavelength[:, i][pc]
        x_dom_wl = xsl[(q1, 0)] + (xsl[(q2, 0)] - xsl[(q1, 0)]) * (h[:, i] - hsl[(q1, 0)]) / (hsl[(q2, 0)] - hsl[(q1, 0)])
        y_dom_wl = ysl[(q1, 0)] + (ysl[(q2, 0)] - ysl[(q1, 0)]) * (h[:, i] - hsl[(q1, 0)]) / (hsl[(q2, 0)] - hsl[(q1, 0)])
        d_wl = (x_dom_wl ** 2.0 + y_dom_wl ** 2.0) ** 0.5
        d = (x[:, i] ** 2.0 + y[:, i] ** 2.0) ** 0.5
        purity[:, i] = d / d_wl
        xy = np.vstack((x[:, i], y[:, i])).T
        xyw = np.hstack((xw, yw))
        xypl1 = np.hstack((xsl[(0, None)], ysl[(0, None)]))
        xypl2 = np.hstack((xsl[(-1, None)], ysl[(-1, None)]))
        da = xy - xyw
        db = xypl2 - xypl1
        dp = xyw - xypl1
        T = np.array([[0.0, -1.0], [1.0, 0.0]])
        dap = np.dot(da, T)
        denom = np.sum((dap * db), axis=1, keepdims=True)
        num = np.sum((dap * dp), axis=1, keepdims=True)
        xy_linecross = num / denom * db + xypl1
        d_linecross = np.atleast_2d((xy_linecross[:, 0] ** 2.0 + xy_linecross[:, 1] ** 2.0) ** 0.5).T
        purity[:, i][pc] = d[pc] / d_linecross[pc][:, 0]

    Ydlep = np.dstack((xyz3[:, :, 1], dominantwavelength, purity))
    if axes12flipped == True:
        Ydlep = Ydlep.transpose((1, 0, 2))
    else:
        Ydlep = Ydlep.transpose((0, 1, 2))
    return Ydlep.reshape(xyz.shape)


def Ydlep_to_xyz(Ydlep, cieobs=_CIEOBS, xyzw=_COLORTF_DEFAULT_WHITE_POINT, flip_axes=False, **kwargs):
    """
    Convert Y, dominant (complementary) wavelength and excitation purity to XYZ
    tristimulus values.

    Args:
        :Ydlep: 
            | ndarray with Y, dominant (complementary) wavelength
              and excitation purity
        :xyzw: 
            | None or narray with tristimulus values of a single (!) native white point, optional
            | None defaults to xyz of CIE D65 using the :cieobs: observer.
        :cieobs:
            | luxpy._CIEOBS, optional
            | CMF set to use when calculating spectrum locus coordinates.
        :flip_axes:
            | False, optional
            | If True: flip axis 0 and axis 1 in Ydelep to increase speed of loop in function.
            |          (single xyzw with is not flipped!)
    Returns:
        :xyz: 
            | ndarray with tristimulus values
    """
    Ydlep3 = np3d(Ydlep).copy().astype(np.float)
    if (Ydlep3.shape[0] < Ydlep3.shape[1]) & (flip_axes == True):
        axes12flipped = True
        Ydlep3 = Ydlep3.transpose((1, 0, 2))
    else:
        axes12flipped = False
    Yxyw = xyz_to_Yxy(xyzw)
    Yxywo = Yxyw.copy()
    SL = _CMF[cieobs]['bar']
    wlsl = SL[(0, None)].T
    Yxysl = xyz_to_Yxy(SL[1:4].T)[:, None]
    Yxysl = Yxysl - Yxyw
    Yxyw = Yxyw - Yxyw
    Y, dom, pur = asplit(Ydlep3)
    Yw, xw, yw = asplit(Yxyw)
    Ywo, xwo, ywo = asplit(Yxywo)
    Ysl, xsl, ysl = asplit(Yxysl)
    x = np.empty(Y.shape)
    y = np.empty(Y.shape)
    for i in range(Ydlep3.shape[1]):
        wlib, wlslb = np.meshgrid(np.abs(dom[:, i]), wlsl)
        dwl = np.abs(wlslb - wlib)
        q1 = dwl.argmin(axis=0)
        dwl[q1] = 10000.0
        q2 = dwl.argmin(axis=0)
        x_dom_wl = xsl[(q1, 0)] + (xsl[(q2, 0)] - xsl[(q1, 0)]) * (np.abs(dom[:, i]) - wlsl[(q1, 0)]) / (wlsl[(q2, 0)] - wlsl[(q1, 0)])
        y_dom_wl = ysl[(q1, 0)] + (ysl[(q2, 0)] - ysl[(q1, 0)]) * (np.abs(dom[:, i]) - wlsl[(q1, 0)]) / (wlsl[(q2, 0)] - wlsl[(q1, 0)])
        d_wl = (x_dom_wl ** 2.0 + y_dom_wl ** 2.0) ** 0.5
        d = pur[:, i] * d_wl
        hdom = math.positive_arctan(x_dom_wl, y_dom_wl, htype='deg')
        x[:, i] = d * np.cos(hdom * np.pi / 180.0)
        y[:, i] = d * np.sin(hdom * np.pi / 180.0)
        pc = np.where(dom[:, i] < 0.0)
        hdom[pc] = hdom[pc] - np.sign(dom[:, i][pc] - 180.0) * 180.0
        xy = np.vstack((x_dom_wl, y_dom_wl)).T
        xyw = np.vstack((xw, yw)).T
        xypl1 = np.vstack((xsl[(0, None)], ysl[(0, None)])).T
        xypl2 = np.vstack((xsl[(-1, None)], ysl[(-1, None)])).T
        da = xy - xyw
        db = xypl2 - xypl1
        dp = xyw - xypl1
        T = np.array([[0.0, -1.0], [1.0, 0.0]])
        dap = np.dot(da, T)
        denom = np.sum((dap * db), axis=1, keepdims=True)
        num = np.sum((dap * dp), axis=1, keepdims=True)
        xy_linecross = num / denom * db + xypl1
        d_linecross = np.atleast_2d((xy_linecross[:, 0] ** 2.0 + xy_linecross[:, 1] ** 2.0) ** 0.5).T[:, 0]
        x[:, i][pc] = pur[:, i][pc] * d_linecross[pc] * np.cos(hdom[pc] * np.pi / 180)
        y[:, i][pc] = pur[:, i][pc] * d_linecross[pc] * np.sin(hdom[pc] * np.pi / 180)

    Yxy = np.dstack((Ydlep3[:, :, 0], x + xwo, y + ywo))
    if axes12flipped == True:
        Yxy = Yxy.transpose((1, 0, 2))
    else:
        Yxy = Yxy.transpose((0, 1, 2))
    return Yxy_to_xyz(Yxy).reshape(Ydlep.shape)


def xyz_to_srgb(xyz, gamma=2.4, **kwargs):
    """
    Calculates IEC:61966 sRGB values from xyz.

    Args:
        :xyz: 
            | ndarray with relative tristimulus values.
        :gamma: 
            | 2.4, optional
            | compression in sRGB

    Returns:
        :rgb: 
            | ndarray with R,G,B values (uint8).
    """
    xyz = np2d(xyz)
    M = np.array([[3.2404542, -1.5371385, -0.4985314],
     [
      -0.969266, 1.8760108, 0.041556],
     [
      0.0556434, -0.2040259, 1.0572252]])
    if len(xyz.shape) == 3:
        srgb = np.einsum('ij,klj->kli', M, xyz / 100)
    else:
        srgb = np.einsum('ij,lj->li', M, xyz / 100)
    srgb[np.where(srgb > 1)] = 1
    srgb[np.where(srgb < 0)] = 0
    dark = np.where(srgb <= 0.0031308)
    g = 1 / gamma
    rgb = srgb.copy()
    rgb = (1.055 * rgb ** g - 0.055) * 255
    rgb[dark] = srgb[dark].copy() * 12.92 * 255
    rgb[rgb > 255] = 255
    rgb[rgb < 0] = 0
    return rgb


def srgb_to_xyz(rgb, gamma=2.4, **kwargs):
    """
    Calculates xyz from IEC:61966 sRGB values.

    Args:
        :rgb: 
            | ndarray with srgb values (uint8).
        :gamma: 
            | 2.4, optional
            | compression in sRGB
            
    Returns:
        :xyz: 
            | ndarray with relative tristimulus values.

    """
    rgb = np2d(rgb)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
     [
      0.2126729, 0.7151522, 0.072175],
     [
      0.0193339, 0.119192, 0.9503041]])
    sRGB = rgb / 255
    nonlin = np.where(rgb / 255 < 0.0031308)
    srgb = sRGB.copy()
    srgb = ((srgb + 0.055) / 1.055) ** gamma
    srgb[nonlin] = sRGB[nonlin] / 12.92
    if len(srgb.shape) == 3:
        xyz = np.einsum('ij,klj->kli', M, srgb) * 100
    else:
        xyz = np.einsum('ij,lj->li', M, srgb) * 100
    return xyz


def xyz_to_jabz(xyz, **kwargs):
    """
    Convert XYZ tristimulus values to Jz,az,bz color coordinates.

    Args:
        :xyz: 
            | ndarray with absolute tristimulus values (Y in cd/m²!)

    Returns:
        :jabz: 
            | ndarray with Jz,az,bz color coordinates

    Notes:
     | 1. :xyz: is assumed to be under D65 viewing conditions! If necessary perform chromatic adaptation!
     |
     | 2a. Jz represents the 'lightness' relative to a D65 white with luminance = 10000 cd/m² 
     |      (note that Jz that not exactly equal 1 for this high value, but rather for 102900 cd/m2)
     | 2b.  az, bz represent respectively a red-green and a yellow-blue opponent axis 
     |      (but note that a D65 shows a small offset from (0,0))

    Reference:
        1. `Safdar, M., Cui, G., Kim,Y. J., and  Luo,M. R. (2017).
            Perceptually uniform color space for image signals including high dynamic range and wide gamut.
            Opt. Express, vol. 25, no. 13, pp. 15131–15151, Jun. 2017.
            <http://www.opticsexpress.org/abstract.cfm?URI=oe-25-13-15131>`_    
    """
    xyz = np2d(xyz)
    b = 1.15
    g = 0.66
    M_to_xyzp = np.array([[b, 0, 1 - b], [1 - g, g, 0], [0, 0, 1]])
    M_to_lms = np.array([[0.41478972, 0.579999, 0.014648],
     [
      -0.20151, 1.120649, 0.0531008],
     [
      -0.0166008, 0.2648, 0.6684799]])
    M = M_to_lms @ M_to_xyzp
    if len(xyz.shape) == 3:
        lms = np.einsum('ij,klj->kli', M, xyz)
    else:
        lms = np.einsum('ij,lj->li', M, xyz)
    lmsp = ((0.8359375 + 18.8515625 * (lms / 10000) ** 0.1593017578125) / (1 + 18.6875 * (lms / 10000) ** 0.1593017578125)) ** 134.03437499999998
    M = np.array([[0.5, 0.5, 0],
     [
      3.524, -4.066708, 0.542708],
     [
      0.199076, 1.096799, -1.295875]])
    if len(lms.shape) == 3:
        Iabz = np.einsum('ij,klj->kli', M, lmsp)
    else:
        Iabz = np.einsum('ij,lj->li', M, lmsp)
    Iabz[(Ellipsis, 0)] = 0.43999999999999995 * Iabz[(Ellipsis, 0)] / (1 - 0.56 * Iabz[(Ellipsis,
                                                                                        0)]) - 1.6295499532821565e-11
    return Iabz


def jabz_to_xyz(jabz, **kwargs):
    """
    Convert Jz,az,bz color coordinates to XYZ tristimulus values.

    Args:
        :jabz: 
            | ndarray with Jz,az,bz color coordinates
            
    Returns:
        :xyz: 
            | ndarray with tristimulus values

    Note:
     | 1. :xyz: is assumed to be under D65 viewing conditions! If necessary perform chromatic adaptation!
     |
     | 2a. Jz represents the 'lightness' relative to a D65 white with luminance = 10000 cd/m² 
     |      (note that Jz that not exactly equal 1 for this high value, but rather for 102900 cd/m2)
     | 2b.  az, bz represent respectively a red-green and a yellow-blue opponent axis 
     |      (but note that a D65 shows a small offset from (0,0))

    Reference:
        1. `Safdar, M., Cui, G., Kim,Y. J., and  Luo,M. R. (2017).
            Perceptually uniform color space for image signals including high dynamic range and wide gamut.
            Opt. Express, vol. 25, no. 13, pp. 15131–15151, Jun. 2017.
            <http://www.opticsexpress.org/abstract.cfm?URI=oe-25-13-15131>`_    
    """
    jabz = np2d(jabz)
    jabz[(Ellipsis, 0)] = (jabz[(Ellipsis, 0)] + 1.6295499532821565e-11) / (1 - 0.56 * (1 - (jabz[(Ellipsis,
                                                                                                   0)] + 1.6295499532821565e-11)))
    M = np.linalg.inv(np.array([[0.5, 0.5, 0],
     [
      3.524, -4.066708, 0.542708],
     [
      0.199076, 1.096799, -1.295875]]))
    if len(jabz.shape) == 3:
        lmsp = np.einsum('ij,klj->kli', M, jabz)
    else:
        lmsp = np.einsum('ij,lj->li', M, jabz)
    lms = 10000 * ((0.8359375 - lmsp ** 0.007460772656268216) / (18.6875 * lmsp ** 0.007460772656268216 - 18.8515625)) ** 6.277394636015326
    b = 1.15
    g = 0.66
    M_to_xyzp = np.array([[b, 0, 1 - b], [1 - g, g, 0], [0, 0, 1]])
    M_to_lms = np.array([[0.41478972, 0.579999, 0.014648],
     [
      -0.20151, 1.120649, 0.0531008],
     [
      -0.0166008, 0.2648, 0.6684799]])
    M = M_to_lms @ M_to_xyzp
    M = np.linalg.inv(M)
    if len(jabz.shape) == 3:
        xyz = np.einsum('ij,klj->kli', M, lms)
    else:
        xyz = np.einsum('ij,lj->li', M, lms)
    return xyz