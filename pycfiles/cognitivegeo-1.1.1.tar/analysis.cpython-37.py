# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\seismic\analysis.py
# Compiled at: 2020-01-04 23:31:18
# Size of source mod 2**32: 94427 bytes
from PyQt5 import QtCore
import sys, os, numpy as np
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.vis.messager as vis_msg
__all__ = [
 'analysis']

def getSeisInfoFrom2DMat(seis2dmat, inlcol=0, xlcol=1, zcol=2):
    """
    Get basic seismic information from 2D seismic matrix

    Args:
        seis2dmat:  2D mat of seismic data containing at least three columns [IL, XL, Z]
        inlcol:     Index of inline column. Default is the first column (0)
        xlcol:      Index of crossline column. Default is the second column (1)
        zcol:       Index of z column. Default is the third column (2)

    Returns:
        seisinfo:   Seismic information as a dictionary as defined above

    Note:
        Negative z is used in the vertical direction
    """
    seisinfo = makeSeisInfo()
    if np.ndim(seis2dmat) != 2:
        vis_msg.print('ERROR in getSeisInfoFrom2DMat: 2D seismic matrix expected', type='error')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) < inlcol:
        vis_msg.print('ERROR in getSeisInfoFrom2DMat: No inline column found in 2D seismic matrix', type='error')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) < xlcol:
        vis_msg.print('ERROR in getSeisInfoFrom2DMat: No crossline column found in 2D seismic matrix', type='error')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) < zcol:
        vis_msg.print('ERROR in getSeisInfoFrom2DMat: No z column found in 2D seismic matrix', type='error')
        sys.exit()
    zrange = seis2dmat[:, zcol]
    zstart = zrange[0]
    zend = zrange[(-1)]
    zstep = -1
    znum = 1
    if zstart != zend:
        zstep = zrange[1] - zrange[0]
        znum = (zend - zstart) / zstep + 1
    zstart = np.round(zstart).astype(np.int32)
    zstep = np.round(zstep).astype(np.int32)
    if zstep == 0:
        zstep = -1
    znum = np.round(znum).astype(np.int32)
    zend = (zstart + (znum - 1) * zstep).astype(np.int32)
    zrange = np.linspace(zstart, zend, znum).astype(np.int32)
    seisinfo['ZStart'] = zstart
    seisinfo['ZEnd'] = zend
    seisinfo['ZStep'] = zstep
    seisinfo['ZNum'] = znum
    seisinfo['ZRange'] = zrange
    xlrange = seis2dmat[:, xlcol]
    xlstart = xlrange[0]
    xlend = xlrange[(-1)]
    xlstep = 1
    xlnum = 1
    if xlstart != xlend:
        xlstep = xlrange[int(znum)] - xlrange[0]
        xlnum = (xlend - xlstart) / xlstep + 1
    xlstart = np.round(xlstart).astype(np.int32)
    xlstep = np.round(xlstep).astype(np.int32)
    if xlstep == 0:
        xlstep = 1
    xlnum = np.round(xlnum).astype(np.int32)
    xlend = (xlstart + (xlnum - 1) * xlstep).astype(np.int32)
    xlrange = np.linspace(xlstart, xlend, xlnum).astype(np.int32)
    seisinfo['XLStart'] = xlstart
    seisinfo['XLEnd'] = xlend
    seisinfo['XLStep'] = xlstep
    seisinfo['XLNum'] = xlnum
    seisinfo['XLRange'] = xlrange
    inlrange = seis2dmat[:, inlcol]
    inlstart = inlrange[0]
    inlend = inlrange[(-1)]
    inlstep = 1
    inlnum = 1
    if inlstart != inlend:
        inlstep = inlrange[int(znum * xlnum)] - inlrange[0]
        inlnum = (inlend - inlstart) / inlstep + 1
    inlstart = np.round(inlstart).astype(np.int32)
    inlstep = np.round(inlstep).astype(np.int32)
    inlnum = np.round(inlnum).astype(np.int32)
    if inlstep == 0:
        inlstep = 1
    inlend = (inlstart + (inlnum - 1) * inlstep).astype(np.int32)
    inlrange = np.linspace(inlstart, inlend, inlnum).astype(np.int32)
    seisinfo['ILStart'] = inlstart
    seisinfo['ILEnd'] = inlend
    seisinfo['ILStep'] = inlstep
    seisinfo['ILNum'] = inlnum
    seisinfo['ILRange'] = inlrange
    return seisinfo


def checkSeisInfo(seisinfo):
    """
    Check if a seismic info dictionary good

    Args:
        seisinfo:   seismic inforamtion dictionary as defined above

    Return:
        True or false

    Note:
        Negative z is used in the vertical direction
    """
    info = [
     'ILStart', 'ILEnd', 'ILStep', 'ILNum', 'ILRange',
     'XLStart', 'XLEnd', 'XLStep', 'XLNum', 'XLRange',
     'ZStart', 'ZEnd', 'ZStep', 'ZNum', 'ZRange']
    if seisinfo is None:
        return False
    for f in info:
        if f not in seisinfo.keys():
            return False

    return True


def makeSeisInfo(inlstart=0, inlstep=1, inlnum=1, xlstart=0, xlstep=1, xlnum=1, zstart=0, zstep=-1, znum=1):
    """
    Make a new seismic information dictionary

    Args:
        inlstart:   first inline. Default is 0
        inlstep:    inline step. Default is 1
        inlnum:     inline number. Default is 1
        xlstart:    first xline. Default is 0
        xlstep:     xline step. Default is 1
        xlnum:      xline number. Default is 1
        zstart:     first z. Default is 0
        zstep:      z step. Default is -1
        znum:       z number. Default is 1

    Return:
         Seismic inforamtion dictionary as defined above
    """
    seisinfo = {}
    seisinfo['ILStart'] = inlstart
    seisinfo['ILEnd'] = inlstart + (inlnum - 1) * inlstep
    seisinfo['ILStep'] = inlstep
    seisinfo['ILNum'] = inlnum
    seisinfo['ILRange'] = np.linspace(0, inlnum - 1, 1) * inlstep + inlstart
    seisinfo['XLStart'] = xlstart
    seisinfo['XLEnd'] = xlstart + (xlnum - 1) * xlstep
    seisinfo['XLStep'] = xlstep
    seisinfo['XLNum'] = xlnum
    seisinfo['XLRange'] = np.linspace(0, inlnum - 1, 1) * xlstep + xlstart
    seisinfo['ZStart'] = zstart
    seisinfo['ZEnd'] = zstart + (znum - 1) * zstep
    seisinfo['ZStep'] = zstep
    seisinfo['ZNum'] = znum
    seisinfo['ZRange'] = np.linspace(0, inlnum - 1, 1) * zstep + zstart
    return seisinfo


def isSeis2DMatConsistentWithSeisInfo(seis2dmat, seisinfo):
    """
    Check if a Seis2DMat is consistent with the given SeisInfo

    Args:
        seis2dmat:  seismic data in 2D array as defined above
        seisinfo:   seismic information as a dictionary as defined above

    Return:
         True or false
    """
    if checkSeisInfo(seisinfo) is False:
        return False
    if np.ndim(seis2dmat) < 2:
        return False
    if np.shape(seis2dmat)[0] != np.int64(seisinfo['ILNum']) * np.int64(seisinfo['XLNum']) * np.int64(seisinfo['ZNum']):
        return False
    return True


def isSeis3DMatConsistentWithSeisInfo(seis3dmat, seisinfo):
    """
    Check if a Seis3DMat is consistent with the given SeisInfo

    Args:
        seis3dmat:  seismic data in 3D array as defined above
        seisinfo:   seismic information as a dictionary as defined above

    Return:
        True or false
    """
    if checkSeisInfo(seisinfo) is False:
        return False
    if np.ndim(seis3dmat) < 3:
        return False
    if np.shape(seis3dmat)[0] != seisinfo['ZNum'] or np.shape(seis3dmat)[1] != seisinfo['XLNum'] or np.shape(seis3dmat)[2] != seisinfo['ILNum']:
        return False
    return True


def createSeisInfoFrom3DMat(seis3dmat, inlstart=0, inlstep=1, xlstart=0, xlstep=1, zstart=0, zstep=-1):
    """
    Create SeisInfo from Seis3DMat

    Args:
        seis3dmat:  3D matrix of the seismic data [Z/XL/IL] as defined above
        inlstart:   first inline No.. Default is 0
        inlstep:    step between two adjacent inlines. Default is 1
        xlstart:    first crosslien No.. Default is 0
        xlstep:     step between two adjacent crosslines. Default is 1
        zstart:     top z slice. Default is 0
        zstep:      step between two adjacent z slices. Default is -1

    Returns:
         seisinfo:  seismic information dictionary as defined above

    Note:
        Negative z is used in the vertical direction
    """
    seisinfo = makeSeisInfo()
    if np.ndim(seis3dmat) != 3:
        vis_msg.print('ERROR in createSeisInfoFrom3DMat: 3D seismic matrix expected', type='error')
        sys.exit()
    znum, xlnum, inlnum = np.shape(seis3dmat)
    inlstart = np.round(inlstart).astype(np.int32)
    inlstep = np.round(inlstep).astype(np.int32)
    inlnum = np.round(inlnum).astype(np.int32)
    if inlstep == 0:
        inlstep = 1
    inlend = (inlstart + inlstep * (inlnum - 1)).astype(np.int32)
    inlrange = np.linspace(inlstart, inlend, inlnum).astype(np.int32)
    seisinfo['ILStart'] = inlstart
    seisinfo['ILEnd'] = inlend
    seisinfo['ILStep'] = inlstep
    seisinfo['ILNum'] = inlnum
    seisinfo['ILRange'] = inlrange
    xlstart = np.round(xlstart).astype(np.int32)
    xlstep = np.round(xlstep).astype(np.int32)
    xlnum = np.round(xlnum).astype(np.int32)
    if xlstep == 0:
        xlstep = 1
    xlend = (xlstart + xlstep * (xlnum - 1)).astype(np.int32)
    xlrange = np.linspace(xlstart, xlend, xlnum).astype(np.int32)
    seisinfo['XLStart'] = xlstart
    seisinfo['XLEnd'] = xlend
    seisinfo['XLStep'] = xlstep
    seisinfo['XLNum'] = xlnum
    seisinfo['XLRange'] = xlrange
    zstart = np.round(zstart).astype(np.int32)
    zstep = np.round(zstep).astype(np.int32)
    znum = np.round(znum).astype(np.int32)
    if zstep == 0:
        zstep = -1
    zend = (zstart + zstep * (znum - 1)).astype(np.int32)
    zrange = np.linspace(zstart, zend, znum).astype(np.int32)
    seisinfo['ZStart'] = zstart
    seisinfo['ZEnd'] = zend
    seisinfo['ZStep'] = zstep
    seisinfo['ZNum'] = znum
    seisinfo['ZRange'] = zrange
    return seisinfo


