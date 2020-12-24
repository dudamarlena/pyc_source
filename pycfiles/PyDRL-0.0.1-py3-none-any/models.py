# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\distortion\models.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
import types, mutil, numpy as np, mutil
from mutil import combin
yes = True
no = False

class GeometryModel:
    """
    Base class for Distortion model.
    There will be a separate class for each type of
    model/filetype used with drizzle, i.e., IDCModel and
    DrizzleModel.

    Each class will know how to apply the distortion to a
    single point and how to convert coefficients to an input table
    suitable for the drizzle task.

    Coefficients will be stored in CX,CY arrays.
    """
    NORDER = 3

    def __init__(self):
        """  This will open the given file and determine its type and norder."""
        self.cx = None
        self.cy = None
        self.refpix = None
        self.norder = self.NORDER
        self.x0 = None
        self.y0 = None
        self.direction = 'forward'
        self.pscale = 1.0
        return

    def shift(self, cx, cy, xs, ys):
        """
        Shift reference position of coefficients to new center
        where (xs,ys) = old-reference-position - subarray/image center.
        This will support creating coeffs files for drizzle which will
        be applied relative to the center of the image, rather than relative
        to the reference position of the chip.
        """
        _cxs = np.zeros(shape=cx.shape, dtype=cx.dtype)
        _cys = np.zeros(shape=cy.shape, dtype=cy.dtype)
        _k = self.norder + 1
        for m in xrange(_k):
            for n in xrange(_k):
                if m >= n:
                    _ilist = range(m, _k)
                    for i in _ilist:
                        _jlist = range(n, i - (m - n) + 1)
                        for j in _jlist:
                            _cxs[(m, n)] += cx[(i, j)] * combin(j, n) * combin(i - j, m - n) * pow(xs, j - n) * pow(ys, i - j - (m - n))
                            _cys[(m, n)] += cy[(i, j)] * combin(j, n) * combin(i - j, m - n) * pow(xs, j - n) * pow(ys, i - j - (m - n))

        return (
         _cxs, _cys)

    def convert(self, tmpname, xref=None, yref=None, delta=yes):
        """
         Open up an ASCII file, output coefficients in drizzle
          format after converting them as necessary.
        First, normalize these coefficients to what drizzle expects
        Normalize the coefficients by the MODEL/output plate scale.

        16-May-2002:
        Revised to work with higher order polynomials by John Blakeslee.
        27-June-2002:
            Added ability to shift coefficients to new center for support
                of subarrays.
        """
        cx = self.cx / self.pscale
        cy = self.cy / self.pscale
        x0 = self.refpix['XDELTA'] + cx[(0, 0)]
        y0 = self.refpix['YDELTA'] + cy[(0, 0)]
        xr = self.refpix['CHIP_XREF']
        yr = self.refpix['CHIP_YREF']
        self.x0 = x0
        self.y0 = y0
        lines = []
        lines.append('# Polynomial distortion coefficients\n')
        lines.append('# Extracted from "%s" \n' % self.name)
        lines.append('refpix %f %f \n' % (xr, yr))
        if self.norder == 3:
            lines.append('cubic\n')
        elif self.norder == 4:
            lines.append('quartic\n')
        elif self.norder == 5:
            lines.append('quintic\n')
        else:
            raise ValueError, 'Drizzle cannot handle poly distortions of order %d' % self.norder
        str = '%16.8f %16.8g %16.8g %16.8g %16.8g \n' % (x0, cx[(1, 1)], cx[(1, 0)], cx[(2, 2)], cx[(2, 1)])
        lines.append(str)
        str = '%16.8g %16.8g %16.8g %16.8g %16.8g \n' % (cx[(2, 0)], cx[(3, 3)], cx[(3, 2)], cx[(3, 1)], cx[(3, 0)])
        lines.append(str)
        if self.norder > 3:
            str = '%16.8g %16.8g %16.8g %16.8g %16.8g \n' % (cx[(4, 4)], cx[(4, 3)], cx[(4, 2)], cx[(4, 1)], cx[(4, 0)])
            lines.append(str)
        if self.norder > 4:
            str = '%16.8g %16.8g %16.8g %16.8g %16.8g %16.8g \n' % (cx[(5, 5)], cx[(5, 4)], cx[(5, 3)], cx[(5, 2)], cx[(5, 1)], cx[(5, 0)])
            lines.append(str)
        lines.append('\n')
        str = '%16.8f %16.8g %16.8g %16.8g %16.8g \n' % (y0, cy[(1, 1)], cy[(1, 0)], cy[(2, 2)], cy[(2, 1)])
        lines.append(str)
        str = '%16.8g %16.8g %16.8g %16.8g %16.8g \n' % (cy[(2, 0)], cy[(3, 3)], cy[(3, 2)], cy[(3, 1)], cy[(3, 0)])
        lines.append(str)
        if self.norder > 3:
            str = '%16.8g %16.8g %16.8g %16.8g %16.8g \n' % (cy[(4, 4)], cy[(4, 3)], cy[(4, 2)], cy[(4, 1)], cy[(4, 0)])
            lines.append(str)
        if self.norder > 4:
            str = '%16.8g %16.8g %16.8g %16.8g %16.8g %16.8g \n' % (cy[(5, 5)], cy[(5, 4)], cy[(5, 3)], cy[(5, 2)], cy[(5, 1)], cy[(5, 0)])
            lines.append(str)
        output = open(tmpname, 'w')
        output.writelines(lines)
        output.close()

    def apply(self, pixpos, scale=1.0, order=None):
        """
         Apply coefficients to a pixel position or a list of positions.
          This should be the same for all coefficients tables.
        Return the geometrically-adjusted position
        in arcseconds from the reference position as a tuple (x,y).

        Compute delta from reference position
        """
        if self.cx == None:
            return (pixpos[:, 0], pixpos[:, 1])
        else:
            if order is None:
                order = self.norder
            _cx = self.cx / (self.pscale * scale)
            _cy = self.cy / (self.pscale * scale)
            _convert = no
            _p = pixpos
            _cx[(0, 0)] = 0.0
            _cy[(0, 0)] = 0.0
            if isinstance(_p, types.ListType) or isinstance(_p, types.TupleType):
                _p = np.array(_p, dtype=np.float64)
                _convert = yes
            dxy = _p - (self.refpix['XREF'], self.refpix['YREF'])
            c = _p * 0.0
            for i in range(order + 1):
                for j in range(i + 1):
                    c[:, 0] = c[:, 0] + _cx[i][j] * pow(dxy[:, 0], j) * pow(dxy[:, 1], i - j)
                    c[:, 1] = c[:, 1] + _cy[i][j] * pow(dxy[:, 0], j) * pow(dxy[:, 1], i - j)

            xc = c[:, 0]
            yc = c[:, 1]
            if _convert:
                xc = xc.tolist()
                yc = yc.tolist()
                if len(xc) == 1:
                    xc = xc[0]
                    yc = yc[0]
            return (xc, yc)

    def setPScaleCoeffs(self, pscale):
        self.cx[(1, 1)] = pscale
        self.cy[(1, 0)] = pscale
        self.refpix['PSCALE'] = pscale
        self.pscale = pscale


