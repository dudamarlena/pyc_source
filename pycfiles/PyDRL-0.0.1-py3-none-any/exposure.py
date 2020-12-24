# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\exposure.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
import os, buildmask, drutil, arrdriz
from obsgeometry import ObsGeometry
from stsci.tools import fileutil, wcsutil
from math import ceil, floor
import numpy as np
yes = True
no = False
__version__ = '0.1.4'

class Exposure:
    """
    This class will provide the basic functionality for keeping
    track of an exposure's parameters, including distortion model,
    WCS information, and metachip shape.
    """

    def __init__(self, expname, handle=None, dqname=None, idckey=None, new=no, wcs=None, mask=None, pa_key=None, parity=None, idcdir=None, rot=None, extver=1, exptime=None, ref_pscale=1.0, binned=1, mt_wcs=None, group_indx=None):
        self.name = fileutil.osfn(expname)
        _path, _name = os.path.split(self.name)
        if _path == os.getcwd():
            self.name = _name
        _fname, _extn = fileutil.parseFilename(expname)
        _open = False
        if not handle and not new:
            handle = fileutil.openImage(expname)
            _open = True
        if handle and _extn == None:
            if handle[0].data == None:
                if len(handle) > 1 and handle[1].data != None:
                    _extn = 1
                    expname += '[1]'
                else:
                    raise IOError, 'No valid image data in %s.\n' % expname
            else:
                _extn = 0
        self.dgeoname = None
        self.xgeoim = ''
        self.ygeoim = ''
        self.exptime = exptime
        self.group_indx = group_indx
        if not new:
            _header = fileutil.getHeader(expname, handle=handle)
            _chip = drutil.getChipId(_header)
            self.chip = str(_chip)
            self.dgeoname = fileutil.getKeyword(expname, 'DGEOFILE', handle=handle)
            self.xgeoim, self.ygeoim = self.getDGEOExtn()
            if self.exptime == None:
                self.exptime = float(_header['EXPTIME'])
                if self.exptime == 0.0:
                    self.exptime = 1.0
            self.plam = float(fileutil.getKeyword(expname, 'PHOTPLAM', handle=handle)) / 10.0
            if self.plam == None:
                self.plam = 555.0
            self.photzpt = float(fileutil.getKeyword(expname, 'PHOTZPT', handle=handle))
            if self.photzpt == None:
                self.photzpt = 0.0
            self.photflam = float(fileutil.getKeyword(expname, 'PHOTFLAM', handle=handle))
            if self.photflam == None:
                self.photflam = 1.0
            if _header:
                if 'date-obs' in _header:
                    self.dateobs = _header['date-obs']
                elif 'date_obs' in _header:
                    self.dateobs = _header['date_obs']
                else:
                    self.dateobs = None
            else:
                self.dateobs = None
            if 'BUNIT' in _header and _header['BUNIT'].find('ergs') < 0:
                self.bunit = _header['BUNIT']
            else:
                self.bunit = 'ELECTRONS'
        else:
            _chip = 1
            _header = None
            self.chip = str(_chip)
            self.plam = 555.0
            self.photzpt = 0.0
            self.photflam = 1.0
            self.dateobs = None
            if self.exptime == None:
                self.exptime = 1.0
        self.parity = parity
        self.header = _header
        self.extver = extver
        self.maskname = None
        self.singlemaskname = None
        self.masklist = None
        if mask != None:
            self.maskname = mask[0]
            self.singlemaskname = mask[1]
            self.masklist = mask[2]
        self.dqname = dqname
        self.coeffs = self.buildCoeffsName()
        if idckey != None and idckey.lower() != 'wcs':
            _indx = expname.find('[')
            if _indx > -1:
                _idc_fname = expname[:_indx] + '[0]'
            else:
                _idc_fname = expname + '[0]'
            idcfile, idctype = drutil.getIDCFile(self.header, keyword=idckey, directory=idcdir)
        else:
            idcfile = None
            idctype = None
        if idckey != None and idckey.lower() == 'header':
            idckey = idctype
        self.geometry = ObsGeometry(expname, idcfile, idckey=idckey, chip=_chip, new=new, header=self.header, pa_key=pa_key, rot=rot, date=self.dateobs, ref_pscale=ref_pscale, binned=binned, mt_wcs=mt_wcs)
        self.idcfile = idcfile
        self.idctype = idctype
        self.filters = self.geometry.filter1 + ',' + self.geometry.filter2
        if wcs != None:
            self.geometry.wcs = wcs
            self.geometry.model.pscale = wcs.pscale
            if expname != None:
                self.geometry.wcs.rootname = expname
        self.naxis1 = self.geometry.wcs.naxis1
        self.naxis2 = self.geometry.wcs.naxis2
        self.pscale = self.geometry.wcs.pscale
        self.shape = (self.naxis1, self.naxis2, self.pscale)
        self.corners = {'raw': np.zeros((4, 2), dtype=np.float64), 'corrected': np.zeros((4, 2), dtype=np.float64)}
        self.setCorners()
        _blot_extn = '_sci' + repr(extver) + '_blt.fits'
        self.outblot = fileutil.buildNewRootname(self.name, extn=_blot_extn)
        self.product_wcs = self.geometry.wcslin
        self.xzero = 0.0
        self.yzero = 0.0
        self.chip_shape = (0.0, 0.0)
        self.xsh2 = 0.0
        self.ysh2 = 0.0
        if _open:
            handle.close()
            del handle
        return

    def set_bunit(self, value=None):
        """Sets the value of bunit to user specified value, if one is provided.
        """
        if value is not None and self.bunit is not None:
            self.bunit = value
        return

    def setCorners(self):
        """ Initializes corners for the raw image. """
        self.corners['raw'] = np.array([(1.0, 1.0), (1.0, self.naxis2), (self.naxis1, 1.0), (self.naxis1, self.naxis2)], dtype=np.float64)

    def setSingleOffsets(self):
        """ Computes the zero-point offset and shape of undistorted single chip relative
            to the full final output product metachip.
        """
        _wcs = self.geometry.wcs
        _corners = np.array([(1.0, 1.0), (1.0, _wcs.naxis2), (_wcs.naxis1, 1.0), (_wcs.naxis1, _wcs.naxis2)], dtype=np.int64)
        _wc = self.geometry.wtraxy(_corners, self.product_wcs)
        _xrange = (
         _wc[:, 0].min(), _wc[:, 0].max())
        _yrange = (_wc[:, 1].min(), _wc[:, 1].max())
        self.xzero = int(_xrange[0] - 1)
        self.yzero = int(_yrange[0] - 1)
        if self.xzero < 0:
            self.xzero = 0
        if self.yzero < 0:
            self.yzero = 0
        _out_naxis1 = int(ceil(_xrange[1]) - floor(_xrange[0]))
        _out_naxis2 = int(ceil(_yrange[1]) - floor(_yrange[0]))
        _max_x = _out_naxis1 + self.xzero
        _max_y = _out_naxis2 + self.yzero
        if _max_x > self.product_wcs.naxis1:
            _out_naxis1 -= _max_x - self.product_wcs.naxis1
        if _max_y > self.product_wcs.naxis2:
            _out_naxis2 -= _max_y - self.product_wcs.naxis2
        self.chip_shape = (
         _out_naxis1, _out_naxis2)
        self.xsh2 = int(ceil((self.product_wcs.naxis1 - _out_naxis1) / 2.0)) - self.xzero
        self.ysh2 = int(ceil((self.product_wcs.naxis2 - _out_naxis2) / 2.0)) - self.yzero

    def getShape(self):
        """
        This method gets the shape after opening and reading
        the input image. This version will be the default
        way of doing this, but each instrument may override
        this method with one specific to their data format.
        """
        return self.shape

    def setShape(self, size, pscale):
        """
        This method will set the shape for a new file if
        there is no image header information.

        Size will be defined as (nx,ny) and pixel size
        """
        self.shape = (
         size[0], size[1], pscale)

    def buildCoeffsName(self):
        """ Define the name of the coeffs file used for this chip. """
        indx = self.name.rfind('.')
        return self.name[:indx] + '_coeffs' + self.chip + '.dat'

    def writeCoeffs(self):
        """ Write out coeffs file for this chip. """
        if 'empty_model' not in self.geometry.model.refpix:
            _xref = self.geometry.wcs.chip_xref
            _yref = self.geometry.wcs.chip_yref
        else:
            _xref = None
            _yref = None
        _delta = not self.geometry.wcslin.subarray
        self.geometry.model.convert(self.coeffs, xref=_xref, yref=_yref, delta=_delta)
        self.setSingleOffsets()
        return

    def getDGEOExtn(self):
        """ Builds filename with extension to access distortion
            correction image extension appropriate to each chip.
        """
        if not self.dgeoname or self.dgeoname == 'N/A':
            return ('', '')
        fimg = fileutil.openImage(self.dgeoname)
        dx_extver = None
        dy_extver = None
        for hdu in fimg:
            hdr = hdu.header
            if 'CCDCHIP' not in hdr:
                _chip = 1
            else:
                _chip = int(hdr['CCDCHIP'])
            if 'EXTNAME' in hdr:
                _extname = hdr['EXTNAME'].lower()
                if _chip == int(self.chip):
                    if _extname == 'dx':
                        dx_extver = hdr['EXTVER']
                    if _extname == 'dy':
                        dy_extver = hdr['EXTVER']

        fimg.close()
        del fimg
        _dxgeo = self.dgeoname + '[DX,' + str(dx_extver) + ']'
        _dygeo = self.dgeoname + '[DY,' + str(dy_extver) + ']'
        return (
         _dxgeo, _dygeo)

    def getDGEOArrays(self):
        """ Return numpy objects for the distortion correction
            image arrays.

            If no DGEOFILE is specified, it will return
            empty 2x2 arrays.
        """
        if self.xgeoim == '':
            xgdim = ygdim = 2
            _pxg = np.zeros((ygdim, xgdim), dtype=np.float32)
            _pyg = np.zeros((ygdim, xgdim), dtype=np.float32)
        else:
            _xgfile = fileutil.openImage(self.xgeoim)
            _xgname, _xgext = fileutil.parseFilename(self.xgeoim)
            _ygname, _ygext = fileutil.parseFilename(self.ygeoim)
            _pxgext = fileutil.getExtn(_xgfile, extn=_xgext)
            _pygext = fileutil.getExtn(_xgfile, extn=_ygext)
            _ltv1 = int(self.geometry.wcs.offset_x)
            _ltv2 = int(self.geometry.wcs.offset_y)
            if _ltv1 != 0.0 or _ltv2 != 0.0:
                _pxg = _pxgext.data[_ltv2:_ltv2 + self.naxis2, _ltv1:_ltv1 + self.naxis1].copy()
                _pyg = _pygext.data[_ltv2:_ltv2 + self.naxis2, _ltv1:_ltv1 + self.naxis1].copy()
            else:
                _pxg = _pxgext.data.copy()
                _pyg = _pygext.data.copy()
            _xgfile.close()
            del _xgfile
        return (
         _pxg, _pyg)

    def applyDeltaWCS(self, dcrval=None, dcrpix=None, drot=None, dscale=None):
        """
        Apply shifts to the WCS of this exposure.

        Shifts are always relative to the current value and in the
        same reference frame.
        """
        in_wcs = self.geometry.wcs
        in_wcslin = self.geometry.wcslin
        if dcrpix:
            _crval = in_wcs.xy2rd((in_wcs.crpix1 - dcrpix[0], in_wcs.crpix2 - dcrpix[1]))
        elif dcrval:
            _crval = (
             in_wcs.crval1 - dcrval[0], in_wcs.crval2 - dcrval[1])
        else:
            _crval = None
        _orient = None
        _scale = None
        if drot:
            _orient = in_wcs.orient + drot
        if dscale:
            _scale = in_wcs.pscale * dscale
        _crpix = (in_wcs.crpix1, in_wcs.crpix2)
        in_wcs.updateWCS(pixel_scale=_scale, orient=_orient, refval=_crval, refpos=_crpix)
        in_wcslin.updateWCS(pixel_scale=_scale, orient=_orient, refval=_crval, refpos=_crpix)
        return

    def calcNewEdges(self, pscale=None):
        """
        This method will compute arrays for all the pixels around
        the edge of an image AFTER applying the geometry model.

        Parameter: delta - offset from nominal crpix center position

        Output:   xsides - array which contains the new positions for
                          all pixels along the LEFT and RIGHT edges
                  ysides - array which contains the new positions for
                          all pixels along the TOP and BOTTOM edges
        The new position for each pixel is calculated by calling
        self.geometry.apply() on each position.
        """
        numpix = self.naxis1 * 2 + self.naxis2 * 2
        border = np.zeros(shape=(numpix, 2), dtype=np.float64)
        xmin = 1.0
        xmax = self.naxis1
        ymin = 1.0
        ymax = self.naxis2
        xside = np.arange(self.naxis1) + xmin
        yside = np.arange(self.naxis2) + ymin
        _range0 = 0
        _range1 = self.naxis1
        border[_range0:_range1, 0] = xside
        border[_range0:_range1, 1] = ymin
        _range0 = _range1
        _range1 = _range0 + self.naxis1
        border[_range0:_range1, 0] = xside
        border[_range0:_range1, 1] = ymax
        _range0 = _range1
        _range1 = _range0 + self.naxis2
        border[_range0:_range1, 0] = xmin
        border[_range0:_range1, 1] = yside
        _range0 = _range1
        _range1 = _range0 + self.naxis2
        border[_range0:_range1, 0] = xmax
        border[_range0:_range1, 1] = yside
        border[:, 0], border[:, 1] = self.geometry.apply(border, pscale=pscale)
        _refpix = self.geometry.model.refpix
        if _refpix != None:
            _ratio = pscale / _refpix['PSCALE']
            _delta = (_refpix['XDELTA'] / _ratio, _refpix['YDELTA'] / _ratio)
        else:
            _delta = (0.0, 0.0)
        return border + _delta

    def getWCS(self):
        return self.geometry.wcs

    def showWCS(self):
        print self.geometry.wcs

    def runDriz(self, pixfrac=1.0, kernel='turbo', fillval='INDEF'):
        """ Runs the 'drizzle' algorithm on this specific chip to create
            a numpy object of the undistorted image.

            The resulting drizzled image gets returned as a numpy object.
        """
        _wcs = self.geometry.wcs
        _wcsout = self.product_wcs
        abxt, cdyt = drutil.wcsfit(self.geometry, self.product_wcs)
        xsh = abxt[2]
        ysh = cdyt[2]
        rot = fileutil.RADTODEG(np.arctan2(abxt[1], cdyt[0]))
        scale = self.product_wcs.pscale / self.geometry.wcslin.pscale
        _out_naxis1, _out_naxis2 = self.chip_shape
        if not os.path.exists(self.coeffs):
            self.writeCoeffs()
        _outsci = np.zeros((_out_naxis2, _out_naxis1), dtype=np.float32)
        _outwht = np.zeros((_out_naxis2, _out_naxis1), dtype=np.float32)
        _inwcs = np.zeros([8], dtype=np.float64)
        _outctx = np.zeros((_out_naxis2, _out_naxis1), dtype=np.int32)
        _pxg, _pyg = self.getDGEOArrays()
        _expname = self.name
        _handle = fileutil.openImage(_expname, mode='readonly', memmap=0)
        _fname, _extn = fileutil.parseFilename(_expname)
        _sciext = fileutil.getExtn(_handle, extn=_extn)
        _inwcs = drutil.convertWCS(wcsutil.WCSObject(_fname, header=_sciext.header), _inwcs)
        _planeid = 1
        _inwht = np.ones((self.naxis2, self.naxis1), dtype=np.float32)
        _wtscl = self.exptime
        _expin = self.exptime
        _uniqid = 1
        ystart = 0
        nmiss = 0
        nskip = 0
        _vers = ''
        _dny = self.naxis2
        _vers, nmiss, nskip = arrdriz.tdriz(_sciext.data.copy(), _inwht, _outsci, _outwht, _outctx, _uniqid, ystart, 1, 1, _dny, xsh, ysh, 'output', 'output', rot, scale, self.xsh2, self.ysh2, 1.0, 1.0, 0.0, 'output', _pxg, _pyg, 'center', pixfrac, kernel, self.coeffs, 'counts', _expin, _wtscl, fillval, _inwcs, nmiss, nskip, 1, 0.0, 0.0)
        if nmiss > 0:
            print '! Warning, ', nmiss, ' points were outside the output image.'
        if nskip > 0:
            print '! Note, ', nskip, ' input lines were skipped completely.'
        _handle.close()
        del _handle
        del _fname
        del _extn
        del _sciext
        del _inwht
        del _pxg
        del _pyg
        del _outwht
        del _outctx
        return _outsci