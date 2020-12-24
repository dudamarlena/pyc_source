# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/edfimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 65459 bytes
from __future__ import with_statement, print_function, absolute_import, division
import os, re, string, logging, numpy
logger = logging.getLogger(__name__)
from . import fabioimage
from .fabioutils import isAscii, toAscii, nice_int, OrderedDict
from .compression import decBzip2, decGzip, decZlib
from . import compression as compression_module
from . import fabioutils
from .utils import deprecation
from collections import namedtuple
BLOCKSIZE = 512
MAX_BLOCKS = 40
DATA_TYPES = {'SignedByte': numpy.int8, 
 'Signed8': numpy.int8, 
 'UnsignedByte': numpy.uint8, 
 'Unsigned8': numpy.uint8, 
 'SignedShort': numpy.int16, 
 'Signed16': numpy.int16, 
 'UnsignedShort': numpy.uint16, 
 'Unsigned16': numpy.uint16, 
 'UnsignedShortInteger': numpy.uint16, 
 'SignedInteger': numpy.int32, 
 'Signed32': numpy.int32, 
 'UnsignedInteger': numpy.uint32, 
 'Unsigned32': numpy.uint32, 
 'SignedLong': numpy.int32, 
 'UnsignedLong': numpy.uint32, 
 'Signed64': numpy.int64, 
 'Unsigned64': numpy.uint64, 
 'FloatValue': numpy.float32, 
 'FLOATVALUE': numpy.float32, 
 'FLOAT': numpy.float32, 
 'Float': numpy.float32, 
 'FloatIEEE32': numpy.float32, 
 'Float32': numpy.float32, 
 'Double': numpy.float64, 
 'DoubleValue': numpy.float64, 
 'FloatIEEE64': numpy.float64, 
 'DoubleIEEE64': numpy.float64}
try:
    DATA_TYPES['FloatIEEE128'] = DATA_TYPES['DoubleIEEE128'] = DATA_TYPES['QuadrupleValue'] = numpy.float128
except AttributeError:
    logger.debug('No support for float128 in your code')

NUMPY_EDF_DTYPE = {'int8': 'SignedByte', 
 'int16': 'SignedShort', 
 'int32': 'SignedInteger', 
 'int64': 'Signed64', 
 'uint8': 'UnsignedByte', 
 'uint16': 'UnsignedShort', 
 'uint32': 'UnsignedInteger', 
 'uint64': 'Unsigned64', 
 'float32': 'FloatValue', 
 'float64': 'DoubleValue', 
 'float128': 'QuadrupleValue'}
MINIMUM_KEYS = set(['HEADERID',
 'IMAGE',
 'BYTEORDER',
 'DATATYPE',
 'DIM_1',
 'DIM_2',
 'SIZE'])
MINIMUM_KEYS2 = set(['EDF_DATABLOCKID',
 'EDF_BINARYSIZE',
 'BYTEORDER',
 'DATATYPE',
 'DIM_1',
 'DIM_2'])
DEFAULT_VALUES = {}
HeaderBlockType = namedtuple('HeaderBlockType', 'header, header_size, binary_size, data_format_version')

class MalformedHeaderError(IOError):
    __doc__ = 'Raised when a header is malformed'