def convertSeis2DMatTo3DMat(seis2dmat, datacol=3, inlcol=0, xlcol=1, zcol=2):
    """
    Convert seismic data from 2D array (Seis2DMat) to 3D array (Seis3DMat)

    Argus:
        seis2dmat:  2D matrix of seismic data containing at least four columns
                    [IL, XL, Z, Value ...]
        datacol:    index of data column for conversion (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)

    Returns:
        seis3dmat:  3D seismic matrix [Z/XL/IL] as defined above
    """
    if np.ndim(seis2dmat) != 2:
        vis_msg.print('ERROR in convertSeis2DMatTo3DMat: 2D seismic matrix expected', type='error')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        vis_msg.print('ERROR in convertSeis2DMatTo3DMat: No data column found in 2D seismic matrix', type='error')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) <= inlcol:
        vis_msg.print('ERROR in convertSeis2DMatTo3DMat: No inline column found in 2D seismic matrix', type='error')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) <= xlcol:
        vis_msg.print('ERROR in convertSeis2DMatTo3DMat: No crossline column found in 2D seismic matrix', type='error')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) <= zcol:
        vis_msg.print('ERROR in convertSeis2DMatTo3DMat: No z column found in 2D seismic matrix', type='error')
        sys.exit()
    seisinfo = getSeisInfoFrom2DMat(seis2dmat, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    inlnum = seisinfo['ILNum']
    xlnum = seisinfo['XLNum']
    znum = seisinfo['ZNum']
    seisdata = seis2dmat[:, datacol]
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [inlnum, xlnum, znum])
    seisdata = seisdata.transpose()
    return seisdata


def convertSeis3DMatTo2DMat(seis3dmat, seisinfo=None):
    """
    Convert seismic data in 3D matrix (Seis3DMat) to 2D matrix (Seis2DMat)

    Args:
        seis3dmat:  3D matrix of seismic data [Z/XL/IL]
        seisinfo:   seismic inforamtion dictionary as defined above
                    Auto-generated from 3D seismic matrix if not provided

    Return:
        seis2dmat:  2D seismic matrix of the datacontaining four columns [IL, XL, Z, Value] as defined above
    """
    if np.ndim(seis3dmat) != 3:
        vis_msg.print('ERROR in convertSeis3DMatTo2DMat: 3D seismic matrix expected', type='error')
        sys.exit()
    if seisinfo is None:
        vis_msg.print('WARNING in convertSeis3DMatTo2DMat: Survey info auto-generated from 3D seismic matrix', type='warning')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)
    inlnum = seisinfo['ILNum']
    xlnum = seisinfo['XLNum']
    znum = seisinfo['ZNum']
    if (
     znum, xlnum, inlnum) != np.shape(seis3dmat):
        vis_msg.print('ERROR in convertSeis3DMatTo2DMat: Dimension not match between 3D matrix and survey info', type='error')
        sys.exit()
    tracenum = (inlnum * xlnum).astype(np.int64)
    samplenum = (tracenum * znum).astype(np.int64)
    seisdata = seis3dmat.transpose()
    seisdata = np.reshape(seisdata, [1, samplenum])
    seisdata = seisdata.transpose()
    inlxlz = convertSeisInfoTo2DMat(seisinfo)
    seis2dmat = np.concatenate((inlxlz, seisdata), axis=1)
    return seis2dmat


def convertSeisInfoTo2DMat(seisinfo):
    """
    Convert seismic info to 2D matrix
    Args:
        seisinfo:   seismic inforamtion dictionary as defined above

    Return:
        seis2dmat:  2D seismic matrix containing three columns [IL, XL, Z]
    """
    if checkSeisInfo(seisinfo) is False:
        vis_msg.print('Error in convertSeisInfoTo2DMat: Seisinfo not correct', type='error')
        sys.exit()
    inlnum = seisinfo['ILNum']
    xlnum = seisinfo['XLNum']
    znum = seisinfo['ZNum']
    tracenum = (inlnum * xlnum).astype(np.int64)
    samplenum = (tracenum * znum).astype(np.int64)
    inlstart = seisinfo['ILStart']
    inlend = seisinfo['ILEnd']
    xlstart = seisinfo['XLStart']
    xlend = seisinfo['XLEnd']
    zstart = seisinfo['ZStart']
    zend = seisinfo['ZEnd']
    all_sample = np.arange(0, samplenum, 1)
    inl = np.linspace(inlstart, inlend, inlnum)
    inl = np.reshape(inl[(all_sample / xlnum / znum).astype(int)], [-1, 1])
    xl = np.linspace(xlstart, xlend, xlnum)
    xl = np.reshape(xl[(all_sample / znum % xlnum).astype(int)], [-1, 1])
    z = np.linspace(zstart, zend, znum)
    z = np.reshape(z[(all_sample % znum).astype(int)], [-1, 1])
    seis2dmat = np.concatenate((inl, xl, z), axis=1)
    return seis2dmat


def retrieveSeisSampleFrom2DMat(seis2dmat, samples=None, datacol=3, inlcol=0, xlcol=1, zcol=2, verbose=True):
    """
    Retrieve seismic data on specified samples from 2D matrix (Seis2DMat)

    Args:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value, ...]
        samples:    list of samples in 2D matrix of three columns [IL, XL, Z]
                    All samples are retrieved if not specified
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        verbose:    flag for message display. Default is True

    Return:
        seisdata:   seismic data on specified samples
                    2D matrix of four columns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis2dmat) != 2:
        vis_msg.print('ERROR in retrieveSeisSampleFrom2DMat: 2D seismic matrix expected', type='error')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        vis_msg.print('ERROR in retrieveSeisSampleFrom2DMat: Not data column found in 2D seismic matrix', type='error')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) < inlcol:
        vis_msg.print('ERROR in retrieveSeisSampleFrom2DMat: No inline column found in 2D seismic matrix', type='error')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) < xlcol:
        vis_msg.print('ERROR in retrieveSeisSampleFrom2DMat: No crossline column found in 2D seismic matrix', type='error')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) < zcol:
        vis_msg.print('ERROR in retrieveSeisSampleFrom2DMat: No z column found in 2D seismic matrix', type='error')
        sys.exit()
    if samples is None:
        vis_msg.print('WARNING in retrieveSeisSampleFrom2DMat: to retrieve all samples in 2D seismic matrix', type='warning')
        inlloc = seis2dmat[:, inlcol]
        xlloc = seis2dmat[:, xlcol]
        zloc = seis2dmat[:, zcol]
        seisdata = seis2dmat[:, datacol]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((inlloc, xlloc, zloc, seisdata), axis=1)
        return seisdata
    if np.ndim(samples) != 2:
        vis_msg.print('ERROR in retrieveSeisSampleFrom2DMat: 2D matrix of samples expected', type='error')
        sys.exit()
    if len(samples[0, :]) < 3:
        vis_msg.print('ERROR in retrieveSeisSampleFrom2DMat: 3 columns expected in 2D sample matrix', type='error')
        sys.exit()
    seisinfo = getSeisInfoFrom2DMat(seis2dmat, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum = seisinfo['ZNum']
    if inlnum == 1:
        inlstep = 1
    if xlnum == 1:
        xlstep = 1
    if znum == 1:
        zstep = -1
    nsample, _ = np.shape(samples)
    if verbose:
        print('Retrieve ' + str(nsample) + ' samples')
    seisdata = np.zeros([nsample, 4], np.float32)
    for i in range(nsample):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nsample) * 100.0))
            sys.stdout.flush()
        inl = samples[(i, 0)]
        xl = samples[(i, 1)]
        z = samples[(i, 2)]
        inlidx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        xlidx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        zidx = np.round((z - zstart) / zstep).astype(np.int32)
        if inlidx >= 0 and inlidx < inlnum and xlidx >= 0 and xlidx < xlnum and zidx >= 0 and zidx < znum:
            idx = inlidx * xlnum * znum + xlidx * znum + zidx
            seisdata[(i, 0)] = seis2dmat[(idx, inlcol)]
            seisdata[(i, 1)] = seis2dmat[(idx, xlcol)]
            seisdata[(i, 2)] = seis2dmat[(idx, zcol)]
            seisdata[(i, 3)] = seis2dmat[(idx, datacol)]

    if verbose:
        sys.stdout.write(' Done\n')
    return seisdata


def retrieveSeisSampleFrom3DMat(seis3dmat, samples=None, seisinfo=None, verbose=True):
    """
    Retrieve seismic data on specified samples from 3D matrix (Seis3DMat)

    Args:
        seis3dmat:  seismic data in 3D matrix [Z/XL/IL]
        samples:    list of samples in 2D matrix of three columns [IL, XL, Z]
                    All samples are retrieved if not specified
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        verbose:    flag for message display. Default is True

    Return:
        seisdata:   seismic data on specified samples
                    2D matrix of four columns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis3dmat) != 3:
        vis_msg.print('ERROR in retrieveSeisSampleFrom3DMat: 3D seismic matrix expected', type='error')
        sys.exit()
    if seisinfo is None:
        vis_msg.print('WARNING in retrieveSeisSampleFrom3DMat: Survey info auto-generated from 3D seismic matrix', type='warning')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)
    if samples is None:
        vis_msg.print('WARNING in retrieveSeisSampleFrom3DMat: to retrieve all samples in 3D seismic matrix', type='warning')
        return convertSeis3DMatTo2DMat(seis3dmat, seisinfo)
    if np.ndim(samples) != 2:
        vis_msg.print('ERROR in retrieveSeisSampleFrom3DMat: 2D matrix of samples expected', type='error')
        sys.exit()
    if len(samples[0, :]) < 3:
        vis_msg.print('ERROR in retrieveSeisSampleFrom3DMat: 3 columns expected in 2D sample matrix', type='error')
        sys.exit()
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum = seisinfo['ZNum']
    if inlnum == 1:
        inlstep = 1
    if xlnum == 1:
        xlstep = 1
    if znum == 1:
        zstep = -1
    nsample, _ = np.shape(samples)
    if verbose:
        print('Retrieve ' + str(nsample) + ' samples')
    seisdata = np.zeros([nsample, 4], np.float32)
    for i in range(nsample):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nsample) * 100.0))
            sys.stdout.flush()
        inl = samples[(i, 0)]
        xl = samples[(i, 1)]
        z = samples[(i, 2)]
        inlidx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        xlidx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        zidx = np.round((z - zstart) / zstep).astype(np.int32)
        if inlidx >= 0 and inlidx < inlnum and xlidx >= 0 and xlidx < xlnum and zidx >= 0 and zidx < znum:
            idx = inlidx * xlnum * znum + xlidx * znum + zidx
            seisdata[(i, 0)] = inlidx * inlstep + inlstart
            seisdata[(i, 1)] = xlidx * xlstep + xlstart
            seisdata[(i, 2)] = zidx * zstep + zstart
            seisdata[(i, 3)] = seis3dmat[(zidx, xlidx, inlidx)]

    if verbose:
        sys.stdout.write(' Done\n')
    return seisdata


