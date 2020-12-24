# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\makewcs.py
# Compiled at: 2014-04-16 13:17:36
__doc__ = "\nMAKEWCS.PY - Updated the WCS in an image header so that\n            it matches the geometric distortion defined in an IDC table\n            which is referenced in the image header.\n\nLicense: http://www.stsci.edu/resources/software_hardware/pyraf/LICENSE\n\nThis version tries to implement a full updating of the WCS based on\ninformation about the V2/V3 plane which is obtained from th IDCTAB and,\nin the case of WFPC2, the OFFTAB.\n\nThe only parameters from the original WCS which are retained are\nthe CRVALs of the reference chip.\n\nThe original WCS are first copied to MCD1_1 etc before being updated.\n\n:UPINCD History:\nFirst try, Richard Hook, ST-ECF/STScI, August 2002.\nVersion 0.0.1 (WJH) - Obtain IDCTAB using PyDrizzle function.\nVersion 0.1 (WJH) - Added support for processing image lists.\n                    Revised to base CD matrix on ORIENTAT, instead of PA_V3\n                    Supports subarrays by shifting coefficients as needed.\nVersion 0.2 (WJH) - Implemented orientation computation based on PA_V3 using\n                    Troll function from Colin to compute new ORIENTAT value.\nVersion 0.3 (WJH) - Supported filter dependent distortion models in IDCTAB\n                    fixed bugs in applying Troll function to WCS.\nVersion 0.4 (WJH) - Updated to support use of 'defaultModel' for generic\n                    cases: XREF/YREF defaults to image center and idctab\n                    name defaults to None.\nVersion 0.5 (WJH) - Added support for WFPC2 OFFTAB updates, which updates\n                    the CRVALs.  However, for WFPC2 data, the creation of\n                    the backup values does not currently work.\n:MAKEWCS History:\nMAKEWCS V0.0 (RNH) - Created new version to implement more complete\n                     WCS creation based on a reference tangent plane.\n\n        V0.1 (RNH) - First working version for tests. May 20th 2004.\n        V0.11 (RNH) - changed reference chip for ACS/WFC. May 26th 2004.\n        V0.2 (WJH) - Removed all dependencies from IRAF and use new WCSObject\n                    class for all WCS operations.\n        V0.4 (WJH/CJH) - Corrected logic for looping of extension in FITS image.\n        V0.5 (RNH) - Chip to chip CRVAL shifting logic change.\n        V0.6 (CJH/WJH) - Added support for non-associated STIS data.\n        V0.6.2 (WJH) - Added support for NICMOS data. This required\n                        new versions of wcsutil and fileutil in PyDrizzle.\n        V0.6.3 (WJH) - Modified to support new version of WCSUtil which correctly\n                        sets up and uses archived WCS keywords.\n        V0.7.0 (WJH) - Revised algorithm to work properly with subarray images.\n                        Also, simplified keyword access using PyFITS object.\n        V0.8.0 (CJH) - Modified to work with either numarray or numpy through\n                        the use of the numerix interface layer.\n\n"
from __future__ import division
from stsci.tools import numerixenv
numerixenv.check()
from math import *
import os.path, pyfits, drutil
from distortion import models, mutil
from stsci.tools import fileutil, wcsutil, parseinput
import numpy as N
yes = True
no = False
PARITY = {'WFC': [[1.0, 0.0], [0.0, -1.0]], 'HRC': [[-1.0, 0.0], [0.0, 1.0]], 'SBC': [
         [
          -1.0, 0.0], [0.0, 1.0]], 
   'default': [[1.0, 0.0], [0.0, 1.0]], 'WFPC2': [
           [
            -1.0, 0.0], [0.0, 1.0]], 
   'STIS': [[-1.0, 0.0], [0.0, 1.0]], 'NICMOS': [
            [
             -1.0, 0.0], [0.0, 1.0]], 
   'UVIS': [[-1.0, 0.0], [0.0, 1.0]], 'IR': [
        [
         -1.0, 0.0], [0.0, 1.0]]}
NUM_PER_EXTN = {'ACS': 3, 'WFPC2': 1, 'STIS': 3, 'NICMOS': 5, 'WFC3': 3}
__version__ = '1.1.7 (6 Jul 2010)'

