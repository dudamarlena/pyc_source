# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/google/protobuf/internal/encoder.py
# Compiled at: 2009-12-02 20:07:05
"""Class for encoding protocol message primitives.

Contains the logic for encoding every logical protocol field type
into one of the 5 physical wire types.
"""
__author__ = 'robinson@google.com (Will Robinson)'
import struct
from google.protobuf import message
from google.protobuf.internal import wire_format
from google.protobuf.internal import output_stream

class Encoder(object):
    """Encodes logical protocol buffer fields to the wire format."""

    def __init__(self):
        self._stream = output_stream.OutputStream()

    def ToString(self):
        """Returns all values encoded in this object as a string."""
        return self._stream.ToString()

    def AppendInt32(self, field_number, value):
        """Appends a 32-bit integer to our buffer, varint-encoded."""
        self._AppendTag(field_number, wire_format.WIRETYPE_VARINT)
        self._stream.AppendVarint32(value)

    def AppendInt64(self, field_number, value):
        """Appends a 64-bit integer to our buffer, varint-encoded."""
        self._AppendTag(field_number, wire_format.WIRETYPE_VARINT)
        self._stream.AppendVarint64(value)

    def AppendUInt32(self, field_number, unsigned_value):
        """Appends an unsigned 32-bit integer to our buffer, varint-encoded."""
        self._AppendTag(field_number, wire_format.WIRETYPE_VARINT)
        self._stream.AppendVarUInt32(unsigned_value)

    def AppendUInt64(self, field_number, unsigned_value):
        """Appends an unsigned 64-bit integer to our buffer, varint-encoded."""
        self._AppendTag(field_number, wire_format.WIRETYPE_VARINT)
        self._stream.AppendVarUInt64(unsigned_value)

    def AppendSInt32(self, field_number, value):
        """Appends a 32-bit integer to our buffer, zigzag-encoded and then
    varint-encoded.
    """
        self._AppendTag(field_number, wire_format.WIRETYPE_VARINT)
        zigzag_value = wire_format.ZigZagEncode(value)
        self._stream.AppendVarUInt32(zigzag_value)

    def AppendSInt64(self, field_number, value):
        """Appends a 64-bit integer to our buffer, zigzag-encoded and then
    varint-encoded.
    """
        self._AppendTag(field_number, wire_format.WIRETYPE_VARINT)
        zigzag_value = wire_format.ZigZagEncode(value)
        self._stream.AppendVarUInt64(zigzag_value)

    def AppendFixed32(self, field_number, unsigned_value):
        """Appends an unsigned 32-bit integer to our buffer, in little-endian
    byte-order.
    """
        self._AppendTag(field_number, wire_format.WIRETYPE_FIXED32)
        self._stream.AppendLittleEndian32(unsigned_value)

    def AppendFixed64(self, field_number, unsigned_value):
        """Appends an unsigned 64-bit integer to our buffer, in little-endian
    byte-order.
    """
        self._AppendTag(field_number, wire_format.WIRETYPE_FIXED64)
        self._stream.AppendLittleEndian64(unsigned_value)

    def AppendSFixed32(self, field_number, value):
        """Appends a signed 32-bit integer to our buffer, in little-endian
    byte-order.
    """
        sign = value & 2147483648 and -1 or 0
        if value >> 32 != sign:
            raise message.EncodeError('SFixed32 out of range: %d' % value)
        self._AppendTag(field_number, wire_format.WIRETYPE_FIXED32)
        self._stream.AppendLittleEndian32(value & 4294967295)

    def AppendSFixed64(self, field_number, value):
        """Appends a signed 64-bit integer to our buffer, in little-endian
    byte-order.
    """
        sign = value & 9223372036854775808 and -1 or 0
        if value >> 64 != sign:
            raise message.EncodeError('SFixed64 out of range: %d' % value)
        self._AppendTag(field_number, wire_format.WIRETYPE_FIXED64)
        self._stream.AppendLittleEndian64(value & 18446744073709551615)

    def AppendFloat(self, field_number, value):
        """Appends a floating-point number to our buffer."""
        self._AppendTag(field_number, wire_format.WIRETYPE_FIXED32)
        self._stream.AppendRawBytes(struct.pack('f', value))

    def AppendDouble(self, field_number, value):
        """Appends a double-precision floating-point number to our buffer."""
        self._AppendTag(field_number, wire_format.WIRETYPE_FIXED64)
        self._stream.AppendRawBytes(struct.pack('d', value))

    def AppendBool(self, field_number, value):
        """Appends a boolean to our buffer."""
        self.AppendInt32(field_number, value)

    def AppendEnum(self, field_number, value):
        """Appends an enum value to our buffer."""
        self.AppendInt32(field_number, value)

    def AppendString(self, field_number, value):
        """Appends a length-prefixed unicode string, encoded as UTF-8 to our buffer,
    with the length varint-encoded.
    """
        self.AppendBytes(field_number, value.encode('utf-8'))

    def AppendBytes(self, field_number, value):
        """Appends a length-prefixed sequence of bytes to our buffer, with the
    length varint-encoded.
    """
        self._AppendTag(field_number, wire_format.WIRETYPE_LENGTH_DELIMITED)
        self._stream.AppendVarUInt32(len(value))
        self._stream.AppendRawBytes(value)

    def AppendGroup(self, field_number, group):
        """Appends a group to our buffer.
    """
        self._AppendTag(field_number, wire_format.WIRETYPE_START_GROUP)
        self._stream.AppendRawBytes(group.SerializeToString())
        self._AppendTag(field_number, wire_format.WIRETYPE_END_GROUP)

    def AppendMessage(self, field_number, msg):
        """Appends a nested message to our buffer.
    """
        self._AppendTag(field_number, wire_format.WIRETYPE_LENGTH_DELIMITED)
        self._stream.AppendVarUInt32(msg.ByteSize())
        self._stream.AppendRawBytes(msg.SerializeToString())

    def AppendMessageSetItem(self, field_number, msg):
        """Appends an item using the message set wire format.

    The message set message looks like this:
      message MessageSet {
        repeated group Item = 1 {
          required int32 type_id = 2;
          required string message = 3;
        }
      }
    """
        self._AppendTag(1, wire_format.WIRETYPE_START_GROUP)
        self.AppendInt32(2, field_number)
        self.AppendMessage(3, msg)
        self._AppendTag(1, wire_format.WIRETYPE_END_GROUP)

    def _AppendTag(self, field_number, wire_type):
        """Appends a tag containing field number and wire type information."""
        self._stream.AppendVarUInt32(wire_format.PackTag(field_number, wire_type))