def retrieveSeisILSliceFrom2DMat(seis2dmat, inlsls=None, datacol=3, inlcol=0, xlcol=1, zcol=2, verbose=True):
    """
    Retrieve seismic data along specified inline slices from 2D matrix (Seis2DMat)

    Args:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value, ...]
        inlsls:     list of inline slices in array [inl1, inl2, ...]
                    Retrieve all inline slices if not specified
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        verbose:    flag for message display. Default is True

    Return:
        seisdata:   seismic data along specified inline slices
                    2D matrix of four columns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis2dmat) != 2:
        vis_msg.print('ERROR in retrieveSeisILSliceFrom2DMat: 2D seismic matrix expected', type='error')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        vis_msg.print('ERROR in retrieveSeisILSliceFrom2DMat: No data columns found in 2D seismic matrix', type='error')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) < inlcol:
        vis_msg.print('ERROR in retrieveSeisILSliceFrom2DMat: No inline column found in 2D seismic matrix', type='error')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) < xlcol:
        vis_msg.print('ERROR in retrieveSeisILSliceFrom2DMat: No crossline column found in 2D seismic matrix', type='error')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) < zcol:
        vis_msg.print('ERROR in retrieveSeisILSliceFrom2DMat: No z column found in 2D seismic matrix', type='error')
        sys.exit()
    if inlsls is None:
        vis_msg.print('WARNING in retrieveSeisILSliceFrom2DMat: to retrieve all inline slices in 2D seismic matrix', type='warning')
        inlloc = seis2dmat[:, inlcol]
        xlloc = seis2dmat[:, xlcol]
        zloc = seis2dmat[:, zcol]
        seisdata = seis2dmat[:, datacol]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((inlloc, xlloc, zloc, seisdata), axis=1)
        return seisdata
    if np.ndim(inlsls) != 1:
        vis_msg.print('ERROR in retrieveSeisILSliceFrom2DMat: 1D array of inline slices expected', type='error')
        sys.exit()
    seisinfo = getSeisInfoFrom2DMat(seis2dmat, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    inl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=inlcol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    xl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=xlcol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    z3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=zcol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if inlnum == 1:
        inlstep = 1
    ninlsls = len(inlsls)
    if verbose:
        print('Retrieve ' + str(ninlsls) + ' inline slices')
    seisinl = np.zeros([znum, xlnum, ninlsls], np.float32)
    seisxl = np.zeros([znum, xlnum, ninlsls], np.float32)
    seisz = np.zeros([znum, xlnum, ninlsls], np.float32)
    seisdata = np.zeros([znum, xlnum, ninlsls], np.float32)
    for i in range(ninlsls):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ninlsls) * 100.0))
            sys.stdout.flush()
        inl = inlsls[i]
        idx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        if idx >= 0 and idx < inlnum:
            seisinl[:, :, i] = inl3dmat[:, :, idx]
            seisxl[:, :, i] = xl3dmat[:, :, idx]
            seisz[:, :, i] = z3dmat[:, :, idx]
            seisdata[:, :, i] = seis3dmat[:, :, idx]

    if verbose:
        sys.stdout.write(' Done\n')
    seisinl = seisinl.transpose()
    seisinl = np.reshape(seisinl, [1, znum * xlnum * ninlsls])
    seisinl = seisinl.transpose()
    seisxl = seisxl.transpose()
    seisxl = np.reshape(seisxl, [1, znum * xlnum * ninlsls])
    seisxl = seisxl.transpose()
    seisz = seisz.transpose()
    seisz = np.reshape(seisz, [1, znum * xlnum * ninlsls])
    seisz = seisz.transpose()
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, znum * xlnum * ninlsls])
    seisdata = seisdata.transpose()
    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)
    return seisdata


def retrieveSeisILSliceFrom3DMat(seis3dmat, inlsls=None, seisinfo=None, verbose=True):
    """
    Retrieve seismic data along specified inline slices from 3D matrix (Seis3DMat)

    Args:
        seisddmat:  seismic data in 3D matrix [Z/XL/IL]
        inlsls:     list of inline slices in array [inl1, inl2, ...]
                    Retrieve all inline slices if not specified
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        verbose:    flag for message display. Default is True

    Return:
        seisdata:   seismic data along specified inline slices
                    2D matrix of four columns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis3dmat) != 3:
        vis_msg.print('ERROR in retrieveSeisILSliceFrom3DMat: 3D seismic matrix expected', type='error')
        sys.exit()
    if seisinfo is None:
        vis_msg.print('WARNING in retrieveSeisILSliceFrom3DMat: Survey info auto-generated from 3D seismic matrix', type='warning')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)
    if inlsls is None:
        vis_msg.print('WARNING in retrieveSeisILSliceFrom3DMat: to retrieve all inline slices in 3D seismic matrix', type='warning')
        seis2dmat = convertSeis3DMatTo2DMat(seis3dmat, seisinfo)
        seisloc = seis2dmat[:, 0:3]
        seisdata = seis2dmat[:, 3]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((seisloc, seisdata), axis=1)
        return seisdata
    if np.ndim(inlsls) != 1:
        vis_msg.print('ERROR in retrieveSeisILSliceFrom3DMat: 1D array of inline slices expected', tpye='error')
        sys.exit()
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if inlnum == 1:
        inlstep = 1
    ninlsls = len(inlsls)
    if verbose:
        print('Retrieve ' + str(ninlsls) + ' inline slices')
    seisdata = np.zeros([znum, xlnum, ninlsls], np.float32)
    for i in range(ninlsls):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i + 1) / float(ninlsls) * 100.0))
            sys.stdout.flush()
        inl = inlsls[i]
        idx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        if idx >= 0 and idx < inlnum:
            seisdata[:, :, i] = seis3dmat[:, :, idx]

    if verbose:
        sys.stdout.write(' Done\n')
    all_sample = np.arange(0, ninlsls * xlnum * znum)
    seisinl = inlsls
    seisinl = np.reshape(seisinl[(all_sample / xlnum / znum).astype(int)], [-1, 1])
    seisxl = seisinfo['XLRange']
    seisxl = np.reshape(seisxl[(all_sample / znum % xlnum).astype(int)], [-1, 1])
    seisz = seisinfo['ZRange']
    seisz = np.reshape(seisz[(all_sample % znum).astype(int)], [-1, 1])
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, znum * xlnum * ninlsls])
    seisdata = seisdata.transpose()
    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)
    return seisdata


def cutSeisILSliceFrom2DMat(seis2dmat, inlsls=None, imageheight=100, imagewidth=100, xlstart=None, xlend=None, xlstep=None, zstart=None, zend=None, zstep=None, datacol=3, inlcol=0, xlcol=1, zcol=2, verbose=True):
    """
    Cut seismic inline slices from Seis2DMat

    Args:
        seis2dmat:      seismic data in 2D array
        inlsls:         inline slices for cutting. Default is None, to cut all slices
        imageheight:    image height. Default is 100
        imagewidth:     image width. Default is 100
        xlstart:        first xline. Default is None, to cut from the first xline
        xlend:          last xline. Default is None, to cut until the last xline
        xlstep:         xline step. Default is None, to cut with the xline step
        zstart:         first z. Default is None, to cut from the z
        zend:           last z. Default is None, to cut until the last z
        zstep:          z step. Default is None, to cut with the z step
        datacol:        data column index in Seis2DMat. Default is 3
        inlcol:         inline column index in Seis2DMat. Default is 0
        xlcol:          xline column index in Seis2DMat. Default is 1
        zcol:           z column index in Seis2DMat. Default is 2
        verbose:        verbose option for progress display. Default is True

    Return:
        A 4D array of the cut inline slices, with
            Dimension 1 ----- inline
            Dimension 2 ----- crossline
            Dimension 3 ----- z
            Dimension 4 ----- pixel
    """
    seisinfo = getSeisInfoFrom2DMat(seis2dmat, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    if inlsls is None:
        vis_msg.print('WARNING in cutSeisILSliceFrom2DMat: to cut all inline slices in 2D seismic matrix', type='error')
        inlsls = seisinfo['ILRange']
    if xlstart is None:
        xlstart = seisinfo['XLStart']
    if xlend is None:
        xlend = seisinfo['XLEnd']
    if xlstep is None:
        xlstep = seisinfo['XLStep']
    if zstart is None:
        zstart = seisinfo['ZStart']
    if zend is None:
        zend = seisinfo['ZEnd']
    if zstep is None:
        zstep = seisinfo['ZStep']
    xlidx = np.arange(xlstart, xlend + 1, xlstep)
    xlidx = np.round((xlidx - seisinfo['XLStart']) / seisinfo['XLStep']).astype(np.int32)
    xlidx = np.unique(xlidx)
    outidx = []
    for i in range(len(xlidx)):
        if xlidx[i] < 0 or xlidx[i] + imagewidth > seisinfo['XLNum']:
            outidx.append(i)

    xlidx = np.delete(xlidx, outidx)
    zidx = np.arange(zstart, zend, zstep)
    zidx = np.round((zidx - seisinfo['ZStart']) / seisinfo['ZStep']).astype(np.int32)
    zidx = np.unique(zidx)
    outidx = []
    for i in range(len(zidx)):
        if not zidx[i] < 0:
            if zidx[i] + imageheight > seisinfo['ZNum']:
                pass
            outidx.append(i)

    zidx = np.delete(zidx, outidx)
    ninlsls = len(inlsls)
    if verbose:
        print('Cut ' + str(ninlsls) + ' inline slices')
    nxlidx = len(xlidx)
    nzidx = len(zidx)
    seisilslicepatch = np.zeros([ninlsls, nxlidx, nzidx, imageheight, imagewidth])
    for i in range(ninlsls):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ninlsls) * 100.0))
            sys.stdout.flush()
        inl = inlsls[i]
        idx = np.round((inl - seisinfo['ILStart']) / seisinfo['ILStep']).astype(np.int32)
        for j in range(nxlidx):
            for k in range(nzidx):
                seisilslicepatch[i, j, k, :, :] = seis3dmat[zidx[k]:zidx[k] + imageheight, xlidx[j]:xlidx[j] + imagewidth, idx]

    if verbose:
        sys.stdout.write(' Done\n')
    return np.reshape(seisilslicepatch, [ninlsls, nxlidx, nzidx, imageheight * imagewidth])


