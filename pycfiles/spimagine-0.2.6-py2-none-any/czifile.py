# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mweigert/python/spimagine/spimagine/lib/czifile.py
# Compiled at: 2017-01-11 23:40:09
"""Read image and metadata from Carl Zeiss(r) ZISRAW (CZI) files.

CZI is the native image file format of the ZEN(r) software by the Carl Zeiss
Microscopy GmbH. It stores multidimensional images and metadata from
microscopy experiments.

:Author:
  `Christoph Gohlke <http://www.lfd.uci.edu/~gohlke/>`_

:Organization:
  Laboratory for Fluorescence Dynamics, University of California, Irvine

:Version: 2013.12.04

Requirements
------------
* `CPython 2.7 or 3.3 <http://www.python.org>`_
* `Numpy 1.7 <http://www.numpy.org>`_
* `Scipy 0.13 <http://www.scipy.org>`_
* `Tifffile.py 2013.11.03 <http://www.lfd.uci.edu/~gohlke/>`_
* `Czifle.pyx 2013.12.04  <http://www.lfd.uci.edu/~gohlke/>`_
  (for decoding JpegXrFile and JpgFile images)

Revisions
---------
2013.12.04
    Decode JpegXrFile and JpgFile via _czifle extension module.
    Attempt to reconstruct tiled mosaic images.
2013.11.20
    Initial release.

Notes
-----
The API is not stable yet and might change between revisions.

The file format design specification [1] is confidential and the licence
agreement does not permit to write data into CZI files.

Only a subset of the 2012 specification is implemented in the initial release.
Specifically, multifile images are not yet supported.

Tested on Windows with a few example files only.

References
----------
(1) ZISRAW (CZI) File Format Design specification Release Version 1.1 for
    ZEN 2012. DS_ZISRAW-FileFormat_Rel_ZEN2012.doc (Confidential)
    Documentation can be requested at
    <http://microscopy.zeiss.com/microscopy/en_us/downloads/zen.html>
(2) CZI The File Format for the Microscope | ZEISS International
    <http://microscopy.zeiss.com/microscopy/en_us/products/microscope-software/
    zen-2012/czi.html>

Examples
--------
>>> with CziFile('test.czi') as czi:
...     image = czi.asarray()
>>> image.shape
(3, 3, 3, 250, 200, 3)
>>> image[0, 0, 0, 0, 0]
array([10, 10, 10], dtype=uint8)

"""
from __future__ import division, print_function, absolute_import
import sys, os, re, uuid, struct, warnings, tempfile
try:
    from lxml import etree
except ImportError:
    from xml.etree import cElementTree as etree

import numpy
from scipy.ndimage.interpolation import zoom
from .tifffile import decodelzw, lazyattr, stripnull
try:
    import _czifile
    _have_czifile = True
except ImportError:
    _have_czifile = False
    warnings.warn('failed to import the optional _czifile C extension module.\nDecoding of JXR and JPG encoded images will be unavailable.\nCzifile.pyx can be obtained at http://www.lfd.uci.edu/~gohlke/')

__version__ = '2013.12.04'
__docformat__ = 'restructuredtext en'
__all__ = ('imread', 'CziFile')

def imread(filename, *args, **kwargs):
    """Return image data from CZI file as numpy array.

    'args' and 'kwargs' are arguments to CziFile.asarray().

    Examples
    --------
    >>> image = imread('test.czi')
    >>> image.shape
    (3, 3, 3, 250, 200, 3)
    >>> image.dtype
    dtype('uint8')

    """
    with CziFile(filename) as (czi):
        result = czi.asarray(*args, **kwargs)
    return result


