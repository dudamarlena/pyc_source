# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: hcpre/duke_siemens/util_mrs_file.py
# Compiled at: 2014-05-12 17:01:30
"""
Helper routines for reading & writing MRS data in various formats.

Except for the map of internal data types to numpy type strings (which
doesn't require an import of numpy), this code is deliberately ignorant of
numpy. It returns native Python types that are easy to convert into
numpy types.
"""
from __future__ import division
import re, struct, os.path, xdrlib, exceptions

class FileNotFoundError(exceptions.Exception):
    """ Specific to VASF. Raised when this module can't find a matching data
    file for a params file or vice versa.
    """
    pass


class UnreadableDataError(exceptions.Exception):
    """ Raised when this module can't make sense of data (raw or XDR) due
    to an unexpected format, buffer underrun (less data than expected),
    buffer overrun (more data than expected), etc.
    """
    pass


class IncompleteMetadataError(exceptions.Exception):
    """ Raised when the metadata associated with a dataset doesn't contain
    required information like the data's type or format.
    """
    pass


_vasf_parameters_regex = re.compile('[[](\\w+\\s*\\w*)[]]')
_vaxml_regex = re.compile('<vasf>|<\\?xml')

class MrsFileTypes(object):
    NONE = 0
    VASF_DATA = 1
    VASF_PARAMETERS = 2
    VAXML = 3
    DICOM_SIEMENS = 4


class DataTypes(object):
    """ Internal representation of data type. INTEGER is for 16 bit values,
    LONG for 32 bit values, FLOAT for 32 bit floats, DOUBLE for 64 bit,
    COMPLEX for two 32 bit floats, COMPLEX_DOUBLE for two 64 bit floats.
    """
    NONE = 0
    BYTE = 1
    INTEGER = 2
    LONG = 3
    FLOAT = 4
    DOUBLE = 5
    COMPLEX = 6
    COMPLEX_DOUBLE = 7
    ALL = (
     BYTE, INTEGER, LONG, FLOAT, DOUBLE, COMPLEX, COMPLEX_DOUBLE)
    _TYPE_SIZES = {NONE: 0, 
       BYTE: 1, 
       INTEGER: 2, 
       LONG: 4, 
       FLOAT: 4, 
       DOUBLE: 8, 
       COMPLEX: 8, 
       COMPLEX_DOUBLE: 16}
    _EXTERNAL_TO_INTERNAL = {'float': FLOAT, 
       'double': DOUBLE, 
       'doublefloat': DOUBLE, 
       'double float': DOUBLE, 
       'shortinteger': INTEGER, 
       'short integer': INTEGER, 
       'integer': INTEGER, 
       'unsignedinteger': INTEGER, 
       'unsigned integer': INTEGER, 
       'integer16bit': INTEGER, 
       'integer 16bit': INTEGER, 
       'integer 16 bit': INTEGER, 
       'integer': INTEGER, 
       'long': LONG, 
       'unsignedlong': LONG, 
       'unsigned long': LONG, 
       'complexinteger8bit': COMPLEX, 
       'complex integer8bit': COMPLEX, 
       'complex integer 8bit': COMPLEX, 
       'complex integer 8 bit': COMPLEX, 
       'complexinteger16bit': COMPLEX, 
       'complex integer16bit': COMPLEX, 
       'complex integer 16bit': COMPLEX, 
       'complex integer 16 bit': COMPLEX, 
       'complexfloat': COMPLEX, 
       'complex float': COMPLEX, 
       'complex': COMPLEX, 
       'complexdouble': COMPLEX_DOUBLE, 
       'complex double': COMPLEX_DOUBLE, 
       'byte': BYTE, 
       'character': BYTE, 
       'int16': INTEGER, 
       'int32': LONG, 
       'float32': FLOAT, 
       'float64': DOUBLE, 
       'complex64': COMPLEX, 
       'complex128': COMPLEX_DOUBLE}
    _INTERNAL_TO_NUMPY = {BYTE: 'byte', 
       INTEGER: 'int16', 
       LONG: 'int32', 
       FLOAT: 'float32', 
       DOUBLE: 'float64', 
       COMPLEX: 'complex64', 
       COMPLEX_DOUBLE: 'complex128'}

    @staticmethod
    def is_complex(the_type):
        return the_type in (DataTypes.COMPLEX, DataTypes.COMPLEX_DOUBLE)

    @staticmethod
    def any_type_to_internal(the_type):
        if the_type in DataTypes.ALL:
            pass
        elif the_type in DataTypes._EXTERNAL_TO_INTERNAL:
            the_type = DataTypes._EXTERNAL_TO_INTERNAL[the_type]
        else:
            raise ValueError, 'Unknown type "%s"' % the_type
        return the_type

    @staticmethod
    def any_type_to_numpy(the_type):
        the_type = DataTypes.any_type_to_internal(the_type)
        return DataTypes._INTERNAL_TO_NUMPY[the_type]


