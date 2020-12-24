# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pydrizzle\drutil.py
# Compiled at: 2014-04-16 13:17:36
"""
Utility functions for PyDrizzle that rely on PyRAF's interface to IRAF
tasks.
"""
from __future__ import division
import os
from math import ceil, floor
import numpy as np
from numpy import linalg
from stsci.tools import fileutil
from stsci.tools.fileutil import buildRotMatrix
DEGTORAD = fileutil.DEGTORAD
no = False
yes = True
IDCTAB = 1
DRIZZLE = 2
TRAUGER = 3
try:
    DEFAULT_IDCDIR = fileutil.osfn('stsdas$pkg/analysis/dither/drizzle/coeffs/')
except:
    DEFAULT_IDCDIR = os.getcwd()

def findNumExt(filename):
    _s = fileutil.getKeyword(filename, keyword='NEXTEND')
    if not _s:
        _s = fileutil.getKeyword(filename, keyword='GCOUNT')
    if _s == '':
        raise ValueError, 'There are NO extensions to be read in this image!'
    return _s


def getLTVOffsets(rootname, header=None):
    _ltv1 = None
    _ltv2 = None
    if header:
        if 'LTV1' in header:
            _ltv1 = header['LTV1']
        if 'LTV2' in header:
            _ltv2 = header['LTV2']
    else:
        _ltv1 = fileutil.getKeyword(rootname, 'LTV1')
        _ltv2 = fileutil.getKeyword(rootname, 'LTV2')
    if _ltv1 == None:
        _ltv1 = 0.0
    if _ltv2 == None:
        _ltv2 = 0.0
    return (
     _ltv1, _ltv2)


def getChipId(header):
    if 'CCDCHIP' in header:
        chip = int(header['CCDCHIP'])
    elif 'DETECTOR' in header and str(header['DETECTOR']).isdigit():
        chip = int(header['DETECTOR'])
    elif 'CAMERA' in header and str(header['CAMERA']).isdigit():
        chip = int(header['CAMERA'])
    else:
        chip = 1
    return chip


def getIDCFile(image, keyword='', directory=None):
    if isinstance(image, basestring):
        header = fileutil.getHeader(image)
    else:
        header = image
    if keyword.lower() == 'header':
        idcfile, idctype = __getIDCTAB(header)
        if idcfile == None:
            idcfile, idctype = __buildIDCTAB(header, directory)
    elif keyword.lower() == 'idctab':
        idcfile, idctype = __getIDCTAB(header)
    elif keyword == '':
        idcfile = None
        idctype = None
    else:
        idcfile, idctype = __buildIDCTAB(header, directory, kw=keyword)
    if idcfile == 'N/A':
        idcfile = None
    if idcfile != None and idcfile != '':
        idcfile = fileutil.osfn(idcfile)
    if idcfile == None:
        print 'WARNING: No valid distortion coefficients available!'
        print 'Using default unshifted, unscaled, unrotated model.'
    return (idcfile, idctype)


def __buildIDCTAB(header, directory, kw='cubic'):
    instrument = header['INSTRUME']
    if instrument != 'NICMOS':
        detector = header['DETECTOR']
    else:
        detector = str(header['CAMERA'])
    keyword = kw
    if not directory:
        default_dir = DEFAULT_IDCDIR
    else:
        default_dir = directory
    if instrument == 'WFPC2':
        if detector == 1:
            detname = 'pc'
        else:
            detname = 'wf'
        idcfile = default_dir + detname + str(detector) + '-' + keyword.lower()
    elif instrument == 'STIS':
        idcfile = default_dir + 'stis-' + detector.lower()
    elif instrument == 'NICMOS':
        if detector != None:
            idcfile = default_dir + 'nic-' + detector
        else:
            idcfile = None
    else:
        idcfile = None
    idctype = getIDCFileType(fileutil.osfn(idcfile))
    return (
     idcfile, idctype)