class CziFile(object):
    """Carl Zeiss Image (CZI) file.

    Attributes
    ----------
    header : FileHeaderSegment
        Global file metadata such as file version and GUID.
    metadata : etree.ElementTree.Element
        Global image metadata in UTF-8 encoded XML format.

    All attributes are read-only.

    """

    def __init__(self, arg, multifile=True, filesize=None, detectmosaic=True):
        """Open CZI file and read header.

        Raise ValueError if file is not a ZISRAW file.

        Parameters
        ----------
        multifile : bool
            If True (default), the master file of a multifile CZI file
            will be opened if applicable.
        filesize : int
            Size of file if arg is a file handle pointing to an
            embedded CZI file.
        detectmosaic : bool
            If True (default), mosaic images will be reconstructed from
            SubBlocks with a tile index.

        Notes
        -----
        CziFile instances created from file name must be closed using the
        'close' method, which is automatically called when using the
        'with' statement.

        """
        self._fh = FileHandle(arg, size=filesize)
        try:
            if self._fh.read(10) != 'ZISRAWFILE':
                raise ValueError('not a CZI file')
            self.header = Segment(self._fh, 0).data()
        except Exception:
            self._fh.close()
            raise

        if multifile and self.header.file_part and isinstance(arg, basestring):
            self._fh.close()
            name, _ = match_filename(arg)
            self._fh = FileHandle(name)
            self.header = Segment(self._fh, 0).data()
            assert self.header.primary_file_guid == self.header.file_guid
            assert self.header.file_part == 0
        if self.header.update_pending:
            warnings.warn('file is pending update')
        self._filter_mosaic = detectmosaic

    def segments(self, kind=None):
        """Return iterator over Segment data of specified kind.

        Parameters
        ----------
        kind : bytestring or sequence thereof
            Segment id(s) as listed in SEGMENT_ID.
            If None (default), all segments are returned.

        """
        fpos = 0
        while True:
            self._fh.seek(fpos)
            try:
                segment = Segment(self._fh)
            except SegmentNotFoundError:
                break

            if kind is None or segment.sid in kind:
                yield segment.data()
            fpos = segment.data_offset + segment.allocated_size

        return

    @lazyattr
    def metadata(self):
        """Return data from MetadataSegment as xml.ElementTree root Element.

        Return None if no Metadata segment is found.

        """
        if self.header.metadata_position:
            segment = Segment(self._fh, self.header.metadata_position)
            if segment.sid == MetadataSegment.SID:
                return etree.fromstring(segment.data().data())
        warnings.warn('Metadata segment not found')
        try:
            metadata = next(self.segments(MetadataSegment.SID))
            return etree.fromstring(metadata.data())
        except StopIteration:
            pass

    @lazyattr
    def subblock_directory(self):
        """Return list of all DirectoryEntryDV in file.

        Use SubBlockDirectorySegment if exists, else find SubBlockSegments.

        """
        if self.header.directory_position:
            segment = Segment(self._fh, self.header.directory_position)
            if segment.sid == SubBlockDirectorySegment.SID:
                return segment.data().entries
        warnings.warn('SubBlockDirectory segment not found')
        return list(segment.directory_entry for segment in self.segments(SubBlockSegment.SID))

    @lazyattr
    def attachment_directory(self):
        """Return list of all AttachmentEntryA1 in file.

        Use AttachmentDirectorySegment if exists, else find AttachmentSegments.

        """
        if self.header.attachment_directory_position:
            segment = Segment(self._fh, self.header.attachment_directory_position)
            if segment.sid == AttachmentDirectorySegment.SID:
                return segment.data().entries
        warnings.warn('AttachmentDirectory segment not found')
        return list(segment.attachment_entry for segment in self.segments(AttachmentSegment.SID))

    def subblocks(self):
        """Return iterator over all SubBlock segments in file."""
        for entry in self.subblock_directory:
            yield entry.data_segment()

    def attachments(self):
        """Return iterator over all Attachment segments in file."""
        for entry in self.attachment_directory:
            yield entry.data_segment()

    def save_attachments(self, directory=None):
        """Save all attachments to files."""
        if directory is None:
            directory = self._fh.filename + '.attachments'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for attachment in self.attachments():
            attachment.save(directory=directory)

        return

    @lazyattr
    def filtered_subblock_directory(self):
        """Return sorted list of DirectoryEntryDV if mosaic, else all."""
        if not self._filter_mosaic:
            return self.subblock_directory
        else:
            filtered = [ directory_entry for directory_entry in self.subblock_directory if directory_entry.mosaic_index is not None
                       ]
            if not filtered:
                return self.subblock_directory
            return list(sorted(filtered, key=lambda x: x.mosaic_index))

    @lazyattr
    def shape(self):
        """Return shape of image data in file."""
        shape = [ [ dim.start + dim.size for dim in directory_entry.dimension_entries if dim.dimension != 'M' ] for directory_entry in self.filtered_subblock_directory
                ]
        shape = numpy.max(shape, axis=0)
        shape = tuple(i - j for i, j in zip(shape, self.start[:-1]))
        dtype = self.filtered_subblock_directory[0].dtype
        sampleshape = numpy.dtype(dtype).shape
        shape = shape + (sampleshape if sampleshape else (1, ))
        return shape

    @lazyattr
    def start(self):
        """Return minimum start indices per dimension of sub images in file."""
        start = [ [ dim.start for dim in directory_entry.dimension_entries if dim.dimension != 'M' ] for directory_entry in self.filtered_subblock_directory
                ]
        start = tuple(numpy.min(start, axis=0)) + (0, )
        return start

    @lazyattr
    def axes(self):
        """Return axes of image data in file."""
        return self.filtered_subblock_directory[0].axes

    @lazyattr
    def dtype(self):
        """Return dtype of image data in file."""
        dtype = self.filtered_subblock_directory[0].dtype[-2:]
        for directory_entry in self.filtered_subblock_directory:
            dtype = numpy.promote_types(dtype, directory_entry.dtype[-2:])

        return dtype

    def asarray(self, bgr2rgb=False, resize=True, order=1):
        """Return image data from file(s) as numpy array.

        Parameters
        ----------
        bgr2rgb : bool
            If True, exchange red and blue samples if applicable.
        resize : bool
            If True (default), resize sub/supersampled subblock data.
        order : int
            The order of spline interpolation used to resize sub/supersampled
            subblock data. Default is 1 (bilinear).

        """
        image = numpy.zeros(self.shape, self.dtype)
        for directory_entry in self.filtered_subblock_directory:
            subblock = directory_entry.data_segment()
            tile = subblock.data(bgr2rgb=bgr2rgb, resize=resize, order=order)
            index = [ slice(i - j, i - j + k) for i, j, k in zip(directory_entry.start, self.start, tile.shape)
                    ]
            try:
                image[index] = tile
            except ValueError as e:
                warnings.warn(str(e))

        return image

    def close(self):
        self._fh.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __str__(self):
        return ('\n ').join((
         self._fh.name.capitalize(),
         '(Carl Zeiss Image File)',
         str(self.header),
         'MetadataSegment',
         str(self.axes),
         str(self.shape),
         str(self.dtype),
         str(etree.tostring(self.metadata))))


