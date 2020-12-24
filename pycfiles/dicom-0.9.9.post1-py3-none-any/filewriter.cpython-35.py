# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\filewriter.py
# Compiled at: 2017-01-26 21:09:38
# Size of source mod 2**32: 16141 bytes
"""Write a dicom media file."""
from struct import pack
import logging
logger = logging.getLogger('pydicom')
from dicom import in_py3
from dicom.charset import default_encoding, text_VRs, convert_encodings
from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
from dicom.filebase import DicomFile, DicomFileLike
from dicom.dataset import Dataset
from dicom.dataelem import DataElement
from dicom.tag import Tag, ItemTag, ItemDelimiterTag, SequenceDelimiterTag
from dicom.valuerep import extra_length_VRs
from dicom.tagtools import tag_in_exception

def write_numbers(fp, data_element, struct_format):
    """Write a "value" of type struct_format from the dicom file.

    "Value" can be more than one number.

    struct_format -- the character format as used by the struct module.

    """
    endianChar = '><'[fp.is_little_endian]
    value = data_element.value
    if value == '':
        return
    format_string = endianChar + struct_format
    try:
        try:
            value.append
        except:
            fp.write(pack(format_string, value))
        else:
            for val in value:
                fp.write(pack(format_string, val))

    except Exception as e:
        raise IOError('{0}\nfor data_element:\n{1}'.format(str(e), str(data_element)))


def write_OBvalue(fp, data_element):
    """Write a data_element with VR of 'other byte' (OB)."""
    fp.write(data_element.value)


def write_OWvalue(fp, data_element):
    """Write a data_element with VR of 'other word' (OW).

    Note: This **does not currently do the byte swapping** for Endian state.

    """
    fp.write(data_element.value)


def write_UI(fp, data_element):
    """Write a data_element with VR of 'unique identifier' (UI)."""
    write_string(fp, data_element, '\x00')


def multi_string(val):
    """Put a string together with delimiter if has more than one value"""
    if isinstance(val, (list, tuple)):
        return '\\'.join(val)
    else:
        return val


def write_PN(fp, data_element, padding=b' ', encoding=None):
    if not encoding:
        encoding = [
         default_encoding] * 3
    if data_element.VM == 1:
        val = [
         data_element.value]
    else:
        val = data_element.value
    if isinstance(val[0], str) or in_py3:
        val = [elem.encode(encoding) for elem in val]
    val = (b'\\').join(val)
    if len(val) % 2 != 0:
        val = val + padding
    fp.write(val)


def write_string(fp, data_element, padding=' ', encoding=default_encoding):
    """Write a single or multivalued string."""
    val = multi_string(data_element.value)
    if len(val) % 2 != 0:
        val = val + padding
    if isinstance(val, str):
        val = val.encode(encoding)
    fp.write(val)


def write_number_string(fp, data_element, padding=' '):
    """Handle IS or DS VR - write a number stored as a string of digits."""
    val = data_element.value
    if isinstance(val, (list, tuple)):
        val = '\\'.join((x.original_string if hasattr(x, 'original_string') else str(x)) for x in val)
    else:
        val = val.original_string if hasattr(val, 'original_string') else str(val)
    if len(val) % 2 != 0:
        val = val + padding
    if in_py3:
        val = bytes(val, default_encoding)
    fp.write(val)


