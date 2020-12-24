# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\filereader.py
# Compiled at: 2017-01-26 21:09:37
# Size of source mod 2**32: 31164 bytes
"""Read a dicom media file"""
import os.path, warnings, zlib
from io import BytesIO
import logging
from dicom.tag import TupleTag
from dicom.dataelem import RawDataElement
from dicom.util.hexutil import bytes2hex
from dicom.valuerep import extra_length_VRs
from dicom.charset import default_encoding, convert_encodings
from dicom import in_py3
logger = logging.getLogger('pydicom')
stat_available = True
try:
    from os import stat
except:
    stat_available = False

from dicom.errors import InvalidDicomError
import dicom.UID
from dicom.filebase import DicomFile
from dicom.dataset import Dataset, FileDataset
from dicom.dicomdir import DicomDir
from dicom.datadict import dictionaryVR
from dicom.dataelem import DataElement
from dicom.tag import ItemTag, SequenceDelimiterTag
from dicom.sequence import Sequence
from dicom.fileutil import read_undefined_length_value
from struct import Struct, unpack
from sys import byteorder
sys_is_little_endian = byteorder == 'little'

class DicomIter(object):
    __doc__ = 'Iterator over DICOM data elements created from a file-like object\n    '

    def __init__(self, fp, stop_when=None, force=False):
        """Read the preamble and meta info, prepare iterator for remainder

        fp -- an open DicomFileLike object, at start of file

        Adds flags to fp: Big/Little-endian and Implicit/Explicit VR
        """
        self.fp = fp
        self.stop_when = stop_when
        self.preamble = preamble = read_preamble(fp, force)
        self.has_header = has_header = preamble is not None
        self.file_meta_info = Dataset()
        if has_header:
            self.file_meta_info = file_meta_info = _read_file_meta_info(fp)
            transfer_syntax = file_meta_info.TransferSyntaxUID
            if transfer_syntax == dicom.UID.ExplicitVRLittleEndian:
                self._is_implicit_VR = False
                self._is_little_endian = True
            else:
                if transfer_syntax == dicom.UID.ImplicitVRLittleEndian:
                    self._is_implicit_VR = True
                    self._is_little_endian = True
                else:
                    if transfer_syntax == dicom.UID.ExplicitVRBigEndian:
                        self._is_implicit_VR = False
                        self._is_little_endian = False
                    else:
                        if transfer_syntax == dicom.UID.DeflatedExplicitVRLittleEndian:
                            zipped = fp.read()
                            unzipped = zlib.decompress(zipped, -zlib.MAX_WBITS)
                            fp = BytesIO(unzipped)
                            self.fp = fp
                            self._is_implicit_VR = False
                            self._is_little_endian = True
                        else:
                            self._is_implicit_VR = False
                            self._is_little_endian = True
        else:
            fp.TransferSyntaxUID = dicom.UID.ImplicitVRLittleEndian
            self._is_little_endian = True
            self._is_implicit_VR = True
        impl_expl = ('Explicit', 'Implicit')[self._is_implicit_VR]
        big_little = ('Big', 'Little')[self._is_little_endian]
        logger.debug('Using {0:s} VR, {1:s} Endian transfer syntax'.format(impl_expl, big_little))

    def __iter__(self):
        tags = sorted(self.file_meta_info.keys())
        for tag in tags:
            yield self.file_meta_info[tag]

        for data_element in data_element_generator(self.fp, self._is_implicit_VR, self._is_little_endian, stop_when=self.stop_when):
            yield data_element