class FileHandle(object):
    """Binary file handle that can handle a file within a file.

    Only binary read, seek, tell and close are supported on embedded files.

    Attributes
    ----------
    name : str
        file name
    path : str
        Absolute path to file.

    All attributes are read-only.

    """

    def __init__(self, arg, mode='rb', name=None, offset=None, size=None):
        """Initialize file handle from file name or another file handle.

        Parameters
        ----------
        arg : str, File, or FileHandle
            File name or open file handle.
        mode : str
            File open mode in case 'arg' is filename.
        name : str
            Optional name of file in case 'arg' is file handle.
        offset : int
            Optional start position of file in the file. By default the
            current file position is used as offset.
        size : int
            Optional size of file in the file. By default the number of
            bytes from the current file position to the end of the file
            is used.

        """
        if isinstance(arg, basestring):
            filename = os.path.abspath(arg)
            self.path, self.name = os.path.split(filename)
            self._fh = open(filename, mode)
            self._close = True
            if offset is None:
                offset = 0
        elif isinstance(arg, FileHandle):
            if offset is None:
                offset = arg.tell()
            else:
                offset = arg._offset + offset
            self._fh = arg._fh
            self._close = False
            if name:
                self.name = name
            else:
                name, ext = os.path.splitext(arg.name)
                self.name = '%s@%i%s' % (name, offset, ext)
            self.path = arg.path
        else:
            if offset is None:
                offset = arg.tell()
            self._fh = arg
            self._close = False
            self.name = name if name else self._fh.name
            self.path = ''
        self._offset = offset
        if size is not None:
            self.size = size
        return

    @property
    def filename(self):
        return os.path.join(self.path, self.name)

    def read(self, size=-1):
        if size < 0 and self._offset:
            size = self.size
        return self._fh.read(size)

    def fromfile(self, dtype, count=-1, sep=''):
        return numpy.fromfile(self._fh, dtype, count, sep)

    def tell(self):
        return self._fh.tell() - self._offset

    def seek(self, offset, whence=0):
        if self._offset:
            if whence == 0:
                self._fh.seek(self._offset + offset, whence)
                return
            if whence == 2:
                self._fh.seek(self._offset + self.size - offset, 0)
                return
        self._fh.seek(offset, whence)

    def close(self):
        if self._close:
            self._fh.close()

    def __getattr__(self, name):
        if name == 'size':
            self._fh.seek(self._offset, 2)
            self.size = self._fh.tell()
            return self.size
        return getattr(self._fh, name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class Segment(object):
    """ZISRAW Segment."""
    __slots__ = ('sid', 'allocated_size', 'used_size', 'data_offset', '_fh')

    def __init__(self, fh, fpos=None):
        """Read segment header from file."""
        if fpos is not None:
            fh.seek(fpos)
        try:
            self.sid, self.allocated_size, self.used_size = struct.unpack('<16sqq', fh.read(32))
        except struct.error:
            raise SegmentNotFoundError('can not read ZISRAW segment')

        self.sid = stripnull(self.sid)
        if self.sid not in SEGMENT_ID:
            if not self.sid.startswith('ZISRAW'):
                raise SegmentNotFoundError('not a ZISRAW segment')
            warnings.warn('unknown segment type %s' % self.sid)
        self.data_offset = fh.tell()
        self._fh = fh
        return

    def data(self):
        r"""Read segment data from file and return as \*Segment instance."""
        self._fh.seek(self.data_offset)
        return SEGMENT_ID.get(self.sid, UnknownSegment)(self._fh)

    def __str__(self):
        return 'Segment %s %i of %i' % (
         self.sid, self.used_size, self.allocated_size)


class SegmentNotFoundError(Exception):
    """Exception to indicate that file position doesn't contain Segment."""
    pass


class FileHeaderSegment(object):
    """ZISRAWFILE file header segment data.

    Contains global file metadata such as file version and GUID.

    """
    __slots__ = ('version', 'primary_file_guid', 'file_guid', 'file_part', 'directory_position',
                 'metadata_position', 'update_pending', 'attachment_directory_position')
    SID = 'ZISRAWFILE'

    def __init__(self, fh):
        major, minor, reserved1, reserved2, primary_file_guid, file_guid, self.file_part, self.directory_position, self.metadata_position, self.update_pending, self.attachment_directory_position = struct.unpack('<iiii16s16siqqiq', fh.read(80))
        self.version = (major, minor)
        self.update_pending = bool(self.update_pending)
        self.primary_file_guid = uuid.UUID(bytes=primary_file_guid)
        self.file_guid = uuid.UUID(bytes=file_guid)

    def __str__(self):
        return 'FileHeaderSegment\n ' + ('\n ').join('%s %s' % (name, str(getattr(self, name))) for name in FileHeaderSegment.__slots__)


class MetadataSegment(object):
    """ZISRAWMETADATA segment data.

    Contains global image metadata in UTF-8 encoded XML format.

    """
    __slots__ = ('xml_size', 'attachment_size', 'xml_offset', '_fh')
    SID = 'ZISRAWMETADATA'

    def __init__(self, fh):
        self.xml_size, self.attachment_size = struct.unpack('<ii', fh.read(8))
        fh.seek(248, 1)
        self.xml_offset = fh.tell()
        self._fh = fh

    def data(self, raw=False):
        """Read XML from file and return as unicode string."""
        self._fh.seek(self.xml_offset)
        data = self._fh.read(self.xml_size)
        if raw:
            return data
        data = data.replace('\r\n', '\n').replace('\r', '\n')
        return unicode(data, 'utf-8')

    def __str__(self):
        return 'MetadataSegment\n %s' % self.data()


class SubBlockSegment(object):
    """ZISRAWSUBBLOCK segment data.

    Contains XML metadata, optional attachments, and homogenous,
    contiguous pixel data.

    """
    __slots__ = ('metadata_size', 'attachment_size', 'data_size', 'directory_entry',
                 'data_offset', '_fh')
    SID = 'ZISRAWSUBBLOCK'

    def __init__(self, fh):
        self.metadata_size, self.attachment_size, self.data_size = struct.unpack('<iiq', fh.read(16))
        self.directory_entry = DirectoryEntryDV(fh)
        self.data_offset = fh.tell()
        self.data_offset += max(240 - self.directory_entry.storage_size, 0)
        self.data_offset += self.metadata_size
        self._fh = fh

    def metadata(self):
        """Read metadata from file and return as XML string."""
        self._fh.seek(self.data_offset - self.metadata_size)
        return unicode(self._fh.read(self.metadata_size), 'utf-8')

    def data(self, raw=False, bgr2rgb=True, resize=True, order=1):
        """Read image data from file and return as numpy array."""
        self._fh.seek(self.data_offset)
        if raw:
            return self._fh.read(self.data_size)
        if self.compression:
            if self.compression not in DECOMPRESS:
                raise ValueError('compression unknown or not supported')
            data = self._fh.read(self.data_size)
            data = DECOMPRESS[self.compression](data)
            if self.compression == 2:
                data = numpy.fromstring(data, self.dtype)
        else:
            dtype = numpy.dtype(self.dtype)
            data = self._fh.fromfile(dtype, self.data_size // dtype.itemsize)
        data = data.reshape(self.stored_shape)
        if self.stored_shape == self.shape or not resize:
            if bgr2rgb and self.stored_shape[(-1)] in (3, 4):
                tmp = data[(Ellipsis, 0)].copy()
                data[(Ellipsis, 0)] = data[(Ellipsis, 2)]
                data[(Ellipsis, 2)] = tmp
            return data
        factors = [ j / i for i, j in zip(self.stored_shape, self.shape) ]
        factors = [ 1.0 if abs(1.0 - f) < 0.0001 else f for f in factors ]
        shape = list(self.stored_shape)
        for factor in factors:
            if factor != 1.0:
                break
            shape = shape[1:]
            factors = factors[1:]

        data.shape = shape
        if shape[(-1)] in (3, 4) and factors[(-1)] == 1.0:
            factors = factors[:-1]
            old = data
            data = numpy.empty(self.shape, self.dtype[-2:])
            for i in range(shape[(-1)]):
                j = {0: 2, 1: 1, 2: 0, 3: 3}[i] if bgr2rgb else i
                data[(..., i)] = zoom(old[(..., j)], zoom=factors, order=order)

        else:
            data = zoom(data, zoom=factors, order=order)
        data.shape = self.shape
        return data

    def attachments(self):
        """Read optional attachments from file and return as bytes."""
        if self.attachment_size < 1:
            return ''
        self._fh.seek(self.data_offset + self.data_size)
        return self._fh.read(self.attachment_size)

    def __getattr__(self, name):
        """Directly access DirectoryEntryDV attributes."""
        return getattr(self.directory_entry, name)

    def __str__(self):
        return 'SubBlockSegment\n %s\n %s' % (
         self.metadata(), str(self.directory_entry))


class DirectoryEntryDV(object):
    """Directory Entry - Schema DV."""

    @staticmethod
    def read_file_position(fh):
        """Return file position of associated SubBlock segment."""
        schema_type, file_position, dimensions_count = struct.unpack('<2s4xq14xi', fh.read(32))
        fh.seek(dimensions_count * 20, 1)
        assert schema_type == 'DV'
        return file_position

    def __init__(self, fh):
        schema_type, pixel_type, self.file_position, self.file_part, self.compression, self.pyramid_type, reserved1, reserved2, dimensions_count = struct.unpack('<2siqiiBB4si', fh.read(32))
        if schema_type != 'DV':
            raise ValueError('not a DirectoryEntryDV')
        self.dtype = PIXEL_TYPE[pixel_type]
        self.dimension_entries = list(reversed([ DimensionEntryDV1(fh) for _ in range(dimensions_count) ]))
        self._fh = fh

    @lazyattr
    def storage_size(self):
        return 32 + len(self.dimension_entries) * 20

    @lazyattr
    def pixel_type(self):
        return PIXEL_TYPE[self.dtype]

    @lazyattr
    def axes(self):
        axes = ('').join(dim.dimension for dim in self.dimension_entries if dim.dimension != 'M')
        return axes + '0'

    @lazyattr
    def shape(self):
        shape = tuple(dim.size for dim in self.dimension_entries if dim.dimension != 'M')
        sampleshape = numpy.dtype(self.dtype).shape
        return shape + (sampleshape if sampleshape else (1, ))

    @lazyattr
    def start(self):
        start = tuple(dim.start for dim in self.dimension_entries if dim.dimension != 'M')
        return start + (0, )

    @lazyattr
    def stored_shape(self):
        shape = tuple(dim.stored_size for dim in self.dimension_entries if dim.dimension != 'M')
        sampleshape = numpy.dtype(self.dtype).shape
        return shape + (sampleshape if sampleshape else (1, ))

    @lazyattr
    def mosaic_index(self):
        for dim in self.dimension_entries:
            if dim.dimension == 'M':
                return dim.start

    def data_segment(self):
        """Read and return SubBlockSegment at file_position."""
        return Segment(self._fh, self.file_position).data()

    def __str__(self):
        return 'DirectoryEntryDV\n  %s %s %s %s\n  %s' % (
         COMPRESSION.get(self.compression, self.compression),
         self.pixel_type, self.axes, str(self.shape),
         ('\n  ').join(str(d) for d in self.dimension_entries))


class DimensionEntryDV1(object):
    """Dimension Entry - Schema DV."""
    __slots__ = ('dimension', 'start', 'size', 'start_coordinate', 'stored_size')

    def __init__(self, fh):
        self.dimension, self.start, self.size, self.start_coordinate, stored_size = struct.unpack('<4siifi', fh.read(20))
        self.dimension = stripnull(self.dimension)
        self.stored_size = stored_size if stored_size else self.size

    def __str__(self):
        return 'DimensionEntryDV1 %s %i %i %f %i' % (
         self.dimension, self.start, self.size,
         self.start_coordinate, self.stored_size)


class SubBlockDirectorySegment(object):
    """ZISRAWDIRECTORY segment data.

    Contains entries of any kind, currently only DirectoryEntryDV.

    """
    __slots__ = ('entries', )
    SID = 'ZISRAWDIRECTORY'

    @staticmethod
    def file_positions(fh):
        """Return list of file positions of associated SubBlock segments."""
        entry_count = struct.unpack('<i', fh.read(4))[0]
        fh.seek(124, 1)
        return tuple(DirectoryEntryDV.read_file_position(fh) for _ in range(entry_count))

    def __init__(self, fh):
        entry_count = struct.unpack('<i', fh.read(4))[0]
        fh.seek(124, 1)
        self.entries = tuple(DirectoryEntryDV(fh) for _ in range(entry_count))

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, key):
        return self.entries[key]

    def __iter__(self):
        return iter(self.entries)

    def __str__(self):
        return 'SubBlockDirectorySegment\n %s' % ('\n ').join(str(e) for e in self.entries)


class AttachmentSegment(object):
    """ZISRAWATTACH segment data.

    Contains binary or text data as specified in attachment_entry.

    """
    __slots__ = ('data_size', 'attachment_entry', 'data_offset', '_fh')
    SID = 'ZISRAWATTACH'

    def __init__(self, fh):
        self.data_size = struct.unpack('<i', fh.read(4))[0]
        fh.seek(12, 1)
        self.attachment_entry = AttachmentEntryA1(fh)
        fh.seek(112, 1)
        self.data_offset = fh.tell()
        self._fh = fh

    def save(self, filename=None, directory='.'):
        """Save attachment to file in directory."""
        self._fh.seek(self.data_offset)
        if not filename:
            filename = self.attachment_entry.filename
        filename = os.path.join(directory, filename)
        with open(filename, 'wb') as (fh):
            fh.write(self._fh.read(self.data_size))

    def data(self, raw=False):
        """Read embedded file and return content.

        If 'raw' is False (default), try return content according to
        CONTENT_FILE_TYPE, else return raw bytes.

        """
        self._fh.seek(self.data_offset)
        cotype = self.attachment_entry.content_file_type
        if not raw and cotype in CONTENT_FILE_TYPE:
            return CONTENT_FILE_TYPE[cotype](self._fh, filesize=self.data_size)
        else:
            return self._fh.read(self.data_size)

    def __str__(self):
        return 'AttachmentSegment\n %s' % self.attachment_entry


class AttachmentEntryA1(object):
    """AttachmentEntry - Schema A1."""
    __slots__ = ('content_guid', 'content_file_type', 'name', 'file_position', '_fh')

    @staticmethod
    def read_file_position(fh):
        """Return file position of associated Attachment segment."""
        schema_type, file_position = struct.unpack('<2s10xq', fh.read(20))
        fh.seek(108, 1)
        assert schema_type == 'A1'
        return file_position

    def __init__(self, fh):
        shema_type, reserved, self.file_position, file_part, content_guid, content_file_type, name = struct.unpack('<2s10sqi16s8s80s', fh.read(128))
        if shema_type != 'A1':
            raise ValueError('not a AttachmentEntryA1')
        self.content_guid = uuid.UUID(bytes=content_guid)
        self.content_file_type = stripnull(content_file_type)
        self.name = unicode(stripnull(name), 'utf-8')
        self._fh = fh

    @property
    def filename(self):
        """Return unique file name for attachment."""
        return '%s@%i.%s' % (self.name, self.file_position,
         unicode(self.content_file_type, 'utf-8').lower())

    def data_segment(self):
        """Read and return AttachmentSegment at file_position."""
        return Segment(self._fh, self.file_position).data()

    def __str__(self):
        return (' ').join(str(i) for i in (
         'AttachmentEntryA1', self.name, self.content_file_type,
         self.content_guid))


class AttachmentDirectorySegment(object):
    """ZISRAWATTDIR segment data. Sequence of AttachmentEntryA1."""
    __slots__ = ('entries', )
    SID = 'ZISRAWATTDIR'

    @staticmethod
    def file_positions(fh):
        """Return list of file positions of associated Attachment segments."""
        entry_count = struct.unpack('<i', fh.read(4))[0]
        fh.seek(252, 1)
        return tuple(AttachmentEntryA1.read_file_position(fh) for _ in range(entry_count))

    def __init__(self, fh):
        entry_count = struct.unpack('<i', fh.read(4))[0]
        fh.seek(252, 1)
        self.entries = tuple(AttachmentEntryA1(fh) for _ in range(entry_count))

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, key):
        return self.entries[key]

    def __iter__(self):
        return iter(self.entries)

    def __str__(self):
        return 'AttachmentDirectorySegment\n %s' % ('\n ').join(str(i) for i in self.entries)