def write_data_element(fp, data_element, encoding=default_encoding):
    """Write the data_element to file fp according to dicom media storage rules.
    """
    fp.write_tag(data_element.tag)
    VR = data_element.VR
    if not fp.is_implicit_VR:
        if len(VR) != 2:
            msg = "Cannot write ambiguous VR of '%s' for data element with tag %r." % (VR, data_element.tag)
            msg += '\nSet the correct VR before writing, or use an implicit VR transfer syntax'
            raise ValueError(msg)
        if in_py3:
            fp.write(bytes(VR, default_encoding))
        else:
            fp.write(VR)
        if VR in extra_length_VRs:
            fp.write_US(0)
        if VR not in writers:
            raise NotImplementedError("write_data_element: unknown Value Representation '{0}'".format(VR))
        length_location = fp.tell()
        if not fp.is_implicit_VR and VR not in ('OB', 'OW', 'OF', 'SQ', 'UT', 'UN'):
            fp.write_US(0)
    else:
        fp.write_UL(4294967295)
    encoding = convert_encodings(encoding)
    writer_function, writer_param = writers[VR]
    if VR in text_VRs:
        writer_function(fp, data_element, encoding=encoding[1])
    else:
        if VR in ('PN', 'SQ'):
            writer_function(fp, data_element, encoding=encoding)
        else:
            if writer_param is not None:
                writer_function(fp, data_element, writer_param)
            else:
                writer_function(fp, data_element)
            is_undefined_length = False
            if hasattr(data_element, 'is_undefined_length') and data_element.is_undefined_length:
                is_undefined_length = True
            location = fp.tell()
            fp.seek(length_location)
            if not fp.is_implicit_VR and VR not in ('OB', 'OW', 'OF', 'SQ', 'UT', 'UN'):
                fp.write_US(location - length_location - 2)
            elif not is_undefined_length:
                fp.write_UL(location - length_location - 4)
    fp.seek(location)
    if is_undefined_length:
        fp.write_tag(SequenceDelimiterTag)
        fp.write_UL(0)


def write_dataset(fp, dataset, parent_encoding=default_encoding):
    """Write a Dataset dictionary to the file. Return the total length written."""
    dataset_encoding = dataset.get('SpecificCharacterSet', parent_encoding)
    fpStart = fp.tell()
    tags = sorted(dataset.keys())
    for tag in tags:
        with tag_in_exception(tag):
            write_data_element(fp, dataset[tag], dataset_encoding)

    return fp.tell() - fpStart


def write_sequence(fp, data_element, encoding):
    """Write a dicom Sequence contained in data_element to the file fp."""
    sequence = data_element.value
    for dataset in sequence:
        write_sequence_item(fp, dataset, encoding)


def write_sequence_item(fp, dataset, encoding):
    """Write an item (dataset) in a dicom Sequence to the dicom file fp."""
    fp.write_tag(ItemTag)
    length_location = fp.tell()
    fp.write_UL(4294967295)
    write_dataset(fp, dataset, parent_encoding=encoding)
    if getattr(dataset, 'is_undefined_length_sequence_item', False):
        fp.write_tag(ItemDelimiterTag)
        fp.write_UL(0)
    else:
        location = fp.tell()
        fp.seek(length_location)
        fp.write_UL(location - length_location - 4)
        fp.seek(location)


def write_UN(fp, data_element):
    """Write a byte string for an DataElement of value 'UN' (unknown)."""
    fp.write(data_element.value)


def write_ATvalue(fp, data_element):
    """Write a data_element tag to a file."""
    try:
        iter(data_element.value)
    except TypeError:
        tag = Tag(data_element.value)
        fp.write_tag(tag)
    else:
        tags = [Tag(tag) for tag in data_element.value]
        for tag in tags:
            fp.write_tag(tag)


def _write_file_meta_info(fp, meta_dataset):
    """Write the dicom group 2 dicom storage File Meta Information to the file.

    The file should already be positioned past the 128 byte preamble.
    Raises ValueError if the required data_elements (elements 2,3,0x10,0x12)
    are not in the dataset. If the dataset came from a file read with
    read_file(), then the required data_elements should already be there.
    """
    fp.write(b'DICM')
    fp.is_little_endian = True
    fp.is_implicit_VR = False
    if Tag((2, 1)) not in meta_dataset:
        meta_dataset.add_new((2, 1), 'OB', b'\x00\x01')
    missing = []
    for element in [2, 3, 16, 18]:
        if Tag((2, element)) not in meta_dataset:
            missing.append(Tag((2, element)))

    if missing:
        raise ValueError('Missing required tags {0} for file meta information'.format(str(missing)))
    meta_dataset[(2, 0)] = DataElement((2, 0), 'UL', 0)
    group_length_data_element_size = 12
    group_length_tell = fp.tell()
    length = write_dataset(fp, meta_dataset)
    group_length = length - group_length_data_element_size
    end_of_file_meta = fp.tell()
    fp.seek(group_length_tell)
    group_length_data_element = DataElement((2, 0), 'UL', group_length)
    write_data_element(fp, group_length_data_element)
    fp.seek(end_of_file_meta)