def retrieveSeisXLSliceFrom2DMat(seis2dmat, xlsls=None, datacol=3, inlcol=0, xlcol=1, zcol=2, verbose=True):
    """
    Retrieve seismic data along specified crossline slices from 2D matrix (Seis2DMat)

    Args:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value, ...]
        xlsls:      list of crossline slices in array [xl1, xl2, ...]
                    Retrieve all crossline slices if not specified
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        verbose:    flag for message display. Default is True

    Return:
        seisdata:   seismic data along specified crossline slices
                    as 2D matrix of four columns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis2dmat) != 2:
        vis_msg.print('ERROR in retrieveSeisXLSliceFrom2DMat: 2D seismic matrix expected', type='error')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        vis_msg.print('ERROR in retrieveSeisXLSliceFrom2Dmat: Not data column found in 2D seismic matrix', type='error')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) <= inlcol:
        vis_msg.print('ERROR in retrieveSeisXLSliceFrom2Dmat: Not inline column found in 2D seismic matrix', type='error')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) <= xlcol:
        vis_msg.print('ERROR in retrieveSeisXLSliceFrom2Dmat: Not crossline column found in 2D seismic matrix', type='error')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) <= zcol:
        vis_msg.print('ERROR in retrieveSeisXLSliceFrom2Dmat: Not z column found in 2D seismic matrix', type='error')
        sys.exit()
    if xlsls is None:
        vis_msg.print('WARNING in retrieveSeisXLSliceFrom2DMat: to retrieve all crossline slices in 2D seismic matrix', type='warning')
        inlloc = seis2dmat[:, inlcol]
        xlloc = seis2dmat[:, xlcol]
        zloc = seis2dmat[:, zcol]
        seisdata = seis2dmat[:, datacol]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((inlloc, xlloc, zloc, seisdata), axis=1)
        return seisdata
    if np.ndim(xlsls) != 1:
        vis_msg.print('ERROR in retrieveSeisXLSliceFrom2DMat: 1D array of crossline slices expected', type='error')
        sys.exit()
    seisinfo = getSeisInfoFrom2DMat(seis2dmat, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    inl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=inlcol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    xl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=xlcol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    z3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=zcol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if xlnum == 1:
        xlstep = 1
    nxlsls = len(xlsls)
    if verbose:
        print('Retrieve ' + str(nxlsls) + ' crossline slices')
    seisinl = np.zeros([znum, nxlsls, inlnum], np.float32)
    seisxl = np.zeros([znum, nxlsls, inlnum], np.float32)
    seisz = np.zeros([znum, nxlsls, inlnum], np.float32)
    seisdata = np.zeros([znum, nxlsls, inlnum], np.float32)
    for i in range(nxlsls):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nxlsls) * 100.0))
            sys.stdout.flush()
        xl = xlsls[i]
        idx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        if idx >= 0 and idx < xlnum:
            seisinl[:, i, :] = inl3dmat[:, idx, :]
            seisxl[:, i, :] = xl3dmat[:, idx, :]
            seisz[:, i, :] = z3dmat[:, idx, :]
            seisdata[:, i, :] = seis3dmat[:, idx, :]

    if verbose:
        sys.stdout.write(' Done\n')
    seisinl = seisinl.transpose()
    seisinl = np.reshape(seisinl, [1, znum * nxlsls * inlnum])
    seisinl = seisinl.transpose()
    seisxl = seisxl.transpose()
    seisxl = np.reshape(seisxl, [1, znum * nxlsls * inlnum])
    seisxl = seisxl.transpose()
    seisz = seisz.transpose()
    seisz = np.reshape(seisz, [1, znum * nxlsls * inlnum])
    seisz = seisz.transpose()
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, znum * nxlsls * inlnum])
    seisdata = seisdata.transpose()
    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)
    return seisdata


def retrieveSeisXLSliceFrom3DMat(seis3dmat, xlsls=None, seisinfo=None, verbose=True):
    """
    Retrieve seismic data along specified crossline slices from 3D matrix (Seis3DMat)

    Args:
        seisddmat:  seismic data in 3D matrix [Z/XL/IL]
        xlsls:     list of crossline slices in array [xl1, xl2, ...]
                    Retrieve all crossline slices if not specified
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        verbose:    flag for message display. Default is True

    Return:
        seisdata:   seismic data along specified inline slices
                    2D matrix of four columns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis3dmat) != 3:
        vis_msg.print('ERROR in retrieveSeisXLSliceFrom3DMat: 3D seismic matrix expected', type='error')
        sys.exit()
    if seisinfo is None:
        vis_msg.print('WARNING in retrieveSeisXLSliceFrom3DMat: Survey info auto-generated from 3D seismic matrix', type='warning')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)
    if xlsls is None:
        vis_msg.print('WARNING in retrieveSeisXLSliceFrom3DMat: to retrieve all crossline slices in 3D seismic matrix', type='warning')
        seis2dmat = convertSeis3DMatTo2DMat(seis3dmat, seisinfo)
        seisloc = seis2dmat[:, 0:3]
        seisdata = seis2dmat[:, 3]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((seisloc, seisdata), axis=1)
        return seisdata
    if np.ndim(xlsls) != 1:
        vis_msg.print('ERROR in retrieveSeisXLSliceFrom3DMat: 1D array of crossline slices expected', type='error')
        sys.exit()
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if xlnum == 1:
        xlstep = 1
    nxlsls = len(xlsls)
    if verbose:
        print('Retrieve ' + str(nxlsls) + ' crossline slices')
    seisdata = np.zeros([znum, nxlsls, inlnum], np.float32)
    for i in range(nxlsls):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i + 1) / float(nxlsls) * 100.0))
            sys.stdout.flush()
        xl = xlsls[i]
        idx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        if idx >= 0 and idx < xlnum:
            seisdata[:, i, :] = seis3dmat[:, idx, :]

    if verbose:
        sys.stdout.write(' Done\n')
    all_sample = np.arange(0, inlnum * nxlsls * znum)
    seisinl = seisinfo['ILRange']
    seisinl = np.reshape(seisinl[(all_sample / nxlsls / znum).astype(int)], [-1, 1])
    seisxl = xlsls
    seisxl = np.reshape(seisxl[(all_sample / znum % nxlsls).astype(int)], [-1, 1])
    seisz = seisinfo['ZRange']
    seisz = np.reshape(seisz[(all_sample % znum).astype(int)], [-1, 1])
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, znum * nxlsls * inlnum])
    seisdata = seisdata.transpose()
    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)
    return seisdata


def cutSeisXLSliceFrom2DMat(seis2dmat, xlsls=None, imageheight=100, imagewidth=100, inlstart=None, inlend=None, inlstep=None, zstart=None, zend=None, zstep=None, datacol=3, inlcol=0, xlcol=1, zcol=2, verbose=True):
    """
    Cut seismic crossline slices from Seis2DMat

    Args:
        seis2dmat:      seismic data in 2D array
        xlsls:          crossline slices for cutting. Default is None, to cut all slices
        imageheight:    image height. Default is 100
        imagewidth:     image width. Default is 100
        inlstart:       first inline. Default is None, to cut from the first inline
        inlend:         last inline. Default is None, to cut until the last inline
        inlstep:        inline step. Default is None, to cut with the inline step
        zstart:         first z. Default is None, to cut from the z
        zend:           last z. Default is None, to cut until the last z
        zstep:          z step. Default is None, to cut with the z step
        datacol:        data column index in Seis2DMat. Default is 3
        inlcol:         inline column index in Seis2DMat. Default is 0
        xlcol:          xline column index in Seis2DMat. Default is 1
        zcol:           z column index in Seis2DMat. Default is 2
        verbose:        verbose option for progress display. Default is True

    Return:
        A 4D array of the cut inline slices, with
            Dimension 1 ----- inline
            Dimension 2 ----- crossline
            Dimension 3 ----- z
            Dimension 4 ----- pixel
    """
    seisinfo = getSeisInfoFrom2DMat(seis2dmat, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    if xlsls is None:
        vis_msg.print('WARNING in cutSeisXLSliceFrom2DMat: to cut all crossline slices in 2D seismic matrix', type='warning')
        inlsls = seisinfo['ILRange']
    if inlstart is None:
        inlstart = seisinfo['ILStart']
    if inlend is None:
        inlend = seisinfo['ILEnd']
    if inlstep is None:
        inlstep = seisinfo['ILStep']
    if zstart is None:
        zstart = seisinfo['ZStart']
    if zend is None:
        zend = seisinfo['ZEnd']
    if zstep is None:
        zstep = seisinfo['ZStep']
    inlidx = np.arange(inlstart, inlend + 1, inlstep)
    inlidx = np.round((inlidx - seisinfo['ILStart']) / seisinfo['ILStep']).astype(np.int32)
    inlidx = np.unique(inlidx)
    outidx = []
    for i in range(len(inlidx)):
        if inlidx[i] < 0 or inlidx[i] + imagewidth > seisinfo['ILNum']:
            outidx.append(i)

    inlidx = np.delete(inlidx, outidx)
    zidx = np.arange(zstart, zend, zstep)
    zidx = np.round((zidx - seisinfo['ZStart']) / seisinfo['ZStep']).astype(np.int32)
    zidx = np.unique(zidx)
    outidx = []
    for i in range(len(zidx)):
        if not zidx[i] < 0:
            if zidx[i] + imageheight > seisinfo['ZNum']:
                pass
            outidx.append(i)

    zidx = np.delete(zidx, outidx)
    nxlsls = len(xlsls)
    if verbose:
        print('Cut ' + str(nxlsls) + ' crossline slices')
    ninlidx = len(inlidx)
    nzidx = len(zidx)
    seisxlslicepatch = np.zeros([ninlidx, nxlsls, nzidx, imageheight, imagewidth])
    for i in range(nxlsls):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nxlsls) * 100.0))
            sys.stdout.flush()
        xl = xlsls[i]
        idx = np.round((xl - seisinfo['XLStart']) / seisinfo['ILStep']).astype(np.int32)
        for j in range(ninlidx):
            for k in range(nzidx):
                seisxlslicepatch[j, i, k, :, :] = seis3dmat[zidx[k]:zidx[k] + imageheight, idx, inlidx[j]:inlidx[j] + imagewidth]

    if verbose:
        sys.stdout.write(' Done\n')
    return np.reshape(seisxlslicepatch, [ninlidx, nxlsls, nzidx, imageheight * imagewidth])