class DeletedSegment(object):
    """DELETED segment data. Ignore."""
    __slots__ = ()
    SID = 'DELETED'

    def __init__(self, fh):
        pass

    def __str__(self):
        return 'DeletedSegment'


class UnknownSegment(object):
    """Unknown segment data. Ignore."""
    __slots__ = ()

    def __init__(self, fh):
        pass

    def __str__(self):
        return 'UnknownSegment'


class TimeStamps(object):
    """CZTIMS TimeStamps content schema.

    Contains sequence of floting point numbers, i.e. seconds relative
    to start time of acquisition.

    """
    __slots__ = ('time_stamps', )

    def __init__(self, fh, filesize=None):
        size, number = struct.unpack('<ii', fh.read(8))
        self.time_stamps = struct.unpack('<%id' % number, fh.read(8 * number))

    def __len__(self):
        return len(self.time_stamps)

    def __getitem__(self, key):
        return self.time_stamps[key]

    def __iter__(self):
        return iter(self.time_stamps)

    def __str__(self):
        return str(self.time_stamps)


class FocusPositions(object):
    """CZFOC FocusPositions content schema.

    Contains sequence of floting point numbers, i.e. micrometers relative
    to Z start position of acquisition.

    """
    __slots__ = ('positions', )

    def __init__(self, fh, filesize=None):
        size, number = struct.unpack('<ii', fh.read(8))
        self.positions = struct.unpack('<%id' % number, fh.read(8 * number))

    def __len__(self):
        return len(self.positions)

    def __getitem__(self, key):
        return self.positions[key]

    def __iter__(self):
        return iter(self.positions)

    def __str__(self):
        return str(self.positions)