def __getIDCTAB(header):
    try:
        idcfile = header['idctab']
    except:
        print 'Warning: No IDCTAB specified in header!'
        idcfile = None

    return (idcfile, 'idctab')


def getIDCFileType(idcfile):
    """ Open ASCII IDCFILE to determine the type: cubic,trauger,... """
    if idcfile == None:
        return
    else:
        ifile = open(idcfile, 'r')
        _line = fileutil.rAsciiLine(ifile)
        while _line[0] == '#':
            _line = fileutil.rAsciiLine(ifile)

        _type = _line.lower().rstrip()
        if _type in ('cubic', 'quartic', 'quintic') or _type.find('poly') > -1:
            _type = 'cubic'
        elif _type == 'trauger':
            _type = 'trauger'
        else:
            _type = None
        ifile.close()
        del ifile
        return _type


def rotateCubic(fxy, theta):
    newf = fxy * 0.0
    cost = np.cos(DEGTORAD(theta))
    sint = np.sin(DEGTORAD(theta))
    cos2t = pow(cost, 2)
    sin2t = pow(sint, 2)
    cos3t = pow(cost, 3)
    sin3t = pow(sint, 3)
    newf[1][1] = fxy[1][1] * cost - fxy[1][0] * sint
    newf[1][0] = fxy[1][1] * sint + fxy[1][0] * cost
    newf[2][2] = fxy[2][2] * cos2t - fxy[2][1] * cost * sint + fxy[2][0] * sin2t
    newf[2][1] = fxy[2][2] * 2 * cost * sint + fxy[2][1] * (cos2t - sin2t) + fxy[2][0] * 2 * sint * cost
    newf[2][0] = fxy[2][2] * sin2t + fxy[2][1] * cost * sint + fxy[2][0] * cos2t
    newf[3][3] = fxy[3][3] * cos3t - fxy[3][2] * sint * cos2t + fxy[3][1] * sin2t * cost - fxy[3][0] * sin3t
    newf[3][2] = fxy[3][3] * 3.0 * cos2t * sint + fxy[3][2] * (cos3t - 2.0 * sin2t * cost) + fxy[3][1] * (sin3t + 2 * sint * cos2t) - fxy[3][0] * sin2t * cost
    newf[3][1] = fxy[3][3] * 3.0 * cost * sin2t + fxy[3][2] * (2.0 * cos2t * sint - sin3t) + fxy[3][1] * (2 * sin2t * cost + cos3t) + fxy[3][0] * sint * cos2t
    newf[3][0] = fxy[3][3] * sin3t + fxy[3][2] * sin2t * cost + fxy[3][1] * sint * cos2t + fxy[3][0] * cos3t
    return newf


def rotatePos(pos, theta, offset=None, scale=None):
    if scale == None:
        scale = 1.0
    if offset == None:
        offset = np.array([0.0, 0.0], dtype=np.float64)
    mrot = buildRotMatrix(theta)
    xr = (pos[0] * mrot[0][0] + pos[1] * mrot[0][1]) / scale + offset[0]
    yr = (pos[0] * mrot[1][0] + pos[1] * mrot[1][1]) / scale + offset[1]
    return (
     xr, yr)


