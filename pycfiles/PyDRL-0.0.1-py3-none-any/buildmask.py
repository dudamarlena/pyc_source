# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\buildmask.py
# Compiled at: 2014-04-16 13:17:36
__doc__ = "\nFunctions to build mask files for PyDrizzle.\n    - buildMaskImage(rootname,bitvalue,extname='DQ',extver=None):\n        This function takes the DQ array(or array from extension given)\n        and builds a bit mask as an input weighting mask for 'drizzle'.\n\n    - buildShadowMaskImage(rootname,detnum,replace=no):\n        This function builds a weighting image for use with drizzle from\n        the WFPC2 shadow mask functions derived from 'wmosaic'.\n"
from __future__ import division
import string, os, types
from stsci.tools import fileutil, readgeis
import pyfits, numpy as np
yes = True
no = False

def buildMask(dqarr, bitvalue):
    """ Builds a bit-mask from an input DQ array and a bitvalue flag"""
    _maskarr = np.bitwise_or(dqarr, np.array([bitvalue]))
    return np.choose(np.greater(_maskarr, bitvalue), (1, 0)).astype(np.uint8)


def buildMaskName(rootname, extver):
    """ Builds name for mask file based on rootname and extver. """
    _indx = rootname.rfind('.')
    if _indx > 0:
        _maskname = rootname[:_indx] + '_final_mask' + repr(extver) + '.fits'
    else:
        _maskname = rootname + '_final_mask' + repr(extver) + '.fits'
    return _maskname


def buildMaskImage(rootname, bitvalue, output, extname='DQ', extver=1):
    """ Builds mask image from rootname's DQ array
        If there is no valid 'DQ' array in image, then return
        an empty string.
    """
    if bitvalue == None or rootname == None:
        return
    maskname = output
    if fileutil.findFile(maskname):
        fileutil.removeFile(maskname)
    fdq = fileutil.openImage(rootname, memmap=0, mode='readonly')
    try:
        _extn = fileutil.findExtname(fdq, extname, extver=extver)
        if _extn != None:
            dqarr = fdq[_extn].data
        else:
            dqarr = None
        if dqarr == None:
            _sci_extn = fileutil.findExtname(fdq, 'SCI', extver=extver)
            if _sci_extn != None:
                _shape = fdq[_sci_extn].data.shape
                dqarr = np.zeros(_shape, dtype=np.uint16)
            else:
                raise Exception
        maskarr = buildMask(dqarr, bitvalue)
        fmask = pyfits.open(maskname, 'append')
        maskhdu = pyfits.PrimaryHDU(data=maskarr)
        fmask.append(maskhdu)
        fmask.close()
        del fmask
        fdq.close()
        del fdq
    except:
        fdq.close()
        del fdq
        if fileutil.findFile(maskname):
            os.remove(maskname)
        _errstr = '\nWarning: Problem creating MASK file for ' + rootname + '.\n'
        print _errstr
        return

    return maskname


def _func_Shadow_WF1y(x, y):
    return y + 0.5 - (42.62779 + 0.009122855 * y - 1.106709e-05 * y ** 2)


def _func_Shadow_WF1x(x, y):
    return x + 0.5 - (52.20921 + 0.009072887 * x - 9.941337e-06 * x ** 2)


def _func_Shadow_WF2y(x, y):
    return y + 0.5 - (47.68184 + 0.00265608 * y - 1.468158e-05 * y ** 2)


def _func_Shadow_WF2x(x, y):
    return x + 0.5 - (21.77283 + 0.01842164 * x - 1.3983e-05 * x ** 2)


def _func_Shadow_WF3y(x, y):
    return y + 0.5 - (30.23626 + 0.008156041 * y - 1.491324e-05 * y ** 2)


def _func_Shadow_WF3x(x, y):
    return x + 0.5 - (44.18944 + 0.0138938 * x - 1.412296e-05 * x ** 2)


def _func_Shadow_WF4y(x, y):
    return y + 0.5 - (40.91462 + 0.01273679 * y - 1.063462e-05 * y ** 2)


def _func_Shadow_WF4x(x, y):
    return x + 0.5 - (44.56632 + 0.003509023 * x - 1.278723e-05 * x ** 2)


def buildShadowMaskImage(rootname, detnum, extnum, maskname, replace=yes, bitvalue=None, binned=1):
    """ Builds mask image from WFPC2 shadow calibrations.
      detnum - string value for 'DETECTOR' detector
    """
    if not isinstance(detnum, types.StringType):
        detnum = repr(detnum)
    _funcroot = '_func_Shadow_WF'
    _mask = 'wfpc2_inmask' + detnum + '.fits'
    if fileutil.findFile(maskname) and replace:
        fileutil.removeFile(maskname)
    _indx = rootname.find('.c1h')
    if _indx < 0:
        _indx = len(rootname)
    if rootname.find('.fits') < 0:
        _dqname = rootname[:_indx] + '.c1h'
    else:
        _dqname = rootname
    _use_inmask = False
    if fileutil.findFile(_dqname) != yes or bitvalue == None:
        _use_inmask = True
    if _use_inmask and not fileutil.findFile(_mask):
        try:
            _funcx = _funcroot + detnum + 'x'
            _funcy = _funcroot + detnum + 'y'
            _xarr = np.clip(np.fromfunction(eval(_funcx), (800, 800)), 0.0, 1.0).astype(np.uint8)
            _yarr = np.clip(np.fromfunction(eval(_funcy), (800, 800)), 0.0, 1.0).astype(np.uint8)
            maskarr = _xarr * _yarr
            if binned != 1:
                print 'in buildmask', binned
                bmaskarr = maskarr[::2, ::2]
                bmaskarr *= maskarr[1::2, ::2]
                bmaskarr *= maskarr[::2, 1::2]
                bmaskarr *= maskarr[1::2, 1::2]
                maskarr = bmaskarr.copy()
                del bmaskarr
            fmask = pyfits.open(_mask, 'append')
            maskhdu = pyfits.PrimaryHDU(data=maskarr)
            fmask.append(maskhdu)
            fmask.close()
            del fmask
        except:
            return

    if fileutil.findFile(_dqname) != yes:
        print 'DQ file ', _dqname, ' NOT found...'
        print 'Copying ', _mask, 'to ', maskname, ' as input mask file.'
        fileutil.copyFile(_mask, maskname, replace=yes)
    elif bitvalue == None:
        fileutil.copyFile(_mask, maskname, replace=yes)
    else:
        fdq = fileutil.openImage(_dqname)
        try:
            dqarr = fdq[int(extnum)].data
            dqmaskarr = buildMask(dqarr, bitvalue)
            fdqmask = pyfits.open(maskname, 'append')
            maskhdu = pyfits.PrimaryHDU(data=dqmaskarr)
            fdqmask.append(maskhdu)
            fdqmask.close()
            del fdqmask
            fdq.close()
            del fdq
        except:
            fdq.close()
            del fdq
            if fileutil.findFile(maskname):
                os.remove(maskname)
            _errstr = '\nWarning: Problem creating DQMASK file for ' + rootname + '.\n'
            print _errstr
            return

    return maskname