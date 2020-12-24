# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/fit2dmaskimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 5300 bytes
"""
Author: Andy Hammersley, ESRF
Translation into python/fabio: Jon Wright, ESRF.
Writer: Jérôme Kieffer
"""
from __future__ import with_statement, print_function
__authors__ = [
 'Jon Wright', 'Jérôme Kieffer']
__contact__ = 'Jerome.Kieffer@esrf.fr'
__license__ = 'GPLv3+'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
__version__ = '06/01/2015'
import numpy, struct
from .fabioimage import FabioImage
from .third_party import six

class Fit2dMaskImage(FabioImage):
    __doc__ = " Read and try to write Andy Hammersley's mask format "
    DESCRIPTION = 'Fit2d mask file format'
    DEFAULT_EXTENSIONS = [
     'msk']

    def _readheader(self, infile):
        """
        Read in a header from an already open file
        """
        header = infile.read(1024)
        for i, j in [(b'M', 0),
         (b'A', 4),
         (b'S', 8),
         (b'K', 12)]:
            if header[j] != i[0]:
                raise Exception('Not a fit2d mask file')

        fit2dhdr = numpy.frombuffer(header, numpy.int32)
        if not numpy.little_endian:
            fit2dhdr.byteswap(True)
        dim1 = fit2dhdr[4]
        dim2 = fit2dhdr[5]
        self._shape = (dim2, dim1)

    def read(self, fname, frame=None):
        """
        Read in header into self.header and
            the data   into self.data
        """
        fin = self._open(fname)
        self._readheader(fin)
        self._dtype = numpy.dtype(numpy.uint8)
        dim2, dim1 = self._shape
        num_ints = (dim1 + 31) // 32
        total = dim2 * num_ints * 4
        data = fin.read(total)
        assert len(data) == total
        fin.close()
        data = numpy.frombuffer(data, numpy.uint8)
        if not numpy.little_endian:
            data.byteswap(True)
        data = numpy.reshape(data, (dim2, num_ints * 4))
        result = numpy.zeros((dim2, num_ints * 4 * 8), numpy.uint8)
        bits = numpy.ones(1, numpy.uint8)
        for i in range(8):
            temp = numpy.bitwise_and(bits, data)
            result[:, i::8] = temp.astype(numpy.uint8)
            bits = bits * 2

        spares = num_ints * 4 * 8 - dim1
        if spares == 0:
            data = numpy.where(result == 0, 0, 1)
        else:
            data = numpy.where(result[:, :-spares] == 0, 0, 1)
        self.data = numpy.ascontiguousarray(data, dtype=numpy.uint8)
        self.data.shape = self._shape
        self._shape = None
        return self

    def write(self, fname):
        """
        Try to write a file
        """
        dim2, dim1 = self.shape
        header = bytearray(b'\x00' * 1024)
        header[0] = 77
        header[4] = 65
        header[8] = 83
        header[12] = 75
        header[24] = 1
        header[16:20] = struct.pack('<I', dim1)
        header[20:24] = struct.pack('<I', dim2)
        compact_array = numpy.zeros((dim2, (dim1 + 31) // 32 * 4), dtype=numpy.uint8)
        large_array = numpy.zeros((dim2, (dim1 + 31) // 32 * 32), dtype=numpy.uint8)
        large_array[:dim2, :dim1] = self.data != 0
        for i in range(8):
            order = 1 << i
            compact_array += large_array[:, i::8] * order

        with self._open(fname, mode='wb') as (outfile):
            outfile.write(six.binary_type(header))
            outfile.write(compact_array.tobytes())

    @staticmethod
    def check_data(data=None):
        if data is None:
            return
        else:
            return (data != 0).astype(numpy.uint8)


fit2dmaskimage = Fit2dMaskImage