class IDCModel(GeometryModel):
    """
    This class will open the IDCTAB, select proper row based on
    chip/direction and populate cx,cy arrays.
    We also need to read in SCALE, XCOM,YCOM, XREF,YREF as well.
    """

    def __init__(self, idcfile, date=None, chip=1, direction='forward', filter1='CLEAR1', filter2='CLEAR2', offtab=None, binned=1, tddcorr=False):
        GeometryModel.__init__(self)
        self.name = idcfile
        self.cx, self.cy, self.refpix, self.norder = mutil.readIDCtab(idcfile, chip=chip, direction=direction, filter1=filter1, filter2=filter2, date=date, offtab=offtab, tddcorr=tddcorr)
        if 'empty_model' in self.refpix and self.refpix['empty_model']:
            pass
        else:
            self.refpix['PSCALE'] = self.refpix['PSCALE'] * binned
            self.cx = self.cx * binned
            self.cy = self.cy * binned
            self.refpix['XREF'] = self.refpix['XREF'] / binned
            self.refpix['YREF'] = self.refpix['YREF'] / binned
            self.refpix['XSIZE'] = self.refpix['XSIZE'] / binned
            self.refpix['YSIZE'] = self.refpix['YSIZE'] / binned
        self.pscale = self.refpix['PSCALE']


class WCSModel(GeometryModel):
    """
    This class sets up a distortion model based on coefficients
    found in the image header.
    """

    def __init__(self, header, rootname):
        GeometryModel.__init__(self)
        if 'rootname' in header:
            self.name = header['rootname']
        else:
            self.name = rootname
        self.name += '_sip'
        if 'wfctdd' in header and header['wfctdd'] == 'T':
            self.name += '_tdd'
        self.cx, self.cy, self.refpix, self.norder = mutil.readWCSCoeffs(header)
        self.pscale = self.refpix['PSCALE']


class DrizzleModel(GeometryModel):
    """
    This class will read in an ASCII Cubic
    drizzle coeffs file and populate the cx,cy arrays.
    """

    def __init__(self, idcfile, scale=None):
        GeometryModel.__init__(self)
        self.name = idcfile
        self.cx, self.cy, self.refpix, self.norder = mutil.readCubicTable(idcfile)
        if scale != None:
            self.pscale = scale
        else:
            self.pscale = self.refpix['PSCALE']
        return


class TraugerModel(GeometryModel):
    """
    This class will read in the ASCII Trauger coeffs
    file, convert them to SIAF coefficients, then populate
    the cx,cy arrays.
    """
    NORDER = 3

    def __init__(self, idcfile, lam):
        GeometryModel.__init__(self)
        self.name = idcfile
        self.cx, self.cy, self.refpix, self.norder = mutil.readTraugerTable(idcfile, lam)
        self.pscale = self.refpix['PSCALE']