def retrieveSeisZSliceFrom2DMat(seis2dmat, zsls=None, datacol=3, inlcol=0, xlcol=1, zcol=2, verbose=True):
    """
    Retrieve seismic data along specified z slices from 2D matrix (Seis2DMat)

    Args:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value]
        zsls:       list of z slices in array [z1, z2, ...]
                    Retrieve all z slices if not specified
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        verbose:    flag for message display. Default is True

    Return:
        seisdata:   seismic data along specified z slices
                    2D matrix of four columns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis2dmat) != 2:
        vis_msg.print('ERROR in retrieveSeisZSliceFrom2DMat: 2D seismic matrix expected', type='error')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        vis_msg.print('ERROR in retrieveSeisZSliceFrom2DMat: Not data column found in 2D seismic matrix', type='error')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) <= inlcol:
        vis_msg.print('ERROR in retrieveSeisZSliceFrom2DMat: Not inline column found in 2D seismic matrix', type='error')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) <= xlcol:
        vis_msg.print('ERROR in retrieveSeisZSliceFrom2DMat: Not crossline column found in 2D seismic matrix', type='error')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) <= zcol:
        vis_msg.print('ERROR in retrieveSeisZSliceFrom2DMat: Not z column found in 2D seismic matrix', tpye='error')
        sys.exit()
    if zsls is None:
        vis_msg.print('WARNING in retrieveSeisZSliceFrom2DMat: to retrieve all z slices in 2D seismic matrix', type='warning')
        inlloc = seis2dmat[:, inlcol]
        xlloc = seis2dmat[:, xlcol]
        zloc = seis2dmat[:, zcol]
        seisdata = seis2dmat[:, datacol]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((inlloc, xlloc, zloc, seisdata), axis=1)
        return seisdata
    if np.ndim(zsls) != 1:
        vis_msg.print('ERROR in retrieveSeisZSliceFrom2DMat: 1D array for z slices expected', type='error')
        sys.exit()
    seisinfo = getSeisInfoFrom2DMat(seis2dmat, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    inl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=inlcol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    xl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=xlcol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    z3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=2, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if znum == 1:
        zstep = -1
    nzsls = len(zsls)
    if verbose:
        print('Retrieve ' + str(nzsls) + ' z slices')
    seisinl = np.zeros([nzsls, xlnum, inlnum], np.float32)
    seisxl = np.zeros([nzsls, xlnum, inlnum], np.float32)
    seisz = np.zeros([nzsls, xlnum, inlnum], np.float32)
    seisdata = np.zeros([nzsls, xlnum, inlnum], np.float32)
    for i in range(nzsls):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nzsls) * 100.0))
            sys.stdout.flush()
        z = zsls[i]
        idx = np.round((z - zstart) / zstep).astype(np.int32)
        if idx >= 0 and idx < znum:
            seisinl[i, :, :] = inl3dmat[idx, :, :]
            seisxl[i, :, :] = xl3dmat[idx, :, :]
            seisz[i, :, :] = z3dmat[idx, :, :]
            seisdata[i, :, :] = seis3dmat[idx, :, :]

    if verbose:
        sys.stdout.write(' Done\n')
    seisinl = seisinl.transpose()
    seisinl = np.reshape(seisinl, [1, nzsls * xlnum * inlnum])
    seisinl = seisinl.transpose()
    seisxl = seisxl.transpose()
    seisxl = np.reshape(seisxl, [1, nzsls * xlnum * inlnum])
    seisxl = seisxl.transpose()
    seisz = seisz.transpose()
    seisz = np.reshape(seisz, [1, nzsls * xlnum * inlnum])
    seisz = seisz.transpose()
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, nzsls * xlnum * inlnum])
    seisdata = seisdata.transpose()
    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)
    return seisdata


def retrieveSeisZSliceFrom3DMat(seis3dmat, zsls=None, seisinfo=None, verbose=True):
    """
    Retrieve seismic data along specified z slices from 3D matrix (Seis3DMat)

    Args:
        seisddmat:  seismic data in 3D matrix [Z/XL/IL]
        zlsls:      list of z slices in array [z1, z2, ...]
                    Retrieve all z slices if not specified
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        verbose:    flag for message display. Default is True

    Return:
        seisdata:   seismic data along specified inline slices
                    2D matrix of four columns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis3dmat) != 3:
        vis_msg.print('ERROR in retrieveSeisZSliceFrom3DMat: 3D seismic matrix expected', type='error')
        sys.exit()
    if seisinfo is None:
        vis_msg.print('WARNING in retrieveSeisZSliceFrom3DMat: Survey info auto-generated from 3D seismic matrix', type='warning')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)
    if zsls is None:
        vis_msg.print('WARNING in retrieveSeisZSliceFrom3DMat: to retrieve all z slices', type='warning')
        seis2dmat = convertSeis3DMatTo2DMat(seis3dmat, seisinfo)
        seisloc = seis2dmat[:, 0:3]
        seisdata = seis2dmat[:, 3]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((seisloc, seisdata), axis=1)
        return seisdata
    if np.ndim(zsls) != 1:
        vis_msg.print('ERROR in retrieveSeisZSliceFrom3DMat: 1D array of z slices expected', type='error')
        sys.exit()
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if znum == 1:
        zstep = -1
    nzsls = len(zsls)
    if verbose:
        print('Retrieve ' + str(nzsls) + ' z slices')
    seisdata = np.zeros([nzsls, xlnum, inlnum], np.float32)
    for i in range(nzsls):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i + 1) / float(nzsls) * 100.0))
            sys.stdout.flush()
        z = zsls[i]
        idx = np.round((z - zstart) / zstep).astype(np.int32)
        if idx >= 0 and idx < znum:
            seisdata[i, :, :] = seis3dmat[idx, :, :]

    if verbose:
        sys.stdout.write(' Done\n')
    all_sample = np.arange(0, inlnum * xlnum * nzsls)
    seisinl = seisinfo['ILRange']
    seisinl = np.reshape(seisinl[(all_sample / xlnum / nzsls).astype(int)], [-1, 1])
    seisxl = seisinfo['XLRange']
    seisxl = np.reshape(seisxl[(all_sample / nzsls % xlnum).astype(int)], [-1, 1])
    seisz = zsls
    seisz = np.reshape(seisz[(all_sample % nzsls).astype(int)], [-1, 1])
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, nzsls * xlnum * inlnum])
    seisdata = seisdata.transpose()
    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)
    return seisdata


