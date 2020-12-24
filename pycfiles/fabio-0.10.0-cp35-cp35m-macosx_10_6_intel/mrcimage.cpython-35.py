# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/mrcimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 6560 bytes
from __future__ import with_statement, print_function
__authors__ = [
 'Jérôme Kieffer']
__contact__ = 'Jerome.Kieffer@terre-adelie.org'
__license__ = 'MIT'
__copyright__ = 'Jérôme Kieffer'
__version__ = '29 Oct 2013'
import logging, numpy
from .fabioimage import FabioImage
from .fabioutils import previous_filename, next_filename
logger = logging.getLogger(__name__)

class MrcImage(FabioImage):
    __doc__ = '\n    FabIO image class for Images from a mrc image stack\n    '
    DESCRIPTION = 'Medical Research Council file format for 3D electron density and 2D images'
    DEFAULT_EXTENSIONS = [
     'mrc', 'map', 'fei']
    KEYS = ('NX', 'NY', 'NZ', 'MODE', 'NXSTART', 'NYSTART', 'NZSTART', 'MX', 'MY',
            'MZ', 'CELL_A', 'CELL_B', 'CELL_C', 'CELL_ALPHA', 'CELL_BETA', 'CELL_GAMMA',
            'MAPC', 'MAPR', 'MAPS', 'DMIN', 'DMAX', 'DMEAN', 'ISPG', 'NSYMBT', 'EXTRA',
            'ORIGIN', 'MAP', 'MACHST', 'RMS', 'NLABL')
    _MODE_TO_DTYPE = {0: numpy.int8, 
     1: numpy.int16, 
     2: numpy.float32, 
     3: numpy.complex64, 
     4: numpy.complex64, 
     6: numpy.uint16}

    def _readheader(self, infile):
        """
        Read and decode the header of an image:

        :param infile: Opened python file (can be stringIO or bipped file)
        """
        self.header = self.check_header()
        int_block = numpy.frombuffer(infile.read(224), dtype=numpy.int32)
        for key, value in zip(self.KEYS, int_block):
            self.header[key] = value

        if self.header['MAP'] != 542130509:
            logger.info("Expected 'MAP ', got %s", self.header['MAP'].tobytes())
        for i in range(10):
            label = 'LABEL_%02i' % i
            self.header[label] = infile.read(80).strip()

        dim1 = int(self.header['NX'])
        dim2 = int(self.header['NY'])
        self._shape = (dim2, dim1)
        self._nframes = self.header['NZ']
        mode = self.header['MODE']
        if mode not in self._MODE_TO_DTYPE:
            raise IOError('Mode %s unsupported' % mode)
        dtype = numpy.dtype(self._MODE_TO_DTYPE[mode])
        self._dtype = dtype
        self.imagesize = dim1 * dim2 * dtype.itemsize

    def read(self, fname, frame=None):
        """
        try to read image
        :param fname: name of the file
        :param frame:
        """
        self.resetvals()
        self.sequencefilename = fname
        self.currentframe = frame or 0
        with self._open(fname) as (infile):
            self._readheader(infile)
            self._readframe(infile, self.currentframe)
        return self

    def _calc_offset(self, frame):
        """
        Calculate the frame position in the file

        :param frame: frame number
        """
        assert frame < self.nframes
        return 1024 + frame * self.imagesize

    def _makeframename(self):
        self.filename = '%s$%04d' % (self.sequencefilename,
         self.currentframe)

    def _readframe(self, infile, img_num):
        """
        Read a frame an populate data
        :param infile: opened file
        :param img_num: frame number (int)
        """
        if img_num > self.nframes or img_num < 0:
            raise RuntimeError('Requested frame number is out of range')
        infile.seek(self._calc_offset(img_num), 0)
        data_buffer = infile.read(self.imagesize)
        data = numpy.frombuffer(data_buffer, self._dtype).copy()
        data.shape = self._shape
        self.data = data
        self._shape = None
        self._dtype = None
        self.currentframe = int(img_num)
        self._makeframename()

    def getframe(self, num):
        """
        Returns a frame as a new FabioImage object
        :param num: frame number
        """
        if num < 0 or num > self.nframes:
            raise RuntimeError('Requested frame number is out of range')
        frame = MrcImage(header=self.header.copy())
        for key in ('dim1', 'dim2', 'nframes', 'bytecode', 'imagesize', 'sequencefilename'):
            frame.__setattr__(key, self.__getattribute__(key))

        with frame._open(self.sequencefilename, 'rb') as (infile):
            frame._readframe(infile, num)
        return frame

    def next(self):
        """
        Get the next image in a series as a fabio image
        """
        if self.currentframe < self.nframes - 1 and self.nframes > 1:
            return self.getframe(self.currentframe + 1)
        else:
            newobj = MrcImage()
            newobj.read(next_filename(self.sequencefilename))
            return newobj

    def previous(self):
        """
        Get the previous image in a series as a fabio image
        """
        if self.currentframe > 0:
            return self.getframe(self.currentframe - 1)
        else:
            newobj = MrcImage()
            newobj.read(previous_filename(self.sequencefilename))
            return newobj


mrcimage = MrcImage