def data_element_generator(fp, is_implicit_VR, is_little_endian, stop_when=None, defer_size=None, encoding=default_encoding):
    """Create a generator to efficiently return the raw data elements
    Returns (VR, length, raw_bytes, value_tell, is_little_endian),
    where:
    VR -- None if implicit VR, otherwise the VR read from the file
    length -- the length as in the DICOM data element (could be
        DICOM "undefined length" 0xffffffffL),
    value_bytes -- the raw bytes from the DICOM file
                    (not parsed into python types)
    is_little_endian -- True if transfer syntax is little endian; else False
    """
    if is_little_endian:
        endian_chr = '<'
    else:
        endian_chr = '>'
    if is_implicit_VR:
        element_struct = Struct(endian_chr + 'HHL')
    else:
        element_struct = Struct(endian_chr + 'HH2sH')
        extra_length_struct = Struct(endian_chr + 'L')
        extra_length_unpack = extra_length_struct.unpack
    fp_read = fp.read
    fp_tell = fp.tell
    logger_debug = logger.debug
    debugging = dicom.debugging
    element_struct_unpack = element_struct.unpack
    while 1:
        bytes_read = fp_read(8)
        if len(bytes_read) < 8:
            raise StopIteration
        if debugging:
            debug_msg = '{0:08x}: {1}'.format(fp.tell() - 8, bytes2hex(bytes_read))
        if is_implicit_VR:
            VR = None
            group, elem, length = element_struct_unpack(bytes_read)
        else:
            group, elem, VR, length = element_struct_unpack(bytes_read)
            if in_py3:
                VR = VR.decode(default_encoding)
        if VR in extra_length_VRs:
            bytes_read = fp_read(4)
            length = extra_length_unpack(bytes_read)[0]
            if debugging:
                debug_msg += ' ' + bytes2hex(bytes_read)
            if debugging:
                debug_msg = '%-47s  (%04x, %04x)' % (debug_msg, group, elem)
                if not is_implicit_VR:
                    debug_msg += ' %s ' % VR
                if length != 4294967295:
                    debug_msg += 'Length: %d' % length
                else:
                    debug_msg += 'Length: Undefined length (FFFFFFFF)'
                logger_debug(debug_msg)
            value_tell = fp_tell()
            tag = TupleTag((group, elem))
            if stop_when is not None and stop_when(tag, VR, length):
                if debugging:
                    logger_debug('Reading ended by stop_when callback. Rewinding to start of data element.')
                rewind_length = 8
                if not is_implicit_VR and VR in extra_length_VRs:
                    rewind_length += 4
                fp.seek(value_tell - rewind_length)
                raise StopIteration
            if length != 4294967295:
                if defer_size is not None and length > defer_size:
                    value = None
                    logger_debug('Defer size exceeded. Skipping forward to next data element.')
                    fp.seek(fp_tell() + length)
                else:
                    value = fp_read(length)
                if debugging:
                    dotdot = '   '
                    if length > 12:
                        dotdot = '...'
                    logger_debug('%08x: %-34s %s %r %s' % (value_tell,
                     bytes2hex(value[:12]), dotdot, value[:12], dotdot))
                if tag == (8, 5):
                    from dicom.values import convert_string
                    encoding = convert_string(value, is_little_endian, encoding=default_encoding)
                    encoding = convert_encodings(encoding)
                yield RawDataElement(tag, VR, length, value, value_tell, is_implicit_VR, is_little_endian)
        elif VR is None:
            try:
                VR = dictionaryVR(tag)
            except KeyError:
                next_tag = TupleTag(unpack(endian_chr + 'HH', fp_read(4)))
                fp.seek(fp_tell() - 4)
                if next_tag == ItemTag:
                    VR = 'SQ'

            if VR == 'SQ':
                if debugging:
                    msg = '{0:08x}: Reading/parsing undefined length sequence'
                    logger_debug(msg.format(fp_tell()))
                seq = read_sequence(fp, is_implicit_VR, is_little_endian, length, encoding)
                yield DataElement(tag, VR, seq, value_tell, is_undefined_length=True)
            else:
                delimiter = SequenceDelimiterTag
                if debugging:
                    logger_debug('Reading undefined length data element')
                value = read_undefined_length_value(fp, is_little_endian, delimiter, defer_size)
                if tag == (8, 5):
                    from dicom.values import convert_string
                    encoding = convert_string(value, is_little_endian, encoding=default_encoding)
                    encoding = convert_encodings(encoding)
                yield RawDataElement(tag, VR, length, value, value_tell, is_implicit_VR, is_little_endian)