class EventList(object):
    """CZEVL EventList content schema. Sequence of EventListEntry."""
    __slots__ = ('events', )

    def __init__(self, fh, filesize=None):
        size, number = struct.unpack('<ii', fh.read(8))
        self.events = [ EventListEntry(fh) for _ in range(number) ]

    def __len__(self):
        return len(self.events)

    def __getitem__(self, key):
        return self.events[key]

    def __iter__(self):
        return iter(self.events)

    def __str__(self):
        return ('\n ').join(str(event) for event in self.events)


class EventListEntry(object):
    """EventListEntry content schema."""
    __slots__ = ('time', 'event_type', 'description')
    EV_TYPE = {0: 'MARKER', 1: 'TIME_CHANGE', 2: 'BLEACH_START', 3: 'BLEACH_STOP', 
       4: 'TRIGGER'}

    def __init__(self, fh):
        size, self.time, self.event_type, description_size = struct.unpack('<idii', fh.read(20))
        description = stripnull(fh.read(description_size))
        self.description = unicode(description, 'utf-8')

    def __str__(self):
        return '%s @ %s (%s)' % (EventListEntry.EV_TYPE[self.event_type],
         self.time, self.description)


class LookupTables(object):
    """CZLUT LookupTables content schema. Sequence of LookupTableEntry."""
    __slots__ = ('lookup_tables', )

    def __init__(self, fh, filesize=None):
        size, number = struct.unpack('<ii', fh.read(8))
        self.lookup_tables = [ LookupTableEntry(fh) for _ in range(number) ]

    def __len__(self):
        return len(self.lookup_tables)

    def __getitem__(self, key):
        return self.lookup_tables[key]

    def __iter__(self):
        return iter(self.lookup_tables)

    def __str__(self):
        return 'LookupTables\n %s' % str(self.lookup_tables)


