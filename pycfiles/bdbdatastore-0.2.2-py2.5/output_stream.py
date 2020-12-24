# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/google/protobuf/internal/output_stream.py
# Compiled at: 2009-12-02 20:07:05
"""OutputStream is the primitive interface for sticking bits on the wire.

All protocol buffer serialization can be expressed in terms of
the OutputStream primitives provided here.
"""
__author__ = 'robinson@google.com (Will Robinson)'
import array, struct
from google.protobuf import message
from google.protobuf.internal import wire_format

class OutputStream(object):
    """Contains all logic for writing bits, and ToString() to get the result."""

    def __init__(self):
        self._buffer = array.array('B')

    def AppendRawBytes(self, raw_bytes):
        """Appends raw_bytes to our internal buffer."""
        self._buffer.fromstring(raw_bytes)

    def AppendLittleEndian32(self, unsigned_value):
        """Appends an unsigned 32-bit integer to the internal buffer,
    in little-endian byte order.
    """
        if not 0 <= unsigned_value <= wire_format.UINT32_MAX:
            raise message.EncodeError('Unsigned 32-bit out of range: %d' % unsigned_value)
        self._buffer.fromstring(struct.pack(wire_format.FORMAT_UINT32_LITTLE_ENDIAN, unsigned_value))

    def AppendLittleEndian64(self, unsigned_value):
        """Appends an unsigned 64-bit integer to the internal buffer,
    in little-endian byte order.
    """
        if not 0 <= unsigned_value <= wire_format.UINT64_MAX:
            raise message.EncodeError('Unsigned 64-bit out of range: %d' % unsigned_value)
        self._buffer.fromstring(struct.pack(wire_format.FORMAT_UINT64_LITTLE_ENDIAN, unsigned_value))

    def AppendVarint32(self, value):
        """Appends a signed 32-bit integer to the internal buffer,
    encoded as a varint.  (Note that a negative varint32 will
    always require 10 bytes of space.)
    """
        if not wire_format.INT32_MIN <= value <= wire_format.INT32_MAX:
            raise message.EncodeError('Value out of range: %d' % value)
        self.AppendVarint64(value)

    def AppendVarUInt32(self, value):
        """Appends an unsigned 32-bit integer to the internal buffer,
    encoded as a varint.
    """
        if not 0 <= value <= wire_format.UINT32_MAX:
            raise message.EncodeError('Value out of range: %d' % value)
        self.AppendVarUInt64(value)

    def AppendVarint64(self, value):
        """Appends a signed 64-bit integer to the internal buffer,
    encoded as a varint.
    """
        if not wire_format.INT64_MIN <= value <= wire_format.INT64_MAX:
            raise message.EncodeError('Value out of range: %d' % value)
        if value < 0:
            value += 18446744073709551616
        self.AppendVarUInt64(value)

    def AppendVarUInt64(self, unsigned_value):
        """Appends an unsigned 64-bit integer to the internal buffer,
    encoded as a varint.
    """
        if not 0 <= unsigned_value <= wire_format.UINT64_MAX:
            raise message.EncodeError('Value out of range: %d' % unsigned_value)
        while True:
            bits = unsigned_value & 127
            unsigned_value >>= 7
            if not unsigned_value:
                self._buffer.append(bits)
                break
            self._buffer.append(128 | bits)

    def ToString(self):
        """Returns a string containing the bytes in our internal buffer."""
        return self._buffer.tostring()