def sniff_file_type(f):
    """ Guesses if a file is a DICOM file, VASF params file, a VASF data file,
    or a VAXML file and returns one of the MrsFileTypes.XXX constants.

    The param f can be a filename (string) or a file object.

    Since VASF data files are just binary glop, they're indistinguishable
    from most other file types and therefore MrsFileTypes.VASF_DATA is
    the default "wild guess" return type.
    """
    file_type = MrsFileTypes.NONE
    close_on_exit = False
    if not hasattr(f, 'read'):
        f = open(f, 'rb')
        close_on_exit = True
    s = f.read(1024)
    if s[128:132] == 'DICM':
        file_type = MrsFileTypes.DICOM_SIEMENS
    elif _vasf_parameters_regex.search(s):
        file_type = MrsFileTypes.VASF_PARAMETERS
    elif _vaxml_regex.search(s):
        file_type = MrsFileTypes.VAXML
    else:
        file_type = MrsFileTypes.VASF_DATA
    if close_on_exit:
        f.close()
    return file_type


def decode_xdr(data, data_type, element_count):
    """ Given a string of data in XDR format and a data type, returns
    an iterable (tuple or list) of Python objects representing the decoded
    data. data_type must be one of the DataTypes.XXX constants defined in
    this module.
    element_count is the number of elements expected in the data.
    """
    p = xdrlib.Unpacker(data)
    is_complex = data_type in (DataTypes.COMPLEX, DataTypes.COMPLEX_DOUBLE)
    if data_type in (DataTypes.COMPLEX, DataTypes.FLOAT):
        unpack_function = p.unpack_float
    else:
        if data_type in (DataTypes.COMPLEX_DOUBLE, DataTypes.DOUBLE):
            unpack_function = p.unpack_double
        else:
            if data_type == DataTypes.LONG:
                unpack_function = p.unpack_int
            elif data_type == DataTypes.INTEGER:
                unpack_function = p.unpack_int
            elif data_type == DataTypes.BYTE:
                unpack_function = p.unpack_byte
            else:
                raise ValueError, "Unknown data type '%s'" % data_type
            if is_complex:
                element_count *= 2
            try:
                data = p.unpack_farray(element_count, unpack_function)
            except (xdrlib.Error, xdrlib.ConversionError) as instance:
                raise UnreadableDataError, instance.msg

        try:
            p.done()
        except xdrlib.Error:
            raise UnreadableDataError, 'More data in file than expected (XDR overrun)'

    if is_complex:
        data = collapse_complexes(data)
    return data


def collapse_complexes(data):
    """Given a list or other iterable that's a series of (real, imaginary)
    pairs, returns a list of complex numbers. For instance, this list --
       [a, b, c, d, e, f]
    this function returns --
       [complex(a, b), complex(c, d), complex(e, f)]

    The returned list is a new list; the original is unchanged.
    """
    return [ complex(data[i], data[(i + 1)]) for i in range(0, len(data), 2) ]


def expand_complexes(data):
    """Expands a list or other iterable of complex numbers into a list of
    (real, imaginary) pairs. For instance, given this list of complex
    numbers --
       [za, zb, zc]
    this function returns --
       [za.real, za.imag, zb.real, zb.imag, zc.real, zc.imag]

    The returned list is a new list; the original is unchanged.
    """
    data = [
     None] * len(data) + list(data)
    j = 0
    for i in range(len(data) // 2, len(data)):
        data[j] = data[i].real
        j += 1
        data[j] = data[i].imag
        j += 1

    return data


def convert_vasf_to_xml(source_filename, target_filename, pack_data=True):
    """ Converts a VASF file pair to VAXML format.
    source_filename can be a VASF parameters or data filename.
    """
    import util_vasf_file, util_vaxml_file
    source_parameters_filename, source_data_filename = util_vasf_file.get_filename_pair(source_filename)
    parameters, data = util_vasf_file.read(source_parameters_filename, source_data_filename)
    util_vaxml_file.write(parameters, parameters['data_type'], data, target_filename, pack_data)


def _test_collapse_expand_complexes():
    import random, numpy
    random.seed()
    LIST_SIZE = random.randint(0, 1000)
    collapsed = []
    raw = []
    for i in range(LIST_SIZE):
        real = random.randint(-1000, 1000) + random.random()
        imaginary = random.randint(-1000, 1000) + random.random()
        raw.append(real)
        raw.append(imaginary)
        collapsed.append(complex(real, imaginary))

    assert collapse_complexes(raw) == collapsed
    assert expand_complexes(collapsed) == raw
    raw = numpy.array(raw)
    collapsed = numpy.array(collapsed)
    assert (numpy.array(collapse_complexes(raw)) == collapsed).all()
    assert (numpy.array(expand_complexes(collapsed)) == raw).all()


if __name__ == '__main__':
    _test_collapse_expand_complexes()