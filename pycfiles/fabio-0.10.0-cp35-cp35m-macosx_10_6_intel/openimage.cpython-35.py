# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/openimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 10925 bytes
"""

Authors: Henning O. Sorensen & Erik Knudsen
         Center for Fundamental Research: Metal Structures in Four Dimensions
         Risoe National Laboratory
         Frederiksborgvej 399
         DK-4000 Roskilde
         email:henning.sorensen@risoe.dk

mods for fabio by JPW
modification for HDF5 by Jérôme Kieffer

"""
from __future__ import with_statement, print_function, absolute_import
import os.path, logging
logger = logging.getLogger(__name__)
from . import fabioutils
from .fabioutils import FilenameObject, BytesIO
from .fabioimage import FabioImage
from . import fabioformats
MAGIC_NUMBERS = [
 (b'FORMAT :100', 'bruker100'),
 (b'FORMAT :        86', 'bruker'),
 (b'MM\x00*', 'tif'),
 (b'II*\x00\x08\x00', 'marccd/tif'),
 (b'II*\x00\x82\x00', 'pilatus'),
 (b'II*\x00', 'tif'),
 (b'{\nHEA', 'dtrek'),
 (b'\r\n{\r\nEDF', 'edf'),
 (b'\n{\r\nEDF', 'edf'),
 (b'{\r\nEDF', 'edf'),
 (b'{\n', 'edf'),
 (b'\n{\n', 'edf'),
 (b'{', 'edf'),
 (b'\r{', 'edf'),
 (b'\n{', 'edf'),
 (b'ADEPT', 'GE'),
 (b'OD', 'OXD'),
 (b'IM', 'HiPiC'),
 (b'-\x04', 'mar345'),
 (b'\xd2\x04', 'mar345'),
 (b'\x04-', 'mar345'),
 (b'\x04\xd2', 'mar345'),
 (b'M\x00\x00\x00A\x00\x00\x00S\x00\x00\x00K\x00\x00\x00', 'fit2dmask'),
 (b'\x00\x00\x00\x03', 'dm3'),
 (b'No', 'kcd'),
 (b'<', 'xsd'),
 (b'\n\xb8\x03\x00', 'pixi'),
 (b'\x89HDF\r\n\x1a\n', 'eiger/hdf5'),
 (b'R-AXIS', 'raxis'),
 (b'\x93NUMPY', 'numpy'),
 (b'\\$FFF_START', 'fit2d'),
 (b'\xff\xd8\xff\xdb', 'jpeg'),
 (b'\xff\xd8\xff\xe0', 'jpeg'),
 (b'\xff\xd8\xff\xe1', 'jpeg'),
 (b'\x00\x00\x00\x0cjP  \r\n\x87\n', 'jpeg2k'),
 (b'ESPERANTO FORMAT', 'esperanto')]

def do_magic(byts, filename):
    """ Try to interpret the bytes starting the file as a magic number """
    for magic, format_type in MAGIC_NUMBERS:
        if byts.startswith(magic):
            if '/' in format_type:
                if format_type == 'eiger/hdf5':
                    if '::' in filename:
                        return 'hdf5'
                    else:
                        return 'eiger'
                else:
                    if format_type == 'marccd/tif':
                        if 'mccd' in filename.split('.'):
                            return 'marccd'
                        return 'tif'
                    else:
                        return format_type

    raise Exception('Could not interpret magic string')


def openimage(filename, frame=None):
    """Open an image.

    It returns a FabioImage-class instance which can be used as a context manager to close the file
    at the termination.

    .. code-block:: python

        with fabio.open("image.edf") as i:
            print(i.nframes)
            print(i.data)

    :param Union[str,FilenameObject] filename: A filename or a filename
        iterator.
    :param Union[int,None] frame: A specific frame inside this file.
    :rtype: FabioImage
    """
    if isinstance(filename, fabioutils.PathTypes):
        if not isinstance(filename, fabioutils.StringTypes):
            filename = str(filename)
        if isinstance(filename, FilenameObject):
            try:
                logger.debug('Attempting to open %s' % filename.tobytes())
                obj = _openimage(filename.tobytes())
                logger.debug('Attempting to read frame %s from %s with reader %s' % (frame, filename.tobytes(), obj.classname))
                obj = obj.read(filename.tobytes(), frame)
            except Exception as ex:
                logger.debug('Exception %s, trying name %s' % (ex, filename.stem))
                obj = _openimage(filename.stem)
                logger.debug('Reading frame %s from %s' % (filename.num, filename.stem))
                obj.read(filename.stem, frame=filename.num)

        else:
            logger.debug('Attempting to open %s' % filename)
            obj = _openimage(filename)
            logger.debug('Attempting to read frame %s from %s with reader %s' % (frame, filename, obj.classname))
            obj = obj.read(obj.filename, frame)
        return obj