def run(input, quiet=yes, restore=no, prepend='O', tddcorr=True):
    print '+ MAKEWCS Version %s' % __version__
    _prepend = prepend
    files = parseinput.parseinput(input)[0]
    newfiles = []
    if files == []:
        print 'No valid input files found.\n'
        raise IOError
    for image in files:
        imgfits, imgtype = fileutil.isFits(image)
        if imgfits and imgtype == 'waiver':
            newfilename = fileutil.buildNewRootname(image, extn='_c0h.fits')
            newimage = fileutil.openImage(image, writefits=True, fitsname=newfilename, clobber=True)
            del newimage
            image = newfilename
            newfiles.append(image)
        if not imgfits:
            newfilename = fileutil.buildFITSName(image)
            newimage = fileutil.openImage(image, writefits=True, fitsname=newfilename, clobber=True)
            del newimage
            image = newfilename
            newfiles.append(image)
        if not quiet:
            print 'Input files: ', files
        idctab = drutil.getIDCFile(image, keyword='idctab')[0]
        _found = fileutil.findFile(idctab)
        if idctab == None or idctab == '':
            print '#\n No IDCTAB specified.  No correction can be done for file %s.Quitting makewcs\n' % image
            continue
        else:
            if not _found:
                print '#\n IDCTAB: ', idctab, ' could not be found. \n'
                print 'WCS keywords for file %s will not be updated.\n' % image
                continue
            _phdu = image + '[0]'
            _instrument = fileutil.getKeyword(_phdu, keyword='INSTRUME')
            if _instrument == 'WFPC2':
                Nrefchip, Nrefext = getNrefchip(image)
            else:
                Nrefchip = None
                Nrefext = None
            if _instrument not in NUM_PER_EXTN:
                raise ValueError('Instrument %s not supported yet. Exiting...' % _instrument)
            _detector = fileutil.getKeyword(_phdu, keyword='DETECTOR')
            _nimsets = get_numsci(image)
            for i in xrange(_nimsets):
                if image.find('.fits') > 0:
                    _img = image + '[sci,' + repr(i + 1) + ']'
                else:
                    _img = image + '[' + repr(i + 1) + ']'
                if not restore:
                    if not quiet:
                        print 'Updating image: ', _img
                    _update(_img, idctab, _nimsets, apply_tdd=False, quiet=quiet, instrument=_instrument, prepend=_prepend, nrchip=Nrefchip, nrext=Nrefext)
                    if _instrument == 'ACS' and _detector == 'WFC':
                        tddswitch = fileutil.getKeyword(_phdu, keyword='TDDCORR')
                        if tddcorr and tddswitch != 'OMIT':
                            print 'Applying time-dependent distortion corrections...'
                            _update(_img, idctab, _nimsets, apply_tdd=True, quiet=quiet, instrument=_instrument, prepend=_prepend, nrchip=Nrefchip, nrext=Nrefext)
                else:
                    if not quiet:
                        print 'Restoring original WCS values for', _img
                    restoreCD(_img, _prepend)

    if newfiles == []:
        return files
    else:
        return newfiles
        return


def restoreCD(image, prepend):
    _prepend = prepend
    try:
        _wcs = wcsutil.WCSObject(image)
        _wcs.restoreWCS(prepend=_prepend)
        del _wcs
    except:
        print 'ERROR: Could not restore WCS keywords for %s.' % image


