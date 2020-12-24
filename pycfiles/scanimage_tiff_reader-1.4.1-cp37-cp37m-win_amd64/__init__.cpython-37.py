# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\src\VIDRIO\TIFF\scanimagetiffreader-python\src\ScanImageTiffReader\__init__.py
# Compiled at: 2019-02-13 10:54:49
# Size of source mod 2**32: 13401 bytes
"""
The ScanImageTiffReader object represents an opened file. It
is used for extracting the image stack
into a numpy array, extracting the image description from individual frames, or
for accessing other ScanImage specific metadata stored in the file.

Example:

    >>> reader=ScanImageTiffReader("data/TR_003.tif")
    >>> stack=reader.data()
    >>> reader.close()

The reader supports python's with syntax:

    >>> import ScanImageTiffReader
    >>> with ScanImageTiffReader.ScanImageTiffReader('data/TR_003.tif') as reader:
    ...     print(reader.shape())
    [10, 512, 512]

In numpy dimensions are ordered like: ``[z,y,x]``.

The API version used by the library can be queried by
running:

    >>> print(ScanImageTiffReader.api_version()) #doctest: +ELLIPSIS
    Version ...
"""
__version__ = '1.4.1'
__author__ = 'Nathan Clack <nathan@vidriotech.com>'
__copyright__ = 'Copyright (C) 2016 Vidrio Technologies'
__license__ = '\nCopyright 2016 Vidrio Technologies, LLC\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n  http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
from ctypes import *
from numpy import dtype, empty

def loadapi():
    from . import external
    return CDLL(external.resource_path())


_api_lib = loadapi()

class ScanImageTiffReaderContext(Structure):
    _fields_ = [
     (
      'handle', c_void_p),
     (
      'log', c_char_p)]


class Shape(Structure):
    _fields_ = [
     (
      'ndim', c_uint32),
     (
      'type', c_uint32),
     (
      'strides', c_int64 * 11),
     (
      'dims', c_uint64 * 10)]


_typemap_ = {0:dtype('u1'), 
 1:dtype('u2'), 
 2:dtype('u4'), 
 3:dtype('u8'), 
 4:dtype('i1'), 
 5:dtype('i2'), 
 6:dtype('i4'), 
 7:dtype('i8'), 
 8:dtype('f4'), 
 9:dtype('f8')}

class API:
    pass


_api = API()
_api.open = _api_lib.ScanImageTiffReader_Open
_api.open.restype = ScanImageTiffReaderContext
_api.open.argtypes = [POINTER(c_char)]
_api.close = _api_lib.ScanImageTiffReader_Close
_api.close.restype = None
_api.close.argtypes = [POINTER(ScanImageTiffReaderContext)]
_api.shape = _api_lib.ScanImageTiffReader_GetShape
_api.shape.restype = Shape
_api.shape.argtypes = [POINTER(ScanImageTiffReaderContext)]
_api.data = _api_lib.ScanImageTiffReader_GetData
_api.data.restype = c_int
_api.data.argtypes = [POINTER(ScanImageTiffReaderContext), c_void_p, c_size_t]
_api.countof_descriptions = _api_lib.ScanImageTiffReader_GetImageDescriptionCount
_api.countof_descriptions.restype = c_int
_api.countof_descriptions.argtypes = [POINTER(ScanImageTiffReaderContext)]
_api.bytesof_description = _api_lib.ScanImageTiffReader_GetImageDescriptionSizeBytes
_api.bytesof_description.restype = c_size_t
_api.bytesof_description.argtypes = [POINTER(ScanImageTiffReaderContext), c_int]
_api.description = _api_lib.ScanImageTiffReader_GetImageDescription
_api.description.restype = c_int
_api.description.argtypes = [POINTER(ScanImageTiffReaderContext), c_int, c_char_p, c_size_t]
_api.bytesof_metadata = _api_lib.ScanImageTiffReader_GetMetadataSizeBytes
_api.bytesof_metadata.restype = c_size_t
_api.bytesof_metadata.argtypes = [POINTER(ScanImageTiffReaderContext)]
_api.metadata = _api_lib.ScanImageTiffReader_GetMetadata
_api.metadata.restype = c_int
_api.metadata.argtypes = [POINTER(ScanImageTiffReaderContext), c_char_p, c_size_t]
_api.apiversion = _api_lib.ScanImageTiffReader_APIVersion
_api.apiversion.restype = c_char_p
_api.apiversion.argtypes = None
_api.bytesof_interval = _api_lib.ScanImageTiffReader_GetFrameIntervalSizeBytes
_api.bytesof_interval.restype = c_size_t
_api.bytesof_interval.argtypes = [POINTER(ScanImageTiffReaderContext), c_ulong, c_ulong]
_api.interval = _api_lib.ScanImageTiffReader_GetFrameInterval
_api.interval.restype = c_int
_api.interval.argtypes = [POINTER(ScanImageTiffReaderContext), c_ulong, c_ulong, c_void_p, c_size_t]