def retrieveSeisWindowFrom2DMat(seis2dmat, wdctrs, datacol=3, inlcol=0, xlcol=1, zcol=2, wdinl=0, wdxl=0, wdz=0, verbose=True, qpgsdlg=None):
    """
    Retrieve seismic data in a specified window from 2D matrix (Seis2DMat)

    Args:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value, ...]
        wdctrs:     list of window centers in 2D matrix of three columns [IL, XL, Z]
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        wdinl:      window radius along inline direction. Default is 0
        wdxl:       window radius along crossline direction. Default is 0
        wdz:        window radius along z direction. Default is 0
        verbose:    flag for message display. Default is True
        qpgsdlg:    QProgressDialog for displaying progress. Default is None

    Return:
        seisdata:   seismic data in a specified window
                    2D matrix of four columns [IL, XL, Z, WD1, WD2, WD3, ...]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis2dmat) != 2:
        vis_msg.print('ERROR in retrieveSeisWindowFrom2DMat: 2D seismic matrix expected', type='error')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        vis_msg.print('ERROR in retrieveSeisWindowFrom2DMat: Not data column found in 2D seismic matrix', type='error')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) < inlcol:
        vis_msg.print('ERROR in retrieveSeisWindowFrom2DMat: No inline column found in 2D seismic matrix', type='error')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) < xlcol:
        vis_msg.print('ERROR in retrieveSeisWindowFrom2DMat: No crossline column found in 2D seismic matrix', type='error')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) < zcol:
        vis_msg.print('ERROR in retrieveSeisWindowFrom2DMat: No z column found in 2D seismic matrix', type='error')
        sys.exit()
    if np.ndim(wdctrs) != 2:
        vis_msg.print('ERROR in retrieveSeisWindowFrom2DMat: 2D matrix of window centers expected', type='error')
        sys.exit()
    if len(wdctrs[0, :]) < 3:
        vis_msg.print('ERROR in retrieveSeisWindowFrom2DMat: 3 columns expected in 2D window-center matrix', type='error')
        sys.exit()
    if wdinl < 0 or wdxl < 0 or wdz < 0:
        vis_msg.print('ERROR in retrieveSeisWindowFrom2DMat: Wrong window size', type='error')
        sys.exit()
    seisinfo = getSeisInfoFrom2DMat(seis2dmat, inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol,
      inlcol=inlcol,
      xlcol=xlcol,
      zcol=zcol)
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum = seisinfo['ZNum']
    if inlnum == 1:
        inlstep = 1
    if xlnum == 1:
        xlstep = 1
    if znum == 1:
        zstep = -1
    nwdctr, _ = np.shape(wdctrs)
    if verbose:
        print('Retrieve ' + str(nwdctr) + ' window centers')
    wdinlsize = 2 * wdinl + 1
    wdxlsize = 2 * wdxl + 1
    wdzsize = 2 * wdz + 1
    wdsize = wdinlsize * wdxlsize * wdzsize
    if qpgsdlg is not None:
        qpgsdlg.setMaximum(nwdctr)
    seisdata = np.zeros([nwdctr, 3 + wdsize], np.float32)
    for i in range(nwdctr):
        if qpgsdlg is not None:
            QtCore.QCoreApplication.instance().processEvents()
            qpgsdlg.setValue(i)
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nwdctr) * 100.0))
            sys.stdout.flush()
        inl = wdctrs[(i, 0)]
        xl = wdctrs[(i, 1)]
        z = wdctrs[(i, 2)]
        inlidx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        xlidx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        zidx = np.round((z - zstart) / zstep).astype(np.int32)
        if inlidx >= wdinl and inlidx < inlnum - wdinl and xlidx >= wdxl and xlidx < xlnum - wdxl and zidx >= wdz and zidx < znum - wdz:
            idx = inlidx * xlnum * znum + xlidx * znum + zidx
            seisdata[(i, 0)] = seis2dmat[(idx, inlcol)]
            seisdata[(i, 1)] = seis2dmat[(idx, xlcol)]
            seisdata[(i, 2)] = seis2dmat[(idx, zcol)]
            seiswd = seis3dmat[zidx - wdz:zidx + wdz + 1, xlidx - wdxl:xlidx + wdxl + 1, inlidx - wdinl:inlidx + wdinl + 1]
            seisdata[i, 3:3 + wdsize] = np.reshape(seiswd, [1, wdsize])

    if qpgsdlg is not None:
        qpgsdlg.setValue(nwdctr)
    if verbose:
        sys.stdout.write(' Done\n')
    return seisdata


def assignSeisWindowTo2DMat(seis2dmat, seiswd, wdinl=0, wdxl=0, wdz=0, verbose=True):
    """
    Assign seismic patches into Seis2DMat

    Args:
        seis2dmat:  Seismic data in a 2D array
        seiswd:     Seismic patches as a 2D array, with inline/crossline/z in column 1/2/3.
                    The pixel number is equal to (2*wdinl+1) * (2*wdxl+1) * (2*wdz+1)
        wdinl:      Window radius along inline. Default is 0
        wdxl:       Window radius along crossline. Default is 0
        wdz:        Window radius along z. Default is 0
        verbose:

    Return:
         Seis2DMat with new values assigned
    """
    seisinfo = getSeisInfoFrom2DMat(seis2dmat)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat)
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum = seisinfo['ZNum']
    nwd = np.shape(seiswd)[0]
    inlsize = 2 * wdinl + 1
    xlsize = 2 * wdxl + 1
    zsize = 2 * wdz + 1
    if verbose:
        print('Assign ' + str(nwd) + ' windows')
    for i in range(nwd):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nwd) * 100.0))
            sys.stdout.flush()
        inl = seiswd[(i, 0)]
        xl = seiswd[(i, 1)]
        z = seiswd[(i, 2)]
        inlidx = int((inl - inlstart) / inlstep)
        xlidx = int((xl - xlstart) / xlstep)
        zidx = int((z - zstart) / zstep)
        if inlidx >= wdinl and inlidx < inlnum - wdinl and xlidx >= wdxl and xlidx < xlnum - wdxl and zidx >= wdz and zidx < znum - wdz:
            seisdata = seis3dmat[zidx - wdz:zidx + wdz + 1, xlidx - wdxl:xlidx + wdxl + 1, inlidx - wdinl:inlidx + wdinl + 1]
            seisdata = np.reshape(seisdata, [inlsize * xlsize * zsize])
            for j in range(inlsize * xlsize * zsize):
                if seisdata[j] == 0.0:
                    seisdata[j] = seiswd[(i, 3 + j)]
                seisdata[j] = 0.5 * (seisdata[j] + seiswd[(i, 3 + j)])

            seisdata = np.reshape(seisdata, [zsize, xlsize, inlsize])
            seis3dmat[zidx - wdz:zidx + wdz + 1, xlidx - wdxl:xlidx + wdxl + 1, inlidx - wdinl:inlidx + wdinl + 1] = seisdata

    if verbose:
        sys.stdout.write(' Done\n')
    return convertSeis3DMatTo2DMat(seis3dmat, seisinfo)


def retrieveSeisWindowFrom3DMat(seis3dmat, wdseeds, seedloc='center', seisinfo=None, wdinl=0, wdxl=0, wdz=0, verbose=True, qpgsdlg=None):
    """
    Retrieve seismic data in a specified window from 3D matrix (Seis3DMat)

    Args:
        seis3dmat:  seismic data in 3D matrix [Z/XL/IL]
        wdseeds:    list of window centers in 2D matrix of three columns [IL, XL, Z]
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        seedloc:    location of the seeds: center or top
        wdinl:      window size (from top) or radius (from center) along inline direction. Default is 0
        wdxl:       window size (from top) or radius (from center) along crossline direction. Default is 0
        wdz:        window size (from top) or radius (from center) along z direction. Default is 0
        verbose:    flag for message display. Default is True
        qpgsdlg:    QProgressDialog for displaying progress. Default is None

    Return:
        seisdata:   seismic data on specified samples
                    2D matrix of four columns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(seis3dmat) != 3:
        vis_msg.print('ERROR in retrieveSeisWindowFrom3DMat: 3D seismic matrix expected', type='error')
        sys.exit()
    else:
        if seisinfo is None:
            vis_msg.print('WARNING in retrieveSeisWindowFrom3DMat: Survey info auto-generated from 3D seismic matrix', type='warning')
            seisinfo = createSeisInfoFrom3DMat(seis3dmat)
        if np.ndim(wdseeds) != 2:
            vis_msg.print('ERROR in retrieveSeisWindowFrom3DMat: 2D matrix of window centers expected', type='warning')
            sys.exit()
        if len(wdseeds[0, :]) < 3:
            vis_msg.print('ERROR in retrieveSeisWindowFrom3DMat: 3-column window-center list expected', type='error')
            sys.exit()
        if not wdinl < 0:
            if wdxl < 0 or wdz < 0:
                vis_msg.print('ERROR in retrieveSeisWindowFrom3DMat: Wrong window size', type='error')
                sys.exit()
            inlstart = seisinfo['ILStart']
            inlstep = seisinfo['ILStep']
            inlnum = seisinfo['ILNum']
            xlstart = seisinfo['XLStart']
            xlstep = seisinfo['XLStep']
            xlnum = seisinfo['XLNum']
            zstart = seisinfo['ZStart']
            zstep = seisinfo['ZStep']
            znum = seisinfo['ZNum']
            if inlnum == 1:
                inlstep = 1
            if xlnum == 1:
                xlstep = 1
            if znum == 1:
                zstep = -1
            nwdctr, _ = np.shape(wdseeds)
            if verbose:
                print('Retrieve ' + str(nwdctr) + ' window centers')
            wdinlsize = 0
            wdxlsize = 0
            wdzsize = 0
            if seedloc == 'center':
                wdinlsize = 2 * wdinl + 1
                wdxlsize = 2 * wdxl + 1
                wdzsize = 2 * wdz + 1
        else:
            wdinlsize = wdinl
        wdxlsize = wdxl
        wdzsize = wdz
    wdsize = wdinlsize * wdxlsize * wdzsize
    if qpgsdlg is not None:
        qpgsdlg.setMaximum(nwdctr)
    seisdata = np.zeros([nwdctr, 3 + wdsize], np.float32)
    for i in range(nwdctr):
        if qpgsdlg is not None:
            QtCore.QCoreApplication.instance().processEvents()
            qpgsdlg.setValue(i)
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nwdctr) * 100.0))
            sys.stdout.flush()
        inl = wdseeds[(i, 0)]
        xl = wdseeds[(i, 1)]
        z = wdseeds[(i, 2)]
        inlidx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        xlidx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        zidx = np.round((z - zstart) / zstep).astype(np.int32)
        if seedloc == 'center' and inlidx >= wdinl and inlidx < inlnum - wdinl and xlidx >= wdxl and xlidx < xlnum - wdxl and zidx >= wdz:
            if zidx < znum - wdz:
                seisdata[(i, 0)] = inlidx * inlstep + inlstart
                seisdata[(i, 1)] = xlidx * xlstep + xlstart
                seisdata[(i, 2)] = zidx * zstep + zstart
                seiswd = seis3dmat[zidx - wdz:zidx + wdz + 1, xlidx - wdxl:xlidx + wdxl + 1, inlidx - wdinl:inlidx + wdinl + 1]
                seisdata[i, 3:3 + wdsize] = np.reshape(seiswd, [1, wdsize])
            if seedloc != 'center' and inlidx >= 0 and inlidx <= inlnum - wdinl and xlidx >= 0 and xlidx <= xlnum - wdxl and zidx >= 0 and zidx <= znum - wdz:
                seisdata[(i, 0)] = inlidx * inlstep + inlstart
                seisdata[(i, 1)] = xlidx * xlstep + xlstart
                seisdata[(i, 2)] = zidx * zstep + zstart
                seiswd = seis3dmat[zidx:zidx + wdz, xlidx:xlidx + wdxl,
                 inlidx:inlidx + wdinl]
                seisdata[i, 3:3 + wdsize] = np.reshape(seiswd, [1, wdsize])

    if qpgsdlg is not None:
        qpgsdlg.setValue(nwdctr)
    if verbose:
        sys.stdout.write(' Done\n')
    return seisdata


def retrieveSeisILTraceFrom2DMat(seis2dmat, trctrs, wdxl=0, wdz=0, verbose=False):
    """
    Retrieve inline traces from 2D matrix (Seis2DMat)

    Args:
        seis2dmat:  Seismic data in 2D matrix
        trctrs:     List of trace locations in a 2D array, [crossline, z]
        seisinfo:   Seismic information dictionary as defined above
        wdxl:      Retrieval radius along crossline direction. Default is 0
        wdz:       Retrieval radius along z direction. Default is 0
        verbose:    Verbose of message display. Default is False

    Return:
        Retrieved traces as a 2D array, with each row representing a trace
        Length = z_sample * (2*wdxl+1) * (2*wdz+1)
        Trace location is at column 1 (inline) and 2 (z)
    """
    ntrace = np.shape(trctrs)[0]
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat)
    seisinfo = getSeisInfoFrom2DMat(seis2dmat)
    znum, xlnum, inlnum = np.shape(seis3dmat)
    rst = np.zeros([ntrace, 2 + inlnum * (2 * wdxl + 1) * (2 * wdz + 1)])
    rst[:, 0:2] = trctrs
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    for i in range(ntrace):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        xl = trctrs[(i, 0)]
        z = trctrs[(i, 1)]
        xl = (xl - seisinfo['XLStart']) / seisinfo['XLStep']
        xl = int(xl)
        z = (z - seisinfo['ZStart']) / seisinfo['ZStep']
        z = int(z)
        if xl - wdxl >= 0 and xl + wdxl < seisinfo['XLNum'] and z - wdz >= 0 and z + wdz < seisinfo['ZNum']:
            dat = seis3dmat[z - wdz:z + wdz + 1, xl - wdxl:xl + wdxl + 1, :]
            rst[i, 2:] = np.reshape(dat, [1, -1])

    if verbose:
        sys.stdout.write(' Done\n')
    return rst


def retrieveSeisILTraceFrom3DMat(seis3dmat, trctrs, wdxl=0, wdz=0, seisinfo=None, verbose=False):
    """
    Retrieve inline traces from 3D matrix (Seis3DMat)

    Args:
        seis3dmat:  Seismic data in 3D matrix
        trctrs:     List of trace locations in a 2D array, [crossline, z]
        seisinfo:   Seismic information dictionary as defined above
        wdxl:      Retrieval radius along crossline direction. Default is 0
        wdz:       Retrieval radius along z direction. Default is 0
        verbose:    Verbose of message display. Default is False

    Return:
        Retrieved traces as a 2D array, with each row representing a trace
        Length = z_sample * (2*wdxl+1) * (2*wdz+1)
        Trace location is at column 1 (inline) and 2 (z)
    """
    if seisinfo is None or checkSeisInfo(seisinfo) is False:
        vis_msg.print('Warning in retrieveSeisILTraceFrom3DMat: SeisInfo automatically generated', type='warning')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)
    ntrace = np.shape(trctrs)[0]
    znum, xlnum, inlnum = np.shape(seis3dmat)
    rst = np.zeros([ntrace, 2 + inlnum * (2 * wdxl + 1) * (2 * wdz + 1)])
    rst[:, 0:2] = trctrs
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    for i in range(ntrace):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        xl = trctrs[(i, 0)]
        z = trctrs[(i, 1)]
        xl = (xl - seisinfo['XLStart']) / seisinfo['XLStep']
        xl = int(xl)
        z = (z - seisinfo['ZStart']) / seisinfo['ZStep']
        z = int(z)
        if xl - wdxl >= 0 and xl + wdxl < seisinfo['XLNum'] and z - wdz >= 0 and z + wdz < seisinfo['ZNum']:
            dat = seis3dmat[z - wdz:z + wdz + 1, xl - wdxl:xl + wdxl + 1, :]
            rst[i, 2:] = np.reshape(dat, [1, -1])

    if verbose:
        sys.stdout.write(' Done\n')
    return rst


def retrieveSeisXLTraceFrom2DMat(seis2dmat, trctrs, wdinl=0, wdz=0, verbose=False):
    """
    Retrieve crossline traces from 3D matrix (Seis3DMat)

    Args:
        seis2dmat:  Seismic data in 2D matrix
        trctrs:     List of trace locations in a 2D array, [inline, z]
        seisinfo:   Seismic information dictionary as defined above
        wdinl:      Retrieval radius along inline direction. Default is 0
        wdz:       Retrieval radius along z direction. Default is 0
        verbose:    Verbose of message display. Default is False

    Return:
        Retrieved traces as a 2D array, with each row representing a trace
        Length = z_sample * (2*wdinl+1) * (2*wdz+1)
        Trace location is at column 1 (inline) and 2 (z)
    """
    ntrace = np.shape(trctrs)[0]
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat)
    seisinfo = getSeisInfoFrom2DMat(seis2dmat)
    znum, xlnum, inlnum = np.shape(seis3dmat)
    rst = np.zeros([ntrace, 2 + xlnum * (2 * wdinl + 1) * (2 * wdz + 1)])
    rst[:, 0:2] = trctrs
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    for i in range(ntrace):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        inl = trctrs[(i, 0)]
        z = trctrs[(i, 1)]
        inl = (inl - seisinfo['ILStart']) / seisinfo['ILStep']
        inl = int(inl)
        z = (z - seisinfo['ZStart']) / seisinfo['ZStep']
        z = int(z)
        if inl - wdinl >= 0 and inl + wdinl < seisinfo['ILNum'] and z - wdz >= 0 and z + wdz < seisinfo['ZNum']:
            dat = seis3dmat[z - wdz:z + wdz + 1, :, inl - wdinl:inl + wdinl + 1]
            rst[i, 2:] = np.reshape(dat, [1, -1])

    if verbose:
        sys.stdout.write(' Done\n')
    return rst