def read_dataset(fp, is_implicit_VR, is_little_endian, bytelength=None, stop_when=None, defer_size=None, parent_encoding=default_encoding):
    """Return a Dataset instance containing the next dataset in the file.
    :param fp: an opened file object
    :param is_implicit_VR: True if file transfer syntax is implicit VR
    :param is_little_endian: True if file has little endian transfer syntax
    :param bytelength: None to read until end of file or ItemDeliterTag, else
    a fixed number of bytes to read
    :param stop_when: optional call_back function which can terminate reading.
    See help for data_element_generator for details
    :param defer_size: optional size to avoid loading large elements in memory.
    See help for data_element_generator for details
    :param parent_encoding: optional encoding to use as a default in case
    a Specific Character Set (0008,0005) isn't specified
    :returns: a Dataset instance
    """
    raw_data_elements = dict()
    fpStart = fp.tell()
    de_gen = data_element_generator(fp, is_implicit_VR, is_little_endian, stop_when, defer_size, parent_encoding)
    try:
        while bytelength is None or fp.tell() - fpStart < bytelength:
            raw_data_element = next(de_gen)
            tag = raw_data_element.tag
            if tag == (65534, 57357):
                break
            raw_data_elements[tag] = raw_data_element

    except StopIteration:
        pass
    except EOFError as details:
        logger.error(str(details) + ' in file ' + getattr(fp, 'name', '<no filename>'))
    except NotImplementedError as details:
        logger.error(details)

    return Dataset(raw_data_elements)


def read_sequence(fp, is_implicit_VR, is_little_endian, bytelength, encoding, offset=0):
    """Read and return a Sequence -- i.e. a list of Datasets"""
    seq = []
    is_undefined_length = False
    if bytelength != 0:
        if bytelength == 4294967295:
            is_undefined_length = True
            bytelength = None
        fp_tell = fp.tell
        fpStart = fp_tell()
        while not bytelength or fp_tell() - fpStart < bytelength:
            file_tell = fp.tell()
            dataset = read_sequence_item(fp, is_implicit_VR, is_little_endian, encoding, offset)
            if dataset is None:
                break
            dataset.file_tell = file_tell + offset
            seq.append(dataset)

    seq = Sequence(seq)
    seq.is_undefined_length = is_undefined_length
    return seq


def read_sequence_item(fp, is_implicit_VR, is_little_endian, encoding, offset=0):
    """Read and return a single sequence item, i.e. a Dataset"""
    seq_item_tell = fp.tell() + offset
    if is_little_endian:
        tag_length_format = '<HHL'
    else:
        tag_length_format = '>HHL'
    try:
        bytes_read = fp.read(8)
        group, element, length = unpack(tag_length_format, bytes_read)
    except:
        raise IOError('No tag to read at file position {0:05x}'.format(fp.tell() + offset))

    tag = (
     group, element)
    if tag == SequenceDelimiterTag:
        logger.debug('{0:08x}: {1}'.format(fp.tell() - 8 + offset, 'End of Sequence'))
        if length != 0:
            logger.warning('Expected 0x00000000 after delimiter, found 0x%x, at position 0x%x' % (
             length, fp.tell() - 4 + offset))
        return
    if tag != ItemTag:
        logger.warning('Expected sequence item with tag %s at file position 0x%x' % (
         ItemTag, fp.tell() - 4 + offset))
    else:
        logger.debug('{0:08x}: {1}  Found Item tag (start of item)'.format(fp.tell() - 4 + offset, bytes2hex(bytes_read)))
    if length == 4294967295:
        ds = read_dataset(fp, is_implicit_VR, is_little_endian, bytelength=None, parent_encoding=encoding)
        ds.is_undefined_length_sequence_item = True
    else:
        ds = read_dataset(fp, is_implicit_VR, is_little_endian, length, parent_encoding=encoding)
        ds.is_undefined_length_sequence_item = False
        logger.debug('%08x: Finished sequence item' % (fp.tell() + offset,))
    ds.seq_item_tell = seq_item_tell
    return ds


def not_group2(tag, VR, length):
    return tag.group != 2


