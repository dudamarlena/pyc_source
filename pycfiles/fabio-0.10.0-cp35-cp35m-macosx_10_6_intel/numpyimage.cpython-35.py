# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/numpyimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 8082 bytes
"""Generic numpy file reader for FabIO"""
from __future__ import with_statement, print_function, division
__authors__ = [
 'Jérôme Kieffer']
__contact__ = 'jerome.kieffer@esrf.fr'
__license__ = 'MIT'
__copyright__ = 'ESRF'
__date__ = '16/11/2018'
import logging
logger = logging.getLogger(__name__)
import numpy
from . import fabioimage

class NumpyImage(fabioimage.FabioImage):
    __doc__ = '\n    FabIO image class for Images for numpy array dumps\n\n    Source: http://docs.scipy.org/doc/numpy/neps/npy-format.html\n\n    Format Specification: Version 1.0::\n\n        The first 6 bytes are a magic string: exactly “x93NUMPY”.\n\n        The next 1 byte is an unsigned byte: the major version number of the file\n        format, e.g. x01.\n\n        The next 1 byte is an unsigned byte: the minor version number of the file\n        format, e.g. x00.\n        Note: the version of the file format is not tied to the version of the numpy\n        package.\n\n        The next 2 bytes form a little-endian unsigned short int: the length of the\n        header data HEADER_LEN.\n\n        The next HEADER_LEN bytes form the header data describing the array’s\n        format. It is an ASCII string which contains a Python literal expression of\n        a dictionary. It is terminated by a newline (‘n’) and padded with\n        spaces (‘x20’) to make the total length of the magic string + 4 + HEADER_LEN\n        be evenly divisible by 16 for alignment purposes.\n\n        The dictionary contains three keys:\n\n            “descr” : dtype.descr\n                An object that can be passed as an argument to the numpy.dtype()\n                constructor to create the array’s dtype.\n            “fortran_order” : bool\n                Whether the array data is Fortran-contiguous or not.\n                Since Fortran-contiguous arrays are a common form of\n                non-C-contiguity, we allow them to be written directly\n                to disk for efficiency.\n            “shape” : tuple of int\n                The shape of the array.\n\n        For repeatability and readability, this dictionary is formatted using\n        pprint.pformat() so the keys are in alphabetic order.\n\n        Following the header comes the array data. If the dtype contains Python\n        objects (i.e. dtype.hasobject is True), then the data is a Python pickle of\n        the array. Otherwise the data is the contiguous (either C- or Fortran-,\n        depending on fortran_order) bytes of the array. Consumers can figure out the\n        number of bytes by multiplying the number of elements given by the shape\n        (noting that shape=() means there is 1 element) by dtype.itemsize.\n\n    Format Specification: Version 2.0::\n\n        The version 1.0 format only allowed the array header to have a total size of\n        65535 bytes. This can be exceeded by structured arrays with a large number\n        of columns. The version 2.0 format extends the header size to 4 GiB.\n        numpy.save will automatically save in 2.0 format if the data requires it,\n        else it will always use the more compatible 1.0 format.\n\n        The description of the fourth element of the header therefore has become:\n\n        The next 4 bytes form a little-endian unsigned int: the length of the\n        header data HEADER_LEN.\n    '
    DESCRIPTION = 'Numpy array file format'
    DEFAULT_EXTENSIONS = [
     'npy']

    def __init__(self, data=None, header=None):
        """
        Set up initial values
        """
        fabioimage.FabioImage.__init__(self, data, header)
        self.dataset = self.data
        self.slice_dataset()
        self.filename = 'Numpy_array_%x' % id(self.dataset)

    def slice_dataset(self, frame=None):
        if self.dataset is None:
            return
        if self.dataset.ndim > 3:
            shape = self.dataset.shape[-2:]
            self.dataset.shape = (-1, ) + shape
        elif self.dataset.ndim < 2:
            self.dataset.shape = (1, -1)
        if self.dataset.ndim == 2:
            self.data = self.dataset
        elif self.dataset.ndim == 3:
            self._nframes = self.dataset.shape[0]
            if frame is None:
                frame = 0
            if frame < self.nframes:
                self.data = self.dataset[frame]
            self.currentframe = frame

    def _readheader(self, infile):
        """
        Read and decode the header of an image:

        :param infile: Opened python file (can be stringIO or bzipped file)
        """
        self.header = self.check_header()
        infile.seek(0)

    def read(self, fname, frame=None):
        """
        Try to read image

        :param fname: name of the file
        """
        self.resetvals()
        infile = self._open(fname)
        self._readheader(infile)
        self.dataset = numpy.load(infile, allow_pickle=False)
        self.slice_dataset(frame)
        return self

    def write(self, fname):
        """
        Try to write image

        :param fname: name of the file
        """
        if self.dataset is None and self.data is not None:
            self.dataset = self.data
        numpy.save(fname, self.dataset)

    def _get_frame(self, num):
        """Inherited function returning a FabioFrame"""
        if self.nframes > 1:
            if num >= 0 and num < self.nframes:
                data = self.dataset[num]
                header = self.header.copy()
                frame = fabioimage.FabioFrame(data=data, header=header)
                frame._set_container(self, num)
                frame._set_file_container(self, num)
            else:
                raise IndexError('getframe %s out of range [%s %s[' % (num, 0, self.nframes))
        else:
            frame = fabioimage.FabioImage._get_frame(self, num)
        return frame

    def getframe(self, num):
        """ returns the frame numbered 'num' in the stack if applicable"""
        if self.nframes > 1:
            frame = None
            if num >= 0 and num < self.nframes:
                data = self.dataset[num]
                frame = self.__class__(data=data, header=self.header)
                frame.dataset = self.dataset
                frame._nframes = self.nframes
                frame.currentframe = num
            else:
                raise IndexError('getframe %s out of range [%s %s[' % (num, 0, self.nframes))
        else:
            frame = fabioimage.FabioImage.getframe(self, num)
        return frame

    def previous(self):
        """ returns the previous frame in the series as a fabioimage """
        return self.getframe(self.currentframe - 1)

    def next(self):
        """ returns the next frame in the series as a fabioimage """
        return self.getframe(self.currentframe + 1)


numpyimage = NumpyImage