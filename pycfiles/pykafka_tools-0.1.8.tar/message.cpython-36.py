# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/protocol/message.py
# Compiled at: 2018-08-15 14:22:35
# Size of source mod 2**32: 11790 bytes
from datetime import datetime
import struct
from pkg_resources import parse_version
from six import integer_types
from zlib import crc32
from ..common import CompressionType, Message
from ..exceptions import MessageSetDecodeFailure
from ..utils import Serializable, struct_helpers, compression
from ..utils.compat import buffer

class Message(Message, Serializable):
    """Message"""
    __slots__ = [
     'compression_type',
     'partition_key',
     'value',
     'offset',
     'partition_id',
     'partition',
     'produce_attempt',
     'delivery_report_q',
     'protocol_version',
     'timestamp']
    VALID_TS_TYPES = integer_types + (float, type(None))

    def __init__(self, value, partition_key=None, compression_type=CompressionType.NONE, offset=-1, partition_id=-1, produce_attempt=0, protocol_version=0, timestamp=None, delivery_report_q=None):
        self.compression_type = compression_type
        self.partition_key = partition_key
        self.value = value
        self.offset = offset
        if timestamp is None:
            if protocol_version > 0:
                timestamp = datetime.utcnow()
        else:
            self.set_timestamp(timestamp)
            self.partition_id = partition_id
            self.partition = None
            self.produce_attempt = produce_attempt
            self.delivery_report_q = delivery_report_q
            assert protocol_version in (0, 1)
        self.protocol_version = protocol_version

    def __len__(self):
        size = 14
        if self.value is not None:
            size += len(self.value)
        if self.partition_key is not None:
            size += len(self.partition_key)
        if self.protocol_version > 0:
            if self.timestamp:
                size += 8
        return size

    @classmethod
    def decode(self, buff, msg_offset=-1, partition_id=-1):
        crc, protocol_version, attr = struct_helpers.unpack_from('iBB', buff, 0)
        offset = 6
        timestamp = 0
        if protocol_version > 0:
            timestamp, = struct_helpers.unpack_from('Q', buff, offset)
            offset += 8
        key, val = struct_helpers.unpack_from('YY', buff, offset)
        return Message(val, partition_key=key,
          compression_type=attr,
          offset=msg_offset,
          protocol_version=protocol_version,
          timestamp=timestamp,
          partition_id=partition_id)

    def pack_into(self, buff, offset):
        """Serialize and write to ``buff`` starting at offset ``offset``.

        Intentionally follows the pattern of ``struct.pack_into``

        :param buff: The buffer to write into
        :param offset: The offset to start the write at
        """
        len_key = -1 if self.partition_key is None else len(self.partition_key)
        len_value = -1 if self.value is None else len(self.value)
        protocol_version = self.protocol_version
        if self.protocol_version == 1:
            if self.timestamp:
                fmt = '!BBQi%dsi%ds' % (max(len_key, 0), max(len_value, 0))
        else:
            protocol_version = 0
            fmt = '!BBi%dsi%ds' % (max(len_key, 0), max(len_value, 0))
        args = [
         protocol_version,
         self.compression_type,
         len_key,
         self.partition_key or '',
         len_value,
         self.value or '']
        if protocol_version > 0:
            args.insert(2, int(self.timestamp))
        (struct.pack_into)(fmt, buff, offset + 4, *args)
        fmt_size = struct.calcsize(fmt)
        data = buffer(buff[offset + 4:offset + 4 + fmt_size])
        crc = crc32(data) & 4294967295
        struct.pack_into('!I', buff, offset, crc)

    @property
    def timestamp_dt(self):
        """Get the timestamp as a datetime, if valid"""
        if self.timestamp > 0:
            return datetime.utcfromtimestamp(self.timestamp / 1000.0)

    @timestamp_dt.setter
    def timestamp_dt(self, dt):
        """Set the timestamp from a datetime object"""
        self.timestamp = int(1000 * (dt - datetime(1970, 1, 1)).total_seconds())

    def set_timestamp(self, ts):
        if type(ts) in self.VALID_TS_TYPES:
            self.timestamp = ts
        else:
            if type(ts) == datetime:
                self.timestamp_dt = ts
            else:
                raise RuntimeError()