def getRange(members, ref_wcs, verbose=None):
    xma, yma = [], []
    xmi, ymi = [], []
    crpix = (
     ref_wcs.crpix1, ref_wcs.crpix2)
    ref_rot = ref_wcs.orient
    _rot = ref_wcs.orient - members[0].geometry.wcslin.orient
    for member in members:
        _model = member.geometry.model
        _wcs = member.geometry.wcs
        _wcslin = member.geometry.wcslin
        _theta = _wcslin.orient - ref_rot
        _scale = _wcslin.pscale / ref_wcs.pscale
        xypos = member.geometry.calcNewCorners() * _scale
        if _theta != 0.0:
            _mrot = buildRotMatrix(_theta)
            xypos = np.dot(xypos, _mrot)
        _oxmax = np.maximum.reduce(xypos[:, 0])
        _oymax = np.maximum.reduce(xypos[:, 1])
        _oxmin = np.minimum.reduce(xypos[:, 0])
        _oymin = np.minimum.reduce(xypos[:, 1])
        member.corners['corrected'] = xypos
        xma.append(_oxmax)
        yma.append(_oymax)
        xmi.append(_oxmin)
        ymi.append(_oymin)

    xmax = np.maximum.reduce(xma)
    ymax = np.maximum.reduce(yma)
    ymin = np.minimum.reduce(ymi)
    xmin = np.minimum.reduce(xmi)
    nref = (
     xmin + xmax, ymin + ymax)
    if _rot != 0.0:
        _mrot = buildRotMatrix(_rot)
        nref = np.dot(nref, _mrot)
    xsize = int(ceil(xmax)) - int(floor(xmin))
    ysize = int(ceil(ymax)) - int(floor(ymin))
    meta_range = {}
    meta_range = {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax, 'nref': nref}
    meta_range['xsize'] = xsize
    meta_range['ysize'] = ysize
    if verbose:
        print 'Meta_WCS:'
        print '    NREF         :', nref
        print '    X range      :', xmin, xmax
        print '    Y range      :', ymin, ymax
        print '    Computed Size: ', xsize, ysize
    return meta_range


def computeRange(corners):
    """ Determine the range spanned by an array of pixel positions. """
    _xrange = (
     np.minimum.reduce(corners[:, 0]), np.maximum.reduce(corners[:, 0]))
    _yrange = (np.minimum.reduce(corners[:, 1]), np.maximum.reduce(corners[:, 1]))
    return (_xrange, _yrange)


def convertWCS(inwcs, drizwcs):
    """ Copy WCSObject WCS into Drizzle compatible array."""
    drizwcs[0] = inwcs.crpix1
    drizwcs[1] = inwcs.crval1
    drizwcs[2] = inwcs.crpix2
    drizwcs[3] = inwcs.crval2
    drizwcs[4] = inwcs.cd11
    drizwcs[5] = inwcs.cd21
    drizwcs[6] = inwcs.cd12
    drizwcs[7] = inwcs.cd22
    return drizwcs


def updateWCS(drizwcs, inwcs):
    """ Copy output WCS array from Drizzle into WCSObject."""
    inwcs.crpix1 = drizwcs[0]
    inwcs.crval1 = drizwcs[1]
    inwcs.crpix2 = drizwcs[2]
    inwcs.crval2 = drizwcs[3]
    inwcs.cd11 = drizwcs[4]
    inwcs.cd21 = drizwcs[5]
    inwcs.cd12 = drizwcs[6]
    inwcs.cd22 = drizwcs[7]
    inwcs.pscale = np.sqrt(np.power(inwcs.cd11, 2) + np.power(inwcs.cd21, 2)) * 3600.0
    inwcs.orient = np.arctan2(inwcs.cd12, inwcs.cd22) * 180.0 / np.pi


