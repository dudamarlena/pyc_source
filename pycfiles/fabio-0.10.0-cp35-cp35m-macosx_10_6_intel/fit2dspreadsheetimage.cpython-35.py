# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/fit2dspreadsheetimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3429 bytes
"""
Read the fit2d ascii image output
        + Jon Wright, ESRF
"""
from __future__ import absolute_import, print_function, with_statement, division
import numpy, logging
_logger = logging.getLogger(__name__)
from .fabioimage import FabioImage

class Fit2dSpreadsheetImage(FabioImage):
    __doc__ = '\n    Read a fit2d ascii format\n    '
    DESCRIPTION = 'Fit2d spreadsheet ascii file format'
    DEFAULT_EXTENSIONS = [
     'spr']

    def _readheader(self, infile):
        """
        Read the header of the file
        """
        line = infile.readline()
        while line.startswith(b'#'):
            line = infile.readline()

        items = line.split()
        xdim = int(items[0])
        ydim = int(items[1])
        self.header['title'] = line
        self.header['Dim_1'] = xdim
        self.header['Dim_2'] = ydim

    def read(self, fname, frame=None):
        """
        Read in header into self.header and
            the data   into self.data
        """
        self.header = self.check_header()
        self.resetvals()
        infile = self._open(fname)
        self._readheader(infile)
        try:
            dim1 = int(self.header['Dim_1'])
            dim2 = int(self.header['Dim_2'])
            self._shape = (dim2, dim1)
        except (ValueError, KeyError):
            raise IOError('file %s is corrupt, cannot read it' % str(fname))

        self._dtype = numpy.dtype(numpy.float32)
        try:
            vals = []
            for line in infile.readlines():
                try:
                    vals.append([float(x) for x in line.split()])
                except Exception:
                    pass

            self.data = numpy.array(vals).astype(self._dtype)
            assert self.data.shape == self._shape
            self._shape = None
            self._dtype = None
        except Exception:
            _logger.debug('Backtrace', exc_info=True)
            raise IOError('Error reading ascii')

        self.resetvals()
        return self


fit2dspreadsheetimage = Fit2dSpreadsheetImage