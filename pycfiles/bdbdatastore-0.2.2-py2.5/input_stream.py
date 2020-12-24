# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/google/protobuf/internal/input_stream.py
# Compiled at: 2009-12-02 20:07:05
"""InputStream is the primitive interface for reading bits from the wire.

All protocol buffer deserialization can be expressed in terms of
the InputStream primitives provided here.
"""
__author__ = 'robinson@google.com (Will Robinson)'
import struct
from google.protobuf import message
from google.protobuf.internal import wire_format
from array import array

class InputStream(object):
    """Contains all logic for reading bits, and dealing with stream position.

  If an InputStream method ever raises an exception, the stream is left
  in an indeterminate state and is not safe for further use.
  """

    def __init__(self, s):
        self._buffer = array('B', s)
        self._pos = 0

    def EndOfStream(self):
        """Returns true iff we're at the end of the stream.
    If this returns true, then a call to any other InputStream method
    will raise an exception.
    """
        return self._pos >= len(self._buffer)

    def Position(self):
        """Returns the current position in the stream, or equivalently, the
    number of bytes read so far.
    """
        return self._pos

    def GetSubBuffer(self, size=None):
        """Returns a sequence-like object that represents a portion of our
    underlying sequence.

    Position 0 in the returned object corresponds to self.Position()
    in this stream.

    If size is specified, then the returned object ends after the
    next "size" bytes in this stream.  If size is not specified,
    then the returned object ends at the end of this stream.

    We guarantee that the returned object R supports the Python buffer
    interface (and thus that the call buffer(R) will work).

    Note that the returned buffer is read-only.

    The intended use for this method is for nested-message and nested-group
    deserialization, where we want to make a recursive MergeFromString()
    call on the portion of the original sequence that contains the serialized
    nested message.  (And we'd like to do so without making unnecessary string
    copies).

    REQUIRES: size is nonnegative.
    """
        if size is None:
            return self._buffer[self._pos:]
        else:
            if size < 0:
                raise message.DecodeError('Negative size %d' % size)
            return self._buffer[self._pos:self._pos + size]
        return

    def SkipBytes(self, num_bytes):
        """Skip num_bytes bytes ahead, or go to the end of the stream, whichever
    comes first.

    REQUIRES: num_bytes is nonnegative.
    """
        if num_bytes < 0:
            raise message.DecodeError('Negative num_bytes %d' % num_bytes)
        self._pos += num_bytes
        self._pos = min(self._pos, len(self._buffer))

    def ReadBytes(self, size):
        """Reads up to 'size' bytes from the stream, stopping early
    only if we reach the end of the stream.  Returns the bytes read
    as a string.
    """
        if size < 0:
            raise message.DecodeError('Negative size %d' % size)
        s = self._buffer[self._pos:self._pos + size]
        self._pos += len(s)
        if len(s) == 0:
            return ''
        else:
            return reduce(lambda x, y: x + y, map(chr, s))

    def ReadLittleEndian32(self):
        """Interprets the next 4 bytes of the stream as a little-endian
    encoded, unsiged 32-bit integer, and returns that integer.
    """
        try:
            i = struct.unpack(wire_format.FORMAT_UINT32_LITTLE_ENDIAN, self._buffer[self._pos:self._pos + 4])
            self._pos += 4
            return i[0]
        except struct.error, e:
            raise message.DecodeError(e)

    def ReadLittleEndian64(self):
        """Interprets the next 8 bytes of the stream as a little-endian
    encoded, unsiged 64-bit integer, and returns that integer.
    """
        try:
            i = struct.unpack(wire_format.FORMAT_UINT64_LITTLE_ENDIAN, self._buffer[self._pos:self._pos + 8])
            self._pos += 8
            return i[0]
        except struct.error, e:
            raise message.DecodeError(e)

    def ReadVarint32(self):
        """Reads a varint from the stream, interprets this varint
    as a signed, 32-bit integer, and returns the integer.
    """
        i = self.ReadVarint64()
        if not wire_format.INT32_MIN <= i <= wire_format.INT32_MAX:
            raise message.DecodeError('Value out of range for int32: %d' % i)
        return int(i)

    def ReadVarUInt32(self):
        """Reads a varint from the stream, interprets this varint
    as an unsigned, 32-bit integer, and returns the integer.
    """
        i = self.ReadVarUInt64()
        if i > wire_format.UINT32_MAX:
            raise message.DecodeError('Value out of range for uint32: %d' % i)
        return i

    def ReadVarint64(self):
        """Reads a varint from the stream, interprets this varint
    as a signed, 64-bit integer, and returns the integer.
    """
        i = self.ReadVarUInt64()
        if i > wire_format.INT64_MAX:
            i -= 18446744073709551616
        return i

    def ReadVarUInt64(self):
        """Reads a varint from the stream, interprets this varint
    as an unsigned, 64-bit integer, and returns the integer.
    """
        i = self._ReadVarintHelper()
        if not 0 <= i <= wire_format.UINT64_MAX:
            raise message.DecodeError('Value out of range for uint64: %d' % i)
        return i

    def _ReadVarintHelper(self):
        """Helper for the various varint-reading methods above.
    Reads an unsigned, varint-encoded integer from the stream and
    returns this integer.

    Does no bounds checking except to ensure that we read at most as many bytes
    as could possibly be present in a varint-encoded 64-bit number.
    """
        result = 0
        shift = 0
        while 1:
            if shift >= 64:
                raise message.DecodeError('Too many bytes when decoding varint.')
            try:
                b = self._buffer[self._pos]
            except IndexError:
                raise message.DecodeError('Truncated varint.')

            self._pos += 1
            result |= (b & 127) << shift
            shift += 7
            if not b & 128:
                return result