def wcsfit(img_geom, ref):
    """
    Perform a linear fit between 2 WCS for shift, rotation and scale.
    Based on 'WCSLIN' from 'drutil.f'(Drizzle V2.9) and modified to
    allow for differences in reference positions assumed by PyDrizzle's
    distortion model and the coeffs used by 'drizzle'.

    Parameters:
        img      - ObsGeometry instance for input image
        ref_wcs  - Undistorted WCSObject instance for output frame
    """
    img_wcs = img_geom.wcs
    in_refpix = img_geom.model.refpix
    ref_wcs = ref.copy()
    _cpix_xyref = np.zeros((4, 2), dtype=np.float64)
    _cpix = (
     img_wcs.crpix1, img_wcs.crpix2)
    _cpix_arr = np.array([_cpix, (_cpix[0], _cpix[1] + 1.0),
     (
      _cpix[0] + 1.0, _cpix[1] + 1.0), (_cpix[0] + 1.0, _cpix[1])], dtype=np.float64)
    _cpix_rd = img_wcs.xy2rd(_cpix_arr)
    for pix in xrange(len(_cpix_rd[0])):
        _cpix_xyref[(pix, 0)], _cpix_xyref[(pix, 1)] = ref_wcs.rd2xy((_cpix_rd[0][pix], _cpix_rd[1][pix]))

    if img_wcs.delta_refx == 0.0 and img_wcs.delta_refy == 0.0:
        offx, offy = (0.0, 0.0)
    else:
        offx, offy = (1.0, 1.0)
    _cpix_xyc = np.zeros((4, 2), dtype=np.float64)
    _cpix_xyc[:, 0], _cpix_xyc[:, 1] = img_geom.apply(_cpix_arr - (offx, offy), order=1)
    if in_refpix:
        _cpix_xyc += (in_refpix['XDELTA'], in_refpix['YDELTA'])
    abxt, cdyt = fitlin(_cpix_xyc, _cpix_xyref)
    abxt[2] -= ref_wcs.crpix1 + offx
    cdyt[2] -= ref_wcs.crpix2 + offy
    return (
     abxt, cdyt)


def fitlin(imgarr, refarr):
    """ Compute the least-squares fit between two arrays.
        A Python translation of 'FITLIN' from 'drutil.f' (Drizzle V2.9).
    """
    _mat = np.zeros((3, 3), dtype=np.float64)
    _xorg = imgarr[0][0]
    _yorg = imgarr[0][1]
    _xoorg = refarr[0][0]
    _yoorg = refarr[0][1]
    _sigxox = 0.0
    _sigxoy = 0.0
    _sigxo = 0.0
    _sigyox = 0.0
    _sigyoy = 0.0
    _sigyo = 0.0
    _npos = len(imgarr)
    for i in xrange(_npos):
        _mat[0][0] += np.power(imgarr[i][0] - _xorg, 2)
        _mat[0][1] += (imgarr[i][0] - _xorg) * (imgarr[i][1] - _yorg)
        _mat[0][2] += imgarr[i][0] - _xorg
        _mat[1][1] += np.power(imgarr[i][1] - _yorg, 2)
        _mat[1][2] += imgarr[i][1] - _yorg
        _sigxox += (refarr[i][0] - _xoorg) * (imgarr[i][0] - _xorg)
        _sigxoy += (refarr[i][0] - _xoorg) * (imgarr[i][1] - _yorg)
        _sigxo += refarr[i][0] - _xoorg
        _sigyox += (refarr[i][1] - _yoorg) * (imgarr[i][0] - _xorg)
        _sigyoy += (refarr[i][1] - _yoorg) * (imgarr[i][1] - _yorg)
        _sigyo += refarr[i][1] - _yoorg

    _mat[2][2] = _npos
    _mat[1][0] = _mat[0][1]
    _mat[2][0] = _mat[0][2]
    _mat[2][1] = _mat[1][2]
    _mat = linalg.inv(_mat)
    _a = _sigxox * _mat[0][0] + _sigxoy * _mat[0][1] + _sigxo * _mat[0][2]
    _b = -1 * (_sigxox * _mat[1][0] + _sigxoy * _mat[1][1] + _sigxo * _mat[1][2])
    _c = _sigyox * _mat[1][0] + _sigyoy * _mat[1][1] + _sigyo * _mat[1][2]
    _d = _sigyox * _mat[0][0] + _sigyoy * _mat[0][1] + _sigyo * _mat[0][2]
    _xt = _xoorg - _a * _xorg + _b * _yorg
    _yt = _yoorg - _d * _xorg - _c * _yorg
    return (
     [
      _a, _b, _xt], [_c, _d, _yt])


def getRotatedSize(corners, angle):
    """ Determine the size of a rotated (meta)image."""
    if angle == 0.0:
        _corners = corners
    else:
        _rotm = buildRotMatrix(angle)
        _corners = np.dot(corners, _rotm)
    return computeRange(_corners)