def write_file(filename, dataset, write_like_original=True):
    """Store a Dataset to the filename specified.

    Set dataset.preamble if you want something other than 128 0-bytes.
    If the dataset was read from an existing dicom file, then its preamble
    was stored at read time. It is up to you to ensure the preamble is still
    correct for its purposes.
    If there is no Transfer Syntax tag in the dataset,
       Set dataset.is_implicit_VR, and .is_little_endian
       to determine the transfer syntax used to write the file.
    write_like_original -- True if want to preserve the following for each sequence
        within this dataset:
        - preamble -- if no preamble in read file, than not used here
        - dataset.hasFileMeta -- if writer did not do file meta information,
            then don't write here either
        - seq.is_undefined_length -- if original had delimiters, write them now too,
            instead of the more sensible length characters
        - <dataset>.is_undefined_length_sequence_item -- for datasets that belong to a
            sequence, write the undefined length delimiters if that is
            what the original had
        Set write_like_original = False to produce a "nicer" DICOM file for other readers,
            where all lengths are explicit.
    """
    preamble = getattr(dataset, 'preamble', None)
    if not preamble and not write_like_original:
        preamble = b'\x00' * 128
    file_meta = dataset.file_meta
    if file_meta is None:
        file_meta = Dataset()
    if 'TransferSyntaxUID' not in file_meta:
        if dataset.is_little_endian and dataset.is_implicit_VR:
            file_meta.add_new((2, 16), 'UI', ImplicitVRLittleEndian)
    else:
        if dataset.is_little_endian and not dataset.is_implicit_VR:
            file_meta.add_new((2, 16), 'UI', ExplicitVRLittleEndian)
        else:
            if not dataset.is_little_endian and not dataset.is_implicit_VR:
                file_meta.add_new((2, 16), 'UI', ExplicitVRBigEndian)
            else:
                raise NotImplementedError('pydicom has not been verified for Big Endian with Implicit VR')
        caller_owns_file = True
        if isinstance(filename, str):
            fp = DicomFile(filename, 'wb')
            caller_owns_file = False
        else:
            fp = DicomFileLike(filename)
    try:
        if preamble:
            fp.write(preamble)
            _write_file_meta_info(fp, file_meta)
        fp.is_implicit_VR = dataset.is_implicit_VR
        fp.is_little_endian = dataset.is_little_endian
        write_dataset(fp, dataset)
    finally:
        if not caller_owns_file:
            fp.close()


writers = {'UL': (write_numbers, 'L'), 
 'SL': (write_numbers, 'l'), 
 'US': (write_numbers, 'H'), 
 'SS': (write_numbers, 'h'), 
 'FL': (write_numbers, 'f'), 
 'FD': (write_numbers, 'd'), 
 'OF': (write_numbers, 'f'), 
 'OB': (write_OBvalue, None), 
 'UI': (write_UI, None), 
 'SH': (write_string, None), 
 'DA': (write_string, None), 
 'TM': (write_string, None), 
 'CS': (write_string, None), 
 'PN': (write_PN, None), 
 'LO': (write_string, None), 
 'IS': (write_number_string, None), 
 'DS': (write_number_string, None), 
 'AE': (write_string, None), 
 'AS': (write_string, None), 
 'LT': (write_string, None), 
 'SQ': (write_sequence, None), 
 'UN': (write_UN, None), 
 'AT': (write_ATvalue, None), 
 'ST': (write_string, None), 
 'OW': (write_OWvalue, None), 
 'US or SS': (write_OWvalue, None), 
 'US or OW': (write_OWvalue, None), 
 'US or SS or OW': (write_OWvalue, None), 
 'OW/OB': (write_OBvalue, None), 
 'OB/OW': (write_OBvalue, None), 
 'OB or OW': (write_OBvalue, None), 
 'OW or OB': (write_OBvalue, None), 
 'DT': (write_string, None), 
 'UT': (write_string, None)}