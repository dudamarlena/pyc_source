# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/raxisimage.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 12642 bytes
"""

Authors: Brian R. Pauw
email:  brian@stack.nl

Written using information gleaned from the ReadRAXISImage program
written by T. L. Hendrixson, made available by Rigaku Americas.
Available at: http://www.rigaku.com/downloads/software/readimage.html

"""
from __future__ import with_statement, print_function, division
__authors__ = [
 'Brian R. Pauw']
__contact__ = 'brian@stack.nl'
__license__ = 'MIT'
__copyright__ = 'Brian R. Pauw'
__date__ = '13/11/2018'
import logging, struct, os, numpy
from .fabioimage import FabioImage
from .fabioutils import OrderedDict
logger = logging.getLogger(__name__)
RIGAKU_KEYS = OrderedDict([
 ('InstrumentType', 10),
 ('Version', 10),
 ('Crystal Name', 20),
 ('Crystal System', 12),
 ('A', 'float'),
 ('B', 'float'),
 ('C', 'float'),
 ('Alpha', 'float'),
 ('Beta', 'float'),
 ('Gamma', 'float'),
 ('Space Group', 12),
 ('Mosaicity', 'float'),
 ('Memo', 80),
 ('Date', 12),
 ('Reserved Space 1', 84),
 ('User', 20),
 ('Xray Target', 4),
 ('Wavelength', 'float'),
 ('Monochromator', 20),
 ('Monochromator 2theta', 'float'),
 ('Collimator', 20),
 ('Filter', 4),
 ('Crystal-to-detector Distance', 'float'),
 ('Generator Voltage', 'float'),
 ('Generator Current', 'float'),
 ('Focus', 12),
 ('Xray Memo', 80),
 ('IP shape', 'long'),
 ('Oscillation Type', 'float'),
 ('Reserved Space 2', 56),
 ('Crystal Mount (spindle axis)', 4),
 ('Crystal Mount (beam axis)', 4),
 ('Phi Datum', 'float'),
 ('Phi Oscillation Start', 'float'),
 ('Phi Oscillation Stop', 'float'),
 ('Frame Number', 'long'),
 ('Exposure Time', 'float'),
 ('Direct beam X position', 'float'),
 ('Direct beam Y position', 'float'),
 ('Omega Angle', 'float'),
 ('Chi Angle', 'float'),
 ('2Theta Angle', 'float'),
 ('Mu Angle', 'float'),
 ('Image Template', 204),
 ('X Pixels', 'long'),
 ('Y Pixels', 'long'),
 ('X Pixel Length', 'float'),
 ('Y Pixel Length', 'float'),
 ('Record Length', 'long'),
 ('Total', 'long'),
 ('Starting Line', 'long'),
 ('IP Number', 'long'),
 ('Photomultiplier Ratio', 'float'),
 ('Fade Time (to start of read)', 'float'),
 ('Fade Time (to end of read)', 'float'),
 ('Host Type/Endian', 10),
 ('IP Type', 10),
 ('Horizontal Scan', 'long'),
 ('Vertical Scan', 'long'),
 ('Front/Back Scan', 'long'),
 ('Pixel Shift (RAXIS V)', 'float'),
 ('Even/Odd Intensity Ratio (RAXIS V)', 'float'),
 ('Magic number', 'long'),
 ('Number of Axes', 'long'),
 ('Goniometer Vector ax.1.1', 'float'),
 ('Goniometer Vector ax.1.2', 'float'),
 ('Goniometer Vector ax.1.3', 'float'),
 ('Goniometer Vector ax.2.1', 'float'),
 ('Goniometer Vector ax.2.2', 'float'),
 ('Goniometer Vector ax.2.3', 'float'),
 ('Goniometer Vector ax.3.1', 'float'),
 ('Goniometer Vector ax.3.2', 'float'),
 ('Goniometer Vector ax.3.3', 'float'),
 ('Goniometer Vector ax.4.1', 'float'),
 ('Goniometer Vector ax.4.2', 'float'),
 ('Goniometer Vector ax.4.3', 'float'),
 ('Goniometer Vector ax.5.1', 'float'),
 ('Goniometer Vector ax.5.2', 'float'),
 ('Goniometer Vector ax.5.3', 'float'),
 ('Goniometer Start ax.1', 'float'),
 ('Goniometer Start ax.2', 'float'),
 ('Goniometer Start ax.3', 'float'),
 ('Goniometer Start ax.4', 'float'),
 ('Goniometer Start ax.5', 'float'),
 ('Goniometer End ax.1', 'float'),
 ('Goniometer End ax.2', 'float'),
 ('Goniometer End ax.3', 'float'),
 ('Goniometer End ax.4', 'float'),
 ('Goniometer End ax.5', 'float'),
 ('Goniometer Offset ax.1', 'float'),
 ('Goniometer Offset ax.2', 'float'),
 ('Goniometer Offset ax.3', 'float'),
 ('Goniometer Offset ax.4', 'float'),
 ('Goniometer Offset ax.5', 'float'),
 ('Goniometer Scan Axis', 'long'),
 ('Axes Names', 40),
 ('file', 16),
 ('cmnt', 20),
 ('smpl', 20),
 ('iext', 'long'),
 ('reso', 'long'),
 ('save', 'long'),
 ('dint', 'long'),
 ('byte', 'long'),
 ('init', 'long'),
 ('ipus', 'long'),
 ('dexp', 'long'),
 ('expn', 'long'),
 ('posx', 20),
 ('posy', 20),
 ('xray', 'long'),
 ('Header Leftovers', -1)])

