# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Newville/Codes/wxmplot/examples/tifffile.py
# Compiled at: 2018-03-19 15:49:40
# Size of source mod 2**32: 99714 bytes
"""Read and write image data from and to TIFF files.

Image and meta-data can be read from TIFF, BigTIFF, OME-TIFF, STK, LSM, NIH,
and FluoView files. Only a subset of the TIFF specification is supported,
mainly uncompressed and losslessly compressed 2**(0 to 6) bit integer,
16, 32 and 64-bit float, grayscale and RGB(A) images, which are commonly
used in bio-scientific imaging. Specifically, reading JPEG/CCITT
compressed image data or EXIF/IPTC/GPS/XMP meta-data is not implemented.
Only primary info records are read for STK, FluoView, and NIH image formats.

TIFF, the Tagged Image File Format, is under the control of Adobe Systems.
BigTIFF allows for files greater than 4 GB. STK, LSM, FluoView, and OME-TIFF
are custom extensions defined by MetaMorph, Carl Zeiss MicroImaging,
Olympus, and the Open Microscopy Environment consortium respectively.

The API is not stable yet and might change between revisions.
Tested on little-endian platforms only.

For command line usage run ``python tifffile.py --help``

:Authors:
  `Christoph Gohlke <http://www.lfd.uci.edu/~gohlke/>`__,
  Laboratory for Fluorescence Dynamics, University of California, Irvine

:Version: 2012.07.05

Requirements
------------
* `CPython 2.7 or 3.2 <http://www.python.org>`__
* `Numpy 1.6 <http://numpy.scipy.org>`__
* `Matplotlib 1.1 <http://matplotlib.sourceforge.net>`__
  (optional for plotting)
* `tifffile.c 2012.01.01 <http://www.lfd.uci.edu/~gohlke/>`__
  (optional for faster decoding of PackBits and LZW encoded strings)

Acknowledgements
----------------
*  Egor Zindy, University of Manchester, for cz_lsm_scan_info specifics.
*  Wim Lewis, for a bug fix and some read_cz_lsm functions.

References
----------
(1) TIFF 6.0 Specification and Supplements. Adobe Systems Incorporated.
    http://partners.adobe.com/public/developer/tiff/
(2) TIFF File Format FAQ. http://www.awaresystems.be/imaging/tiff/faq.html
(3) MetaMorph Stack (STK) Image File Format.
    http://support.meta.moleculardevices.com/docs/t10243.pdf
(4) File Format Description - LSM 5xx Release 2.0.
    http://ibb.gsf.de/homepage/karsten.rodenacker/IDL/Lsmfile.doc
(5) BioFormats. http://www.loci.wisc.edu/ome/formats.html
(6) The OME-TIFF format.
    http://www.openmicroscopy.org/site/support/file-formats/ome-tiff

Examples
--------
>>> data = numpy.random.rand(301, 219)
>>> imsave('temp.tif', data)
>>> image = imread('temp.tif')
>>> assert numpy.all(image == data)

>>> tif = TIFFfile('test.tif')
>>> images = tif.asarray()
>>> image0 = tif[0].asarray()
>>> for page in tif:
...     for tag in page.tags.values():
...         t = tag.name, tag.value
...     image = page.asarray()
...     if page.is_rgb: pass
...     if page.is_palette:
...         t = page.color_map
...     if page.is_stk:
...         t = page.mm_uic_tags.number_planes
...     if page.is_lsm:
...         t = page.cz_lsm_info
>>> tif.close()

"""
from __future__ import division, print_function
import sys, os, math, zlib, time, struct, warnings, datetime, collections
from xml.etree import cElementTree as ElementTree
import numpy
__all__ = [
 'imsave', 'imread', 'imshow', 'TIFFfile']