def retrieveSeisXLTraceFrom3DMat(seis3dmat, trctrs, wdinl=0, wdz=0, seisinfo=None, verbose=False):
    """
    Retrieve crossline traces from 3D matrix (Seis3DMat)

    Args:
        seis3dmat:  Seismic data in 3D matrix
        trctrs:     List of trace locations in a 2D array, [inline, z]
        seisinfo:   Seismic information dictionary as defined above
        wdinl:      Retrieval radius along inline direction. Default is 0
        wdz:       Retrieval radius along z direction. Default is 0
        verbose:    Verbose of message display. Default is False

    Return:
        Retrieved traces as a 2D array, with each row representing a trace
        Length = z_sample * (2*wdinl+1) * (2*wdz+1)
        Trace location is at column 1 (inline) and 2 (z)
    """
    if seisinfo is None or checkSeisInfo(seisinfo) is False:
        vis_msg.print('Warning in retrieveSeisXLTraceFrom3DMat: SeisInfo automatically generated', type='warning')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)
    ntrace = np.shape(trctrs)[0]
    znum, xlnum, inlnum = np.shape(seis3dmat)
    rst = np.zeros([ntrace, 2 + xlnum * (2 * wdinl + 1) * (2 * wdz + 1)])
    rst[:, 0:2] = trctrs
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    for i in range(ntrace):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        inl = trctrs[(i, 0)]
        z = trctrs[(i, 1)]
        inl = (inl - seisinfo['ILStart']) / seisinfo['ILStep']
        inl = int(inl)
        z = (z - seisinfo['ZStart']) / seisinfo['ZStep']
        z = int(z)
        if inl - wdinl >= 0 and inl + wdinl < seisinfo['ILNum'] and z - wdz >= 0 and z + wdz < seisinfo['ZNum']:
            dat = seis3dmat[z - wdz:z + wdz + 1, :, inl - wdinl:inl + wdinl + 1]
            rst[i, 2:] = np.reshape(dat, [1, -1])

    if verbose:
        sys.stdout.write(' Done\n')
    return rst


def retrieveSeisZTraceFrom2DMat(seis2dmat, trctrs, wdinl=0, wdxl=0, verbose=False):
    """
    Retrieve z traces from 2D matrix (Seis2DMat)

    Args:
        seis2dmat:  Seismic data in 2D matrix
        trctrs:     List of trace locations in a 2D array, [inline, crossline]
        wdinl:      Retrieval radius along inline direction. Default is 0
        wdxl:       Retrieval radius along crossline direction. Default is 0
        verbose:    Verbose of message display. Default is False

    Return:
        Retrieved traces as a 2D array, with each row representing a trace
        Length = z_sample * (2*wdinl+1) * (2*wdxl+1)
        Trace location is at column 1 (inline) and 2 (crossline)
    """
    ntrace = np.shape(trctrs)[0]
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat)
    seisinfo = getSeisInfoFrom2DMat(seis2dmat)
    znum, xlnum, inlnum = np.shape(seis3dmat)
    rst = np.zeros([ntrace, 2 + znum * (2 * wdinl + 1) * (2 * wdxl + 1)])
    rst[:, 0:2] = trctrs
    if verbose:
        print('Retrieve ' + str(trctrs) + ' z traces')
    for i in range(ntrace):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        inl = trctrs[(i, 0)]
        xl = trctrs[(i, 1)]
        inl = (inl - seisinfo['ILStart']) / seisinfo['ILStep']
        inl = int(inl)
        xl = (xl - seisinfo['XLStart']) / seisinfo['XLStep']
        xl = int(xl)
        if inl - wdinl >= 0 and inl + wdinl < seisinfo['ILNum'] and xl - wdxl >= 0 and xl + wdxl < seisinfo['XLNum']:
            dat = seis3dmat[:, xl - wdxl:xl + wdxl + 1, inl - wdinl:inl + wdinl + 1]
            rst[i, 2:] = np.reshape(dat, [1, -1])

    if verbose:
        sys.stdout.write(' Done\n')
    return rst


def retrieveSeisZTraceFrom3DMat(seis3dmat, trctrs, seisinfo=None, wdinl=0, wdxl=0, verbose=False):
    """
    Retrieve z traces from 3D matrix (Seis3DMat)

    Args:
        seis3dmat:  Seismic data in 3D matrix
        trctrs:     List of trace locations in a 2D array, [inline, crossline]
        seisinfo:   Seismic information dictionary as defined above
        wdinl:      Retrieval radius along inline direction. Default is 0
        wdxl:       Retrieval radius along crossline direction. Default is 0
        verbose:    Verbose of message display. Default is False

    Return:
        Retrieved traces as a 2D array, with each row representing a trace
        Length = z_sample * (2*wdinl+1) * (2*wdxl+1)
        Trace location is at column 1 (inline) and 2 (crossline)
    """
    if seisinfo is None or checkSeisInfo(seisinfo) is False:
        vis_msg.print('Warning in retrieveSeisZTraceFrom3DMat: SeisInfo automatically generated', type='warning')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)
    ntrace = np.shape(trctrs)[0]
    znum, xlnum, inlnum = np.shape(seis3dmat)
    rst = np.zeros([ntrace, 2 + znum * (2 * wdinl + 1) * (2 * wdxl + 1)])
    rst[:, 0:2] = trctrs
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    for i in range(ntrace):
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        inl = trctrs[(i, 0)]
        xl = trctrs[(i, 1)]
        inl = (inl - seisinfo['ILStart']) / seisinfo['ILStep']
        inl = int(inl)
        xl = (xl - seisinfo['XLStart']) / seisinfo['XLStep']
        xl = int(xl)
        if inl - wdinl >= 0 and inl + wdinl < seisinfo['ILNum'] and xl - wdxl >= 0 and xl + wdxl < seisinfo['XLNum']:
            dat = seis3dmat[:, xl - wdxl:xl + wdxl + 1, inl - wdinl:inl + wdinl + 1]
            rst[i, 2:] = np.reshape(dat, [1, -1])

    if verbose:
        sys.stdout.write(' Done\n')
    return rst


def removeOutofSurveySample(pts, inlstart=0, inlend=100, xlstart=0, xlend=100, zstart=0, zend=-1000):
    """
    Remove samples out of a given survey

    Args:
        pts:        Seismic points as 2D array, with each row representing a point.
                    Trace location is represented as inline (column 1), crossline (column 2), and z (column 3)
        inlstart:   First inline No. of the survey
        inlend:     Last inline No. of the survey
        xlstart:    First crossline No. of the survey
        xlend:      Last crossline No. of the survey
        zstart:     First z No. of the survey
        zend:       Last z No. of the survey

    Return:
        samples after removal.
    """
    pts_in = []
    npts = np.shape(pts)[0]
    for i in range(npts):
        if pts[(i, 0)] >= inlstart and pts[(i, 0)] <= inlend and pts[(i, 1)] >= xlstart and pts[(i, 1)] <= xlend and pts[(i, 2)] <= zstart and pts[(i, 2)] >= zend:
            pts_in.append(pts[i, :])

    return np.array(pts_in)


def removeOutofSurveyXLTrace(tcs, inlstart=0, inlend=100, zstart=0, zend=-1000):
    """
    Remove crossline traces out of a given survey

    Args:
        tcs:        Seismic traces as 2D array, with each row representing a trace.
                    Trace location is represented as inline (column 1) and crossline (column 2)
        inlstart:   First inline No. of the survey
        inlend:     Last inline No. of the survey
        zstart:    First z No. of the survey
        zend:      Last z No. of the survey

    Return:
        traces after removal.
    """
    tcs_in = []
    ntc = np.shape(tcs)[0]
    for i in range(ntc):
        if tcs[(i, 0)] >= inlstart and tcs[(i, 0)] <= inlend and tcs[(i, 1)] <= zstart and tcs[(i, 1)] >= zend:
            tcs_in.append(tcs[i, :])

    return np.array(tcs_in)


def removeOutofSurveyZTrace(tcs, inlstart=0, inlend=100, xlstart=0, xlend=100):
    """
    Remove z traces out of a given survey

    Args:
        tcs:        Seismic traces as 2D array, with each row representing a trace.
                    Trace location is represented as inline (column 1) and crossline (column 2)
        inlstart:   First inline No. of the survey
        inlend:     Last inline No. of the survey
        xlstart:    First crossline No. of the survey
        xlend:      Last crossline No. of the survey

    Return:
        z traces after removal.
    """
    tcs_in = []
    ntc = np.shape(tcs)[0]
    for i in range(ntc):
        if tcs[(i, 0)] >= inlstart and tcs[(i, 0)] <= inlend and tcs[(i, 1)] >= xlstart and tcs[(i, 1)] <= xlend:
            tcs_in.append(tcs[i, :])

    return np.array(tcs_in)