class RaxisImage(FabioImage):
    __doc__ = '\n    FabIO image class to read Rigaku RAXIS image files.\n    Write functions are not planned as there are plenty of more suitable\n    file formats available for storing detector data.\n    In particular, the MSB used in Rigaku files is used in an uncommon way:\n    it is used as a *multiply-by* flag rather than a normal image value bit.\n    While it is said to multiply by the value specified in the header, there\n    is at least one case where this is found not to hold, so YMMV and be careful.\n    '
    DESCRIPTION = 'Rigaku RAXIS file format'
    DEFAULT_EXTENSIONS = [
     'img']

    def __init__(self, *arg, **kwargs):
        """
        Generic constructor
        """
        FabioImage.__init__(self, *arg, **kwargs)
        self._dtype = numpy.dtype('uint16')
        self.endianness = '>'

    def swap_needed(self):
        """not sure if this function is needed"""
        endian = self.endianness
        if endian == '<' and numpy.little_endian or endian == '>' and not numpy.little_endian:
            return False
        if endian == '>' and numpy.little_endian or endian == '<' and not numpy.little_endian:
            return True

    def _readheader(self, infile):
        """
        Read and decode the header of a Rigaku RAXIS image.
        The Rigaku format uses a block of (at least) 1400 bytes for storing
        information. The information has a fixed structure, but endianness
        can be flipped for non-char values. Header items which are not
        capitalised form part of a non-standardized data block and may not
        be accurate.

        TODO: It would be useful to have an automatic endianness test in here.

        :param infile: Opened python file (can be stringIO or bzipped file)
        """
        endianness = self.endianness
        self.header = self.check_header()
        fs = endianness
        minHeaderLength = 1400
        infile.seek(0)
        rawHead = infile.read(minHeaderLength)
        curByte = 0
        for key, kind in RIGAKU_KEYS.items():
            if isinstance(kind, int):
                if kind == -1:
                    rByte = len(rawHead) - curByte
                    self.header[key] = struct.unpack(fs + str(rByte) + 's', rawHead[curByte:curByte + rByte])[0]
                    curByte += rByte
                    break
                rByte = kind
                self.header[key] = struct.unpack(fs + str(rByte) + 's', rawHead[curByte:curByte + rByte])[0]
                curByte += rByte
            else:
                if kind == 'float':
                    rByte = 4
                    self.header[key] = struct.unpack(fs + 'f', rawHead[curByte:curByte + rByte])[0]
                    curByte += rByte
                else:
                    if kind == 'long':
                        rByte = 4
                        self.header[key] = struct.unpack(fs + 'l', rawHead[curByte:curByte + rByte])[0]
                        curByte += rByte
                    else:
                        logger.warning('special header data type %s not understood', kind)
            if len(rawHead) == curByte:
                break

    def read(self, fname, frame=None):
        """
        try to read image
        :param fname: name of the file
        :param frame:
        """
        self.resetvals()
        infile = self._open(fname, 'rb')
        offset = -1
        self._readheader(infile)
        dim1 = self.header['X Pixels']
        dim2 = self.header['Y Pixels']
        self._shape = (dim2, dim1)
        self._dtype = numpy.dtype(numpy.uint16)
        shape = self.shape
        size = shape[0] * shape[1] * self._dtype.itemsize
        if offset >= 0:
            infile.seek(offset)
        else:
            try:
                attrs = dir(infile)
                if 'measure_size' in attrs:
                    infile.seek(infile.measure_size() - size)
                else:
                    if 'size' in attrs:
                        infile.seek(infile.size - size)
                    if 'len' in attrs:
                        infile.seek(infile.len - size)
                    else:
                        infile.seek(-size + offset + 1, os.SEEK_END)
            except IOError as error:
                logger.warning('expected datablock too large, please check bytecode settings: %s, IOError: %s' % (self._dtype.type, error))
            except Exception as error:
                logger.error('Uncommon error encountered when reading file: %s' % error)

        rawData = infile.read(size)
        data = numpy.frombuffer(rawData, self._dtype).copy().reshape(shape)
        if self.swap_needed():
            data.byteswap(True)
        di = data >> 15 != 0
        if di.sum() >= 1:
            logger.debug('Correct for PM: %s' % di.sum())
            data = data << 1 >> 1
            self._dtype = numpy.dtype(numpy.uint32)
            data = data.astype(self._dtype)
            sf = self.header['Photomultiplier Ratio']
            data[di] = (sf * data[di]).astype(self._dtype)
        self.data = data
        self._shape = None
        self._dtype = None
        return self

    def rigakuKeys(self):
        RKey = RIGAKU_KEYS
        orderList = list(RIGAKU_KEYS.keys())
        return (RKey, orderList)


raxisimage = RaxisImage