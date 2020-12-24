# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/fit2dimage.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 6363 bytes
"""FabIO reader for Fit2D binary images

TODO: handle big-endian files
"""
from __future__ import with_statement, print_function, division
__authors__ = [
 'Jérôme Kieffer']
__contact__ = 'jerome.kiefer@esrf.fr'
__license__ = 'MIT'
__copyright__ = '2016-2016 European Synchrotron Radiation Facility'
__date__ = '29/10/2018'
import logging
logger = logging.getLogger(__name__)
import numpy
from .fabioimage import FabioImage, OrderedDict

def hex_to(stg, type_='int'):
    """convert a 8-byte-long string (bytes) into an int or a float

    :param stg: bytes string
    :param str type_: "int" or "float"
    """
    value = int(stg, 16)
    if type_ == 'float':
        value = numpy.array([int('38d1b717', 16)], 'int32').view('float32')[0]
    return value


class Fit2dImage(FabioImage):
    __doc__ = '\n    FabIO image class for Images for XXX detector\n    '
    DESCRIPTION = 'Fit2d file format'
    DEFAULT_EXTENSIONS = [
     'f2d']
    BUFFER_SIZE = 512
    PIXELS_PER_CHUNK = 128
    ENC = 'ascii'

    def __init__(self, *arg, **kwargs):
        """
        Generic constructor
        """
        FabioImage.__init__(self, *arg, **kwargs)
        self.num_block = None

    def _readheader(self, infile):
        """
        Read and decode the header of an image:

        :param infile: Opened python file (can be stringIO or bipped file)
        """
        header = OrderedDict()
        self.header = self.check_header()
        while 1:
            line = infile.read(self.BUFFER_SIZE)
            if len(line) < self.BUFFER_SIZE:
                break
            if line[0:1] != b'\\':
                for block_read in range(2, 16):
                    line = infile.read(self.BUFFER_SIZE)
                    if line[0:1] == b'\\':
                        self.BUFFER_SIZE *= block_read
                        logger.warning('Increase block size to %s ', self.BUFFER_SIZE)
                        infile.seek(0)
                        break
                else:
                    err = "issue while reading header, expected '', got %s" % line[0]
                    logger.error(err)
                    raise RuntimeError(err)

            key, line = line.split(b':', 1)
            num_block = hex_to(line[:8])
            metadatatype = line[8:9].decode(self.ENC)
            key = key[1:].decode(self.ENC)
            if metadatatype == 's':
                len_value = hex_to(line[9:17])
                header[key] = line[17:17 + len_value].decode(self.ENC)
            else:
                if metadatatype == 'r':
                    header[key] = hex_to(line[9:17], 'float')
                else:
                    if metadatatype == 'i':
                        header[key] = hex_to(line[9:17])
                    elif metadatatype == 'a' and num_block != 0:
                        self.num_block = num_block
                        array_type = line[9:10].decode(self.ENC)
                        dim1 = hex_to(line[26:34])
                        dim2 = hex_to(line[34:42])
                        if array_type == 'i':
                            bytecode = 'int32'
                            bpp = 4
                        else:
                            if array_type == 'r':
                                bytecode = 'float32'
                                bpp = 4
                            else:
                                if array_type == 'l':
                                    bytecode = 'int8'
                                    bpp = 1
                                    raw = infile.read(self.num_block * self.BUFFER_SIZE)
                                    i32 = numpy.frombuffer(raw, numpy.int32).copy()
                                    if numpy.little_endian:
                                        i32.byteswap(True)
                                    r32 = numpy.unpackbits(i32.view('uint8')).reshape((-1,
                                                                                       32))
                                    r31 = r32[:, -1:0:-1]
                                    mask = r31.ravel()[:dim1 * dim2].reshape((dim2, dim1))
                                    header[key] = mask
                                    continue
                                else:
                                    err = 'unsupported data type: %s' % array_type
                                    logger.error(err)
                                    raise RuntimeError(err)
                            raw = infile.read(self.num_block * self.BUFFER_SIZE)
                            decoded = numpy.frombuffer(raw, bytecode).copy().reshape((-1, self.BUFFER_SIZE // bpp))
                            decoded = decoded[:, :self.PIXELS_PER_CHUNK].ravel()
                            header[key] = decoded[:dim1 * dim2].reshape(dim2, dim1)

        self.header = header

    def read(self, fname, frame=None):
        """try to read image

        :param fname: name of the file
        """
        self.resetvals()
        with self._open(fname) as (infile):
            self._readheader(infile)
        self.data = self.header.pop('data_array')
        return self


fit2dimage = Fit2dImage