def isOutOfSurvey--- This code section failed: ---

 L.2283         0  LOAD_GLOBAL              np
                2  LOAD_METHOD              ndim
                4  LOAD_FAST                'ixzlist'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  LOAD_CONST               2
               10  COMPARE_OP               <
               12  POP_JUMP_IF_TRUE     32  'to 32'
               14  LOAD_GLOBAL              np
               16  LOAD_METHOD              shape
               18  LOAD_FAST                'ixzlist'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  LOAD_CONST               1
               24  BINARY_SUBSCR    
               26  LOAD_CONST               3
               28  COMPARE_OP               <
               30  POP_JUMP_IF_FALSE    54  'to 54'
             32_0  COME_FROM            12  '12'

 L.2284        32  LOAD_GLOBAL              vis_msg
               34  LOAD_ATTR                print
               36  LOAD_STR                 'ERROR in isOutOfSurvey: 2-D matrix of at least 3 columns expected'
               38  LOAD_STR                 'error'
               40  LOAD_CONST               ('type',)
               42  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               44  POP_TOP          

 L.2285        46  LOAD_GLOBAL              sys
               48  LOAD_METHOD              exit
               50  CALL_METHOD_0         0  '0 positional arguments'
               52  POP_TOP          
             54_0  COME_FROM            30  '30'

 L.2287        54  LOAD_GLOBAL              np
               56  LOAD_METHOD              shape
               58  LOAD_FAST                'ixzlist'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  STORE_FAST               'nsample'

 L.2288        68  LOAD_GLOBAL              np
               70  LOAD_METHOD              zeros
               72  LOAD_FAST                'nsample'
               74  LOAD_CONST               1
               76  BUILD_LIST_2          2 
               78  CALL_METHOD_1         1  '1 positional argument'
               80  STORE_FAST               'flags'

 L.2289        82  SETUP_LOOP          248  'to 248'
               84  LOAD_GLOBAL              range
               86  LOAD_FAST                'nsample'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  GET_ITER         
             92_0  COME_FROM           234  '234'
             92_1  COME_FROM           226  '226'
             92_2  COME_FROM           218  '218'
             92_3  COME_FROM           210  '210'
             92_4  COME_FROM           202  '202'
             92_5  COME_FROM           194  '194'
               92  FOR_ITER            246  'to 246'
               94  STORE_FAST               'i'

 L.2290        96  LOAD_FAST                'ixzlist'
               98  LOAD_FAST                'i'
              100  LOAD_CONST               0
              102  BUILD_TUPLE_2         2 
              104  BINARY_SUBSCR    
              106  STORE_FAST               'il'

 L.2291       108  LOAD_FAST                'ixzlist'
              110  LOAD_FAST                'i'
              112  LOAD_CONST               1
              114  BUILD_TUPLE_2         2 
              116  BINARY_SUBSCR    
              118  STORE_FAST               'xl'

 L.2292       120  LOAD_FAST                'ixzlist'
              122  LOAD_FAST                'i'
              124  LOAD_CONST               2
              126  BUILD_TUPLE_2         2 
              128  BINARY_SUBSCR    
              130  STORE_FAST               'z'

 L.2294       132  LOAD_FAST                'il'
              134  LOAD_FAST                'inlstart'
              136  COMPARE_OP               <
              138  POP_JUMP_IF_TRUE    180  'to 180'
              140  LOAD_FAST                'il'
              142  LOAD_FAST                'inlend'
              144  COMPARE_OP               >
              146  POP_JUMP_IF_TRUE    180  'to 180'

 L.2295       148  LOAD_FAST                'xl'
              150  LOAD_FAST                'xlstart'
              152  COMPARE_OP               <
              154  POP_JUMP_IF_TRUE    180  'to 180'
              156  LOAD_FAST                'xl'
              158  LOAD_FAST                'xlend'
              160  COMPARE_OP               >
              162  POP_JUMP_IF_TRUE    180  'to 180'

 L.2296       164  LOAD_FAST                'z'
              166  LOAD_FAST                'zstart'
              168  COMPARE_OP               >
              170  POP_JUMP_IF_TRUE    180  'to 180'
              172  LOAD_FAST                'z'
              174  LOAD_FAST                'zend'
              176  COMPARE_OP               <
              178  POP_JUMP_IF_FALSE   188  'to 188'
            180_0  COME_FROM           170  '170'
            180_1  COME_FROM           162  '162'
            180_2  COME_FROM           154  '154'
            180_3  COME_FROM           146  '146'
            180_4  COME_FROM           138  '138'

 L.2297       180  LOAD_CONST               1
              182  LOAD_FAST                'flags'
              184  LOAD_FAST                'i'
              186  STORE_SUBSCR     
            188_0  COME_FROM           178  '178'

 L.2299       188  LOAD_FAST                'il'
              190  LOAD_FAST                'inlstart'
              192  COMPARE_OP               >
              194  POP_JUMP_IF_FALSE    92  'to 92'
              196  LOAD_FAST                'il'
              198  LOAD_FAST                'inlend'
              200  COMPARE_OP               <
              202  POP_JUMP_IF_FALSE    92  'to 92'

 L.2300       204  LOAD_FAST                'xl'
              206  LOAD_FAST                'xlstart'
              208  COMPARE_OP               >
              210  POP_JUMP_IF_FALSE    92  'to 92'
              212  LOAD_FAST                'xl'
              214  LOAD_FAST                'xlend'
              216  COMPARE_OP               <
              218  POP_JUMP_IF_FALSE    92  'to 92'

 L.2301       220  LOAD_FAST                'z'
              222  LOAD_FAST                'zstart'
              224  COMPARE_OP               <
              226  POP_JUMP_IF_FALSE    92  'to 92'
              228  LOAD_FAST                'z'
              230  LOAD_FAST                'zend'
              232  COMPARE_OP               >
              234  POP_JUMP_IF_FALSE    92  'to 92'

 L.2302       236  LOAD_CONST               -1
              238  LOAD_FAST                'flags'
              240  LOAD_FAST                'i'
              242  STORE_SUBSCR     
              244  JUMP_BACK            92  'to 92'
              246  POP_BLOCK        
            248_0  COME_FROM_LOOP       82  '82'

 L.2304       248  LOAD_FAST                'flags'
              250  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 188_0


def convertIXZToIJK(ixz, inlstart=0, inlstep=1, xlstart=0, xlstep=1, zstart=0, zstep=-1):
    """
    Convert inline/crossline/z [IL, XL, Z] to index [I, J, K]

    Args:
        ixz:        2D matrix of inline/crossline/z
        inlstart:   start inline
        inlstep:    inline step
        xlstart:    start crossline
        xlstep:     crossline step
        zstart:     start z in ms
        zstep:      z step in ms

    Return:
        2D array for index [I, J, K]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(ixz) < 2 or np.shape(ixz)[1] < 3:
        vis_msg.print('ERROR in convertIXZToIJK: 2-D matrix of at least 3 columns expected', type='error')
        sys.exit()
    if inlstep <= 0 or xlstep <= 0 or zstep >= 0:
        vis_msg.print('ERROR in convertIXZToIJK: wrong inline/crossline/z step', type='error')
        sys.exit()
    ijk = ixz
    if np.shape(ijk)[0] > 0:
        ijk[:, 0] = (ixz[:, 0] - inlstart) / inlstep
        ijk[:, 1] = (ixz[:, 1] - xlstart) / xlstep
        ijk[:, 2] = (ixz[:, 2] - zstart) / zstep
    return ijk


def convertIJKToIXZ(ijk, inlstart=0, inlstep=1, xlstart=0, xlstep=1, zstart=0, zstep=-1):
    """
    Convert index [I, J, K] to inline/crossline/z [IL, XL, Z]

    Args:
        ijk:        2D matrix of [I, J, K]
        inlstart:   start inline
        inlstep:    inline step
        xlstart:    start crossline
        xlstep:     crossline step
        zstart:     start z in ms
        zstep:      z step in ms

    Return:
        2D array for [IL, XL, Z]

    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(ijk) < 2 or np.shape(ijk)[1] < 3:
        vis_msg.print('ERROR in convertIJKToIXZ: 2-D matrix of at least 3 columns expected', type='error')
        sys.exit()
    ixz = ijk
    if np.shape(ijk)[0] > 0:
        ixz[:, 0] = ijk[:, 0] * inlstep + inlstart
        ixz[:, 1] = ijk[:, 1] * xlstep + xlstart
        ixz[:, 2] = ijk[:, 2] * zstep + zstart
    return ixz


def getRandomSample(inl, xl, z, nsample=1000, unique=False):
    """
    Get samples randomly from the given inlines, xlines, and zs

    Args:
        inl:        a list of inline sections
        xl:         a list of crossline section
        z:          a list of z sections
        nsample:    number of samples expected
        unique:     Unique samples or not. If so, No. of returned samples may be shorter than nsample

    Return:
         2D matrix with each row representing a sample
    """
    inlnum = len(inl)
    xlnum = len(xl)
    znum = len(z)
    seeds = np.zeros([nsample, 3])
    seed_idx = np.random.randint((znum * xlnum * inlnum), size=nsample)
    if unique is True:
        seed_idx = np.unique(seed_idx)
    seeds[:, 0] = inl[(seed_idx / xlnum / znum).astype(int)]
    seeds[:, 1] = xl[(seed_idx / znum % xlnum).astype(int)]
    seeds[:, 2] = z[(seed_idx % znum).astype(int)]
    return seeds


class analysis:
    getSeisInfoFrom2DMat = getSeisInfoFrom2DMat
    checkSeisInfo = checkSeisInfo
    makeSeisInfo = makeSeisInfo
    isSeis2DMatConsistentWithSeisInfo = isSeis2DMatConsistentWithSeisInfo
    isSeis3DMatConsistentWithSeisInfo = isSeis3DMatConsistentWithSeisInfo
    createSeisInfoFrom3DMat = createSeisInfoFrom3DMat
    convertSeis2DMatTo3DMat = convertSeis2DMatTo3DMat
    convertSeis3DMatTo2DMat = convertSeis3DMatTo2DMat
    convertSeisInfoTo2DMat = convertSeisInfoTo2DMat
    retrieveSeisSampleFrom2DMat = retrieveSeisSampleFrom2DMat
    retrieveSeisSampleFrom3DMat = retrieveSeisSampleFrom3DMat
    retrieveSeisILSliceFrom2DMat = retrieveSeisILSliceFrom2DMat
    retrieveSeisILSliceFrom3DMat = retrieveSeisILSliceFrom3DMat
    retrieveSeisXLSliceFrom2DMat = retrieveSeisXLSliceFrom2DMat
    retrieveSeisXLSliceFrom3DMat = retrieveSeisXLSliceFrom3DMat
    retrieveSeisZSliceFrom2DMat = retrieveSeisZSliceFrom2DMat
    retrieveSeisZSliceFrom3DMat = retrieveSeisZSliceFrom3DMat
    retrieveSeisWindowFrom2DMat = retrieveSeisWindowFrom2DMat
    retrieveSeisWindowFrom3DMat = retrieveSeisWindowFrom3DMat
    retrieveSeisILTraceFrom2DMat = retrieveSeisILTraceFrom2DMat
    retrieveSeisILTraceFrom3DMat = retrieveSeisILTraceFrom3DMat
    retrieveSeisXLTraceFrom2DMat = retrieveSeisXLTraceFrom2DMat
    retrieveSeisXLTraceFrom3DMat = retrieveSeisXLTraceFrom3DMat
    retrieveSeisZTraceFrom2DMat = retrieveSeisZTraceFrom2DMat
    retrieveSeisZTraceFrom3DMat = retrieveSeisZTraceFrom3DMat
    cutSeisILSliceFrom2DMat = cutSeisILSliceFrom2DMat
    cutSeisXLSliceFrom2DMat = cutSeisXLSliceFrom2DMat
    assignSeisWindowTo2DMat = assignSeisWindowTo2DMat
    removeOutofSurveySample = removeOutofSurveySample
    removeOutofSurveyXLTrace = removeOutofSurveyXLTrace
    removeOutofSurveyZTrace = removeOutofSurveyZTrace
    isOutOfSurvey = isOutOfSurvey
    convertIXZToIJK = convertIXZToIJK
    convertIJKToIXZ = convertIJKToIXZ
    getRandomSample = getRandomSample