class LookupTableEntry(object):
    """LookupTableEntry content schema. Sequence of ComponentEntry."""
    __slots__ = ('identifier', 'components')

    def __init__(self, fh):
        size, identifier, number = struct.unpack('<i80si', fh.read(88))
        self.identifier = unicode(stripnull(identifier), 'utf-8')
        self.components = [ ComponentEntry(fh) for _ in range(number) ]

    def __len__(self):
        return len(self.components)

    def __getitem__(self, key):
        return self.components[key]

    def __iter__(self):
        return iter(self.components)

    def __str__(self):
        return 'LookupTableEntry\n %s\n %s' % (
         self.identifier, ('\n ').join(str(i) for i in self.components))


class ComponentEntry(object):
    """ComponentEntry content schema."""
    __slots__ = ('component_type', 'intensity')
    CO_TYPE = {-1: 'RGB', 1: 'RED', 2: 'GREEN', 3: 'BLUE'}

    def __init__(self, fh):
        size, self.component_type, number = struct.unpack('<iii', fh.read(12))
        self.intensity = fh.fromfile(dtype='<i2', count=number // 2)
        if self.component_type == -1:
            self.intensity = self.intensity.reshape(-1, 3)

    def __str__(self):
        return 'ComponentEntry %s %s' % (
         ComponentEntry.CO_TYPE[self.component_type],
         str(self.intensity.shape))


def xml_reader(fh, filesize):
    """Read XML from file and return as xml.ElementTree root Element."""
    xml = unicode(stripnull(fh.read(filesize)), 'utf-8')
    return etree.fromstring(xml)


def match_filename(filename):
    """Return master file name and file part number from CZI file name."""
    match = re.search('(.*?)(?:\\((\\d+)\\))?\\.czi$', filename, re.IGNORECASE).groups()
    name = match[0] + '.czi'
    part = int(match[1]) if len(match) > 1 else 0
    return (name, part)


def decodejxr(data):
    """Decode JXR data stream into ndarray via temporary file."""
    fd, filename = tempfile.mkstemp(suffix='.jxr')
    with os.fdopen(fd, 'wb') as (fh):
        fh.write(data)
    if isinstance(filename, unicode):
        filename = filename.encode('ascii')
    try:
        out = _czifile.decodejxr(filename)
    finally:
        os.remove(filename)

    return out


def decodejpg(data):
    """Decode JPG data stream into ndarray."""
    return _czifile.decodejpg(data, len(data))


SEGMENT_ID = {FileHeaderSegment.SID: FileHeaderSegment, 
   SubBlockDirectorySegment.SID: SubBlockDirectorySegment, 
   SubBlockSegment.SID: SubBlockSegment, 
   MetadataSegment.SID: MetadataSegment, 
   AttachmentSegment.SID: AttachmentSegment, 
   AttachmentDirectorySegment.SID: AttachmentDirectorySegment, 
   DeletedSegment.SID: DeletedSegment}
CONTENT_FILE_TYPE = {'CZI': CziFile, 
   'ZISRAW': CziFile, 
   'CZTIMS': TimeStamps, 
   'CZEVL': EventList, 
   'CZLUT': LookupTables, 
   'CZFOC': FocusPositions, 
   'CZEXP': xml_reader, 
   'CZHWS': xml_reader, 
   'CZMVM': xml_reader}
PIXEL_TYPE = {0: '<u1', 
   'Gray8': '<u1', '<u1': 'Gray8', 1: '<u2', 
   'Gray16': '<u2', '<u2': 'Gray16', 2: '<f4', 
   'Gray32Float': '<f4', '<f4': 'Gray32Float', 3: '<3u1', 
   'Bgr24': '<3u1', '<3u1': 'Bgr24', 4: '<3u2', 
   'Bgr48': '<3u2', '<3u2': 'Bgr48', 8: '<3f4', 
   'Bgr96Float': '<3f4', '<3f4': 'Bgr96Float', 9: '<4u1', 
   'Bgra32': '<4u1', '<4u1': 'Bgra32', 10: '<F8', 
   'Gray64ComplexFloat': '<F8', '<F8': 'Gray64ComplexFloat', 11: '<3F8', 
   'Bgr192ComplexFloat': '<3F8', '<3F8': 'Bgr192ComplexFloat', 12: '<i4', 
   'Gray32': '<i4', '<i4': 'Gray32', 13: '<i8', 
   'Gray64': '<i8', '<i8': 'Gray64'}
DIMENSIONS = {'0': 'Sample', 
   'X': 'Width', 
   'Y': 'Height', 
   'C': 'Channel', 
   'Z': 'Slice', 
   'T': 'Time', 
   'R': 'Rotation', 
   'S': 'Scene', 
   'I': 'Illumination', 
   'B': 'Block', 
   'M': 'Mosaic', 
   'H': 'Phase', 
   'V': 'View'}
COMPRESSION = {0: 'Uncompressed', 
   1: 'JpgFile', 
   2: 'LZW', 
   4: 'JpegXrFile'}
DECOMPRESS = {0: lambda x: x, 
   2: decodelzw}
if _have_czifile:
    DECOMPRESS[1] = decodejpg
    DECOMPRESS[4] = decodejxr
if sys.version_info[0] > 2:
    unicode = str
    basestring = (str, bytes)
if __name__ == '__main__':
    import doctest
    numpy.set_printoptions(suppress=True, precision=5)
    doctest.testmod()