def _read_file_meta_info(fp):
    """Return the file meta information.
    fp must be set after the 128 byte preamble and 'DICM' marker
    """
    fp_save = fp.tell()
    debugging = dicom.debugging
    if debugging:
        logger.debug('Try to read group length info...')
    bytes_read = fp.read(8)
    group, elem, VR, length = unpack('<HH2sH', bytes_read)
    if debugging:
        debug_msg = '{0:08x}: {1}'.format(fp.tell() - 8, bytes2hex(bytes_read))
    if in_py3:
        VR = VR.decode(default_encoding)
    if VR in extra_length_VRs:
        bytes_read = fp.read(4)
        length = unpack('<L', bytes_read)[0]
        if debugging:
            debug_msg += ' ' + bytes2hex(bytes_read)
    if debugging:
        debug_msg = '{0:<47s}  ({1:04x}, {2:04x}) {3:2s} Length: {4:d}'.format(debug_msg, group, elem, VR, length)
        logger.debug(debug_msg)
    if group == 2 and elem == 0:
        bytes_read = fp.read(length)
        if debugging:
            logger.debug('{0:08x}: {1}'.format(fp.tell() - length, bytes2hex(bytes_read)))
        group_length = unpack('<L', bytes_read)[0]
        expected_ds_start = fp.tell() + group_length
        if debugging:
            msg = 'value (group length) = {0:d}'.format(group_length)
            msg += '  regular dataset should start at {0:08x}'.format(expected_ds_start)
            logger.debug('          ' + msg)
    else:
        expected_ds_start = None
        if debugging:
            logger.debug('          ' + '(0002,0000) Group length not found.')
        if debugging:
            logger.debug('Rewinding and reading whole dataset including this first data element')
        fp.seek(fp_save)
        file_meta = read_dataset(fp, is_implicit_VR=False, is_little_endian=True, stop_when=not_group2)
        fp_now = fp.tell()
        if expected_ds_start and fp_now != expected_ds_start:
            logger.info('*** Group length for file meta dataset did not match end of group 2 data ***')
        elif debugging:
            logger.debug('--- End of file meta data found as expected ---------')
    return file_meta


def read_file_meta_info(filename):
    """Read and return the DICOM file meta information only.

    This function is meant to be used in user code, for quickly going through
    a series of files to find one which is referenced to a particular SOP,
    without having to read the entire files.
    """
    fp = DicomFile(filename, 'rb')
    read_preamble(fp, False)
    return _read_file_meta_info(fp)


def read_preamble(fp, force):
    """Read and return the DICOM preamble and read past the 'DICM' marker.
    If 'DICM' does not exist, assume no preamble, return None, and
    rewind file to the beginning..
    """
    logger.debug('Reading preamble...')
    preamble = fp.read(128)
    if dicom.debugging:
        sample = bytes2hex(preamble[:8]) + '...' + bytes2hex(preamble[-8:])
        logger.debug('{0:08x}: {1}'.format(fp.tell() - 128, sample))
    magic = fp.read(4)
    if magic != b'DICM':
        if force:
            logger.info("File is not a standard DICOM file; 'DICM' header is missing. Assuming no header and continuing")
            preamble = None
            fp.seek(0)
        else:
            raise InvalidDicomError("File is missing 'DICM' marker. Use force=True to force reading")
    else:
        logger.debug("{0:08x}: 'DICM' marker found".format(fp.tell() - 4))
    return preamble


def _at_pixel_data(tag, VR, length):
    return tag == (32736, 16)


def read_partial(fileobj, stop_when=None, defer_size=None, force=False):
    """Parse a DICOM file until a condition is met

    ``read_partial`` is normally not called directly. Use ``read_file``
    instead, unless you need to stop on some condition
    other than reaching pixel data.

    :arg fileobj: a file-like object. This function does not close it.
    :arg stop_when: a callable which takes tag, VR, length,
        and returns True or False. If stop_when returns True,
        read_data_element will raise StopIteration.
        If None (default), then the whole file is read.
    :returns: a FileDataset instance, or if a DICOMDIR, a DicomDir instance.
    """
    preamble = read_preamble(fileobj, force)
    file_meta_dataset = Dataset()
    is_implicit_VR = True
    is_little_endian = True
    if preamble:
        file_meta_dataset = _read_file_meta_info(fileobj)
        transfer_syntax = file_meta_dataset.TransferSyntaxUID
        if transfer_syntax == dicom.UID.ImplicitVRLittleEndian:
            pass
        else:
            if transfer_syntax == dicom.UID.ExplicitVRLittleEndian:
                is_implicit_VR = False
            else:
                if transfer_syntax == dicom.UID.ExplicitVRBigEndian:
                    is_implicit_VR = False
                    is_little_endian = False
                else:
                    if transfer_syntax == dicom.UID.DeflatedExplicitVRLittleEndian:
                        zipped = fileobj.read()
                        unzipped = zlib.decompress(zipped, -zlib.MAX_WBITS)
                        fileobj = BytesIO(unzipped)
                        is_implicit_VR = False
                    else:
                        is_implicit_VR = False
    else:
        file_meta_dataset.TransferSyntaxUID = dicom.UID.ImplicitVRLittleEndian
    try:
        dataset = read_dataset(fileobj, is_implicit_VR, is_little_endian, stop_when=stop_when, defer_size=defer_size)
    except EOFError:
        pass

    class_uid = file_meta_dataset.get('MediaStorageSOPClassUID', None)
    if class_uid and class_uid == 'Media Storage Directory Storage':
        return DicomDir(fileobj, dataset, preamble, file_meta_dataset, is_implicit_VR, is_little_endian)
    else:
        return FileDataset(fileobj, dataset, preamble, file_meta_dataset, is_implicit_VR, is_little_endian)