class EdfFrame(fabioimage.FabioFrame):
    __doc__ = '\n    A class representing a single frame in an EDF file\n    '

    def __init__(self, data=None, header=None, number=None):
        header = EdfImage.check_header(header)
        super(EdfFrame, self).__init__(data, header=header)
        self._data_compression = None
        self._data_swap_needed = None
        self._data = data
        self.start = None
        self.blobsize = None
        self.size = None
        self.file = None
        self._dtype = None
        self.incomplete_data = False
        self.bfname = None
        self.bfstart = 0
        self.bfsize = None
        if number is not None:
            deprecation.deprecated_warning(reason="Argument 'number' is not used anymore", deprecated_since='0.10.0beta')

    @staticmethod
    def get_data_rank(header=None, capsHeader=None):
        """
        Get the rank of the data array by searching the header for the
        key DIM_i with the highest index i. The smallest index of
        DIM_i is 1 (1-based). The highest index is equal to the rank.

        :param: dict header
        :param: dict capsHeader (optional)
        :return: int rank
        """
        if header is None:
            header = {}
        if capsHeader is None:
            capsHeader = {}
            for key in header:
                capsHeader[key.upper()] = key

        rank = 0
        if capsHeader is not None:
            rank = 0
            for key in capsHeader:
                if key[0:4] == 'DIM_':
                    try:
                        index = int(key[4:])
                    except ValueError:
                        logger.error('Unable converting index of {} to integer.'.format(key))

                    if index > rank:
                        rank = index

        return rank

    @staticmethod
    def get_data_shape(rank=0, header=None, capsHeader=None):
        """
        Returns a tuple with the number of dimensions up to the given rank.
        The dimensions DIM_i are read from the header dictionary. The
        values of missing DIM_i keys are set to 1, except DIM_1 which has
        the default 0.

        The DIM_i header indices are 1-based and are equal to the number of
        elements in each dimension of a data array, starting with DIM_1 as
        the number of elements of a linear array, DIM_2 is the number of
        stacked linear arrays with DIM_1 elements, etc. (FORTRAN-type
        indexing).

        The shape tuple is filled from the end to the beginning with the values
        of DIM_i, i.e. shape[0] is equal to value of DIM_rank, shape[rank-i] is
        equal to the value of DIM_i (e.g. for rank==2, shape[0]==value(DIM_2),
        shape[1]==value(DIM_1)). The returned shape tuple can be used with
        numpy arrays.

        :param: int rank
        :param: dict header
        :param: dict capsHeader (optional)
        :return: tuple shape
        """
        if rank is None:
            rank = 0
        if header is None:
            header = {}
        if capsHeader is None:
            capsHeader = {}
            for key in header:
                capsHeader[key.upper()] = key

        shape = []
        for irank in range(1, rank + 1):
            strDim = 'DIM_{:d}'.format(irank)
            if strDim in capsHeader:
                try:
                    dimi = nice_int(header[capsHeader[strDim]])
                except ValueError:
                    logger.error('Unable converting value of {} to integer: {}'.format(capsHeader[strDim], header[capsHeader[strDim]]))

            else:
                if irank == 1:
                    dimi = 0
                else:
                    dimi = 1
                shape.insert(0, dimi)

        return tuple(shape)

    @staticmethod
    def get_data_counts(shape=None):
        """
        Counts items specified by shape (returns 1 for shape==None)

        :param: tuple shape
        :return: int counts
        """
        if shape is None:
            shape = ()
        counts = 1
        for ishape in range(0, len(shape)):
            counts *= shape[ishape]

        return counts

    def _compute_capsheader(self):
        """
        Returns the mapping from capitalized keys of the header to the original
        keys.

        :rtype: dict
        """
        capsHeader = {}
        for key in self.header:
            upperkey = key.upper()
            if upperkey not in capsHeader:
                capsHeader[upperkey] = key

        return capsHeader

    def _extract_header_metadata(self, capsHeader=None):
        """Extract from the header metadata expected to read the data.

        Store them in this frame.

        For reading binary data from an external file self.bfname, self.bfsize
        and self.bfstart are updated with the values of the header values
        EDF_BinaryFileName, EDF_BinaryFileSize and EDF_BinaryFilePosition.
        All EDF_ keys are case sensitive. The external file must be different
        from the actual file!

        If bfname is set _unpack(self) will read the binary data from the file bfname
        instead of reading it from the binary blob of the current frame.

        EDF_BinaryFileName sets bfname (if not set, use the binary blob),
        EDF_BinaryFileSize sets bfsize (default shape*bpp, i.e. read as much as needed),
        EDF_BinaryFilePosition sets bfstart (default 0, i.e. read from the start of the file)

        The binary file is searched in the same folder as the edf input file.
        Only the basename without path is used. A path cannot be specified.
        It is automatically removed.

        Attention: The length of the binary file name string in the header
        is not explicitly restricted and could therefore exceed the first 512 bytes
        of a header, where the keywords EDF_DataBlockID | EDF_DataFormatVersion,
        EDF_BinarySize and EDF_HeaderSize are expected.

        The keywords EDF_BinaryFileName, EDF_BinaryFileSize, EDF_BinaryFilePosition
        musst always be written AFTER these keywords.  Therefore, bfname, bfsize
        and bfstart can only be updated when the full header has been read.

        The parameters EDF_BinaryFilePosition and EDF_BinaryFileSize specify the
        file called EDF_BinaryFileName as it is, eventually with an internally applied
        compression (keyword Compression). If the file is externally compressed, i.e.
        if a compression suffix is appended to bfname, e.g. .gz, .bz etc. it will first
        be decompressed to bfname before using bfstart and bfsize.

        :param dict capsHeader: Precached mapping from capitalized keys of the
            header to the original keys.
        """
        calcsize = 1
        shape = []
        if capsHeader is None:
            capsHeader = self._compute_capsheader()
        if 'SIZE' in capsHeader:
            try:
                self.blobsize = nice_int(self.header[capsHeader['SIZE']])
            except ValueError:
                logger.warning('Unable to convert to integer : %s %s ' % (capsHeader['SIZE'], self.header[capsHeader['SIZE']]))

            rank = self.get_data_rank(self.header, capsHeader)
            shape = self.get_data_shape(rank, self.header, capsHeader)
            counts = self.get_data_counts(shape)
            self._shape = shape
            if self._dtype is None:
                if 'DATATYPE' in capsHeader:
                    bytecode = DATA_TYPES[self.header[capsHeader['DATATYPE']]]
                else:
                    bytecode = numpy.uint16
                    logger.warning('Defaulting type to uint16')
                self._dtype = numpy.dtype(bytecode)
            if 'COMPRESSION' in capsHeader:
                self._data_compression = self.header[capsHeader['COMPRESSION']].upper()
                if self._data_compression == 'NONE':
                    self._data_compression = None
                elif self._data_compression.startswith('NO'):
                    self._data_compression = None
            else:
                self._data_compression = None
            bpp = self._dtype.itemsize
            calcsize = counts * bpp
            if self.blobsize is None and self._data_compression is None:
                self.blobsize = calcsize
            infile = self.file.name
            dirname = os.path.dirname(infile)
            if 'EDF_BinaryFileName' in self.header:
                self.bfname = os.path.basename(self.header['EDF_BinaryFileName'])
                if dirname != '':
                    self.bfname = dirname + '/' + self.bfname
            else:
                self.bfname = None
            if 'EDF_BinaryFilePosition' in self.header:
                self.bfstart = int(self.header['EDF_BinaryFilePosition'])
            else:
                self.bfstart = 0
            if 'EDF_BinaryFileSize' in self.header:
                self.bfsize = int(self.header['EDF_BinaryFileSize'])
        else:
            self.bfsize = calcsize
        if self._data_compression is None:
            if self.bfname is None and self.blobsize < calcsize:
                logger.warning('Malformed file: The physical size of the binary block {} is too small {}. This and the following frames could be broken.'.format(self.blobsize, calcsize))
        else:
            if self.bfsize < calcsize:
                logger.warning('The size available in the binary file {} is smaller than required {}.'.format(self.bfsize, calcsize))
            if self.size is None:
                self.size = calcsize
            byte_order = self.header[capsHeader['BYTEORDER']]
            if 'Low' in byte_order and numpy.little_endian or 'High' in byte_order and not numpy.little_endian:
                self._data_swap_needed = False
            if 'High' in byte_order and numpy.little_endian or 'Low' in byte_order and not numpy.little_endian:
                if bpp in (2, 4, 8):
                    self._data_swap_needed = True
            else:
                self._data_swap_needed = False

    def _create_header(self, inputheader, defaultheader=None):
        """
        Create self.header as an ordered dictionary and initialize it
        with the inputheader. Copy all key-value pairs of defaultheader
        to self.header that are missing in the inputheader and that are
        not starting with EDF_, nor with the reserved keys "SIZE", "IMAGE",
        "HEADERID".

        :param OrderedDict inputheader: the input header
        :param dict defaultheader: header values to include as default
        :return: dict capsHeader
        """
        self.header = OrderedDict()
        capsHeader = {}
        self.header = inputheader
        if defaultheader is not None:
            for key in defaultheader:
                if key[0:4] != 'EDF_' and key.upper() not in ('SIZE', 'IMAGE', 'HEADERID') and key not in self.header:
                    self.header[key] = defaultheader[key]

        for key in self.header:
            capsHeader[key.upper()] = key

        return capsHeader

    def _check_header_mandatory_keys(self, filename=''):
        """Check that frame header contains all mandatory keys

        :param str filename: Name of the EDF file
        :rtype: bool
        """
        capsKeys = set([k.upper() for k in self.header.keys()])
        missing = list(MINIMUM_KEYS2 - capsKeys)
        if len(missing) > 0:
            missing = list(MINIMUM_KEYS - capsKeys)
        if len(missing) > 0:
            msg = 'EDF file {}{} misses mandatory keys: {} '
            if self.index is not None:
                frame = ' (frame {:d})'.format(self.index)
            else:
                frame = ''
            logger.info(msg.format(filename, frame, ' '.join(missing)))
        return len(missing) == 0

    def swap_needed(self):
        """
        Decide if we need to byteswap
        """
        return self._data_swap_needed

    def _unpack(self):
        """
        Unpack a binary blob according to the specification given in the header
        If self.bfname is set unpack it from an external file.

        :return: dataset as numpy.ndarray
        """
        data = None
        if self._data is not None:
            data = self._data
        else:
            if self.file is None:
                data = self._data
            else:
                if self._dtype is None:
                    assert False
                shape = self.shape
                if self.bfname is None:
                    with self.file.lock:
                        if self.file.closed:
                            logger.error('file: %s from %s is closed. Cannot read data.' % (self.file, self.file.name))
                            return
                        self.file.seek(self.start)
                        try:
                            fileData = self.file.read(self.blobsize)
                        except Exception as e:
                            if isinstance(self.file, fabioutils.GzipFile) and compression_module.is_incomplete_gz_block_exception(e):
                                return numpy.zeros(shape)
                            raise e

        if os.path.exists(self.bfname):
            with open(self.bfname, 'rb') as (f):
                f.seek(self.bfstart)
                fileData = f.read(self.bfsize)
        else:
            if os.path.exists(self.bfname + '.gz'):
                import gzip
                with gzip.open(self.bfname + '.gz', 'rb') as (f):
                    f.seek(self.bfstart)
                    fileData = f.read(self.bfsize)
            else:
                raise IOError('The binary file {} of {} does not exist'.format(self.bfname, self.file.name))
            if self._data_compression is not None:
                compression = self._data_compression
                uncompressed_size = self._dtype.itemsize
                for i in shape:
                    uncompressed_size *= i

                if 'OFFSET' in compression:
                    try:
                        import byte_offset
                    except ImportError as error:
                        logger.error('Unimplemented compression scheme:  %s (%s)' % (compression, error))
                    else:
                        myData = byte_offset.analyseCython(fileData, size=uncompressed_size)
                        rawData = myData.astype(self._dtype).tobytes()
                        self.size = uncompressed_size
                else:
                    if compression == 'NONE':
                        rawData = fileData
                    else:
                        if 'GZIP' in compression:
                            rawData = decGzip(fileData)
                            self.size = uncompressed_size
                        else:
                            if 'BZ' in compression:
                                rawData = decBzip2(fileData)
                                self.size = uncompressed_size
                            else:
                                if 'Z' in compression:
                                    rawData = decZlib(fileData)
                                    self.size = uncompressed_size
                                else:
                                    logger.warning('Unknown compression scheme %s' % compression)
                                    rawData = fileData
            else:
                rawData = fileData
            expected = self.size
            obtained = len(rawData)
            if expected > obtained:
                logger.error('Data stream is incomplete: %s < expected %s bytes' % (obtained, expected))
                rawData += b'\x00' * (expected - obtained)
            else:
                if expected < obtained:
                    logger.info('Data stream is padded : %s > required %s bytes' % (obtained, expected))
                    rawData = rawData[:expected]
                count = self.size // self._dtype.itemsize
                data = numpy.frombuffer(rawData, self._dtype, count).copy().reshape(shape)
                if self.swap_needed():
                    data.byteswap(True)
                self._data = data
                self._dtype = None
            return data

    @property
    def data(self):
        """
        Returns the data after unpacking it if needed.

        :return: dataset as numpy.ndarray
        """
        return self._unpack()

    @data.setter
    def data(self, value):
        """Setter for data in edf frame"""
        self._data = value

    @deprecation.deprecated(reason="Prefer using 'frame.data'", deprecated_since='0.10.0beta')
    def getData(self):
        """
        Returns the data after unpacking it if needed.

        :return: dataset as numpy.ndarray
        """
        return self.data

    @deprecation.deprecated(reason="Prefer using 'frame.data ='", deprecated_since='0.10.0beta')
    def setData(self, npa=None):
        """Setter for data in edf frame"""
        self._data = npa

    def get_edf_block(self, force_type=None, fit2dMode=False):
        """
        :param force_type: type of the dataset to be enforced like "float64" or "uint16"
        :type force_type: string or numpy.dtype
        :param boolean fit2dMode: enforce compatibility with fit2d and starts counting number of images at 1
        :return: ascii header block + binary data block
        :rtype: python bytes with the concatenation of the ascii header and the binary data block
        """
        if force_type is not None:
            data = self.data.astype(force_type)
        else:
            data = self.data
        fit2dMode = bool(fit2dMode)
        capsHeader = {}
        for key in self.header:
            upperkey = key.upper()
            if upperkey not in capsHeader:
                capsHeader[upperkey] = key

        header = self.header.copy()
        header_keys = list(self.header.keys())
        listHeader = [
         '{\n']
        for i in capsHeader:
            if 'DIM_' in i:
                header.pop(capsHeader[i])
                header_keys.remove(capsHeader[i])

        for KEY in ['SIZE', 'EDF_BINARYSIZE', 'EDF_HEADERSIZE', 'BYTEORDER', 'DATATYPE', 'HEADERID', 'IMAGE']:
            if KEY in capsHeader:
                header.pop(capsHeader[KEY])
                header_keys.remove(capsHeader[KEY])

        if 'EDF_DATABLOCKID' in capsHeader:
            header_keys.remove(capsHeader['EDF_DATABLOCKID'])
            if capsHeader['EDF_DATABLOCKID'] != 'EDF_DataBlockID':
                header['EDF_DataBlockID'] = header.pop(capsHeader['EDF_DATABLOCKID'])
                capsHeader['EDF_DATABLOCKID'] = 'EDF_DataBlockID'
            header_keys.insert(0, 'Size')
            header['Size'] = data.nbytes
            header_keys.insert(0, 'HeaderID')
            header['HeaderID'] = 'EH:%06d:000000:000000' % (self.index + fit2dMode)
            header_keys.insert(0, 'Image')
            header['Image'] = str(self.index + fit2dMode)
            dims = list(data.shape)
            nbdim = len(dims)
            for i in dims:
                key = 'Dim_%i' % nbdim
                header[key] = i
                header_keys.insert(0, key)
                nbdim -= 1

            header_keys.insert(0, 'DataType')
            header['DataType'] = NUMPY_EDF_DTYPE[str(numpy.dtype(data.dtype))]
            header_keys.insert(0, 'ByteOrder')
            if numpy.little_endian:
                header['ByteOrder'] = 'LowByteFirst'
            else:
                header['ByteOrder'] = 'HighByteFirst'
            approxHeaderSize = 100
            for key in header:
                approxHeaderSize += 7 + len(key) + len(str(header[key]))

            approxHeaderSize = BLOCKSIZE * (approxHeaderSize // BLOCKSIZE + 1)
            header_keys.insert(0, 'EDF_HeaderSize')
            header['EDF_HeaderSize'] = '%5s' % approxHeaderSize
            header_keys.insert(0, 'EDF_BinarySize')
            header['EDF_BinarySize'] = data.nbytes
            header_keys.insert(0, 'EDF_DataBlockID')
            if 'EDF_DataBlockID' not in header:
                header['EDF_DataBlockID'] = '%i.Image.Psd' % (self.index + fit2dMode)
            preciseSize = 4
            for key in header_keys:
                strKey = str(key)
                if not isAscii(strKey, listExcluded=['}', '{']):
                    logger.warning('Non ascii key %s, skipping' % strKey)
                    continue
                    strValue = str(header[key])
                    if not isAscii(strValue, listExcluded=['}', '{']):
                        logger.warning('Non ascii value %s, skipping' % strValue)
                        continue
                        line = strKey + ' = ' + strValue + ' ;\n'
                        preciseSize += len(line)
                        listHeader.append(line)

            if preciseSize > approxHeaderSize:
                logger.error('I expected the header block only at %s in fact it is %s' % (approxHeaderSize, preciseSize))
                for idx, line in enumerate(listHeader[:]):
                    if line.startswith('EDF_HeaderSize'):
                        headerSize = BLOCKSIZE * (preciseSize // BLOCKSIZE + 1)
                        newline = 'EDF_HeaderSize = %5s ;\n' % headerSize
                        delta = len(newline) - len(line)
                        if preciseSize // BLOCKSIZE != (preciseSize + delta) // BLOCKSIZE:
                            headerSize = BLOCKSIZE * ((preciseSize + delta) // BLOCKSIZE + 1)
                            newline = 'EDF_HeaderSize = %5s ;\n' % headerSize
                        preciseSize = preciseSize + delta
                        listHeader[idx] = newline
                        break

        else:
            headerSize = approxHeaderSize
        listHeader.append(' ' * (headerSize - preciseSize) + '}\n')
        return ''.join(listHeader).encode('ASCII') + data.tobytes()

    @deprecation.deprecated(reason="Prefer using 'getEdfBlock'", deprecated_since='0.10.0beta')
    def getEdfBlock(self, force_type=None, fit2dMode=False):
        return self.get_edf_block(force_type, fit2dMode)

    @property
    @deprecation.deprecated(reason="Prefer using 'index'", deprecated_since='0.10.0beta')
    def iFrame(self):
        """Returns the frame index of this frame"""
        return self._index


class EdfImage(fabioimage.FabioImage):
    __doc__ = ' Read and try to write the ESRF edf data format '
    DESCRIPTION = 'European Synchrotron Radiation Facility data format'
    DEFAULT_EXTENSIONS = [
     'edf', 'cor']
    RESERVED_HEADER_KEYS = [
     'HEADERID', 'IMAGE', 'BYTEORDER', 'DATATYPE',
     'DIM_1', 'DIM_2', 'DIM_3', 'SIZE']

    def __init__(self, data=None, header=None, frames=None, generalframe=None):
        self.currentframe = 0
        self.filesize = None
        self._incomplete_file = False
        if data is None:
            stored_data = None
        else:
            try:
                dim = len(data.shape)
            except Exception as error:
                logger.debug("Data don't look like a numpy array (%s), resetting all!!" % error)
                dim = 0

            if dim == 0:
                raise Exception('Data with empty shape is unsupported')
            else:
                if dim == 1:
                    logger.warning('Data in 1d dimension will be stored as a 2d dimension array')
                    stored_data = numpy.array(data, copy=False)
                    stored_data.shape = (1, len(data))
                else:
                    if dim == 2:
                        stored_data = data
                    elif dim >= 3:
                        raise Exception('Data dimension too big. Only 1d or 2d arrays are supported.')
            fabioimage.FabioImage.__init__(self, stored_data, header)
            if frames is None:
                frame = EdfFrame(data=self.data, header=self.header)
                self._frames = [frame]
            else:
                self._frames = frames
        self.generalframe = generalframe

    def _get_frame(self, num):
        if self._frames is None:
            return IndexError('No frames available')
        frame = self._frames[num]
        frame._set_container(self, num)
        frame._set_file_container(self, num)
        return frame

    @staticmethod
    def check_header(header=None):
        """
        Empty for FabioImage but may be populated by other classes
        """
        if not isinstance(header, dict):
            return OrderedDict()
        new = OrderedDict()
        for key, value in header.items():
            new[toAscii(key, ';{}')] = toAscii(value, ';{}')

        return new

    @staticmethod
    def _read_header_block(infile, frame_id):
        """
        Reads the header block of the EDF frame frame_id as an
        ASCII string and returns the found key-value pairs in
        the OrderedDict header.

        The header block string is split at each semicolon in
        lines. These lines are split at the first equal sign
        in key-value pairs and then added to the header in the
        order of appearance.

        The results are returned in the named tuple HeaderBlockType.

        Attention, it must be absolutely prevented that header values
        contain semicolons. In that case the value would be split
        there instead at the end of the actual line. The result of
        the operation on the rest of the file would be unpredictable.
        Values must be cleaned from semicolons before writing
        them actually to edf files.

        edf-format specification keys starting with EDF_ are
        expected at the beginning of the block. They must not
        be preceded by standard header values, i.e. without EDF_.
        EDF_ keys are case sensitive.

        Only the keyword EDF_HeaderSize is directly read from the
        file. All other edf-specification keys are read from the
        header dictionary.

        :param fileid infile: file object open in read mode
        :param int frame_id: frame ID number
               This parameter is only used as debugging output. In all
               cases the header is read from the current position of the
               infile pointer, independent of the given frame_id.
        :return namedtuple("HeaderBlockType", "header, header_size, binary_size, data_format_version")
                in case of an error all return values are None
        :raises MalformedHeaderError: If the header can't be read
        """
        data_format_version = None
        header_block = None
        header_size = None
        binary_size = None
        MAX_HEADER_SIZE = BLOCKSIZE * MAX_BLOCKS
        try:
            block = infile.read(BLOCKSIZE)
        except Exception as e:
            if isinstance(infile, fabioutils.GzipFile) and compression_module.is_incomplete_gz_block_exception(e):
                raise MalformedHeaderError('Incomplete GZ block for header frame %i', frame_id)
            raise e

        if len(block) == 0:
            return HeaderBlockType(None, None, None, None)
        begin_block = block.find(b'{')
        if begin_block < 0:
            if len(block) < BLOCKSIZE and len(block.strip()) == 0:
                return HeaderBlockType(None, None, None, None)
            logger.debug('Malformed header: %s', block)
            raise MalformedHeaderError("Header frame %i does not contain '{'" % frame_id)
        start = block[0:begin_block]
        if start.strip() != b'':
            logger.debug('Malformed header: %s', start)
            raise MalformedHeaderError("Header frame %i contains non-whitespace before '{'" % frame_id)
        begin_block = begin_block + 1
        start = block.find(b'EDF_HeaderSize', begin_block)
        if start >= 0:
            end_pattern = re.compile(b'}(\r{0,1})\n')
            end = end_pattern.search(block)
            if end is not None and start < end.start():
                pass
            equal = block.index(b'=', start + len(b'EDF_HeaderSize'))
            end = block.index(b';', equal + 1)
            try:
                chunk = block[equal + 1:end].strip()
                max_header_size = int(chunk)
            except Exception:
                logger.warning('Unable to read header size, got: %s', chunk)
            else:
                if max_header_size > MAX_HEADER_SIZE:
                    logger.info('Redefining MAX_HEADER_SIZE to %s', max_header_size)
                    MAX_HEADER_SIZE = max_header_size
        block_size = len(block)
        blocks = [block]
        end_pattern = re.compile(b'}(\r{0,1})\n')
        while 1:
            end = end_pattern.search(block)
            if end is not None:
                end_block = block_size - len(block) + end.start()
                start_blob = block_size - len(block) + end.end()
                offset = start_blob - block_size
                break
            nextblock = infile.read(BLOCKSIZE)
            if block[-1:] == b'}':
                if nextblock[:1] == b'\n':
                    end_block = block_size
                    start_blob = block_size + 1
                    offset = start_blob - block_size - len(nextblock)
                    break
                elif nextblock[:2] == b'\r\n':
                    end_block = block_size
                    start_blob = block_size + 2
                    offset = start_blob - block_size - len(nextblock)
                    break
            elif block[-2:] == b'}\r' and nextblock[:1] == b'\n':
                end_block = block_size - 1
                start_blob = block_size + 1
                offset = start_blob - block_size - len(nextblock)
                break
            block = nextblock
            block_size += len(block)
            blocks.append(block)
            if len(block) == 0 or block_size > MAX_HEADER_SIZE:
                block = (b'').join(blocks)
                logger.debug('Runaway header in EDF file MAX_HEADER_SIZE: %s\n%s', MAX_HEADER_SIZE, block)
                raise MalformedHeaderError('Runaway header frame %i (max size: %i)' % (frame_id, MAX_HEADER_SIZE))

        block = (b'').join(blocks)
        infile.seek(offset, os.SEEK_CUR)
        header_block = block[begin_block:end_block].decode('ASCII')
        header = OrderedDict()
        whitespace = string.whitespace + '\x00'
        for line in header_block.split(';'):
            if '=' in line:
                key, val = line.split('=', 1)
                key = key.strip(whitespace)
                header[key] = val.strip(whitespace)

        if 'EDF_DataFormatVersion' in header:
            data_format_version = header['EDF_DataFormatVersion']
        if 'EDF_BinarySize' in header:
            try:
                binary_size = int(header['EDF_BinarySize'])
            except Exception:
                logger.warning('Unable to read binary size, got: %s', header['EDF_BinarySize'])
                binary_size = None

        if header_size is None:
            header_size = block_size
        if binary_size is None:
            if data_format_version is not None:
                binary_size = 0
        return HeaderBlockType(header, header_size, binary_size, data_format_version)

    @property
    def incomplete_file(self):
        """Returns true if the file is not complete.

        :rtype: bool
        """
        return self._incomplete_file

    def _readheader(self, infile):
        """
        Read all headers in a file and populate self.header
        data is not yet populated
        :type infile: file object open in read mode
        """
        self._frames = []
        self.generalframe = None
        while 1:
            try:
                value = self._read_header_block(infile, len(self._frames))
            except MalformedHeaderError:
                logger.debug('Backtrace', exc_info=True)
                if len(self._frames) == 0:
                    raise IOError('Invalid first header')
                self._incomplete_file = True
                break

            if value.header is None:
                if len(self._frames) == 0:
                    raise IOError('Empty file')
                break
            if value.data_format_version is None:
                is_general_header = False
            else:
                is_general_header = True
            frame = EdfFrame()
            frame.file = infile
            frame._index = len(self._frames)
            defaultheader = None
            if not is_general_header:
                if self.generalframe is not None:
                    defaultheader = self.generalframe._header
                capsHeader = frame._create_header(value.header, defaultheader)
                if value.binary_size is None:
                    if 'SIZE' in capsHeader:
                        try:
                            frame.blobsize = nice_int(frame.header[capsHeader['SIZE']])
                        except ValueError:
                            logger.warning('Unable to convert to integer : %s %s ' % (capsHeader['SIZE'], frame.header[capsHeader['SIZE']]))

                else:
                    frame.blobsize = value.binary_size
                frame.start = infile.tell()
                if not is_general_header:
                    frame._extract_header_metadata(capsHeader)
                if is_general_header:
                    if self.generalframe is not None:
                        logger.warning('_readheader: Overwriting an existing general frame (file={},frame={}).'.format(frame.file, frame._index))
                    self.generalframe = frame
                else:
                    self._frames += [frame]
                if not is_general_header:
                    frame._check_header_mandatory_keys(filename=self.filename)
                try:
                    infile.seek(frame.blobsize - 1, os.SEEK_CUR)
                    data = infile.read(1)
                    if len(data) == 0:
                        pass
                    self._incomplete_file = True
                    frame.incomplete_data = True
                    break
                except Exception as error:
                    if isinstance(infile, fabioutils.GzipFile) and compression_module.is_incomplete_gz_block_exception(error):
                        self._incomplete_file = True
                        frame.incomplete_data = True
                        break
                    logger.warning('infile is %s' % infile)
                    logger.warning('position is %s' % infile.tell())
                    logger.warning('blobsize is %s' % frame.blobsize)
                    logger.error('It seams this error occurs under windows when reading a (large-) file over network: %s ', error)
                    raise Exception(error)

        self.currentframe = 0

    def read(self, fname, frame=None):
        """
        Read in header into self.header and
            the data   into self.data
        """
        self.resetvals()
        self.filename = fname
        infile = self._open(fname, 'rb')
        try:
            self._readheader(infile)
            if frame is None:
                pass
            else:
                if frame < self.nframes:
                    self = self.getframe(frame)
                else:
                    logger.error('Reading file %s You requested frame %s but only %s frames are available', fname, frame, self.nframes)
                self.resetvals()
        except Exception as e:
            infile.close()
            raise e

        return self

    def swap_needed(self):
        """
        Decide if we need to byteswap

        :return: True if needed, False else and None if not understood
        """
        return self._frames[self.currentframe].swap_needed()

    def unpack(self):
        """
        Unpack a binary blob according to the specification given in the header and return the dataset

        :return: dataset as numpy.ndarray
        """
        return self._frames[self.currentframe].getData()

    def getframe(self, num):
        """ returns the file numbered 'num' in the series as a FabioImage """
        newImage = None
        if self.nframes == 1:
            logger.debug('Single frame EDF; having FabioImage default behavior: %s' % num)
            newImage = fabioimage.FabioImage.getframe(self, num)
            newImage._file = self._file
        else:
            if num < self.nframes:
                logger.debug('Multi frame EDF; having EdfImage specific behavior frame %s: 0<=frame<%s' % (
                 num, self.nframes))
                newImage = self.__class__(frames=self._frames)
                newImage.currentframe = num
                newImage.filename = self.filename
                newImage._file = self._file
            else:
                raise IOError('EdfImage.getframe: Cannot access frame %s: 0<=frame<%s' % (
                 num, self.nframes))
        return newImage

    def previous(self):
        """ returns the previous file in the series as a FabioImage """
        newImage = None
        if self.nframes == 1:
            newImage = fabioimage.FabioImage.previous(self)
        else:
            newFrameId = self.currentframe - 1
            newImage = self.getframe(newFrameId)
        return newImage

    def next(self):
        """Returns the next file in the series as a fabioimage

        :raise IOError: When there is no next file or image in the series.
        """
        newImage = None
        if self.nframes == 1:
            newImage = fabioimage.FabioImage.next(self)
        else:
            newFrameId = self.currentframe + 1
            newImage = self.getframe(newFrameId)
        return newImage

    def write(self, fname, force_type=None, fit2dMode=False):
        """
        Try to write a file
        check we can write zipped also
        mimics that fabian was writing uint16 (we sometimes want floats)

        :param force_type: can be numpy.uint16 or simply "float"
        """
        if fname == self.filename:
            [(frame.header, frame.data) for frame in self._frames]
        with self._open(fname, mode='wb') as (outfile):
            for i, frame in enumerate(self._frames):
                frame._set_container(self, i)
                outfile.write(frame.get_edf_block(force_type=force_type, fit2dMode=fit2dMode))

    def append_frame(self, frame=None, data=None, header=None):
        """
        Method used add a frame to an EDF file
        :param frame: frame to append to edf image
        :type frame: instance of Frame
        """
        if isinstance(frame, EdfFrame):
            self._frames.append(frame)
        else:
            if hasattr(frame, 'header') and hasattr(frame, 'data'):
                self._frames.append(EdfFrame(frame.data, frame.header))
            else:
                self._frames.append(EdfFrame(data, header))

    @deprecation.deprecated(reason="Prefer using 'append_frame'", deprecated_since='0.10.0beta')
    def appendFrame(self, frame=None, data=None, header=None):
        self.append_frame(frame, data, header)

    def delete_frame(self, frameNb=None):
        """
        Method used to remove a frame from an EDF image. by default the last one is removed.
        :param int frameNb: frame number to remove, by  default the last.
        """
        if frameNb is None:
            self._frames.pop()
        else:
            self._frames.pop(frameNb)

    @deprecation.deprecated(reason="Prefer using 'delete_frame'", deprecated_since='0.10.0beta')
    def deleteFrame(self, frameNb=None):
        self.delete_frame(frameNb)

    def fast_read_data(self, filename=None):
        """
        This is a special method that will read and return the data from another file ...
        The aim is performances, ... but only supports uncompressed files.

        :return: data from another file using positions from current EdfImage
        """
        if filename is None or not os.path.isfile(filename):
            raise RuntimeError('EdfImage.fast_read_data is only valid with another file: %s does not exist' % filename)
        data = None
        frame = self._frames[self.currentframe]
        with open(filename, 'rb') as (f):
            f.seek(frame.start)
            raw = f.read(frame.blobsize)
        try:
            data = numpy.frombuffer(raw, dtype=self.bytecode).copy()
            data.shape = self.data.shape
        except Exception as error:
            logger.error('unable to convert file content to numpy array: %s', error)

        if frame.swap_needed():
            data.byteswap(True)
        return data

    @deprecation.deprecated(reason="Prefer using 'fastReadData'", deprecated_since='0.10.0beta')
    def fastReadData(self, filename):
        return self.fast_read_data(filename)

    def fast_read_roi(self, filename, coords=None):
        """
        Method reading Region of Interest of another file  based on metadata available in current EdfImage.
        The aim is performances, ... but only supports uncompressed files.

        :return: ROI-data from another file using positions from current EdfImage
        :rtype: numpy 2darray
        """
        if filename is None or not os.path.isfile(filename):
            raise RuntimeError('EdfImage.fast_read_roi is only valid with another file: %s does not exist' % filename)
        data = None
        frame = self._frames[self.currentframe]
        if len(coords) == 4:
            slice1 = self.make_slice(coords)
        else:
            if len(coords) == 2 and isinstance(coords[0], slice) and isinstance(coords[1], slice):
                slice1 = coords
            else:
                logger.warning('readROI: Unable to understand Region Of Interest: got %s', coords)
                return
        d1 = self.data.shape[(-1)]
        start0 = slice1[0].start
        start1 = slice1[1].start
        slice2 = (slice(0, slice1[0].stop - start0, slice1[0].step),
         slice(0, slice1[1].stop - start1, slice1[1].step))
        start = frame.start + self.bpp * (d1 * start0 + start1)
        size = self.bpp * (slice2[0].stop * d1)
        with open(filename, 'rb') as (f):
            f.seek(start)
            raw = f.read(size)
        try:
            data = numpy.frombuffer(raw, dtype=self.bytecode).copy()
            data.shape = (-1, d1)
        except Exception as error:
            logger.error('unable to convert file content to numpy array: %s', error)

        if frame.swap_needed():
            data.byteswap(True)
        return data[slice2]

    @deprecation.deprecated(reason="Prefer using 'fast_read_roi'", deprecated_since='0.10.0beta')
    def fastReadROI(self, filename, coords=None):
        return self.fast_read_roi(filename, coords)

    def _get_any_frame(self):
        """Returns the current if available, else create and return a new empty
        frame."""
        try:
            return self._frames[self.currentframe]
        except AttributeError:
            frame = EdfFrame()
            self._frames = [frame]
            return frame
        except IndexError:
            if self.currentframe < len(self._frames):
                frame = EdfFrame()
                self._frames.append(frame)
                return frame
            raise

    @property
    def nframes(self):
        """Returns the number of frames contained in this file

        :rtype: int
        """
        return len(self._frames)

    @deprecation.deprecated(reason="Prefer using 'img.nframes'", deprecated_since='0.10.0beta')
    def getNbFrames(self):
        """
        Getter for number of frames
        """
        return len(self._frames)

    @deprecation.deprecated(reason="This call to 'setNbFrames' does nothing and should be removed", deprecated_since='0.10.0beta')
    def setNbFrames(self, val):
        """
        Setter for number of frames ... should do nothing. Here just to avoid bugs
        """
        if val != len(self._frames):
            logger.warning('Setting the number of frames is not allowed.')

    @property
    def header(self):
        frame = self._get_any_frame()
        return frame.header

    @header.setter
    def header(self, value):
        frame = self._get_any_frame()
        frame.header = value

    @header.deleter
    def header(self):
        frame = self._get_any_frame()
        frame.header = None

    @deprecation.deprecated(reason="Prefer using 'img.header'", deprecated_since='0.10.0beta')
    def getHeader(self):
        """
        Getter for the headers. used by the property header,
        """
        return self._frames[self.currentframe].header

    @deprecation.deprecated(reason="Prefer using 'img.header ='", deprecated_since='0.10.0beta')
    def setHeader(self, _dictHeader):
        """
        Enforces the propagation of the header to the list of frames
        """
        frame = self._get_any_frame()
        frame.header = _dictHeader

    @deprecation.deprecated(reason="Prefer using 'del img.header'", deprecated_since='0.10.0beta')
    def delHeader(self):
        """
        Deleter for edf header
        """
        self._frames[self.currentframe].header = {}

    @property
    def shape(self):
        frame = self._get_any_frame()
        return frame.shape

    @property
    def dtype(self):
        frame = self._get_any_frame()
        return frame.dtype

    @property
    def data(self):
        frame = self._get_any_frame()
        return frame.data

    @data.setter
    def data(self, value):
        frame = self._get_any_frame()
        frame.data = value

    @data.deleter
    def data(self):
        frame = self._get_any_frame()
        frame.data = None

    @deprecation.deprecated(reason="Prefer using 'img.data'", deprecated_since='0.10.0beta')
    def getData(self):
        """
        getter for edf Data
        :return: data for current frame
        :rtype: numpy.ndarray
        """
        return self.data

    @deprecation.deprecated(reason="Prefer using 'img.data ='", deprecated_since='0.10.0beta')
    def setData(self, _data=None):
        """
        Enforces the propagation of the data to the list of frames
        :param data: numpy array representing data
        """
        frame = self._get_any_frame()
        frame.data = _data

    @deprecation.deprecated(reason="Prefer using 'del img.data'", deprecated_since='0.10.0beta')
    def delData(self):
        """
        deleter for edf Data
        """
        self._frames[self.currentframe].data = None

    @deprecation.deprecated(reason="Prefer using 'dim1'", deprecated_since='0.10.0beta')
    def getDim1(self):
        return self.dim1

    @deprecation.deprecated(reason='Setting dim1 is not anymore allowed. If the data is not set use shape instead.', deprecated_since='0.10.0beta')
    def setDim1(self, _iVal=None):
        frame = self._get_any_frame()
        frame.dim1 = _iVal

    @property
    def dim1(self):
        return self._frames[self.currentframe].dim1

    @deprecation.deprecated(reason="Prefer using 'dim2'", deprecated_since='0.10.0beta')
    def getDim2(self):
        return self._frames[self.currentframe].dim2

    @deprecation.deprecated(reason='Setting dim2 is not anymore allowed. If the data is not set use shape instead.', deprecated_since='0.10.0beta')
    def setDim2(self, _iVal=None):
        frame = self._get_any_frame()
        frame.dim2 = _iVal

    @property
    def dim2(self):
        return self._frames[self.currentframe].dim2

    @deprecation.deprecated(reason="Prefer using 'dims'", deprecated_since='0.10.0beta')
    def getDims(self):
        return self._frames[self.currentframe].dims

    @property
    def dims(self):
        return self._frames[self.currentframe].dims

    @deprecation.deprecated(reason="Prefer using 'bytecode'", deprecated_since='0.10.0beta')
    def getByteCode(self):
        return self.bytecode

    @deprecation.deprecated(reason='Setting bytecode is not anymore allowed. If the data is not set use dtype instead.', deprecated_since='0.10.0beta')
    def setByteCode(self, iVal=None, _iVal=None):
        raise NotImplementedError('No more implemented')

    @property
    def bytecode(self):
        return self._frames[self.currentframe].bytecode

    @deprecation.deprecated(reason="Prefer using 'bpp'", deprecated_since='0.10.0beta')
    def getBpp(self):
        return self._frames[self.currentframe].bpp

    @deprecation.deprecated(reason='Setting bpp is not anymore allowed. If the data is not set use dtype instead.', deprecated_since='0.10.0beta')
    def setBpp(self, iVal=None, _iVal=None):
        raise NotImplementedError('No more implemented')

    @property
    def bpp(self):
        return self._frames[self.currentframe].bpp

    @deprecation.deprecated(reason="Prefer using 'incomplete_data'", deprecated_since='0.10.0beta')
    def isIncompleteData(self):
        return self.incomplete_data

    @property
    def incomplete_data(self):
        return self._frames[self.currentframe].incomplete_data

    @classmethod
    def lazy_iterator(cls, filename):
        """Iterates over the frames of an EDF multi-frame file.

        This function optimizes sequential access to multi-frame EDF files
        by avoiding to read the whole file at first in order to get the number
        of frames and build an index of frames for faster random access.

        Usage:

        >>> from fabio.edfimage import EdfImage

        >>> for frame in EdfImage.lazy_iterator("multiframe.edf"):
        ...     print('Header:', frame.header)
        ...     print('Data:', frame.data)

        :param str filename: File name of the EDF file to read
        :yield: frames one after the other
        """
        edf = cls()
        infile = edf._open(filename, 'rb')
        index = 0
        while 1:
            try:
                value = cls._read_header_block(infile, index)
            except MalformedHeaderError:
                logger.debug('Backtrace', exc_info=True)
                if index == 0:
                    infile.close()
                    raise IOError('Invalid first header')
                break

            if value.header is None:
                if index == 0:
                    infile.close()
                    raise IOError('Empty file')
                break
            if value.data_format_version is None:
                is_general_header = False
            else:
                is_general_header = True
            frame = EdfFrame()
            frame.file = infile
            frame._set_container(edf, index)
            frame._set_file_container(edf, index)
            defaultheader = None
            if not is_general_header:
                if edf.generalframe is not None:
                    defaultheader = edf.generalframe._header
                capsHeader = frame._create_header(value.header, defaultheader)
                if value.binary_size is None:
                    if 'SIZE' in capsHeader:
                        try:
                            blobsize = nice_int(frame.header[capsHeader['SIZE']])
                        except ValueError:
                            logger.warning('Unable to convert to integer : %s %s ' % (capsHeader['SIZE'], frame.header[capsHeader['SIZE']]))

                else:
                    blobsize = value.binary_size
                if not is_general_header:
                    frame._extract_header_metadata(capsHeader)
                frame.start = infile.tell()
                frame.blobsize = blobsize
                if not is_general_header:
                    try:
                        frame._unpack()
                    except Exception as error:
                        if isinstance(infile, fabioutils.GzipFile) and compression_module.is_incomplete_gz_block_exception(error):
                            frame.incomplete_data = True
                            break
                        logger.warning('infile is %s' % infile)
                        logger.warning('position is %s' % infile.tell())
                        logger.warning('blobsize is %s' % blobsize)
                        logger.error('It seams this error occurs under windows when reading a (large-) file over network: %s ', error)
                        infile.close()
                        raise Exception(error)

                    frame._check_header_mandatory_keys(filename=filename)
                    yield frame
                    index += 1
                else:
                    edf.generalframe = frame
                    if frame.blobsize > 0:
                        blobend = frame.start + frame.blobsize
                        frame.file.seek(blobend)

        infile.close()


Frame = EdfFrame
edfimage = EdfImage