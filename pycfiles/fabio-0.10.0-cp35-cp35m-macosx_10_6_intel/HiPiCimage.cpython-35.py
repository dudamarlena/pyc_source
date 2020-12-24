# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/HiPiCimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 5346 bytes
"""
Authors: Henning O. Sorensen & Erik Knudsen
         Center for Fundamental Research: Metal Structures in Four Dimensions
         Risoe National Laboratory
         Frederiksborgvej 399
         DK-4000 Roskilde
         email:erik.knudsen@risoe.dk

        + Jon Wright, ESRF

Information about the file format from Masakatzu Kobayashi is highly appreciated
"""
from __future__ import with_statement, print_function
import numpy, logging
logger = logging.getLogger(__name__)
from .fabioimage import FabioImage

class HipicImage(FabioImage):
    __doc__ = ' Read HiPic images e.g. collected with a Hamamatsu CCD camera'
    DESCRIPTION = 'HiPic file format from Hamamatsu CCD cameras'
    DEFAULT_EXTENSIONS = [
     'img']

    def _readheader(self, infile):
        """
        Read in a header from an already open file

        """
        Image_tag = infile.read(2)
        Comment_len = numpy.frombuffer(infile.read(2), numpy.uint16)
        Dim_1 = numpy.frombuffer(infile.read(2), numpy.uint16)[0]
        Dim_2 = numpy.frombuffer(infile.read(2), numpy.uint16)[0]
        Dim_1_offset = numpy.frombuffer(infile.read(2), numpy.uint16)[0]
        Dim_2_offset = numpy.frombuffer(infile.read(2), numpy.uint16)[0]
        _HeaderType = numpy.frombuffer(infile.read(2), numpy.uint16)[0]
        _Dump = infile.read(50)
        Comment = infile.read(Comment_len)
        self.header['Image_tag'] = Image_tag
        self.header['Dim_1'] = Dim_1
        self.header['Dim_2'] = Dim_2
        self.header['Dim_1_offset'] = Dim_1_offset
        self.header['Dim_2_offset'] = Dim_2_offset
        if Image_tag != 'IM':
            logger.warning('No opening. Corrupt header of HiPic file %s', str(infile.name))
        Comment_split = Comment[:Comment.find('\x00')].split('\r\n')
        for topcomment in Comment_split:
            topsplit = topcomment.split(',')
            for line in topsplit:
                if '=' in line:
                    key, val = line.split('=', 1)
                    key = key.rstrip().lstrip()
                    self.header_keys.append(key)
                    self.header[key] = val.lstrip().rstrip()
                    self.header[key] = val.lstrip('"').rstrip('"')

    def read(self, fname, frame=None):
        """
        Read in header into self.header and
            the data   into self.data
        """
        self.header = self.check_header()
        self.resetvals()
        infile = self._open(fname, 'rb')
        self._readheader(infile)
        try:
            dim1 = int(self.header['Dim_1'])
            dim2 = int(self.header['Dim_2'])
            self._shape = (dim2, dim1)
        except (ValueError, KeyError):
            raise IOError('HiPic file %s is corrupted, cannot read it' % str(fname))

        dtype = numpy.dtype(numpy.uint16)
        self._dtype = dtype
        block = infile.read(dim1 * dim2 * dtype.itemsize)
        infile.close()
        try:
            self.data = numpy.frombuffer(block, dtype).copy().reshape((dim2, dim1))
        except Exception:
            logger.debug('%s %s %s %s %s', len(block), dtype, self.bpp, dim2, dim1)
            logger.debug('Backtrace', exc_info=True)
            raise IOError('Size spec in HiPic-header does not match size of image data field')

        self._dtype = None
        self._shape = None
        if self.data.max() > 4095:
            gt12bit = self.data > 4095
            self.data = self.data - gt12bit * 65535
        return self


HiPiCimage = HipicImage