def imsave(filename, data, photometric=None, planarconfig=None, resolution=None, description=None, software='tifffile.py', byteorder=None, bigtiff=False):
    """Write image data to TIFF file.

    Image data are written uncompressed in one stripe per plane.
    Dimensions larger than 2 or 3 (depending on photometric mode and
    planar configuration) are flattened and saved as separate pages.

    Parameters
    ----------
    filename : str
        Name of file to write.
    data : array_like
        Input image. The last dimensions are assumed to be image height,
        width, and samples.
    photometric : {'minisblack', 'miniswhite', 'rgb'}
        The color space of the image data.
        By default this setting is inferred from the data shape.
    planarconfig : {'contig', 'planar'}
        Specifies if samples are stored contiguous or in separate planes.
        By default this setting is inferred from the data shape.
        'contig': last dimension contains samples.
        'planar': third last dimension contains samples.
    resolution : ((int, int), (int, int))
        X and Y resolution in dots per inch as rational numbers.
    description : str
        The subject of the image. Saved with the first page only.
    software : str
        Name of the software used to create the image.
        Saved with the first page only.
    byteorder : {'<', '>'}
        The endianness of the data in the file.
        By default this is the system's native byte order.
    bigtiff : bool
        If True the BigTIFF format is used.
        By default the standard TIFF format is used for data less than 2040 MB.

    Examples
    --------
    >>> data = numpy.random.rand(10, 3, 301, 219)
    >>> imsave('temp.tif', data)

    """
    if not photometric in (None, 'minisblack', 'miniswhite', 'rgb'):
        raise AssertionError
    else:
        if not planarconfig in (None, 'contig', 'planar'):
            raise AssertionError
        else:
            if not byteorder in (None, '<', '>'):
                raise AssertionError
            elif byteorder is None:
                byteorder = '<' if sys.byteorder == 'little' else '>'
            else:
                data = numpy.asarray(data, dtype=(byteorder + data.dtype.char), order='C')
                data_shape = shape = data.shape
                data = numpy.atleast_2d(data)
                if not bigtiff:
                    if data.size * data.dtype.itemsize < 2139095040:
                        bigtiff = False
                        offset_size = 4
                        tag_size = 12
                        numtag_format = 'H'
                        offset_format = 'I'
                        val_format = '4s'
                else:
                    bigtiff = True
                    offset_size = 8
                    tag_size = 20
                    numtag_format = 'Q'
                    offset_format = 'Q'
                    val_format = '8s'
                samplesperpixel = 1
                extrasamples = 0
                if photometric is None:
                    if data.ndim > 2:
                        if shape[(-3)] in (3, 4) or shape[(-1)] in (3, 4):
                            photometric = 'rgb'
                    else:
                        photometric = 'minisblack'
                if photometric == 'rgb':
                    if len(shape) < 3:
                        raise ValueError('not a RGB(A) image')
                    if planarconfig is None:
                        planarconfig = 'planar' if shape[(-3)] in (3, 4) else 'contig'
                    if planarconfig == 'contig':
                        if shape[(-1)] not in (3, 4):
                            raise ValueError('not a contiguous RGB(A) image')
                        data = data.reshape((-1, 1) + shape[-3:])
                        samplesperpixel = shape[(-1)]
                    else:
                        if shape[(-3)] not in (3, 4):
                            raise ValueError('not a planar RGB(A) image')
                        data = data.reshape((-1, ) + shape[-3:] + (1, ))
                        samplesperpixel = shape[(-3)]
                    if samplesperpixel == 4:
                        extrasamples = 1
                elif planarconfig:
                    if len(shape) > 2:
                        if planarconfig == 'contig':
                            data = data.reshape((-1, 1) + shape[-3:])
                            samplesperpixel = shape[(-1)]
                        else:
                            data = data.reshape((-1, ) + shape[-3:] + (1, ))
                            samplesperpixel = shape[(-3)]
                        extrasamples = samplesperpixel - 1
                else:
                    planarconfig = None
                    data = data.reshape((-1, 1) + shape[-2:] + (1, ))
                shape = data.shape
                bytestr = bytes if sys.version[0] == '2' else (lambda x: bytes(x, 'ascii'))
                tifftypes = {'B':1,  's':2,  'H':3,  'I':4,  '2I':5,  'b':6,  'h':8, 
                 'i':9,  'f':11,  'd':12,  'Q':16,  'q':17}
                tifftags = {'new_subfile_type':254,  'subfile_type':255,  'image_width':256, 
                 'image_length':257,  'bits_per_sample':258,  'compression':259, 
                 'photometric':262,  'fill_order':266,  'document_name':269, 
                 'image_description':270,  'strip_offsets':273,  'orientation':274, 
                 'samples_per_pixel':277,  'rows_per_strip':278,  'strip_byte_counts':279, 
                 'x_resolution':282,  'y_resolution':283,  'planar_configuration':284, 
                 'page_name':285,  'resolution_unit':296,  'software':305, 
                 'datetime':306,  'predictor':317,  'color_map':320,  'extra_samples':338, 
                 'sample_format':339}
                tags = []
                tag_data = []

                def pack(fmt, *val):
                    return (struct.pack)(byteorder + fmt, *val)

                def tag(name, dtype, number, value, offset=[
 0]):
                    if dtype == 's':
                        value = bytestr(value) + b'\x00'
                        number = len(value)
                        value = (value,)
                    else:
                        t = [
                         pack('HH', tifftags[name], tifftypes[dtype]),
                         pack(offset_format, number)]
                        if len(dtype) > 1:
                            number *= int(dtype[:-1])
                            dtype = dtype[(-1)]
                        if number == 1:
                            if isinstance(value, (tuple, list)):
                                value = value[0]
                            t.append(pack(val_format, pack(dtype, value)))
                        else:
                            if struct.calcsize(dtype) * number <= offset_size:
                                t.append(pack(val_format, pack(str(number) + dtype, *value)))
                            else:
                                t.append(pack(offset_format, 0))
                                tag_data.append((offset[0] + offset_size + 4,
                                 pack(str(number) + dtype, *value)))
                    tags.append((b'').join(t))
                    offset[0] += tag_size

                if software:
                    tag('software', 's', 0, software)
                if description:
                    tag('image_description', 's', 0, description)
                else:
                    if shape != data_shape:
                        tag('image_description', 's', 0, 'shape=(%s)' % ','.join('%i' % i for i in data_shape))
                    tag('datetime', 's', 0, datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S'))
                    writeonce = (len(tags), len(tag_data)) if shape[0] > 1 else None
                    tag('compression', 'H', 1, 1)
                    tag('orientation', 'H', 1, 1)
                    tag('image_width', 'I', 1, shape[(-2)])
                    tag('image_length', 'I', 1, shape[(-3)])
                    tag('new_subfile_type', 'I', 1, 0 if shape[0] == 1 else 2)
                    tag('sample_format', 'H', 1, {'u':1, 
                     'i':2,  'f':3,  'c':6}[data.dtype.kind])
                    tag('photometric', 'H', 1, {'miniswhite':0, 
                     'minisblack':1,  'rgb':2}[photometric])
                    tag('samples_per_pixel', 'H', 1, samplesperpixel)
                    if planarconfig:
                        tag('planar_configuration', 'H', 1, 1 if planarconfig == 'contig' else 2)
                        tag('bits_per_sample', 'H', samplesperpixel, (
                         data.dtype.itemsize * 8,) * samplesperpixel)
                    else:
                        tag('bits_per_sample', 'H', 1, data.dtype.itemsize * 8)
                if extrasamples:
                    if photometric == 'rgb':
                        tag('extra_samples', 'H', 1, 1)
                    else:
                        tag('extra_samples', 'H', extrasamples, (0, ) * extrasamples)
            if resolution:
                tag('x_resolution', '2I', 1, resolution[0])
                tag('y_resolution', '2I', 1, resolution[1])
                tag('resolution_unit', 'H', 1, 2)
        tag('rows_per_strip', 'I', 1, shape[(-3)])
        strip_byte_counts = (
         data[(0, 0)].size * data.dtype.itemsize,) * shape[1]
        tag('strip_byte_counts', offset_format, shape[1], strip_byte_counts)
        tag('strip_offsets', offset_format, shape[1], (0, ) * shape[1])
        fd = open(filename, 'wb')
        seek = fd.seek
        tell = fd.tell

        def write(arg, *args):
            fd.write(pack(arg, *args) if args else arg)

        write({'<':b'II',  '>':b'MM'}[byteorder])
        if bigtiff:
            write('HHH', 43, 8, 0)
        else:
            write('H', 42)
    ifd_offset = tell()
    write(offset_format, 0)
    for i in range(shape[0]):
        pos = tell()
        seek(ifd_offset)
        write(offset_format, pos)
        seek(pos)
        write(numtag_format, len(tags))
        tag_offset = tell()
        write((b'').join(tags))
        ifd_offset = tell()
        write(offset_format, 0)
        for off, dat in tag_data:
            pos = tell()
            seek(tag_offset + off)
            write(offset_format, pos)
            seek(pos)
            write(dat)

        pos = tell()
        if len(strip_byte_counts) == 1:
            seek(ifd_offset - offset_size)
            write(offset_format, pos)
        else:
            seek(pos - offset_size * shape[1])
            strip_offset = pos
            for size in strip_byte_counts:
                write(offset_format, strip_offset)
                strip_offset += size

        seek(pos)
        data[i].tofile(fd)
        fd.flush()
        if writeonce:
            tags = tags[writeonce[0]:]
            d = writeonce[0] * tag_size
            tag_data = [(o - d, v) for o, v in tag_data[writeonce[1]:]]
            writeonce = None

    fd.close()


def imread(filename, *args, **kwargs):
    """Return image data from TIFF file as numpy array.

    The first image series is returned if no arguments are provided.

    Parameters
    ----------
    key : int, slice, or sequence of page indices
        Defines which pages to return as array.
    series : int
        Defines which series of pages to return as array.

    Examples
    --------
    >>> image = imread('test.tif', 0)

    """
    with TIFFfile(filename) as (tif):
        return (tif.asarray)(*args, **kwargs)


class lazyattr(object):
    __doc__ = 'Lazy object attribute whose value is computed on first access.'

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            result = self.func(instance)
            if result is NotImplemented:
                return getattr(super(owner, instance), self.func.__name__)
            setattr(instance, self.func.__name__, result)
            return result


class TIFFfile(object):
    __doc__ = "Read image and meta-data from TIFF, STK, LSM, and FluoView files.\n\n    TIFFfile instances must be closed using the close method.\n\n    Attributes\n    ----------\n    pages : list\n        All TIFFpages in file.\n    series : list of Records(shape, dtype, axes, TIFFpages)\n        TIFF pages with compatible shapes and types.\n\n    All attributes are read-only.\n\n    Examples\n    --------\n    >>> tif = TIFFfile('test.tif')\n    ... try:\n    ...     images = tif.asarray()\n    ... except Exception as e:\n    ...     print(e)\n    ... finally:\n    ...     tif.close()\n\n    "

    def __init__(self, filename):
        """Initialize instance from file."""
        filename = os.path.abspath(filename)
        self._fd = open(filename, 'rb')
        self.fname = os.path.basename(filename)
        self.fpath = os.path.dirname(filename)
        self._tiffs = {self.fname: self}
        self.offset_size = None
        self.pages = []
        try:
            self._fromfile()
        except Exception:
            self._fd.close()
            raise

    def close(self):
        """Close open file handle(s)."""
        if not hasattr(self, 'tiffs'):
            return
        for tif in self._tiffs.values():
            if tif._fd:
                tif._fd.close()
                tif._fd = None

    def _fromfile(self):
        """Read TIFF header and all page records from file."""
        self._fd.seek(0)
        try:
            self.byte_order = {b'II':'<', 
             b'MM':'>'}[self._fd.read(2)]
        except KeyError:
            raise ValueError('not a valid TIFF file')

        version = struct.unpack(self.byte_order + 'H', self._fd.read(2))[0]
        if version == 43:
            self.offset_size, zero = struct.unpack(self.byte_order + 'HH', self._fd.read(4))
            if zero or self.offset_size != 8:
                raise ValueError('not a valid BigTIFF file')
        else:
            if version == 42:
                self.offset_size = 4
            else:
                raise ValueError('not a TIFF file')
        self.pages = []
        while True:
            try:
                page = TIFFpage(self)
                self.pages.append(page)
            except StopIteration:
                break

        if not self.pages:
            raise ValueError('empty TIFF file')

    @lazyattr
    def series(self):
        """Return series of TIFFpage with compatible shape and properties."""
        if self.is_ome:
            series = self._omeseries()
        else:
            if self.is_fluoview:
                dims = {b'X':'X', 
                 b'Y':'Y',  b'Z':'Z',  b'T':'T',  b'WAVELENGTH':'C', 
                 b'TIME':'T',  b'XY':'R',  b'EVENT':'V', 
                 b'EXPOSURE':'L'}
                mmhd = list(reversed(self.pages[0].mm_header.dimensions))
                series = [
                 Record(axes=(''.join(dims.get(i[0].strip().upper(), 'O') for i in mmhd if i[1] > 1)),
                   shape=(tuple(int(i[1]) for i in mmhd if i[1] > 1)),
                   pages=(self.pages),
                   dtype=(numpy.dtype(self.pages[0].dtype)))]
            else:
                if self.is_lsm:
                    lsmi = self.pages[0].cz_lsm_info
                    axes = CZ_SCAN_TYPES[lsmi.scan_type]
                    if self.pages[0].is_rgb:
                        axes = axes.replace('C', '').replace('XY', 'XYC')
                    axes = axes[::-1]
                    shape = [getattr(lsmi, CZ_DIMENSIONS[i]) for i in axes]
                    pages = [p for p in self.pages if not p.is_reduced]
                    series = [
                     Record(axes=axes, shape=shape, pages=pages, dtype=(numpy.dtype(pages[0].dtype)))]
                    if len(pages) != len(self.pages):
                        pages = [p for p in self.pages if p.is_reduced]
                        cp = 1
                        i = 0
                        while cp < len(pages) and i < len(shape) - 2:
                            cp *= shape[i]
                            i += 1

                        shape = shape[:i] + list(pages[0].shape)
                        axes = axes[:i] + 'CYX'
                        series.append(Record(axes=axes, shape=shape, pages=pages, dtype=(numpy.dtype(pages[0].dtype))))
                else:
                    if self.is_nih:
                        series = [
                         Record(pages=(self.pages), shape=((
                          len(self.pages),) + self.pages[0].shape),
                           axes=('I' + self.pages[0].axes),
                           dtype=(numpy.dtype(self.pages[0].dtype)))]
                    else:
                        if self.pages[0].is_shaped:
                            shape = self.pages[0].tags['image_description'].value[7:-1]
                            shape = tuple(int(i) for i in shape.split(b','))
                            series = [
                             Record(pages=(self.pages), shape=shape, axes=('O' * len(shape)),
                               dtype=(numpy.dtype(self.pages[0].dtype)))]
                        else:
                            shapes = []
                            pages = {}
                            for page in self.pages:
                                shape = page.shape + (page.axes,
                                 page.compression in TIFF_DECOMPESSORS)
                                if shape not in pages:
                                    shapes.append(shape)
                                    pages[shape] = [page]
                                else:
                                    pages[shape].append(page)

                            series = [Record(pages=(pages[s]), axes=('I' + s[(-2)] if len(pages[s]) > 1 else s[(-2)]), dtype=(numpy.dtype(pages[s][0].dtype)), shape=((len(pages[s]),) + s[:-2] if len(pages[s]) > 1 else s[:-2])) for s in shapes]
        return series

    def asarray(self, key=None, series=None):
        """Return image data of multiple TIFF pages as numpy array.

        By default the first image series is returned.

        Parameters
        ----------
        key : int, slice, or sequence of page indices
            Defines which pages to return as array.
        series : int
            Defines which series of pages to return as array.

        """
        if key is None:
            if series is None:
                series = 0
        else:
            if series is not None:
                pages = self.series[series].pages
            else:
                pages = self.pages
        if key is None:
            pass
        else:
            if isinstance(key, int):
                pages = [
                 pages[key]]
            else:
                if isinstance(key, slice):
                    pages = pages[key]
                else:
                    if isinstance(key, collections.Iterable):
                        pages = [pages[k] for k in key]
                    else:
                        raise TypeError('key must be an int, slice, or sequence')
            if len(pages) == 1:
                return pages[0].asarray()
            if self.is_nih:
                result = numpy.vstack(p.asarray(colormapped=False, squeeze=False) for p in pages)
                if pages[0].is_palette:
                    result = numpy.take((pages[0].color_map), result, axis=1)
                    result = numpy.swapaxes(result, 0, 1)
            else:
                if self.is_ome:
                    if any(p is None for p in pages):
                        firstpage = next(p for p in pages if p)
                        nopage = numpy.zeros_like(firstpage.asarray())
                    result = numpy.vstack((p.asarray() if p else nopage) for p in pages)
                else:
                    if key is None:
                        try:
                            result.shape = self.series[series].shape
                        except ValueError:
                            warnings.warn('failed to reshape %s to %s' % (
                             result.shape, self.series[series].shape))
                            result.shape = (-1, ) + pages[0].shape

                    else:
                        result.shape = (-1, ) + pages[0].shape
                return result

    def _omeseries(self):
        """Return image series in OME-TIFF files."""
        root = ElementTree.XML(self.pages[0].tags['image_description'].value)
        uuid = root.attrib.get('UUID', None)
        self._tiffs = {uuid: self}
        modulo = {}
        result = []
        for element in root:
            if element.tag.endswith('BinaryOnly'):
                warnings.warn('not an OME-TIFF master file')
                break
            if element.tag.endswith('StructuredAnnotations'):
                for annot in element:
                    if not annot.attrib.get('Namespace', '').endswith('modulo'):
                        pass
                    else:
                        for value in annot:
                            for modul in value:
                                for along in modul:
                                    if not along.tag[:-1].endswith('Along'):
                                        pass
                                    else:
                                        axis = along.tag[(-1)]
                                        newaxis = along.attrib.get('Type', 'other')
                                        newaxis = AXES_LABELS[newaxis]
                                        if 'Start' in along.attrib:
                                            labels = range(int(along.attrib['Start']), int(along.attrib['End']) + 1, int(along.attrib.get('Step', 1)))
                                        else:
                                            labels = [label.text for label in along if label.tag.endswith('Label')]
                                        modulo[axis] = (
                                         newaxis, labels)

            if not element.tag.endswith('Image'):
                pass
            else:
                for pixels in element:
                    if not pixels.tag.endswith('Pixels'):
                        continue
                    atr = pixels.attrib
                    axes = ''.join(reversed(atr['DimensionOrder']))
                    shape = list(int(atr[('Size' + ax)]) for ax in axes)
                    size = numpy.prod(shape[:-2])
                    ifds = [None] * size
                    for data in pixels:
                        if not data.tag.endswith('TiffData'):
                            continue
                        atr = data.attrib
                        ifd = int(atr.get('IFD', 0))
                        num = int(atr.get('NumPlanes', 1 if 'IFD' in atr else 0))
                        num = int(atr.get('PlaneCount', num))
                        idx = [int(atr.get('First' + ax, 0)) for ax in axes[:-2]]
                        idx = numpy.ravel_multi_index(idx, shape[:-2])
                        for uuid in data:
                            if uuid.tag.endswith('UUID'):
                                if uuid.text not in self._tiffs:
                                    fn = uuid.attrib['FileName']
                                    try:
                                        tf = TIFFfile(os.path.join(self.fpath, fn))
                                    except (IOError, ValueError):
                                        warnings.warn('failed to read %s' % fn)
                                        break

                                    self._tiffs[uuid.text] = tf
                                pages = self._tiffs[uuid.text].pages
                                try:
                                    for i in range(num if num else len(pages)):
                                        ifds[idx + i] = pages[(ifd + i)]

                                except IndexError:
                                    warnings.warn('ome-xml: index out of range')

                                break
                        else:
                            pages = self.pages
                            try:
                                for i in range(num if num else len(pages)):
                                    ifds[idx + i] = pages[(ifd + i)]

                            except IndexError:
                                warnings.warn('ome-xml: index out of range')

                    result.append(Record(axes=axes, shape=shape, pages=ifds, dtype=(numpy.dtype(ifds[0].dtype))))

        for record in result:
            for axis, (newaxis, labels) in modulo.items():
                i = record.axes.index(axis)
                size = len(labels)
                if record.shape[i] == size:
                    record.axes = record.axes.replace(axis, newaxis, 1)
                else:
                    record.shape[i] //= size
                    record.shape.insert(i + 1, size)
                    record.axes = record.axes.replace(axis, axis + newaxis, 1)

        return result

    def __len__(self):
        """Return number of image pages in file."""
        return len(self.pages)

    def __getitem__(self, key):
        """Return specified page."""
        return self.pages[key]

    def __iter__(self):
        """Return iterator over pages."""
        return iter(self.pages)

    def __str__(self):
        """Return string containing information about file."""
        result = [
         self.fname.capitalize(),
         '%.2f MB' % (self.fstat[6] / 1048576),
         {'<':'little endian', 
          '>':'big endian'}[self.byte_order]]
        if self.is_bigtiff:
            result.append('bigtiff')
        if len(self.pages) > 1:
            result.append('%i pages' % len(self.pages))
        if len(self.series) > 1:
            result.append('%i series' % len(self.series))
        if len(self._tiffs) > 1:
            result.append('%i files' % len(self._tiffs))
        return ', '.join(result)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @lazyattr
    def fstat(self):
        return os.fstat(self._fd.fileno())

    @lazyattr
    def is_bigtiff(self):
        return self.offset_size != 4

    @lazyattr
    def is_rgb(self):
        return all(p.is_rgb for p in self.pages)

    @lazyattr
    def is_palette(self):
        return all(p.is_palette for p in self.pages)

    @lazyattr
    def is_stk(self):
        return all(p.is_stk for p in self.pages)

    @lazyattr
    def is_lsm(self):
        return self.pages[0].is_lsm

    @lazyattr
    def is_nih(self):
        return self.pages[0].is_nih

    @lazyattr
    def is_fluoview(self):
        return self.pages[0].is_fluoview

    @lazyattr
    def is_ome(self):
        return self.pages[0].is_ome


class TIFFpage(object):
    __doc__ = "A TIFF image file directory (IFD).\n\n    Attributes\n    ----------\n    index : int\n        Index of page in file.\n    dtype : str {TIFF_SAMPLE_DTYPES}\n        Data type of image, colormapped if applicable.\n    shape : tuple\n        Dimensions of the image array in TIFF page,\n        colormapped and with one alpha channel if applicable.\n    axes : str\n        Axes label codes:\n        'X' width, 'Y' height, 'S' sample, 'P' plane, 'I' image series,\n        'Z' depth, 'C' color|em-wavelength|channel, 'E' ex-wavelength|lambda,\n        'T' time, 'R' region|tile, 'A' angle, 'F' phase, 'H' lifetime,\n        'L' exposure, 'V' event, 'O' unknown, '_' missing\n    tags : TiffTags\n        Dictionary of tags in page.\n        Tag values are also directly accessible as attributes.\n    color_map : numpy array\n        Color look up table if exists.\n    mm_uic_tags: Record(dict)\n        Consolidated MetaMorph mm_uic# tags, if exists.\n    cz_lsm_scan_info: Record(dict)\n        LSM scan info attributes, if exists.\n\n    All attributes are read-only.\n\n    "

    def __init__(self, parent):
        """Initialize instance from file."""
        self.parent = parent
        self.index = len(parent.pages)
        self.shape = self._shape = ()
        self.dtype = self._dtype = None
        self.axes = ''
        self.tags = TiffTags()
        self._fromfile()
        self._process_tags()

    def _fromfile(self):
        """Read TIFF IFD structure and its tags from file.

        File cursor must be at storage position of IFD offset and is left at
        offset to next IFD.

        Raises StopIteration if offset (first bytes read) is 0.

        """
        fd = self.parent._fd
        byte_order = self.parent.byte_order
        offset_size = self.parent.offset_size
        fmt = {4:'I', 
         8:'Q'}[offset_size]
        offset = struct.unpack(byte_order + fmt, fd.read(offset_size))[0]
        if not offset:
            raise StopIteration()
        tags = self.tags
        fd.seek(offset)
        fmt, size = {4:('H', 2),  8:('Q', 8)}[offset_size]
        try:
            numtags = struct.unpack(byte_order + fmt, fd.read(size))[0]
        except Exception:
            warnings.warn('corrupted page list')
            raise StopIteration()

        for _ in range(numtags):
            tag = TIFFtag(self.parent)
            tags[tag.name] = tag

        if self.is_lsm:
            pos = fd.tell()
            for name, reader in CZ_LSM_INFO_READERS.items():
                try:
                    offset = self.cz_lsm_info[('offset_' + name)]
                except KeyError:
                    continue

                if not offset:
                    pass
                else:
                    fd.seek(offset)
                    try:
                        setattr(self, 'cz_lsm_' + name, reader(fd, byte_order))
                    except ValueError:
                        pass

            fd.seek(pos)

    def _process_tags(self):
        """Validate standard tags and initialize attributes.

        Raise ValueError if tag values are not supported.

        """
        tags = self.tags
        for code, (name, default, dtype, count, validate) in TIFF_TAGS.items():
            if not (name in tags or default is None):
                tags[name] = TIFFtag(code, dtype=dtype, count=count, value=default,
                  name=name)
            if name in tags and validate:
                try:
                    if tags[name].count == 1:
                        setattr(self, name, validate[tags[name].value])
                    else:
                        setattr(self, name, tuple(validate[value] for value in tags[name].value))
                except KeyError:
                    raise ValueError('%s.value (%s) not supported' % (
                     name, tags[name].value))

        tag = tags['bits_per_sample']
        if tag.count == 1:
            self.bits_per_sample = tag.value
        else:
            value = tag.value[:self.samples_per_pixel]
            if any(v - value[0] for v in value):
                self.bits_per_sample = value
            else:
                self.bits_per_sample = value[0]
            tag = tags['sample_format']
            if tag.count == 1:
                self.sample_format = TIFF_SAMPLE_FORMATS[tag.value]
            else:
                value = tag.value[:self.samples_per_pixel]
                if any(v - value[0] for v in value):
                    self.sample_format = [TIFF_SAMPLE_FORMATS[v] for v in value]
                else:
                    self.sample_format = TIFF_SAMPLE_FORMATS[value[0]]
                self.strips_per_image = int(math.floor(float(self.image_length + self.rows_per_strip - 1) / self.rows_per_strip))
                key = (
                 self.sample_format, self.bits_per_sample)
                self.dtype = self._dtype = TIFF_SAMPLE_DTYPES.get(key, None)
                if self.is_stk:
                    planes = tags['mm_uic2'].count
                    self.mm_uic_tags = Record(tags['mm_uic2'].value)
                    for key in ('mm_uic3', 'mm_uic4', 'mm_uic1'):
                        if key in tags:
                            self.mm_uic_tags.update(tags[key].value)

                    if self.planar_configuration == 'contig':
                        self._shape = (
                         planes, 1, self.image_length,
                         self.image_width, self.samples_per_pixel)
                        self.shape = tuple(self._shape[i] for i in (0, 2, 3, 4))
                        self.axes = 'PYXS'
                    else:
                        self._shape = (
                         planes, self.samples_per_pixel,
                         self.image_length, self.image_width, 1)
                        self.shape = self._shape[:4]
                        self.axes = 'PSYX'
                else:
                    if self.is_palette:
                        self.dtype = self.tags['color_map'].dtype[1]
                        self.color_map = numpy.array(self.color_map, self.dtype)
                        dmax = self.color_map.max()
                        if dmax < 256:
                            self.dtype = numpy.uint8
                            self.color_map = self.color_map.astype(self.dtype)
                        self.color_map.shape = (3, -1)
                        self._shape = (1, 1, self.image_length, self.image_width, 1)
                        if self.color_map.shape[1] >= 2 ** self.bits_per_sample:
                            self.shape = (
                             3, self.image_length, self.image_width)
                            self.axes = 'SYX'
                        else:
                            self.shape = (
                             self.image_length, self.image_width)
                            self.axes = 'YX'
                    else:
                        if self.is_rgb or self.samples_per_pixel > 1:
                            if self.planar_configuration == 'contig':
                                self._shape = (
                                 1, 1, self.image_length, self.image_width,
                                 self.samples_per_pixel)
                                self.shape = (self.image_length, self.image_width,
                                 self.samples_per_pixel)
                                self.axes = 'YXS'
                            else:
                                self._shape = (
                                 1, self.samples_per_pixel, self.image_length,
                                 self.image_width, 1)
                                self.shape = self._shape[1:-1]
                                self.axes = 'SYX'
                            if self.is_rgb:
                                if 'extra_samples' in self.tags:
                                    extra_samples = self.extra_samples
                                    if self.tags['extra_samples'].count == 1:
                                        extra_samples = (
                                         extra_samples,)
                                    for exs in extra_samples:
                                        if exs in ('unassalpha', 'assocalpha'):
                                            if self.planar_configuration == 'contig':
                                                self.shape = self.shape[:2] + (4, )
                                            else:
                                                self.shape = (4, ) + self.shape[1:]
                                            break

                        else:
                            self._shape = (
                             1, 1, self.image_length, self.image_width, 1)
                            self.shape = self._shape[2:4]
                            self.axes = 'YX'
        if not self.compression:
            if 'strip_byte_counts' not in tags:
                self.strip_byte_counts = numpy.prod(self.shape) * (self.bits_per_sample // 8)

    def asarray(self, squeeze=True, colormapped=True, rgbonly=True):
        """Read image data from file and return as numpy array.

        Raise ValueError if format is unsupported.
        If any argument is False, the shape of the returned array might be
        different from the page shape.

        Parameters
        ----------
        squeeze : bool
            If True all length-1 dimensions (except X and Y) are
            squeezed out from result.
        colormapped : bool
            If True color mapping is applied for palette-indexed images.
        rgbonly : bool
            If True return RGB(A) image without additional extra samples.

        """
        fd = self.parent._fd
        if not fd:
            raise IOError('TIFF file is not open')
        if self.dtype is None:
            raise ValueError('data type not supported: %s%i' % (
             self.sample_format, self.bits_per_sample))
        if self.compression not in TIFF_DECOMPESSORS:
            raise ValueError('cannot decompress %s' % self.compression)
        if 'ycbcr_subsampling' in self.tags:
            if self.tags['ycbcr_subsampling'].value not in (1, (1, 1)):
                raise ValueError('YCbCr subsampling not supported')
        tag = self.tags['sample_format']
        if tag.count != 1:
            if any(i - tag.value[0] for i in tag.value):
                raise ValueError("sample formats don't match %s" % str(tag.value))
        dtype = self._dtype
        shape = self._shape
        image_width = self.image_width
        image_length = self.image_length
        typecode = self.parent.byte_order + dtype
        bits_per_sample = self.bits_per_sample
        if self.is_tiled:
            if 'tile_offsets' in self.tags:
                byte_counts = self.tile_byte_counts
                offsets = self.tile_offsets
            else:
                byte_counts = self.strip_byte_counts
                offsets = self.strip_offsets
            tile_width = self.tile_width
            tile_length = self.tile_length
            tw = (image_width + tile_width - 1) // tile_width
            tl = (image_length + tile_length - 1) // tile_length
            shape = shape[:-3] + (tl * tile_length, tw * tile_width, shape[(-1)])
            tile_shape = (tile_length, tile_width, shape[(-1)])
            runlen = tile_width
        else:
            byte_counts = self.strip_byte_counts
            offsets = self.strip_offsets
            runlen = image_width
        try:
            offsets[0]
        except TypeError:
            offsets = (
             offsets,)
            byte_counts = (byte_counts,)

        if any(o < 2 for o in offsets):
            raise ValueError('corrupted file')
        if not self.is_tiled:
            if self.is_stk or not self.compression and bits_per_sample in (8, 16, 32,
                                                                           64) and all(offsets[i] == offsets[(i + 1)] - byte_counts[i] for i in range(len(offsets) - 1)):
                fd.seek(offsets[0])
                result = numpy.fromfile(fd, typecode, numpy.prod(shape))
                result = result.astype('=' + dtype)
        if self.planar_configuration == 'contig':
            runlen *= self.samples_per_pixel
        if bits_per_sample in (8, 16, 32, 64, 128):
            if bits_per_sample * runlen % 8:
                raise ValueError('data and sample size mismatch')
            unpack = lambda x: numpy.fromstring(x, typecode)
        else:
            if isinstance(bits_per_sample, tuple):
                unpack = lambda x: unpackrgb(x, typecode, bits_per_sample)
            else:
                unpack = lambda x: unpackints(x, typecode, bits_per_sample, runlen)
            decompress = TIFF_DECOMPESSORS[self.compression]
            if self.is_tiled:
                result = numpy.empty(shape, dtype)
                tw, tl, pl = (0, 0, 0)
                for offset, bytecount in zip(offsets, byte_counts):
                    fd.seek(offset)
                    tile = unpack(decompress(fd.read(bytecount)))
                    tile.shape = tile_shape
                    result[0, pl, tl:tl + tile_length, tw:tw + tile_width, :] = tile
                    del tile
                    tw += tile_width
                    if tw >= shape[(-2)]:
                        tw, tl = 0, tl + tile_length
                        if tl >= shape[(-3)]:
                            tl, pl = 0, pl + 1

                result = result[..., :image_length, :image_width, :]
            else:
                result = numpy.empty(shape, dtype).reshape(-1)
                index = 0
                for offset, bytecount in zip(offsets, byte_counts):
                    fd.seek(offset)
                    stripe = unpack(decompress(fd.read(bytecount)))
                    size = min(result.size, stripe.size)
                    result[index:index + size] = stripe[:size]
                    del stripe
                    index += size

        result.shape = self._shape
        if self.predictor == 'horizontal':
            if not (self.parent.is_lsm and not self.compression):
                numpy.cumsum(result, axis=3, dtype=dtype, out=result)
        if colormapped and self.is_palette:
            if self.color_map.shape[1] >= 2 ** bits_per_sample:
                result = numpy.take((self.color_map), result, axis=1)
        else:
            if rgbonly:
                if self.is_rgb:
                    if 'extra_samples' in self.tags:
                        extra_samples = self.extra_samples
                        if self.tags['extra_samples'].count == 1:
                            extra_samples = (
                             extra_samples,)
                        for i, exs in enumerate(extra_samples):
                            if exs in ('unassalpha', 'assocalpha'):
                                if self.planar_configuration == 'contig':
                                    result = result[(..., [0, 1, 2, 3 + i])]
                                else:
                                    result = result[:, [0, 1, 2, 3 + i]]
                                break
                        else:
                            if self.planar_configuration == 'contig':
                                result = result[..., :3]
                            else:
                                result = result[:, :3]

        if squeeze:
            try:
                result.shape = self.shape
            except ValueError:
                pass

        return result

    def __str__(self):
        """Return string containing information about page."""
        s = ', '.join(s for s in (
         ' x '.join(str(i) for i in self.shape),
         str(numpy.dtype(self.dtype)),
         '%s bit' % str(self.bits_per_sample),
         self.photometric,
         self.compression if self.compression else 'raw',
         ','.join(t[3:] for t in ('is_stk', 'is_lsm', 'is_nih', 'is_ome', 'is_fluoview', 'is_reduced',
                         'is_tiled') if getattr(self, t))) if s)
        return 'Page %i: %s' % (self.index, s)

    def __getattr__(self, name):
        """Return tag value."""
        if name in self.tags:
            value = self.tags[name].value
            setattr(self, name, value)
            return value
        raise AttributeError(name)

    @lazyattr
    def is_rgb(self):
        """True if page contains a RGB image."""
        return self.tags['photometric'].value == 2

    @lazyattr
    def is_palette(self):
        """True if page contains a palette-colored image."""
        return self.tags['photometric'].value == 3

    @lazyattr
    def is_tiled(self):
        """True if page contains tiled image."""
        return 'tile_width' in self.tags

    @lazyattr
    def is_reduced(self):
        """True if page is a reduced image of another image."""
        return bool(self.tags['new_subfile_type'].value & 1)

    @lazyattr
    def is_stk(self):
        """True if page contains MM_UIC2 tag."""
        return 'mm_uic2' in self.tags

    @lazyattr
    def is_lsm(self):
        """True if page contains LSM CZ_LSM_INFO tag."""
        return 'cz_lsm_info' in self.tags

    @lazyattr
    def is_fluoview(self):
        """True if page contains FluoView MM_STAMP tag."""
        return 'mm_stamp' in self.tags

    @lazyattr
    def is_nih(self):
        """True if page contains NIH image header."""
        return 'nih_image_header' in self.tags

    @lazyattr
    def is_ome(self):
        """True if page contains OME-XML in image_description tag."""
        return 'image_description' in self.tags and self.tags['image_description'].value.startswith(b'<?xml version=')

    @lazyattr
    def is_shaped(self):
        """True if page contains shape in image_description tag."""
        return 'image_description' in self.tags and self.tags['image_description'].value.startswith(b'shape=(')


class TIFFtag(object):
    __doc__ = 'A TIFF tag structure.\n\n    Attributes\n    ----------\n    name : string\n        Attribute name of tag.\n    code : int\n        Decimal code of tag.\n    dtype : str\n        Datatype of tag data. One of TIFF_DATA_TYPES.\n    count : int\n        Number of values.\n    value : various types\n        Tag data. For codes in CUSTOM_TAGS the 4 bytes file content.\n    value_offset : int\n        Location of value in file\n\n    All attributes are read-only.\n\n    '
    __slots__ = ('code', 'name', 'count', 'dtype', 'value', 'value_offset', '_offset')

    def __init__(self, arg, **kwargs):
        """Initialize instance from file or arguments."""
        self._offset = None
        if hasattr(arg, '_fd'):
            (self._fromfile)(arg, **kwargs)
        else:
            (self._fromdata)(arg, **kwargs)

    def _fromdata(self, code, dtype, count, value, name=None):
        """Initialize instance from arguments."""
        self.code = int(code)
        self.name = name if name else str(code)
        self.dtype = TIFF_DATA_TYPES[dtype]
        self.count = int(count)
        self.value = value

    def _fromfile(self, parent):
        """Read tag structure from open file. Advance file cursor."""
        fd = parent._fd
        byte_order = parent.byte_order
        self._offset = fd.tell()
        self.value_offset = self._offset + parent.offset_size + 4
        fmt, size = {4:('HHI4s', 12), 
         8:('HHQ8s', 20)}[parent.offset_size]
        data = fd.read(size)
        code, dtype = struct.unpack(byte_order + fmt[:2], data[:4])
        count, value = struct.unpack(byte_order + fmt[2:], data[4:])
        if code in TIFF_TAGS:
            name = TIFF_TAGS[code][0]
        else:
            if code in CUSTOM_TAGS:
                name = CUSTOM_TAGS[code][0]
            else:
                name = str(code)
            try:
                dtype = TIFF_DATA_TYPES[dtype]
            except KeyError:
                raise ValueError('unknown TIFF tag data type %i' % dtype)

            fmt = '%s%i%s' % (byte_order, count * int(dtype[0]), dtype[1])
            size = struct.calcsize(fmt)
            if size > parent.offset_size or code in CUSTOM_TAGS:
                pos = fd.tell()
                tof = {4:'I',  8:'Q'}[parent.offset_size]
                self.value_offset = struct.unpack(byte_order + tof, value)[0]
                fd.seek(self.value_offset)
                if code in CUSTOM_TAGS:
                    readfunc = CUSTOM_TAGS[code][1]
                    value = readfunc(fd, byte_order, dtype, count)
                    fd.seek(0, 2)
                    if isinstance(value, dict):
                        value = Record(value)
                else:
                    if code in TIFF_TAGS or dtype[(-1)] == 's':
                        value = struct.unpack(fmt, fd.read(size))
                    else:
                        value = read_numpy(fd, byte_order, dtype, count)
                        fd.seek(0, 2)
                fd.seek(pos)
            else:
                value = struct.unpack(fmt, value[:size])
        if code not in CUSTOM_TAGS:
            if len(value) == 1:
                value = value[0]
        if dtype.endswith('s'):
            value = stripnull(value)
        self.code = code
        self.name = name
        self.dtype = dtype
        self.count = count
        self.value = value

    def __str__(self):
        """Return string containing information about tag."""
        return ' '.join(str(getattr(self, s)) for s in self.__slots__)


class Record(dict):
    __doc__ = 'Dictionary with attribute access.\n\n    Can also be initialized with numpy.core.records.record.\n\n    '
    __slots__ = ()

    def __init__(self, arg=None, **kwargs):
        if kwargs:
            arg = kwargs
        else:
            if arg is None:
                arg = {}
        try:
            dict.__init__(self, arg)
        except TypeError:
            for i, name in enumerate(arg.dtype.names):
                v = arg[i]
                self[name] = v if v.dtype.char != 'S' else stripnull(v)

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def __str__(self):
        """Pretty print Record."""
        s = []
        lists = []
        for k in sorted(self):
            if k.startswith('_'):
                pass
            else:
                v = self[k]
                if isinstance(v, (list, tuple)):
                    if len(v):
                        if isinstance(v[0], Record):
                            lists.append((k, v))
                            continue
                        elif isinstance(v[0], TIFFpage):
                            v = [i.index for i in v if i]
                s.append(('* %s: %s' % (k, str(v))).split('\n', 1)[0][:PRINT_LINE_LEN])

        for k, v in lists:
            l = []
            for i, w in enumerate(v):
                l.append('* %s[%i]\n  %s' % (k, i,
                 str(w).replace('\n', '\n  ')))

            s.append('\n'.join(l))

        return '\n'.join(s)


class TiffTags(Record):
    __doc__ = 'Dictionary of TIFFtags with attribute access.'

    def __str__(self):
        """Return string with information about all tags."""
        s = []
        for tag in sorted((self.values()), key=(lambda x: x.code)):
            typecode = '%i%s' % (tag.count * int(tag.dtype[0]), tag.dtype[1])
            line = '* %i %s (%s) %s' % (tag.code, tag.name, typecode,
             str(tag.value).split('\n', 1)[0])
            s.append(line[:PRINT_LINE_LEN])

        return '\n'.join(s)


def read_bytes(fd, byte_order, dtype, count):
    """Read tag data from file and return as byte string."""
    return numpy.fromfile(fd, byte_order + dtype[(-1)], count).tostring()


def read_numpy(fd, byte_order, dtype, count):
    """Read tag data from file and return as numpy array."""
    return numpy.fromfile(fd, byte_order + dtype[(-1)], count)


def read_nih_image_header(fd, byte_order, dtype, count):
    """Read NIH_IMAGE_HEADER tag from file and return as dictionary."""
    fd.seek(12, 1)
    return {'version': struct.unpack(byte_order + 'H', fd.read(2))[0]}


def read_mm_header(fd, byte_order, dtype, count):
    """Read MM_HEADER tag from file and return as numpy.rec.array."""
    return numpy.rec.fromfile(fd, MM_HEADER, 1, byteorder=byte_order)[0]


def read_mm_stamp(fd, byte_order, dtype, count):
    """Read MM_STAMP tag from file and return as numpy.array."""
    return numpy.fromfile(fd, byte_order + '8f8', 1)[0]


def read_mm_uic1(fd, byte_order, dtype, count):
    """Read MM_UIC1 tag from file and return as dictionary."""
    t = fd.read(8 * count)
    t = struct.unpack('%s%iI' % (byte_order, 2 * count), t)
    return dict((MM_TAG_IDS[k], v) for k, v in zip(t[::2], t[1::2]) if k in MM_TAG_IDS)


def read_mm_uic2(fd, byte_order, dtype, count):
    """Read MM_UIC2 tag from file and return as dictionary."""
    result = {'number_planes': count}
    values = numpy.fromfile(fd, byte_order + 'I', 6 * count)
    result['z_distance'] = values[0::6] // values[1::6]
    return result


def read_mm_uic3(fd, byte_order, dtype, count):
    """Read MM_UIC3 tag from file and return as dictionary."""
    t = numpy.fromfile(fd, byte_order + 'I', 2 * count)
    return {'wavelengths': t[0::2] // t[1::2]}


def read_mm_uic4(fd, byte_order, dtype, count):
    """Read MM_UIC4 tag from file and return as dictionary."""
    t = struct.unpack(byte_order + 'hI' * count, fd.read(6 * count))
    return dict((MM_TAG_IDS[k], v) for k, v in zip(t[::2], t[1::2]) if k in MM_TAG_IDS)


def read_cz_lsm_info(fd, byte_order, dtype, count):
    """Read CS_LSM_INFO tag from file and return as numpy.rec.array."""
    result = numpy.rec.fromfile(fd, CZ_LSM_INFO, 1, byteorder=byte_order)[0]
    {50350412:'1.3',  67127628:'2.0'}[result.magic_number]
    return result


def read_cz_lsm_time_stamps(fd, byte_order):
    """Read LSM time stamps from file and return as list."""
    size, count = struct.unpack(byte_order + 'II', fd.read(8))
    if size != 8 + 8 * count:
        raise ValueError('lsm_time_stamps block is too short')
    return struct.unpack('%s%dd' % (byte_order, count), fd.read(8 * count))


def read_cz_lsm_event_list(fd, byte_order):
    """Read LSM events from file and return as list of (time, type, text)."""
    count = struct.unpack(byte_order + 'II', fd.read(8))[1]
    events = []
    while count > 0:
        esize, etime, etype = struct.unpack(byte_order + 'IdI', fd.read(16))
        etext = stripnull(fd.read(esize - 16))
        events.append((etime, etype, etext))
        count -= 1

    return events


def read_cz_lsm_scan_info(fd, byte_order):
    """Read LSM scan information from file and return as Record."""
    block = Record()
    blocks = [block]
    unpack = struct.unpack
    if 268435456 != struct.unpack(byte_order + 'I', fd.read(4))[0]:
        raise ValueError('not a lsm_scan_info structure')
    fd.read(8)
    while 1:
        entry, dtype, size = unpack(byte_order + 'III', fd.read(12))
        if dtype == 2:
            value = stripnull(fd.read(size))
        else:
            if dtype == 4:
                value = unpack(byte_order + 'i', fd.read(4))[0]
            else:
                if dtype == 5:
                    value = unpack(byte_order + 'd', fd.read(8))[0]
                else:
                    value = 0
                if entry in CZ_LSM_SCAN_INFO_ARRAYS:
                    blocks.append(block)
                    name = CZ_LSM_SCAN_INFO_ARRAYS[entry]
                    newobj = []
                    setattr(block, name, newobj)
                    block = newobj
                else:
                    if entry in CZ_LSM_SCAN_INFO_STRUCTS:
                        blocks.append(block)
                        newobj = Record()
                        block.append(newobj)
                        block = newobj
                    else:
                        if entry in CZ_LSM_SCAN_INFO_ATTRIBUTES:
                            name = CZ_LSM_SCAN_INFO_ATTRIBUTES[entry]
                            setattr(block, name, value)
                        else:
                            if entry == 4294967295:
                                block = blocks.pop()
                            else:
                                setattr(block, 'unknown_%x' % entry, value)
        if not blocks:
            break

    return block


def _replace_by(module_function, warn=False):
    """Try replace decorated function by module.function."""

    def decorate(func, module_function=module_function, warn=warn):
        sys.path.append(os.path.dirname(__file__))
        try:
            module, function = module_function.split('.')
            func, oldfunc = getattr(__import__(module), function), func
            globals()['__old_' + func.__name__] = oldfunc
        except Exception:
            if warn:
                warnings.warn('failed to import %s' % module_function)

        sys.path.pop()
        return func

    return decorate


@_replace_by('_tifffile.decodepackbits')
def decodepackbits(encoded):
    """Decompress PackBits encoded byte string.

    PackBits is a simple byte-oriented run-length compression scheme.

    """
    func = ord if sys.version[0] == '2' else (lambda x: x)
    result = []
    i = 0
    try:
        while 1:
            n = func(encoded[i]) + 1
            i += 1
            if n < 129:
                result.extend(encoded[i:i + n])
                i += n
            else:
                if n > 129:
                    result.extend(encoded[i:i + 1] * (258 - n))
                    i += 1

    except IndexError:
        pass

    if sys.version[0] == '2':
        return (b'').join(result)
    else:
        return bytes(result)


@_replace_by('_tifffile.decodelzw')
def decodelzw(encoded):
    """Decompress LZW (Lempel-Ziv-Welch) encoded TIFF strip (byte string).

    The strip must begin with a CLEAR code and end with an EOI code.

    This is an implementation of the LZW decoding algorithm described in (1).
    It is not compatible with old style LZW compressed files like quad-lzw.tif.

    """
    unpack = struct.unpack
    if sys.version[0] == '2':
        newtable = [chr(i) for i in range(256)]
    else:
        newtable = [bytes([i]) for i in range(256)]
    newtable.extend((0, 0))

    def next_code():
        start = bitcount // 8
        s = encoded[start:start + 4]
        try:
            code = unpack('>I', s)[0]
        except Exception:
            code = unpack('>I', s + b'\x00' * (4 - len(s)))[0]

        code = code << bitcount % 8
        code = code & mask
        return code >> shr

    switchbitch = {255:(
      9, 23, int('111111111' + '0' * 23, 2)), 
     511:(
      10, 22, int('1111111111' + '0' * 22, 2)), 
     1023:(
      11, 21, int('11111111111' + '0' * 21, 2)), 
     2047:(
      12, 20, int('11111111111100000000000000000000', 2))}
    bitw, shr, mask = switchbitch[255]
    bitcount = 0
    if len(encoded) < 4:
        raise ValueError('strip must be at least 4 characters long')
    if next_code() != 256:
        raise ValueError('strip must begin with CLEAR code')
    code = oldcode = 0
    result = []
    while 1:
        code = next_code()
        bitcount += bitw
        if code == 257:
            break
        if code == 256:
            table = newtable[:]
            lentable = 258
            bitw, shr, mask = switchbitch[255]
            code = next_code()
            bitcount += bitw
            if code == 257:
                break
            result.append(table[code])
        else:
            if code < lentable:
                decoded = table[code]
                newcode = table[oldcode] + decoded[:1]
            else:
                newcode = table[oldcode]
                newcode += newcode[:1]
                decoded = newcode
            result.append(decoded)
            table.append(newcode)
            lentable += 1
        oldcode = code
        if lentable in switchbitch:
            bitw, shr, mask = switchbitch[lentable]

    if code != 257:
        raise ValueError('unexpected end of stream (code %i)' % code)
    return (b'').join(result)


@_replace_by('_tifffile.unpackints')
def unpackints(data, dtype, itemsize, runlen=0):
    """Decompress byte string to array of integers of any bit size <= 32.

    Parameters
    ----------
    data : byte str
        Data to decompress.
    dtype : numpy.dtype or str
        A numpy boolean or integer type.
    itemsize : int
        Number of bits per integer.
    runlen : int
        Number of consecutive integers, after which to start at next byte.

    """
    if itemsize == 1:
        data = numpy.fromstring(data, '|B')
        data = numpy.unpackbits(data)
        if runlen % 8:
            data = data.reshape(-1, runlen + (8 - runlen % 8))
            data = data[:, :runlen].reshape(-1)
        return data.astype(dtype)
    else:
        dtype = numpy.dtype(dtype)
        if itemsize in (8, 16, 32, 64):
            return numpy.fromstring(data, dtype)
        if itemsize < 1 or itemsize > 32:
            raise ValueError('itemsize out of range: %i' % itemsize)
        if dtype.kind not in 'biu':
            raise ValueError('invalid dtype')
        itembytes = next(i for i in (1, 2, 4, 8) if 8 * i >= itemsize)
        if itembytes != dtype.itemsize:
            raise ValueError('dtype.itemsize too small')
        if runlen == 0:
            runlen = len(data) // itembytes
        skipbits = runlen * itemsize % 8
        if skipbits:
            skipbits = 8 - skipbits
        shrbits = itembytes * 8 - itemsize
        bitmask = int(itemsize * '1' + '0' * shrbits, 2)
        dtypestr = '>' + dtype.char
        unpack = struct.unpack
        l = runlen * (len(data) * 8 // (runlen * itemsize + skipbits))
        result = numpy.empty((l,), dtype)
        bitcount = 0
        for i in range(len(result)):
            start = bitcount // 8
            s = data[start:start + itembytes]
            try:
                code = unpack(dtypestr, s)[0]
            except Exception:
                code = unpack(dtypestr, s + b'\x00' * (itembytes - len(s)))[0]

            code = code << bitcount % 8
            code = code & bitmask
            result[i] = code >> shrbits
            bitcount += itemsize
            if (i + 1) % runlen == 0:
                bitcount += skipbits

        return result


def unpackrgb(data, dtype='<B', bitspersample=(5, 6, 5), rescale=True):
    """Return array from byte string containing packed samples.

    Use to unpack RGB565 or RGB555 to RGB888 format.

    Parameters
    ----------
    data : byte str
        The data to be decoded. Samples in each pixel are stored consecutively.
        Pixels are aligned to 8, 16, or 32 bit boundaries.
    dtype : numpy.dtype
        The sample data type. The byteorder applies also to the data stream.
    bitspersample : tuple
        Number of bits for each sample in a pixel.
    rescale : bool
        Upscale samples to the number of bits in dtype.

    Returns
    -------
    result : ndarray
        Flattened array of unpacked samples of native dtype.

    Examples
    --------
    >>> data = struct.pack('BBBB', 0x21, 0x08, 0xff, 0xff)
    >>> print(unpackrgb(data, '<B', (5, 6, 5), False))
    [ 1  1  1 31 63 31]
    >>> print(unpackrgb(data, '<B', (5, 6, 5)))
    [  8   4   8 255 255 255]
    >>> print(unpackrgb(data, '<B', (5, 5, 5)))
    [ 16   8   8 255 255 255]

    """
    dtype = numpy.dtype(dtype)
    bits = int(numpy.sum(bitspersample))
    if not (bits <= 32 and all(i <= dtype.itemsize * 8 for i in bitspersample)):
        raise ValueError('sample size not supported %s' % str(bitspersample))
    dt = next(i for i in 'BHI' if numpy.dtype(i).itemsize * 8 >= bits)
    data = numpy.fromstring(data, dtype.byteorder + dt)
    result = numpy.empty((data.size, len(bitspersample)), dtype.char)
    for i, bps in enumerate(bitspersample):
        t = data >> int(numpy.sum(bitspersample[i + 1:]))
        t &= int('0b' + '1' * bps, 2)
        if rescale:
            o = (dtype.itemsize * 8 // bps + 1) * bps
            if o > data.dtype.itemsize * 8:
                t = t.astype('I')
            t *= (2 ** o - 1) // (2 ** bps - 1)
            t //= 2 ** (o - dtype.itemsize * 8)
        result[:, i] = t

    return result.reshape(-1)


def reorient(image, orientation):
    """Return reoriented view of image array.

    Parameters
    ----------
    image : numpy array
        Non-squeezed output of asarray() functions.
        Axes -3 and -2 must be image length and width respectively.
    orientation : int or str
        One of TIFF_ORIENTATIONS keys or values.

    """
    o = TIFF_ORIENTATIONS.get(orientation, orientation)
    if o == 'top_left':
        return image
    if o == 'top_right':
        return image[..., ::-1, :]
    if o == 'bottom_left':
        return image[..., ::-1, :, :]
    if o == 'bottom_right':
        return image[..., ::-1, ::-1, :]
    if o == 'left_top':
        return numpy.swapaxes(image, -3, -2)
    if o == 'right_top':
        return numpy.swapaxes(image, -3, -2)[..., ::-1, :]
    if o == 'left_bottom':
        return numpy.swapaxes(image, -3, -2)[..., ::-1, :, :]
    if o == 'right_bottom':
        return numpy.swapaxes(image, -3, -2)[..., ::-1, ::-1, :]


def stripnull(string):
    """Return string truncated at first null character."""
    i = string.find(b'\x00')
    if i < 0:
        return string
    else:
        return string[:i]


def datetime_from_timestamp(n, epoch=datetime.datetime.fromordinal(693594)):
    """Return datetime object from timestamp in Excel serial format.

    Examples
    --------
    >>> datetime_from_timestamp(40237.029999999795)
    datetime.datetime(2010, 2, 28, 0, 43, 11, 999982)

    """
    return epoch + datetime.timedelta(n)


def test_tifffile(directory='testimages', verbose=True):
    """Read all images in directory. Print error message on failure.

    Examples
    --------
    >>> test_tifffile(verbose=False)

    """
    import glob
    successful = 0
    failed = 0
    start = time.time()
    for f in glob.glob(os.path.join(directory, '*.*')):
        if verbose:
            print(('\n%s>\n' % f.lower()), end='')
        t0 = time.time()
        try:
            tif = TIFFfile(f)
        except Exception as e:
            if not verbose:
                print(f, end=' ')
            print('ERROR:', e)
            failed += 1
            continue

        try:
            try:
                img = tif.asarray()
            except ValueError:
                try:
                    img = tif[0].asarray()
                except Exception as e:
                    if not verbose:
                        print(f, end=' ')
                    print('ERROR:', e)
                    failed += 1
                    continue

        finally:
            tif.close()

        successful += 1
        if verbose:
            print('%s, %s %s, %s, %.0f ms' % (str(tif), str(img.shape),
             img.dtype, tif[0].compression, (time.time() - t0) * 1000.0))

    if verbose:
        print('\nSuccessfully read %i of %i files in %.3f s\n' % (
         successful, successful + failed, time.time() - start))


class TIFF_SUBFILE_TYPES(object):

    def __getitem__(self, key):
        result = []
        if key & 1:
            result.append('reduced_image')
        if key & 2:
            result.append('page')
        if key & 4:
            result.append('mask')
        return tuple(result)


TIFF_PHOTOMETRICS = {0:'miniswhite', 
 1:'minisblack', 
 2:'rgb', 
 3:'palette', 
 4:'mask', 
 5:'separated', 
 6:'cielab', 
 7:'icclab', 
 8:'itulab', 
 32844:'logl', 
 32845:'logluv'}
TIFF_COMPESSIONS = {1:None, 
 2:'ccittrle', 
 3:'ccittfax3', 
 4:'ccittfax4', 
 5:'lzw', 
 6:'ojpeg', 
 7:'jpeg', 
 8:'adobe_deflate', 
 9:'t85', 
 10:'t43', 
 32766:'next', 
 32771:'ccittrlew', 
 32773:'packbits', 
 32809:'thunderscan', 
 32895:'it8ctpad', 
 32896:'it8lw', 
 32897:'it8mp', 
 32898:'it8bl', 
 32908:'pixarfilm', 
 32909:'pixarlog', 
 32946:'deflate', 
 32947:'dcs', 
 34661:'jbig', 
 34676:'sgilog', 
 34677:'sgilog24', 
 34712:'jp2000'}
TIFF_DECOMPESSORS = {None:lambda x: x, 
 'adobe_deflate':zlib.decompress, 
 'deflate':zlib.decompress, 
 'packbits':decodepackbits, 
 'lzw':decodelzw}
TIFF_DATA_TYPES = {1:'1B', 
 2:'1s', 
 3:'1H', 
 4:'1I', 
 5:'2I', 
 6:'1b', 
 7:'1B', 
 8:'1h', 
 9:'1i', 
 10:'2i', 
 11:'1f', 
 12:'1d', 
 13:'1I', 
 16:'1Q', 
 17:'1q', 
 18:'1Q'}
TIFF_SAMPLE_FORMATS = {1:'uint', 
 2:'int', 
 3:'float', 
 6:'complex'}
TIFF_SAMPLE_DTYPES = {('uint', 1): '?', 
 ('uint', 2): 'B', 
 ('uint', 3): 'B', 
 ('uint', 4): 'B', 
 ('uint', 5): 'B', 
 ('uint', 6): 'B', 
 ('uint', 7): 'B', 
 ('uint', 8): 'B', 
 ('uint', 9): 'H', 
 ('uint', 10): 'H', 
 ('uint', 11): 'H', 
 ('uint', 12): 'H', 
 ('uint', 13): 'H', 
 ('uint', 14): 'H', 
 ('uint', 15): 'H', 
 ('uint', 16): 'H', 
 ('uint', 17): 'I', 
 ('uint', 18): 'I', 
 ('uint', 19): 'I', 
 ('uint', 20): 'I', 
 ('uint', 21): 'I', 
 ('uint', 22): 'I', 
 ('uint', 23): 'I', 
 ('uint', 24): 'I', 
 ('uint', 25): 'I', 
 ('uint', 26): 'I', 
 ('uint', 27): 'I', 
 ('uint', 28): 'I', 
 ('uint', 29): 'I', 
 ('uint', 30): 'I', 
 ('uint', 31): 'I', 
 ('uint', 32): 'I', 
 ('uint', 64): 'Q', 
 ('int', 8): 'b', 
 ('int', 16): 'h', 
 ('int', 32): 'i', 
 ('int', 64): 'q', 
 ('float', 16): 'e', 
 ('float', 32): 'f', 
 ('float', 64): 'd', 
 ('complex', 64): 'F', 
 ('complex', 128): 'D', 
 ('uint', (5, 6, 5)): 'B'}
TIFF_ORIENTATIONS = {1:'top_left', 
 2:'top_right', 
 3:'bottom_right', 
 4:'bottom_left', 
 5:'left_top', 
 6:'right_top', 
 7:'right_bottom', 
 8:'left_bottom'}
AXES_LABELS = {'X':'width', 
 'Y':'height', 
 'Z':'depth', 
 'S':'sample', 
 'P':'plane', 
 'T':'time', 
 'C':'channel', 
 'A':'angle', 
 'F':'phase', 
 'R':'tile', 
 'H':'lifetime', 
 'E':'lambda', 
 'L':'exposure', 
 'V':'event', 
 'O':'other'}
AXES_LABELS.update(dict((v, k) for k, v in AXES_LABELS.items()))
MM_TAG_IDS = {0:'auto_scale', 
 1:'min_scale', 
 2:'max_scale', 
 3:'spatial_calibration', 
 8:'thresh_state', 
 9:'thresh_state_red', 
 11:'thresh_state_green', 
 12:'thresh_state_blue', 
 13:'thresh_state_lo', 
 14:'thresh_state_hi', 
 15:'zoom', 
 18:'current_buffer', 
 19:'gray_fit', 
 20:'gray_point_count', 
 26:'standard_lut', 
 27:'wavelength', 
 36:'image_property', 
 47:'new_lut', 
 49:'plane_property', 
 51:'red_autoscale_info', 
 54:'red_minscale_info', 
 55:'red_maxscale_info', 
 56:'green_autoscale_info', 
 59:'green_minscale_info', 
 60:'green_maxscale_info', 
 61:'blue_autoscale_info', 
 64:'blue_min_scale_info', 
 65:'blue_max_scale_info'}
MM_DIMENSION = [
 ('name', 'a16'),
 ('size', 'i4'),
 ('origin', 'f8'),
 ('resolution', 'f8'),
 ('unit', 'a64')]
MM_HEADER = [
 ('header_flag', 'i2'),
 ('image_type', 'u1'),
 ('image_name', 'a257'),
 ('offset_data', 'u4'),
 ('palette_size', 'i4'),
 ('offset_palette0', 'u4'),
 ('offset_palette1', 'u4'),
 ('comment_size', 'i4'),
 ('offset_comment', 'u4'),
 (
  'dimensions', MM_DIMENSION, 10),
 ('offset_position', 'u4'),
 ('map_type', 'i2'),
 ('map_min', 'f8'),
 ('map_max', 'f8'),
 ('min_value', 'f8'),
 ('max_value', 'f8'),
 ('offset_map', 'u4'),
 ('gamma', 'f8'),
 ('offset', 'f8'),
 (
  'gray_channel', MM_DIMENSION),
 ('offset_thumbnail', 'u4'),
 ('voice_field', 'i4'),
 ('offset_voice_field', 'u4')]
CZ_LSM_INFO = [
 ('magic_number', 'i4'),
 ('structure_size', 'i4'),
 ('dimension_x', 'i4'),
 ('dimension_y', 'i4'),
 ('dimension_z', 'i4'),
 ('dimension_channels', 'i4'),
 ('dimension_time', 'i4'),
 ('dimension_data_type', 'i4'),
 ('thumbnail_x', 'i4'),
 ('thumbnail_y', 'i4'),
 ('voxel_size_x', 'f8'),
 ('voxel_size_y', 'f8'),
 ('voxel_size_z', 'f8'),
 ('origin_x', 'f8'),
 ('origin_y', 'f8'),
 ('origin_z', 'f8'),
 ('scan_type', 'u2'),
 ('spectral_scan', 'u2'),
 ('data_type', 'u4'),
 ('offset_vector_overlay', 'u4'),
 ('offset_input_lut', 'u4'),
 ('offset_output_lut', 'u4'),
 ('offset_channel_colors', 'u4'),
 ('time_interval', 'f8'),
 ('offset_channel_data_types', 'u4'),
 ('offset_scan_information', 'u4'),
 ('offset_ks_data', 'u4'),
 ('offset_time_stamps', 'u4'),
 ('offset_event_list', 'u4'),
 ('offset_roi', 'u4'),
 ('offset_bleach_roi', 'u4'),
 ('offset_next_recording', 'u4'),
 ('display_aspect_x', 'f8'),
 ('display_aspect_y', 'f8'),
 ('display_aspect_z', 'f8'),
 ('display_aspect_time', 'f8'),
 ('offset_mean_of_roi_overlay', 'u4'),
 ('offset_topo_isoline_overlay', 'u4'),
 ('offset_topo_profile_overlay', 'u4'),
 ('offset_linescan_overlay', 'u4'),
 ('offset_toolbar_flags', 'u4')]
CZ_LSM_INFO_READERS = {'scan_information':read_cz_lsm_scan_info, 
 'time_stamps':read_cz_lsm_time_stamps, 
 'event_list':read_cz_lsm_event_list}
CZ_SCAN_TYPES = {0:'XYZCT', 
 1:'XYZCT', 
 2:'XYZCT', 
 3:'XYTCZ', 
 4:'XYZTC', 
 5:'XYTCZ', 
 6:'XYZTC', 
 7:'XYCTZ', 
 8:'XYCZT', 
 9:'XYTCZ', 
 10:'XYZCT'}
CZ_DIMENSIONS = {'X':'dimension_x', 
 'Y':'dimension_y', 
 'Z':'dimension_z', 
 'C':'dimension_channels', 
 'T':'dimension_time'}
CZ_DATA_TYPES = {0:'varying data types', 
 2:'12 bit unsigned integer', 
 5:'32 bit float'}
CZ_LSM_SCAN_INFO_ARRAYS = {536870912:'tracks', 
 805306368:'lasers', 
 1610612736:'detectionchannels', 
 2147483648:'illuminationchannels', 
 2684354560:'beamsplitters', 
 3221225472:'datachannels', 
 318767104:'markers', 
 285212672:'timers'}
CZ_LSM_SCAN_INFO_STRUCTS = {1073741824:'tracks', 
 1342177280:'lasers', 
 1879048192:'detectionchannels', 
 2415919104:'illuminationchannels', 
 2952790016:'beamsplitters', 
 3489660928:'datachannels', 
 335544320:'markers', 
 301989888:'timers'}
CZ_LSM_SCAN_INFO_ATTRIBUTES = {268435457:'name', 
 268435458:'description', 
 268435459:'notes', 
 268435460:'objective', 
 268435461:'processing_summary', 
 268435462:'special_scan_mode', 
 268435463:'oledb_recording_scan_type', 
 268435464:'oledb_recording_scan_mode', 
 268435465:'number_of_stacks', 
 268435466:'lines_per_plane', 
 268435467:'samples_per_line', 
 268435468:'planes_per_volume', 
 268435469:'images_width', 
 268435470:'images_height', 
 268435471:'images_number_planes', 
 268435472:'images_number_stacks', 
 268435473:'images_number_channels', 
 268435474:'linscan_xy_size', 
 268435475:'scan_direction', 
 268435476:'time_series', 
 268435477:'original_scan_data', 
 268435478:'zoom_x', 
 268435479:'zoom_y', 
 268435480:'zoom_z', 
 268435481:'sample_0x', 
 268435482:'sample_0y', 
 268435483:'sample_0z', 
 268435484:'sample_spacing', 
 268435485:'line_spacing', 
 268435486:'plane_spacing', 
 268435487:'plane_width', 
 268435488:'plane_height', 
 268435489:'volume_depth', 
 268435491:'nutation', 
 268435508:'rotation', 
 268435509:'precession', 
 268435510:'sample_0time', 
 268435511:'start_scan_trigger_in', 
 268435512:'start_scan_trigger_out', 
 268435513:'start_scan_event', 
 268435520:'start_scan_time', 
 268435521:'stop_scan_trigger_in', 
 268435522:'stop_scan_trigger_out', 
 268435523:'stop_scan_event', 
 268435524:'stop_scan_time', 
 268435525:'use_rois', 
 268435526:'use_reduced_memory_rois', 
 268435527:'user', 
 268435528:'use_bccorrection', 
 268435529:'position_bccorrection1', 
 268435536:'position_bccorrection2', 
 268435537:'interpolation_y', 
 268435538:'camera_binning', 
 268435539:'camera_supersampling', 
 268435540:'camera_frame_width', 
 268435541:'camera_frame_height', 
 268435542:'camera_offset_x', 
 268435543:'camera_offset_y', 
 1342177281:'name', 
 1342177282:'acquire', 
 1342177283:'power', 
 1073741825:'multiplex_type', 
 1073741826:'multiplex_order', 
 1073741827:'sampling_mode', 
 1073741828:'sampling_method', 
 1073741829:'sampling_number', 
 1073741830:'acquire', 
 1073741831:'sample_observation_time', 
 1073741835:'time_between_stacks', 
 1073741836:'name', 
 1073741837:'collimator1_name', 
 1073741838:'collimator1_position', 
 1073741839:'collimator2_name', 
 1073741840:'collimator2_position', 
 1073741841:'is_bleach_track', 
 1073741842:'is_bleach_after_scan_number', 
 1073741843:'bleach_scan_number', 
 1073741844:'trigger_in', 
 1073741845:'trigger_out', 
 1073741846:'is_ratio_track', 
 1073741847:'bleach_count', 
 1073741848:'spi_center_wavelength', 
 1073741849:'pixel_time', 
 1073741857:'condensor_frontlens', 
 1073741859:'field_stop_value', 
 1073741860:'id_condensor_aperture', 
 1073741861:'condensor_aperture', 
 1073741862:'id_condensor_revolver', 
 1073741863:'condensor_filter', 
 1073741864:'id_transmission_filter1', 
 1073741865:'id_transmission1', 
 1073741872:'id_transmission_filter2', 
 1073741873:'id_transmission2', 
 1073741874:'repeat_bleach', 
 1073741875:'enable_spot_bleach_pos', 
 1073741876:'spot_bleach_posx', 
 1073741877:'spot_bleach_posy', 
 1073741878:'spot_bleach_posz', 
 1073741879:'id_tubelens', 
 1073741880:'id_tubelens_position', 
 1073741881:'transmitted_light', 
 1073741882:'reflected_light', 
 1073741883:'simultan_grab_and_bleach', 
 1073741884:'bleach_pixel_time', 
 1879048193:'integration_mode', 
 1879048194:'special_mode', 
 1879048195:'detector_gain_first', 
 1879048196:'detector_gain_last', 
 1879048197:'amplifier_gain_first', 
 1879048198:'amplifier_gain_last', 
 1879048199:'amplifier_offs_first', 
 1879048200:'amplifier_offs_last', 
 1879048201:'pinhole_diameter', 
 1879048202:'counting_trigger', 
 1879048203:'acquire', 
 1879048204:'point_detector_name', 
 1879048205:'amplifier_name', 
 1879048206:'pinhole_name', 
 1879048207:'filter_set_name', 
 1879048208:'filter_name', 
 1879048211:'integrator_name', 
 1879048212:'detection_channel_name', 
 1879048213:'detection_detector_gain_bc1', 
 1879048214:'detection_detector_gain_bc2', 
 1879048215:'detection_amplifier_gain_bc1', 
 1879048216:'detection_amplifier_gain_bc2', 
 1879048217:'detection_amplifier_offset_bc1', 
 1879048224:'detection_amplifier_offset_bc2', 
 1879048225:'detection_spectral_scan_channels', 
 1879048226:'detection_spi_wavelength_start', 
 1879048227:'detection_spi_wavelength_stop', 
 1879048230:'detection_dye_name', 
 1879048231:'detection_dye_folder', 
 2415919105:'name', 
 2415919106:'power', 
 2415919107:'wavelength', 
 2415919108:'aquire', 
 2415919109:'detchannel_name', 
 2415919110:'power_bc1', 
 2415919111:'power_bc2', 
 2952790017:'filter_set', 
 2952790018:'filter', 
 2952790019:'name', 
 3489660929:'name', 
 3489660931:'acquire', 
 3489660932:'color', 
 3489660933:'sample_type', 
 3489660934:'bits_per_sample', 
 3489660935:'ratio_type', 
 3489660936:'ratio_track1', 
 3489660937:'ratio_track2', 
 3489660938:'ratio_channel1', 
 3489660939:'ratio_channel2', 
 3489660940:'ratio_const1', 
 3489660941:'ratio_const2', 
 3489660942:'ratio_const3', 
 3489660943:'ratio_const4', 
 3489660944:'ratio_const5', 
 3489660945:'ratio_const6', 
 3489660946:'ratio_first_images1', 
 3489660947:'ratio_first_images2', 
 3489660948:'dye_name', 
 3489660949:'dye_folder', 
 3489660950:'spectrum', 
 3489660951:'acquire', 
 335544321:'name', 
 335544322:'description', 
 335544323:'trigger_in', 
 335544324:'trigger_out', 
 301989889:'name', 
 301989890:'description', 
 301989891:'interval', 
 301989892:'trigger_in', 
 301989893:'trigger_out', 
 301989894:'activation_time', 
 301989895:'activation_number'}
TIFF_TAGS = {254:(
  'new_subfile_type', 0, 4, 1, TIFF_SUBFILE_TYPES()), 
 255:(
  'subfile_type', None, 3, 1,
  {0:'undefined', 
   1:'image',  2:'reduced_image',  3:'page'}), 
 256:('image_width', None, 4, 1, None), 
 257:('image_length', None, 4, 1, None), 
 258:('bits_per_sample', 1, 3, 1, None), 
 259:(
  'compression', 1, 3, 1, TIFF_COMPESSIONS), 
 262:(
  'photometric', None, 3, 1, TIFF_PHOTOMETRICS), 
 266:(
  'fill_order', 1, 3, 1, {1:'msb2lsb',  2:'lsb2msb'}), 
 269:('document_name', None, 2, None, None), 
 270:('image_description', None, 2, None, None), 
 271:('make', None, 2, None, None), 
 272:('model', None, 2, None, None), 
 273:('strip_offsets', None, 4, None, None), 
 274:(
  'orientation', 1, 3, 1, TIFF_ORIENTATIONS), 
 277:('samples_per_pixel', 1, 3, 1, None), 
 278:('rows_per_strip', 4294967295, 4, 1, None), 
 279:('strip_byte_counts', None, 4, None, None), 
 282:('x_resolution', None, 5, 1, None), 
 283:('y_resolution', None, 5, 1, None), 
 284:(
  'planar_configuration', 1, 3, 1, {1:'contig',  2:'separate'}), 
 285:('page_name', None, 2, None, None), 
 296:(
  'resolution_unit', 2, 4, 1, {1:'none',  2:'inch',  3:'centimeter'}), 
 305:('software', None, 2, None, None), 
 306:('datetime', None, 2, None, None), 
 315:('artist', None, 2, None, None), 
 316:('host_computer', None, 2, None, None), 
 317:(
  'predictor', 1, 3, 1, {1:None,  2:'horizontal'}), 
 320:('color_map', None, 3, None, None), 
 322:('tile_width', None, 4, 1, None), 
 323:('tile_length', None, 4, 1, None), 
 324:('tile_offsets', None, 4, None, None), 
 325:('tile_byte_counts', None, 4, None, None), 
 338:(
  'extra_samples', None, 3, None,
  {0:'unspecified', 
   1:'assocalpha',  2:'unassalpha'}), 
 339:(
  'sample_format', 1, 3, 1, TIFF_SAMPLE_FORMATS), 
 530:('ycbcr_subsampling', 1, 3, 2, None), 
 531:('ycbcr_positioning', 1, 3, 1, None), 
 33432:('copyright', None, 1, None, None), 
 32997:('image_depth', None, 4, 1, None), 
 32998:('tile_depth', None, 4, 1, None), 
 34665:('exif_ifd', None, None, 1, None), 
 34853:('gps_ifd', None, None, 1, None), 
 42112:('gdal_metadata', None, 2, None, None)}
CUSTOM_TAGS = {700:(
  'xmp', read_bytes), 
 34377:(
  'photoshop', read_numpy), 
 33723:(
  'iptc', read_bytes), 
 34675:(
  'icc_profile', read_numpy), 
 33628:(
  'mm_uic1', read_mm_uic1), 
 33629:(
  'mm_uic2', read_mm_uic2), 
 33630:(
  'mm_uic3', read_mm_uic3), 
 33631:(
  'mm_uic4', read_mm_uic4), 
 34361:(
  'mm_header', read_mm_header), 
 34362:(
  'mm_stamp', read_mm_stamp), 
 34386:(
  'mm_user_block', read_bytes), 
 34412:(
  'cz_lsm_info', read_cz_lsm_info), 
 43314:(
  'nih_image_header', read_nih_image_header)}
PRINT_LINE_LEN = 79

def imshow(data, title=None, vmin=0, vmax=None, cmap=None, bitspersample=None, photometric='rgb', interpolation='nearest', dpi=96, figure=None, subplot=111, maxdim=4096, **kwargs):
    """Plot n-dimensional images using matplotlib.pyplot.

    Return figure, subplot and plot axis.
    Requires pyplot already imported ``from matplotlib import pyplot``.

    Parameters
    ----------
    bitspersample : int or None
        Number of bits per channel in integer RGB images.
    photometric : {'miniswhite', 'minisblack', 'rgb', or 'palette'}
        The color space of the image data.
    title : str
        Window and subplot title.
    figure : matplotlib.figure.Figure (optional).
        Matplotlib to use for plotting.
    subplot : int
        A matplotlib.pyplot.subplot axis.
    maxdim : int
        maximum image size in any dimension.
    kwargs : optional
        Arguments for matplotlib.pyplot.imshow.

    """
    isrgb = photometric in ('rgb', 'palette')
    data = numpy.atleast_2d(data.squeeze())
    data = data[((slice(0, maxdim),) * len(data.shape))]
    dims = data.ndim
    if dims < 2:
        raise ValueError('not an image')
    else:
        if dims == 2:
            dims = 0
            isrgb = False
        elif isrgb:
            if data.shape[(-3)] in (3, 4):
                data = numpy.swapaxes(data, -3, -2)
                data = numpy.swapaxes(data, -2, -1)
            else:
                if not isrgb:
                    if data.shape[(-1)] in (3, 4):
                        data = numpy.swapaxes(data, -3, -1)
                        data = numpy.swapaxes(data, -2, -1)
            isrgb = isrgb and data.shape[(-1)] in (3, 4)
            dims -= 3 if isrgb else 2
        else:
            if photometric == 'palette':
                datamax = data.max()
                if datamax > 255:
                    data >>= 8
                data = data.astype('B')
            else:
                if data.dtype.kind in 'ui':
                    if not isrgb or bitspersample is None:
                        bitspersample = int(math.ceil(math.log(data.max(), 2)))
                    elif not isinstance(bitspersample, int):
                        bitspersample = data.dtype.itemsize * 8
                    datamax = 2 ** bitspersample
                    if isrgb:
                        if bitspersample < 8:
                            data <<= 8 - bitspersample
                        else:
                            if bitspersample > 8:
                                data >>= bitspersample - 8
                        data = data.astype('B')
                else:
                    if data.dtype.kind == 'f':
                        datamax = data.max()
                        if isrgb:
                            if datamax > 1.0:
                                if data.dtype.char == 'd':
                                    data = data.astype('f')
                                data /= datamax
                    elif data.dtype.kind == 'b':
                        datamax = 1
    if vmax is None:
        vmax = datamax
    if vmin is None:
        if data.dtype.kind != 'f':
            vmin = 0
    pyplot = sys.modules['matplotlib.pyplot']
    if figure is None:
        pyplot.rc('font', family='sans-serif', weight='normal', size=8)
        figure = pyplot.figure(dpi=dpi, figsize=(10.3, 6.3), frameon=True, facecolor='1.0',
          edgecolor='w')
        try:
            figure.canvas.manager.window.title(title)
        except Exception:
            pass

        pyplot.subplots_adjust(bottom=(0.03 * (dims + 2)), top=0.9, left=0.1,
          right=0.95,
          hspace=0.05,
          wspace=0.0)
    subplot = pyplot.subplot(subplot)
    if title:
        pyplot.title(title, size=11)
    if cmap is None:
        if photometric == 'miniswhite':
            cmap = 'gray_r' if vmin == 0 else 'coolwarm_r'
        else:
            cmap = 'gray' if vmin == 0 else 'coolwarm'
    image = (pyplot.imshow)(data[((0, ) * dims)].squeeze(), vmin=vmin, vmax=vmax, cmap=cmap, 
     interpolation=interpolation, **kwargs)
    if not isrgb:
        pyplot.colorbar()

    def format_coord(x, y):
        x = int(x + 0.5)
        y = int(y + 0.5)
        try:
            if dims:
                return '%s @ %s [%4i, %4i]' % (cur_ax_dat[1][(y, x)],
                 current, x, y)
            else:
                return '%s @ [%4i, %4i]' % (data[(y, x)], x, y)
        except IndexError:
            return ''

    pyplot.gca().format_coord = format_coord
    if dims:
        current = list((0, ) * dims)
        cur_ax_dat = [0, data[tuple(current)].squeeze()]
        sliders = [pyplot.Slider((pyplot.axes([0.125, 0.03 * (axis + 1), 0.725, 0.025])), ('Dimension %i' % axis), 0, (data.shape[axis] - 1), 0, facecolor='0.5', valfmt=('%%.0f [%i]' % data.shape[axis])) for axis in range(dims)]
        for slider in sliders:
            slider.drawon = False

        def set_image(current, sliders=sliders, data=data):
            cur_ax_dat[1] = data[tuple(current)].squeeze()
            image.set_data(cur_ax_dat[1])
            for ctrl, index in zip(sliders, current):
                ctrl.eventson = False
                ctrl.set_val(index)
                ctrl.eventson = True

            figure.canvas.draw()

        def on_changed(index, axis, data=data, current=current):
            index = int(round(index))
            cur_ax_dat[0] = axis
            if index == current[axis]:
                return
            if index >= data.shape[axis]:
                index = 0
            else:
                if index < 0:
                    index = data.shape[axis] - 1
            current[axis] = index
            set_image(current)

        def on_keypressed(event, data=data, current=current):
            key = event.key
            axis = cur_ax_dat[0]
            if str(key) in '0123456789':
                on_changed(key, axis)
            else:
                if key == 'right':
                    on_changed(current[axis] + 1, axis)
                else:
                    if key == 'left':
                        on_changed(current[axis] - 1, axis)
                    else:
                        if key == 'up':
                            cur_ax_dat[0] = 0 if axis == len(data.shape) - 1 else axis + 1
                        else:
                            if key == 'down':
                                cur_ax_dat[0] = len(data.shape) - 1 if axis == 0 else axis - 1
                            else:
                                if key == 'end':
                                    on_changed(data.shape[axis] - 1, axis)
                                elif key == 'home':
                                    on_changed(0, axis)

        figure.canvas.mpl_connect('key_press_event', on_keypressed)
        for axis, ctrl in enumerate(sliders):
            ctrl.on_changed(lambda k, a=axis: on_changed(k, a))

    return (
     figure, subplot, image)


def _app_show():
    """Block the GUI. For use as skimage plugin."""
    pyplot = sys.modules['matplotlib.pyplot']
    pyplot.show()


def main(argv=None):
    """Command line usage main function."""
    if float(sys.version[0:3]) < 2.6:
        print('This script requires Python version 2.6 or better.')
        print('This is Python version %s' % sys.version)
        return 0
    elif argv is None:
        argv = sys.argv
    else:
        import re, optparse
        search_doc = lambda r, d: re.search(r, __doc__).group(1) if __doc__ else d
        parser = optparse.OptionParser(usage='usage: %prog [options] path',
          description=(search_doc('\n\n([^|]*?)\n\n', '')),
          version=('%%prog %s' % search_doc(':Version: (.*)', 'Unknown')))
        opt = parser.add_option
        opt('-p', '--page', dest='page', type='int', default=(-1), help='display single page')
        opt('-s', '--series', dest='series', type='int', default=(-1), help='display series of pages of same shape')
        opt('--noplot', dest='noplot', action='store_true', default=False, help="don't display images")
        opt('--interpol', dest='interpol', metavar='INTERPOL', default='bilinear', help='image interpolation method')
        opt('--dpi', dest='dpi', type='int', default=96, help='set plot resolution')
        opt('--debug', dest='debug', action='store_true', default=False, help='raise exception on failures')
        opt('--test', dest='test', action='store_true', default=False, help='try read all images in path')
        opt('--doctest', dest='doctest', action='store_true', default=False, help='runs the internal tests')
        opt('-v', '--verbose', dest='verbose', action='store_true', default=True)
        opt('-q', '--quiet', dest='verbose', action='store_false')
        settings, path = parser.parse_args()
        path = ' '.join(path)
        if settings.doctest:
            import doctest
            doctest.testmod()
            return 0
        if not path:
            parser.error('No file specified')
        if settings.test:
            test_tifffile(path, settings.verbose)
            return 0
        print('Reading file structure...', end=' ')
        start = time.time()
        try:
            tif = TIFFfile(path)
        except Exception as e:
            if settings.debug:
                raise
            else:
                print('\n', e)
                sys.exit(0)

        print('%.3f ms' % ((time.time() - start) * 1000.0))
        if tif.is_ome:
            settings.norgb = True
        images = [(None, tif[(0 if settings.page < 0 else settings.page)])]
        if not settings.noplot:
            print('Reading image data... ', end=' ')
            notnone = lambda x: next(i for i in x if i is not None)
            start = time.time()
            try:
                if settings.page >= 0:
                    images = [(
                      tif.asarray(key=(settings.page)),
                      tif[settings.page])]
                else:
                    if settings.series >= 0:
                        images = [(
                          tif.asarray(series=(settings.series)),
                          notnone(tif.series[settings.series].pages))]
                    else:
                        images = []
                        for i, s in enumerate(tif.series):
                            try:
                                images.append((
                                 tif.asarray(series=i), notnone(s.pages)))
                            except ValueError as e:
                                images.append((None, notnone(s.pages)))
                                if settings.debug:
                                    raise
                                else:
                                    print(('\n* series %i failed: %s... ' % (i, e)), end='')

                print('%.3f ms' % ((time.time() - start) * 1000.0))
            except Exception as e:
                if settings.debug:
                    raise
                else:
                    print(e)

        tif.close()
        print('\nTIFF file:', tif)
        print()
        for i, s in enumerate(tif.series):
            print('Series %i' % i)
            print(s)
            print()

        for i, page in images:
            print(page)
            print(page.tags)
            if page.is_palette:
                print('\nColor Map:', page.color_map.shape, page.color_map.dtype)
            for attr in ('cz_lsm_info', 'cz_lsm_scan_information', 'mm_uic_tags', 'mm_header',
                         'nih_image_header'):
                if hasattr(page, attr):
                    print('', (attr.upper()), (Record(getattr(page, attr))), sep='\n')

            print()

        if images:
            if not settings.noplot:
                try:
                    import matplotlib
                    matplotlib.use('TkAgg')
                    from matplotlib import pyplot
                except ImportError as e:
                    warnings.warn('failed to import matplotlib.\n%s' % e)
                else:
                    for img, page in images:
                        if img is None:
                            pass
                        else:
                            vmin, vmax = (None, None)
                            if page.is_stk:
                                try:
                                    vmin = page.mm_uic_tags['min_scale']
                                    vmax = page.mm_uic_tags['max_scale']
                                except KeyError:
                                    pass
                                else:
                                    if vmax <= vmin:
                                        vmin, vmax = (None, None)
                            title = '%s\n %s' % (str(tif), str(page))
                            imshow(img, title=title, vmin=vmin, vmax=vmax, bitspersample=(page.bits_per_sample),
                              photometric=(page.photometric),
                              interpolation=(settings.interpol),
                              dpi=(settings.dpi))

                    pyplot.show()


__version__ = '2012.07.05'
__docformat__ = 'restructuredtext en'
if __name__ == '__main__':
    sys.exit(main())