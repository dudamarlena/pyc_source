# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/google/protobuf/internal/wire_format.py
# Compiled at: 2009-12-02 20:07:05
"""Constants and static functions to support protocol buffer wire format."""
__author__ = 'robinson@google.com (Will Robinson)'
import struct
from google.protobuf import message
TAG_TYPE_BITS = 3
_TAG_TYPE_MASK = (1 << TAG_TYPE_BITS) - 1
WIRETYPE_VARINT = 0
WIRETYPE_FIXED64 = 1
WIRETYPE_LENGTH_DELIMITED = 2
WIRETYPE_START_GROUP = 3
WIRETYPE_END_GROUP = 4
WIRETYPE_FIXED32 = 5
_WIRETYPE_MAX = 5
INT32_MAX = int(2147483647)
INT32_MIN = int(-2147483648)
UINT32_MAX = 4294967295
INT64_MAX = 9223372036854775807
INT64_MIN = -9223372036854775808
UINT64_MAX = 18446744073709551615
FORMAT_UINT32_LITTLE_ENDIAN = '<I'
FORMAT_UINT64_LITTLE_ENDIAN = '<Q'
if struct.calcsize(FORMAT_UINT32_LITTLE_ENDIAN) != 4:
    raise AssertionError('Format "I" is not a 32-bit number.')
if struct.calcsize(FORMAT_UINT64_LITTLE_ENDIAN) != 8:
    raise AssertionError('Format "Q" is not a 64-bit number.')

def PackTag(field_number, wire_type):
    """Returns an unsigned 32-bit integer that encodes the field number and
  wire type information in standard protocol message wire format.

  Args:
    field_number: Expected to be an integer in the range [1, 1 << 29)
    wire_type: One of the WIRETYPE_* constants.
  """
    if not 0 <= wire_type <= _WIRETYPE_MAX:
        raise message.EncodeError('Unknown wire type: %d' % wire_type)
    return field_number << TAG_TYPE_BITS | wire_type


def UnpackTag(tag):
    """The inverse of PackTag().  Given an unsigned 32-bit number,
  returns a (field_number, wire_type) tuple.
  """
    return (
     tag >> TAG_TYPE_BITS, tag & _TAG_TYPE_MASK)


def ZigZagEncode(value):
    """ZigZag Transform:  Encodes signed integers so that they can be
  effectively used with varint encoding.  See wire_format.h for
  more details.
  """
    if value >= 0:
        return value << 1
    return value << 1 ^ -1


def ZigZagDecode(value):
    """Inverse of ZigZagEncode()."""
    if not value & 1:
        return value >> 1
    return value >> 1 ^ -1


def Int32ByteSize(field_number, int32):
    return Int64ByteSize(field_number, int32)


def Int64ByteSize(field_number, int64):
    return UInt64ByteSize(field_number, 18446744073709551615 & int64)


def UInt32ByteSize(field_number, uint32):
    return UInt64ByteSize(field_number, uint32)


def UInt64ByteSize(field_number, uint64):
    return _TagByteSize(field_number) + _VarUInt64ByteSizeNoTag(uint64)


def SInt32ByteSize(field_number, int32):
    return UInt32ByteSize(field_number, ZigZagEncode(int32))


def SInt64ByteSize(field_number, int64):
    return UInt64ByteSize(field_number, ZigZagEncode(int64))


def Fixed32ByteSize(field_number, fixed32):
    return _TagByteSize(field_number) + 4


def Fixed64ByteSize(field_number, fixed64):
    return _TagByteSize(field_number) + 8


def SFixed32ByteSize(field_number, sfixed32):
    return _TagByteSize(field_number) + 4


def SFixed64ByteSize(field_number, sfixed64):
    return _TagByteSize(field_number) + 8


def FloatByteSize(field_number, flt):
    return _TagByteSize(field_number) + 4


def DoubleByteSize(field_number, double):
    return _TagByteSize(field_number) + 8


def BoolByteSize(field_number, b):
    return _TagByteSize(field_number) + 1


def EnumByteSize(field_number, enum):
    return UInt32ByteSize(field_number, enum)


def StringByteSize(field_number, string):
    return BytesByteSize(field_number, string.encode('utf-8'))


def BytesByteSize(field_number, b):
    return _TagByteSize(field_number) + _VarUInt64ByteSizeNoTag(len(b)) + len(b)


def GroupByteSize(field_number, message):
    return 2 * _TagByteSize(field_number) + message.ByteSize()


def MessageByteSize(field_number, message):
    return _TagByteSize(field_number) + _VarUInt64ByteSizeNoTag(message.ByteSize()) + message.ByteSize()


def MessageSetItemByteSize(field_number, msg):
    total_size = 2 * _TagByteSize(1) + _TagByteSize(2) + _TagByteSize(3)
    total_size += _VarUInt64ByteSizeNoTag(field_number)
    message_size = msg.ByteSize()
    total_size += _VarUInt64ByteSizeNoTag(message_size)
    total_size += message_size
    return total_size


def _TagByteSize(field_number):
    """Returns the bytes required to serialize a tag with this field number."""
    return _VarUInt64ByteSizeNoTag(PackTag(field_number, 0))


def _VarUInt64ByteSizeNoTag(uint64):
    """Returns the bytes required to serialize a single varint.
  uint64 must be unsigned.
  """
    if uint64 > UINT64_MAX:
        raise message.EncodeError('Value out of range: %d' % uint64)
    bytes = 1
    while uint64 > 127:
        bytes += 1
        uint64 >>= 7

    return bytes