# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\segpy\packer.py
# Compiled at: 2019-12-13 21:48:37
# Size of source mod 2**32: 7716 bytes
from collections import OrderedDict
from struct import Struct
from itertools import zip_longest
import os, sys
sys.path.append(os.path.dirname(__file__)[:-6][:-4][:-13])
from cognitivegeo.src.segpy.datatypes import SEG_Y_TYPE_TO_CTYPE
from cognitivegeo.src.segpy.util import pairwise, intervals_partially_overlap, complementary_intervals

def size_of(t):
    return t.SIZE


def compile_struct(header_format_class, start_offset=0, length_in_bytes=None, endian='>'):
    """Compile a struct description from a record.

    Args:
        header_format_class: A header_format class.

        start_offset: Optional start offset for the header in bytes.  Indicates the position of the start of
            the header in the same reference frame as which the field offsets are given.

        length_in_bytes: Optional length in bytes for the header. If the supplied header described a format shorter
            than this value the returned format will be padded with placeholders for bytes to be discarded. If the
            value is less than the minimum required for the format described by header_format_class an error will be
            raised.

        endian: '>' for big-endian data (the standard and default), '<'
            for little-endian (non-standard).

    Returns:
        A two-tuple containing in the zeroth element a format string which can be used with the struct.unpack function,
        and in the second element containing a list-of-lists for field names.  Each item in the outer list corresponds
        to an element of the tuple of data values returned by struct.unpack(); each name associated with that index is a
        field to which the unpacked value should be assigned.

        format, allocations = compile_struct(TraceHeaderFormat)
        values = struct.unpack(format)
        field_names_to_values = {}
        for field_names, value in zip(allocations, values):
            for field_name in field_names:
                field_names_to_values[field_name] = value
        header = Header(**field_names_to_values)

    Raises:
        ValueError: If header_format_class defines no fields.
        ValueError: If header_format_class contains fields which overlap but are not exactly coincident.
        ValueError: If header_format_class contains coincident fields of different types.
        ValueError: If header_format_class described a format longer than length_in_bytes.

    """
    fields = [getattr(header_format_class, name) for name in header_format_class.ordered_field_names()]
    sorted_fields = sorted(fields, key=(lambda f: f.offset))
    if len(sorted_fields) < 1:
        raise ValueError('Header format class {!r} defines no fields'.format(header_format_class.__name__))
    if len(sorted_fields) > 1:
        for a, b in pairwise(sorted_fields):
            if intervals_partially_overlap(range(a.offset, a.offset + size_of(a.value_type)), range(b.offset, b.offset + size_of(b.value_type))):
                raise ValueError('Record fields {!r} at offset {} and {!r} at offset {} are distinct but overlap.'.format(a.name, a.offset, b.name, b.offset))

    last_field = sorted_fields[(-1)]
    defined_length = last_field.offset - start_offset + size_of(last_field.value_type)
    specified_length = defined_length if length_in_bytes is None else length_in_bytes
    padding_length = specified_length - defined_length
    if padding_length < 0:
        raise ValueError('Header length {!r} bytes defined by {!r} is less than specified length in bytes {!r}'.format(defined_length, header_format_class.__name__, specified_length))
    offset_to_fields = OrderedDict()
    for field in sorted_fields:
        relative_offset = field.offset - start_offset
        if relative_offset not in offset_to_fields:
            offset_to_fields[relative_offset] = []
        if len(offset_to_fields[relative_offset]) > 0:
            if offset_to_fields[relative_offset][0].value_type is not field.value_type:
                raise ValueError('Coincident fields {!r} and {!r} at offset {} have different types {!r} and {!r}'.format(offset_to_fields[relative_offset][0], field, offset_to_fields[relative_offset][0].offset, offset_to_fields[relative_offset][0].value_type, field.value_type))
        offset_to_fields[relative_offset].append(field)

    field_spans = [range(offset, offset + size_of(fields[0].value_type)) for offset, fields in offset_to_fields.items()]
    gap_intervals = complementary_intervals(field_spans, start=0, stop=specified_length)
    format_chunks = [
     endian]
    representative_fields = (fields[0] for fields in offset_to_fields.values())
    for gap_interval, field in zip_longest(gap_intervals, representative_fields, fillvalue=None):
        gap_length = len(gap_interval)
        if gap_length > 0:
            format_chunks.append('x' * gap_length)
        if field is not None:
            format_chunks.append(SEG_Y_TYPE_TO_CTYPE[field.value_type.SEG_Y_TYPE])

    cformat = ''.join(format_chunks)
    field_name_allocations = [[field.name for field in fields] for fields in offset_to_fields.values()]
    return (
     cformat, field_name_allocations)


class HeaderPacker:
    """HeaderPacker"""

    def __init__(self, header_format_class, endian='>'):
        self._header_format_class = header_format_class
        self._format, self._field_name_allocations = compile_struct(header_format_class, header_format_class.START_OFFSET_IN_BYTES, header_format_class.LENGTH_IN_BYTES, endian)
        self._struct = Struct(self._format)

    @property
    def header_format_class(self):
        return self._header_format_class

    def pack(self, header):
        """Pack a header into a buffer.
        """
        if not isinstance(header, self._header_format_class):
            raise TypeError('{}({}) cannot pack header of type {}.'.format(self.__class__.__name__, self._header_format_class.__name__, header.__class__.__name__))
        values = [getattr(header, names[0]) for names in self._field_name_allocations]
        return (self._struct.pack)(*values)

    def unpack(self, buffer):
        """Unpack a header into a header object.

        Overwrites any existing header field values with new values
        obtained from the buffer.

        Returns:
            The header object.
        """
        values = self._struct.unpack(buffer)
        kwargs = {name:value for names, value in zip(self._field_name_allocations, values) for name in names}
        return (self._header_format_class)(**kwargs)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._header_format_class.__name__)


def main():
    from segpy.trace_header import TraceHeaderRev0
    compile_struct(TraceHeaderRev0, 1, 240)


if __name__ == '__main__':
    main()