def _update(image, idctab, nimsets, apply_tdd=False, quiet=None, instrument=None, prepend=None, nrchip=None, nrext=None):
    tdd_xyref = {1: [2048, 3072], 2: [2048, 1024]}
    _prepend = prepend
    _dqname = None
    hdr = fileutil.getHeader(image)
    instrument = readKeyword(hdr, 'INSTRUME')
    binned = 1
    offtab = readKeyword(hdr, 'OFFTAB')
    dateobs = readKeyword(hdr, 'DATE-OBS')
    if not quiet:
        print 'OFFTAB, DATE-OBS: ', offtab, dateobs
    print '-Updating image ', image
    if not quiet:
        print '-Reading IDCTAB file ', idctab
    pvt = readKeyword(hdr, 'PA_V3')
    if pvt == None:
        sptfile = fileutil.buildNewRootname(image, extn='_spt.fits')
        if os.path.exists(sptfile):
            spthdr = fileutil.getHeader(sptfile)
            pvt = readKeyword(spthdr, 'PA_V3')
    if pvt != None:
        pvt = float(pvt)
    else:
        print 'PA_V3 keyword not found, WCS cannot be updated. Quitting ...'
        raise ValueError
    detector = readKeyword(hdr, 'DETECTOR')
    Nrefchip = 1
    if instrument == 'WFPC2':
        filter1 = readKeyword(hdr, 'FILTNAM1')
        filter2 = readKeyword(hdr, 'FILTNAM2')
        mode = readKeyword(hdr, 'MODE')
        if os.path.exists(fileutil.buildNewRootname(image, extn='_c1h.fits')):
            _dqname = fileutil.buildNewRootname(image, extn='_c1h.fits')
            dqhdr = pyfits.getheader(_dqname, 1)
            dqext = readKeyword(dqhdr, 'EXTNAME')
        if mode == 'AREA':
            binned = 2
        Nrefchip = nrchip
    else:
        if instrument == 'NICMOS':
            filter1 = readKeyword(hdr, 'FILTER')
            filter2 = None
        elif instrument == 'WFC3':
            filter1 = readKeyword(hdr, 'FILTER')
            filter2 = None
            binned = readKeyword(hdr, 'BINAXIS1')
        else:
            filter1 = readKeyword(hdr, 'FILTER1')
            filter2 = readKeyword(hdr, 'FILTER2')
        if filter1 == None or filter1.strip() == '':
            filter1 = 'CLEAR'
        else:
            filter1 = filter1.strip()
        if filter2 == None or filter2.strip() == '':
            filter2 = 'CLEAR'
        else:
            filter2 = filter2.strip()
        if filter1.find('CLEAR') == 0:
            filter1 = 'CLEAR'
        if filter2.find('CLEAR') == 0:
            filter2 = 'CLEAR'
        if instrument == 'WFPC2' or instrument == 'STIS' or instrument == 'NICMOS':
            parity = PARITY[instrument]
        elif detector in PARITY:
            parity = PARITY[detector]
        else:
            raise ValueError('Detector ', detector, ' Not supported at this time. Exiting...')
        _va_key = readKeyword(hdr, 'VAFACTOR')
        if _va_key != None:
            VA_fac = float(_va_key)
        else:
            VA_fac = 1.0
        if not quiet:
            print 'VA factor: ', VA_fac
        _c = readKeyword(hdr, 'CAMERA')
        _s = readKeyword(hdr, 'CCDCHIP')
        _d = readKeyword(hdr, 'DETECTOR')
        if _c != None and str(_c).isdigit():
            chip = int(_c)
        elif _s == None and _d == None:
            chip = 1
        elif _s:
            chip = int(_s)
        elif str(_d).isdigit():
            chip = int(_d)
        else:
            chip = 1
        nr = 1
        if instrument == 'ACS' and detector == 'WFC' or instrument == 'WFC3' and detector == 'UVIS':
            if nimsets > 1:
                Nrefchip = 2
            else:
                Nrefchip = chip
        elif instrument == 'NICMOS':
            Nrefchip = readKeyword(hdr, 'CAMERA')
        elif instrument == 'WFPC2':
            nr = nrext
        elif nimsets > 1:
            nr = Nrefchip
        if not quiet:
            print '-PA_V3 : ', pvt, ' CHIP #', chip
        idcmodel = models.IDCModel(idctab, chip=chip, direction='forward', date=dateobs, filter1=filter1, filter2=filter2, offtab=offtab, binned=binned, tddcorr=apply_tdd)
        fx = idcmodel.cx
        fy = idcmodel.cy
        refpix = idcmodel.refpix
        order = idcmodel.norder
        if apply_tdd:
            alpha = refpix['TDDALPHA']
            beta = refpix['TDDBETA']
            tdd = N.array([[beta, alpha], [alpha, -beta]])
            mrotp = fileutil.buildRotMatrix(2.234529) / 2048.0
        else:
            alpha = 0.0
            beta = 0.0
        Old = wcsutil.WCSObject(image, prefix=_prepend)
        Old.restore()
        ltv1, ltv2 = drutil.getLTVOffsets(image)
        offsetx = Old.crpix1 - ltv1 - refpix['XREF']
        offsety = Old.crpix2 - ltv2 - refpix['YREF']
        shiftx = refpix['XREF'] + ltv1
        shifty = refpix['YREF'] + ltv2
        if ltv1 != 0.0 or ltv2 != 0.0:
            ltvoffx = ltv1 + offsetx
            ltvoffy = ltv2 + offsety
            offshiftx = offsetx + shiftx
            offshifty = offsety + shifty
        else:
            ltvoffx = 0.0
            ltvoffy = 0.0
            offshiftx = 0.0
            offshifty = 0.0
        if ltv1 != 0.0 or ltv2 != 0.0:
            fx, fy = idcmodel.shift(idcmodel.cx, idcmodel.cy, offsetx, offsety)
        ridcmodel = models.IDCModel(idctab, chip=Nrefchip, direction='forward', date=dateobs, filter1=filter1, filter2=filter2, offtab=offtab, binned=binned, tddcorr=apply_tdd)
        rfx = ridcmodel.cx
        rfy = ridcmodel.cy
        rrefpix = ridcmodel.refpix
        rorder = ridcmodel.norder
        rimage = image.split('[')[0] + '[sci,%d]' % nr
        if not quiet:
            print 'Reference image: ', rimage
        R = wcsutil.WCSObject(rimage)
        R.write_archive(rimage)
        R.restore()
        dec = float(R.crval2)
        rref = (
         rrefpix['XREF'] + ltvoffx, rrefpix['YREF'] + ltvoffy)
        crval1, crval2 = R.xy2rd(rref)
        if apply_tdd:
            tddscale = R.pscale / fx[1][1]
            rxy0 = N.array([[tdd_xyref[Nrefchip][0] - 2048.0], [tdd_xyref[Nrefchip][1] - 2048.0]])
            xy0 = N.array([[tdd_xyref[chip][0] - 2048.0], [tdd_xyref[chip][1] - 2048.0]])
            rv23_corr = N.dot(mrotp, N.dot(tdd, rxy0)) * tddscale
            v23_corr = N.dot(mrotp, N.dot(tdd, xy0)) * tddscale
        else:
            rv23_corr = N.array([[0], [0]])
            v23_corr = N.array([[0], [0]])
        v2ref = rrefpix['V2REF'] + rv23_corr[0][0] * 0.05
        v3ref = rrefpix['V3REF'] - rv23_corr[1][0] * 0.05
        v2 = refpix['V2REF'] + v23_corr[0][0] * 0.05
        v3 = refpix['V3REF'] - v23_corr[1][0] * 0.05
        pv = wcsutil.troll(pvt, dec, v2ref, v3ref)
        if rrefpix['THETA']:
            pv += rrefpix['THETA']
        R.crval1 = crval1
        R.crval2 = crval2
        R.crpix1 = 0.0 + offshiftx
        R.crpix2 = 0.0 + offshifty
        R_scale = rrefpix['PSCALE'] / 3600.0
        R.cd11 = parity[0][0] * cos(pv * pi / 180.0) * R_scale
        R.cd12 = parity[0][0] * -sin(pv * pi / 180.0) * R_scale
        R.cd21 = parity[1][1] * sin(pv * pi / 180.0) * R_scale
        R.cd22 = parity[1][1] * cos(pv * pi / 180.0) * R_scale
        R_cdmat = N.array([[R.cd11, R.cd12], [R.cd21, R.cd22]])
        if not quiet:
            print '  Reference Chip Scale (arcsec/pix): ', rrefpix['PSCALE']
        off = sqrt((v2 - v2ref) ** 2 + (v3 - v3ref) ** 2) / (R_scale * 3600.0)
        if v3 == v3ref:
            theta = 0.0
        else:
            theta = atan2(parity[0][0] * (v2 - v2ref), parity[1][1] * (v3 - v3ref))
        if rrefpix['THETA']:
            theta += rrefpix['THETA'] * pi / 180.0
        dX = off * sin(theta) + offshiftx
        dY = off * cos(theta) + offshifty
        _fname, _iextn = fileutil.parseFilename(image)
        if _fname.find('.fits') < 0:
            _fitsname = fileutil.buildFITSName(_fname)
        else:
            _fitsname = None
        if _fitsname == None:
            _new_name = image
        else:
            _new_name = _fitsname + '[' + str(_iextn) + ']'
        New = Old.copy()
        New.crval1, New.crval2 = R.xy2rd((dX, dY))
        New.crpix1 = refpix['XREF'] + ltvoffx
        New.crpix2 = refpix['YREF'] + ltvoffy
        if refpix['THETA']:
            dtheta = refpix['THETA'] - rrefpix['THETA']
        else:
            dtheta = 0.0
        delXX = fx[(1, 1)] / R_scale / 3600.0
        delYX = fy[(1, 1)] / R_scale / 3600.0
        delXY = fx[(1, 0)] / R_scale / 3600.0
        delYY = fy[(1, 0)] / R_scale / 3600.0
        rr = dtheta * pi / 180.0
        dXX = cos(rr) * delXX - sin(rr) * delYX
        dYX = sin(rr) * delXX + cos(rr) * delYX
        dXY = cos(rr) * delXY - sin(rr) * delYY
        dYY = sin(rr) * delXY + cos(rr) * delYY
        a, b = R.xy2rd((dX + dXX, dY + dYX))
        c, d = R.xy2rd((dX + dXY, dY + dYY))
        New.cd11 = diff_angles(a, New.crval1) * cos(New.crval2 * pi / 180.0)
        New.cd12 = diff_angles(c, New.crval1) * cos(New.crval2 * pi / 180.0)
        New.cd21 = diff_angles(b, New.crval2)
        New.cd22 = diff_angles(d, New.crval2)
        if VA_fac != 1.0:
            New.crval1 = R.crval1 + VA_fac * diff_angles(New.crval1, R.crval1)
            New.crval2 = R.crval2 + VA_fac * diff_angles(New.crval2, R.crval2)
            New.cd11 = New.cd11 * VA_fac
            New.cd12 = New.cd12 * VA_fac
            New.cd21 = New.cd21 * VA_fac
            New.cd22 = New.cd22 * VA_fac
        New_cdmat = N.array([[New.cd11, New.cd12], [New.cd21, New.cd22]])
        New.write(fitsname=_new_name, overwrite=no, quiet=quiet, archive=yes)
        if _dqname:
            _dq_iextn = _iextn.replace('sci', dqext.lower())
            _new_dqname = _dqname + '[' + _dq_iextn + ']'
            dqwcs = wcsutil.WCSObject(_new_dqname)
            dqwcs.write(fitsname=_new_dqname, wcs=New, overwrite=no, quiet=quiet, archive=yes)
        f = refpix['PSCALE'] / 3600.0
        a = fx[(1, 1)] / 3600.0
        b = fx[(1, 0)] / 3600.0
        c = fy[(1, 1)] / 3600.0
        d = fy[(1, 0)] / 3600.0
        det = (a * d - b * c) * refpix['PSCALE']
        fimg = fileutil.openImage(_new_name, mode='update')
        _new_root, _nextn = fileutil.parseFilename(_new_name)
        _new_extn = fileutil.getExtn(fimg, _nextn)
        for n in range(order + 1):
            for m in range(order + 1):
                if n >= m and n >= 2:
                    Akey = 'A_%d_%d' % (m, n - m)
                    Bkey = 'B_%d_%d' % (m, n - m)
                    Aval = f * (d * fx[(n, m)] - b * fy[(n, m)]) / det
                    Bval = f * (a * fy[(n, m)] - c * fx[(n, m)]) / det
                    _new_extn.header.update(Akey, Aval)
                    _new_extn.header.update(Bkey, Bval)

    _new_extn.header.update('CTYPE1', 'RA---TAN-SIP')
    _new_extn.header.update('CTYPE2', 'DEC--TAN-SIP')
    _new_extn.header.update('A_ORDER', order)
    _new_extn.header.update('B_ORDER', order)
    _new_extn.header.update('IDCSCALE', refpix['PSCALE'])
    _new_extn.header.update('IDCV2REF', refpix['V2REF'])
    _new_extn.header.update('IDCV3REF', refpix['V3REF'])
    _new_extn.header.update('IDCTHETA', refpix['THETA'])
    _new_extn.header.update('OCX10', fx[1][0])
    _new_extn.header.update('OCX11', fx[1][1])
    _new_extn.header.update('OCY10', fy[1][0])
    _new_extn.header.update('OCY11', fy[1][1])
    if instrument == 'ACS' and detector == 'WFC':
        _new_extn.header.update('TDDALPHA', alpha)
        _new_extn.header.update('TDDBETA', beta)
    fimg.close()
    del fimg
    return