def api_version():
    """ Returns a string stating the version of the c library that
    this python code is using.

    :Example:

    >>> print(ScanImageTiffReader.api_version()) #doctest: +ELLIPSIS
    Version ...
    """
    return _api.apiversion().decode('utf-8', 'strict')


__version__ = api_version()

class ScanImageTiffReader:
    __doc__ = ' Reader for ScanImage Tiff and BigTiff files.\n\n    The constructor opens a file and builds an index by scanning\n    through the file.\n    '

    def __init__(self, filename):
        """ Opens a ScanImage tiff file for reading.

        :Example:

        >>> reader=ScanImageTiffReader("data/TR_003.tif")
        >>> stack=reader.data()
        >>> reader.close()
        """
        self._is_open = False
        self.open(filename)

    def __del__(self):
        """ Closes the open file context releasing any bound resources. """
        self.close()

    def __enter__(self):
        """Support python's with syntax"""
        return self

    def __exit__(self, type, value, traceback):
        """Support python's with syntax"""
        self.close()
        return False

    @staticmethod
    def api_version():
        """ Returns a string stating the version of the c library that
        this python code is using.

        :Example:

        >>> print(ScanImageTiffReader.api_version()) #doctest: +ELLIPSIS
        Version ...
        """
        return _api.apiversion().decode('utf-8', 'strict')

    def open(self, filename):
        """ Opens a ScanImage tiff file for reading.

        Called by the constructor.  Normally you don't need to use this
        function.  It's possible, however to reuse an instance of this class:

        :Example:

        >>> reader=ScanImageTiffReader("data/TR_003.tif")
        >>> stack=reader.data()
        >>> reader.close()
        >>> reader.open("data/resj_00001.tif")
        >>> print(reader.shape())
        [10, 512, 512]
        >>> reader.close()

        However, there's probably no real reason to use this pattern over just
        constructing new readers.
        """
        self.close()
        self._ScanImageTiffReader__ctx = _api.open(filename.encode('utf8'))
        if self._ScanImageTiffReader__ctx.log:
            raise Exception(self._ScanImageTiffReader__ctx.log.decode('utf-8', 'strict'))
        self._is_open = True

    def close(self):
        """ Closes the open file context releasing any bound resources. """
        if self._is_open:
            _api.close(self._ScanImageTiffReader__ctx)
        self._is_open = False
        self._ScanImageTiffReader__ctx = ScanImageTiffReaderContext(None, None)

    def _shape(self):
        """ (private) return raw shape"""
        s = _api.shape(self._ScanImageTiffReader__ctx)
        if self._ScanImageTiffReader__ctx.log:
            raise Exception(self._ScanImageTiffReader__ctx.log.decode('utf-8', 'strict'))
        return s

    def dtype(self):
        """Returns a tuple corresponding to self.data().dtype

        :rtype: numpy.dtype

        :Example:

        >>> with ScanImageTiffReader("data/resj_00001.tif") as reader:
        ...     print(reader.dtype())
        int16
        """
        return _typemap_[self._shape().type]

    def shape(self):
        """Returns a tuple corresponding to self.data().shape

        :Example:

        >>> with ScanImageTiffReader("data/resj_00001.tif") as reader:
        ...     print(reader.shape())
        [10, 512, 512]
        """
        s = self._shape()
        sh = s.dims[:s.ndim]
        return sh[::-1]

    def data(self, beg=None, end=None):
        """Returns a numpy array with the image stack.  By default, reads
        the entire stack into memory.

        Optionally, reads a subinterval of the file starting with frame ``beg``
        and up to, but not including, the frame ``end``.  If one of ``beg`` or 
        ``end`` is supplied, but the other is not, either the first or the last 
        frame will be used as a default.

        :rtype: numpy.array

        :Example:

        >>> v=ScanImageTiffReader("data/TR_003.tif").data()
        >>> print(v.shape)
        (10, 512, 512)
        >>> print(v[0][0][0:10])
        [6 6 7 5 7 8 8 9 6 9]

        Notice that in numpy dimensions are ordered like: ``[z,y,x]``.

        :Example:

        >>> v=ScanImageTiffReader("data/TR_003.tif").data(beg=2,end=5)
        >>> print(v.shape)
        (3, 512, 512)
        >>> print(v[0][0][0:10])
        [6 5 4 4 6 8 8 7 7 6]
        """
        s = self._shape()
        d = _typemap_[self._shape().type]
        sh = s.dims[:s.ndim]
        sh = sh[::-1]
        if beg is None and end is None:
            a = empty(sh, dtype=d)
            _api.data(self._ScanImageTiffReader__ctx, a.ctypes.data, a.size * a.itemsize)
        else:
            beg = 0 if beg is None else beg
            end = sh[0] if end is None else end
            sh[0] = end - beg
            a = empty(sh, dtype=d)
            _api.interval(self._ScanImageTiffReader__ctx, beg, end, a.ctypes.data, a.size * a.itemsize)
        if self._ScanImageTiffReader__ctx.log:
            raise Exception(self._ScanImageTiffReader__ctx.log.decode('utf-8', 'strict'))
        return a

    def __len__(self):
        """ returns the number of planes in the image stack

        :Example:

        >>> with ScanImageTiffReader("data/resj_00001.tif") as reader:
        ...     print(len(reader))
        10
        """
        n = _api.countof_descriptions(self._ScanImageTiffReader__ctx)
        if self._ScanImageTiffReader__ctx.log:
            raise Exception(self._ScanImageTiffReader__ctx.log.decode('utf-8', 'strict'))
        return n

    def description(self, iframe):
        """Returns the contents of the image description tag for the indicated
        frame.

        :param iframe: An integer between 0 and len(self)-1
        :rtype: string

        :Example:

        >>> with ScanImageTiffReader("data/res_00001.tif") as reader:
        ...     print(reader.description(0))
        frameNumbers = 1
        acquisitionNumbers = 1
        frameNumberAcquisition = 1
        frameTimestamps_sec = 0.000000000
        acqTriggerTimestamps_sec = 0.000000000
        nextFileMarkerTimestamps_sec = -1.000000000
        endOfAcquisition = 0
        endOfAcquisitionMode = 0
        dcOverVoltage = 0
        epoch = [1601  1  1  0  0 25.045]
        auxTrigger0 = []
        auxTrigger1 = []
        auxTrigger2 = []
        auxTrigger3 = []
        I2CData = {}
        <BLANKLINE>

        Another example from a file that was saved using the json-style header:

        >>> with ScanImageTiffReader("data/resj_2018a_00002.tif") as reader:
        ...     print(reader.description(0)) # doctest: +NORMALIZE_WHITESPACE
        {
          "frameNumbers": 1,
          "acquisitionNumbers": 1,
          "frameNumberAcquisition": 1,
          "frameTimestamps_sec": 0.000000000,
          "acqTriggerTimestamps_sec": -0.000087000,
          "nextFileMarkerTimestamps_sec": -1.000000000,
          "endOfAcquisition": 0,
          "endOfAcquisitionMode": 0,
          "dcOverVoltage": 0,
          "epoch": [2018,10, 9,11,58,49.866],
          "auxTrigger0": [],
          "auxTrigger1": [],
          "auxTrigger2": [],
          "auxTrigger3": [],
          "I2CData": []
        }
        """
        if iframe < 0 or iframe >= len(self):
            raise IndexError('iframe out of bounds.  Must be between 0 and len(self)-1, inclusive.')
        sz = _api.bytesof_description(self._ScanImageTiffReader__ctx, iframe)
        if self._ScanImageTiffReader__ctx.log:
            raise Exception(self._ScanImageTiffReader__ctx.log.decode('utf-8', 'strict'))
        buf = create_string_buffer(sz)
        _api.description(self._ScanImageTiffReader__ctx, iframe, buf, len(buf))
        if self._ScanImageTiffReader__ctx.log:
            raise Exception(self._ScanImageTiffReader__ctx.log)
        return buf.value.decode('utf-8', 'strict')

    def metadata(self):
        """Reads the ScanImage metadata section from the file.  This data
        section is not part of the Tiff specification, so common Tiff readers
        will not be able to access this data.

        In ScanImage 2016, this is a JSON string.  For previous versions of
        ScanImage, this is a bytestring that must be deserialized in matlab.

        :rtype: string

        :Example:

        >>> import json
        >>> with ScanImageTiffReader("data/resj_00001.tif") as reader:
        ...     o=json.loads(reader.metadata())
        ...     print(o["RoiGroups"]["imagingRoiGroup"]["rois"]["scanfields"]["affine"])
        [[23.4, 0, -11.7], [0, 23.4, -11.7], [0, 0, 1]]

        """
        sz = _api.bytesof_metadata(self._ScanImageTiffReader__ctx)
        if self._ScanImageTiffReader__ctx.log:
            raise Exception(self._ScanImageTiffReader__ctx.log.decode('utf-8', 'strict'))
        if sz == 0:
            return ''
        buf = create_string_buffer(sz)
        _api.metadata(self._ScanImageTiffReader__ctx, buf, len(buf))
        if self._ScanImageTiffReader__ctx.log:
            raise Exception(self._ScanImageTiffReader__ctx.log.decode('utf-8', 'strict'))
        return buf.value.decode('utf-8', 'strict')