class MessageSet(Serializable):
    """MessageSet"""

    def __init__(self, compression_type=CompressionType.NONE, messages=None, broker_version='0.9.0'):
        """Create a new MessageSet

        :param compression_type: Compression to use on the messages
        :param messages: An initial list of messages for the set
        :param broker_version: A broker version with which this MessageSet is compatible
        """
        self.compression_type = compression_type
        self._messages = messages or []
        self._compressed = None
        self._broker_version = broker_version

    def __len__(self):
        """Length of the serialized message, in bytes

        We don't put the MessageSetSize in front of the serialization
        because that's *technically* not part of the MessageSet. Most
        requests/responses using MessageSets need that size, though, so
        be careful when using this.
        """
        if self.compression_type == CompressionType.NONE:
            messages = self._messages
        else:
            if self._compressed is None:
                self._compressed = self._get_compressed()
            messages = [
             self._compressed]
        return 12 * len(messages) + sum(len(m) for m in messages)

    @property
    def messages(self):
        self._compressed = None
        return self._messages

    def _get_compressed(self):
        """Get a compressed representation of all current messages.

        Returns a Message object with correct headers set and compressed
        data in the value field.
        """
        if not self.compression_type != CompressionType.NONE:
            raise AssertionError
        else:
            tmp_mset = MessageSet(messages=(self._messages))
            uncompressed = bytearray(len(tmp_mset))
            tmp_mset.pack_into(uncompressed, 0)
            if self.compression_type == CompressionType.GZIP:
                compressed = compression.encode_gzip(buffer(uncompressed))
            else:
                if self.compression_type == CompressionType.SNAPPY:
                    compressed = compression.encode_snappy(buffer(uncompressed))
                else:
                    if self.compression_type == CompressionType.LZ4:
                        if parse_version(self._broker_version) >= parse_version('0.10.0'):
                            compressed = compression.encode_lz4(buffer(uncompressed))
                        else:
                            compressed = compression.encode_lz4_old_kafka(buffer(uncompressed))
                    else:
                        raise TypeError('Unknown compression: %s' % self.compression_type)
        protocol_version = max(m.protocol_version for m in self._messages)
        return Message(compressed, compression_type=(self.compression_type), protocol_version=protocol_version)

    @classmethod
    def decode(cls, buff, partition_id=-1):
        """Decode a serialized MessageSet."""
        messages = []
        offset = 0
        attempted = False
        while offset < len(buff):
            if len(buff) - offset < 12:
                break
            msg_offset, size = struct.unpack_from('!qi', buff, offset)
            offset += 12
            attempted = True
            if len(buff) - offset < size:
                break
            message = Message.decode((buff[offset:offset + size]), msg_offset,
              partition_id=partition_id)
            messages.append(message)
            offset += size

        if len(messages) == 0:
            if attempted:
                raise MessageSetDecodeFailure(size)
        return MessageSet(messages=messages)

    def pack_into(self, buff, offset):
        """Serialize and write to ``buff`` starting at offset ``offset``.

        Intentionally follows the pattern of ``struct.pack_into``

        :param buff: The buffer to write into
        :param offset: The offset to start the write at
        """
        if self.compression_type == CompressionType.NONE:
            messages = self._messages
        else:
            if self._compressed is None:
                self._compressed = self._get_compressed()
            messages = [
             self._compressed]
        for message in messages:
            mlen = len(message)
            struct.pack_into('!qi', buff, offset, -1, mlen)
            offset += 12
            message.pack_into(buff, offset)
            offset += mlen