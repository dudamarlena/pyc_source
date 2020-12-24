# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/kcdimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 6569 bytes
"""
Authors: Jerome Kieffer, ESRF
         email:jerome.kieffer@esrf.fr

kcd images are 2D images written by the old KappaCCD diffractometer built by Nonius in the 1990's
Based on the edfimage.py parser.
"""
from __future__ import with_statement, print_function
import numpy, logging, os, string
from .fabioimage import FabioImage
from .fabioutils import six
logger = logging.getLogger(__name__)
import io
if not hasattr(io, 'SEEK_END'):
    SEEK_END = 2
else:
    SEEK_END = io.SEEK_END
DATA_TYPES = {'u16': numpy.uint16}
MINIMUM_KEYS = [
 'Data type',
 'X dimension',
 'Y dimension',
 'Number of readouts']
DEFAULT_VALUES = {'Data type': 'u16'}
if six.PY2:
    ALPHANUM = string.digits + string.letters + '. '
else:
    ALPHANUM = bytes(string.digits + string.ascii_letters + '. ', encoding='ASCII')

class KcdImage(FabioImage):
    __doc__ = '\n    Read the Nonius kcd data format '
    DESCRIPTION = "KCD file format from Nonius's KappaCCD diffractometer"
    DEFAULT_EXTENSIONS = [
     'kcd']

    def _readheader(self, infile):
        """
        Read in a header in some KCD format from an already open file
        """
        one_line = infile.readline()
        asciiHeader = True
        for oneChar in one_line.strip():
            if oneChar not in ALPHANUM:
                asciiHeader = False

        if asciiHeader is False:
            logger.warning('First line of %s does not seam to be ascii text!' % infile.name)
        end_of_headers = False
        while not end_of_headers:
            one_line = infile.readline()
            try:
                one_line = one_line.decode('ASCII')
            except UnicodeDecodeError:
                end_of_headers = True
            else:
                if len(one_line) > 100:
                    end_of_headers = True
            if not end_of_headers:
                if one_line.strip() == 'Binned mode':
                    one_line = 'Mode = Binned'
                if '=' in one_line:
                    key, val = one_line.split('=', 1)
                    key = key.strip()
                    self.header[key] = val.strip()
                else:
                    end_of_headers = True

        missing = []
        for item in MINIMUM_KEYS:
            if item not in self.header:
                missing.append(item)

        if len(missing) > 0:
            logger.debug('KCD file misses the keys ' + ' '.join(missing))

    def read(self, fname, frame=None):
        """
        Read in header into self.header and
            the data   into self.data
        """
        self.header = self.check_header()
        self.resetvals()
        with self._open(fname, 'rb') as (infile):
            self._readheader(infile)
            try:
                dim1 = int(self.header['X dimension'])
                dim2 = int(self.header['Y dimension'])
                self._shape = (dim2, dim1)
            except (KeyError, ValueError):
                raise IOError('KCD file %s is corrupt, cannot read it' % fname)

            try:
                bytecode = DATA_TYPES[self.header['Data type']]
            except KeyError:
                bytecode = numpy.uint16
                logger.warning('Defaulting type to uint16')

            self._dtype = numpy.dtype(bytecode)
            try:
                nbReadOut = int(self.header['Number of readouts'])
            except KeyError:
                logger.warning('Defaulting number of ReadOut to 1')
                nbReadOut = 1

            expected_size = dim1 * dim2 * self._dtype.itemsize * nbReadOut
            try:
                infile.seek(-expected_size, SEEK_END)
            except Exception:
                logger.debug('Backtrace', exc_info=True)
                logger.warning('seeking from end is not implemeneted for file %s', fname)
                if hasattr(infile, 'measure_size'):
                    fileSize = infile.measure_size()
                else:
                    if hasattr(infile, 'size'):
                        fileSize = infile.size
                    else:
                        if hasattr(infile, 'getSize'):
                            fileSize = infile.getSize()
                        else:
                            logger.warning('Unable to guess the file-size of %s', fname)
                            fileSize = os.stat(fname)[6]
                infile.seek(fileSize - expected_size - infile.tell(), 1)

            block = infile.read(expected_size)
        self.data = numpy.zeros((dim2, dim1), numpy.int32)
        stop = 0
        for i in range(nbReadOut):
            start = stop
            stop = (i + 1) * expected_size // nbReadOut
            data = numpy.frombuffer(block[start:stop], self._dtype).copy()
            data.shape = (dim2, dim1)
            if not numpy.little_endian:
                data.byteswap(True)
            self.data += data

        self._dtype = None
        self._shape = None
        self.resetvals()
        return self

    @staticmethod
    def checkData(data=None):
        if data is None:
            return
        else:
            return data.astype(int)


kcdimage = KcdImage