def read_file(fp, defer_size=None, stop_before_pixels=False, force=False):
    """Read and parse a DICOM file

    :param fp: either a file-like object, or a string containing the file name.
            If a file-like object, the caller is responsible for closing it.
    :param defer_size: if a data element value is larger than defer_size,
            then the value is not read into memory until it is accessed in code.
            Specify an integer (bytes), or a string value with units, e.g.
            "512 KB", "2 MB". Default None means all elements read into memory.
    :param stop_before_pixels: Set True to stop before reading pixels
        (and anything after them).
        If False (default), the full file will be read and parsed.
    :param force: Set to True to force reading even if no header is found.
                  If False, a dicom.filereader.InvalidDicomError is raised
                  when the file is not valid DICOM.
    :returns: a FileDataset instance
    """
    caller_owns_file = True
    if isinstance(fp, str):
        caller_owns_file = False
        logger.debug("Reading file '{0}'".format(fp))
        fp = open(fp, 'rb')
    if dicom.debugging:
        logger.debug('\n' + '-' * 80)
        logger.debug('Call to read_file()')
        msg = "filename:'%s', defer_size='%s', stop_before_pixels=%s, force=%s"
        logger.debug(msg % (fp.name, defer_size, stop_before_pixels, force))
        if caller_owns_file:
            logger.debug('Caller passed file object')
        else:
            logger.debug('Caller passed file name')
        logger.debug('-' * 80)
    stop_when = None
    if stop_before_pixels:
        stop_when = _at_pixel_data
    try:
        dataset = read_partial(fp, stop_when, defer_size=defer_size, force=force)
    finally:
        if not caller_owns_file:
            fp.close()

    return dataset


def read_dicomdir(filename='DICOMDIR'):
    """Read a DICOMDIR file and return a DicomDir instance
    This is just a wrapper around read_file, which gives a default file name

    :param filename: full path and name to DICOMDIR file to open
    :return: a DicomDir instance
    :raise: InvalidDicomError is raised if file is not a DICOMDIR file.
    """
    ds = read_file(filename)
    if not isinstance(ds, DicomDir):
        msg = "File '{0}' is not a Media Storage Directory file".format(filename)
        raise InvalidDicomError(msg)
    return ds


def data_element_offset_to_value(is_implicit_VR, VR):
    """Return number of bytes from start of data element to start of value"""
    if is_implicit_VR:
        offset = 8
    else:
        if VR in extra_length_VRs:
            offset = 12
        else:
            offset = 8
    return offset


def read_deferred_data_element(fileobj_type, filename, timestamp, raw_data_elem):
    """Read the previously deferred value from the file into memory
    and return a raw data element"""
    logger.debug('Reading deferred element %r' % str(raw_data_elem.tag))
    if filename is None:
        raise IOError('Deferred read -- original filename not stored. Cannot re-open')
    if not os.path.exists(filename):
        raise IOError('Deferred read -- original file {0:s} is missing'.format(filename))
    if stat_available and timestamp is not None:
        statinfo = stat(filename)
        if statinfo.st_mtime != timestamp:
            warnings.warn('Deferred read warning -- file modification time has changed.')
    fp = fileobj_type(filename, 'rb')
    is_implicit_VR = raw_data_elem.is_implicit_VR
    is_little_endian = raw_data_elem.is_little_endian
    offset = data_element_offset_to_value(is_implicit_VR, raw_data_elem.VR)
    fp.seek(raw_data_elem.value_tell - offset)
    elem_gen = data_element_generator(fp, is_implicit_VR, is_little_endian, defer_size=None)
    data_elem = next(elem_gen)
    fp.close()
    if data_elem.VR != raw_data_elem.VR:
        raise ValueError('Deferred read VR {0:s} does not match original {1:s}'.format(data_elem.VR, raw_data_elem.VR))
    if data_elem.tag != raw_data_elem.tag:
        raise ValueError('Deferred read tag {0!r} does not match original {1!r}'.format(data_elem.tag, raw_data_elem.tag))
    return data_elem