def diff_angles(a, b):
    """ Perform angle subtraction a-b taking into account
        small-angle differences across 360degree line. """
    diff = a - b
    if diff > 180.0:
        diff -= 360.0
    if diff < -180.0:
        diff += 360.0
    return diff


def readKeyword(hdr, keyword):
    try:
        value = hdr[keyword]
    except KeyError:
        value = None

    if isinstance(value, basestring):
        if value[-1:] == '/':
            value = value[:-1]
    return value


def get_numsci(image):
    """ Find the number of SCI extensions in the image.
        Input:
            image - name of single input image
    """
    handle = fileutil.openImage(image)
    num_sci = 0
    for extn in handle:
        if 'extname' in extn.header:
            if extn.header['extname'].lower() == 'sci':
                num_sci += 1

    handle.close()
    return num_sci


def shift_coeffs(cx, cy, xs, ys, norder):
    """
    Shift reference position of coefficients to new center
    where (xs,ys) = old-reference-position - subarray/image center.
    This will support creating coeffs files for drizzle which will
    be applied relative to the center of the image, rather than relative
    to the reference position of the chip.

    Derived directly from PyDrizzle V3.3d.
    """
    _cxs = N.zeros(shape=cx.shape, dtype=cx.dtype.name)
    _cys = N.zeros(shape=cy.shape, dtype=cy.dtype.name)
    _k = norder + 1
    for m in xrange(_k):
        for n in xrange(_k):
            if m >= n:
                _ilist = N.array(range(_k - m)) + m
                for i in _ilist:
                    _jlist = N.array(range(i - (m - n) - n + 1)) + n
                    for j in _jlist:
                        _cxs[(m, n)] = _cxs[(m, n)] + cx[(i, j)] * pydrizzle._combin(j, n) * pydrizzle._combin(i - j, m - n) * pow(xs, j - n) * pow(ys, i - j - (m - n))
                        _cys[(m, n)] = _cys[(m, n)] + cy[(i, j)] * pydrizzle._combin(j, n) * pydrizzle._combin(i - j, m - n) * pow(xs, j - n) * pow(ys, i - j - (m - n))

    _cxs[(0, 0)] = _cxs[(0, 0)] - xs
    _cys[(0, 0)] = _cys[(0, 0)] - ys
    return (
     _cxs, _cys)