def openheader(filename):
    """ return only the header"""
    if isinstance(filename, fabioutils.PathTypes):
        if not isinstance(filename, fabioutils.StringTypes):
            filename = str(filename)
        obj = _openimage(filename)
        obj.readheader(obj.filename)
        return obj


def _openimage(filename):
    """
    determine which format for a filename
    and return appropriate class which can be used for opening the image

    :param filename: can be an url like:

    hdf5:///example.h5?entry/instrument/detector/data/data#slice=[:,:,5]

    """
    if hasattr(filename, 'seek') and hasattr(filename, 'read'):
        if not isinstance(filename, BytesIO):
            filename.seek(0)
            actual_filename = BytesIO(filename.read())
    else:
        if os.path.exists(filename):
            actual_filename = filename
        else:
            if '::' in filename:
                actual_filename = filename.split('::')[0]
            else:
                actual_filename = filename
    try:
        imo = FabioImage()
        with imo._open(actual_filename) as (f):
            magic_bytes = f.read(18)
    except IOError:
        logger.debug('Backtrace', exc_info=True)
        raise
    else:
        imo = None
    filetype = None
    try:
        filetype = do_magic(magic_bytes, filename)
    except Exception:
        logger.debug('Backtrace', exc_info=True)
        try:
            file_obj = FilenameObject(filename=filename)
            if file_obj is None:
                raise Exception('Unable to deconstruct filename')
            if file_obj.format is not None and len(file_obj.format) != 1 and isinstance(file_obj.format, list):
                raise Exception('openimage failed on magic bytes & name guess')
            filetype = file_obj.format
        except Exception:
            logger.debug('Backtrace', exc_info=True)
            raise IOError('Fabio could not identify ' + filename)

    if filetype is None:
        raise IOError('Fabio could not identify ' + filename)
    klass_name = ''.join(filetype) + 'image'
    try:
        obj = fabioformats.factory(klass_name)
    except (RuntimeError, Exception):
        logger.debug('Backtrace', exc_info=True)
        raise IOError("Filename %s can't be read as format %s" % (filename, klass_name))

    obj.filename = filename
    return obj


def open_series(filenames=None, first_filename=None, single_frame=None, fixed_frames=None, fixed_frame_number=None):
    """
    Create an object to iterate frames through a file series.

    This function is a wrapper over :class:`~file_series.FileSeries` to facilitate
    simple uses of file series iterations.

    :param Union[Generator,Iterator,List] filenames: Ordered list of filenames
        to process as a file series. It also can be a generator, and
        iterator, or :class:`~fabio.file_series.filename_series` or
        :class:`~fabio.file_series.file_series` objects.
    :param str first_filename: If provided iterate filenames from this filename
        and try to consecutivelly open next files. If this argument is specified
        the `filenames` have to unspecified. Internally it uses
        :class:`~fabio.file_series.filename_series` to iterate the filenames.
    :param Union[Bool,None] single_frame: If True, all files are supposed to
        contain only one frame.
    :param Union[Bool,None] fixed_frames: If True, all files are supposed to
        contain the same amount of frames (this fixed amount will be reached
        from the first file of the serie).
    :param Union[Integer,None] fixed_frame_number: If set, all files are
        supposed to contain the same amount of frames (sepecified by this
        argument)
    :rtype: :class:`~file_series.FileSeries`
    """
    from . import file_series
    if filenames is not None and first_filename is not None:
        raise ValueError("'filenames' and 'first_filename' are mutual exclusive")
    if first_filename is not None:
        filenames = file_series.filename_series(filename=first_filename)
    return file_series.FileSeries(filenames=filenames, single_frame=single_frame, fixed_frames=fixed_frames, fixed_frame_number=fixed_frame_number)