def getNrefchip(image, instrument='WFPC2'):
    """
    This handles the fact that WFPC2 subarray observations
    may not include chip 3 which is the default reference chip for
    full observations. Also for subarrays chip 3  may not be the third
    extension in a MEF file. It is a kludge but this whole module is
    one big kludge. ND
    """
    hdu = fileutil.openImage(image)
    if instrument == 'WFPC2':
        detectors = [ img.header['DETECTOR'] for img in hdu[1:] ]
    if 3 not in detectors:
        Nrefchip = detectors[0]
        Nrefext = 1
    else:
        Nrefchip = 3
        Nrefext = detectors.index(3) + 1
    hdu.close()
    return (
     Nrefchip, Nrefext)


_help_str = " makewcs - a task for updating an image header WCS to make\n      it consistent with the distortion model and velocity aberration.\n\nThis task will read in a distortion model from the IDCTAB and generate\na new WCS matrix based on the value of ORIENTAT.  It will support subarrays\nby shifting the distortion coefficients to image reference position before\napplying them to create the new WCS, including velocity aberration.\nOriginal WCS values will be moved to an O* keywords (OCD1_1,...).\nCurrently, this task will only support ACS and WFPC2 observations.\n\nParameters\n----------\ninput: str\n    The filename(s) of image(s) to be updated given either as:\n      * a single image with extension specified,\n      * a substring common to all desired image names,\n      * a wildcarded filename\n      * '@file' where file is a file containing a list of images\n\nquiet: bool\n    turns off ALL reporting messages: 'yes' or 'no'(default)\n\nprepend: char\n    This parameter specifies what prefix letter should be used to\n    create a new set of WCS keywords for recording the original values\n    [Default: 'O']\n\nrestore: bool\n    restore WCS for all input images to defaults if possible:\n    'yes' or 'no'(default)\n\ntddcorr: bool\n    applies the time-dependent skew terms to the SIP coefficients\n    written out to the header: 'yes' or True or, 'no' or False (default).\n\nNotes\n-----\nThis function can be run using the syntax:\n    makewcs.run(image,quiet=no,prepend='O',restore=no,tddcorr=True)\nAn example of how this can be used is given as::\n\n    >>> import makewcs\n    >>> makewcs.run('raw') # This will update all _raw files in directory\n    >>> makewcs.run('j8gl03igq_raw.fits[sci,1]')\n"

def help():
    print _help_str


run.__doc__ = _help_str