# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/protocol/offset.py
# Compiled at: 2018-07-25 17:55:59
# Size of source mod 2**32: 7022 bytes
import struct
from collections import namedtuple, defaultdict
from .base import Request, Response
from ..utils import struct_helpers
from ..utils.compat import iteritems
_PartitionOffsetRequest = namedtuple('PartitionOffsetRequest', [
 'topic_name', 'partition_id', 'offsets_before', 'max_offsets'])

class PartitionOffsetRequest(_PartitionOffsetRequest):
    """PartitionOffsetRequest"""
    pass


class ListOffsetRequest(Request):
    """ListOffsetRequest"""
    API_VERSION = 0
    API_KEY = 2

    @classmethod
    def get_versions(cls):
        return {0:ListOffsetRequest, 
         1:ListOffsetRequest}

    def __init__(self, partition_requests):
        """Create a new offset request"""
        self._reqs = defaultdict(dict)
        for t in partition_requests:
            self._reqs[t.topic_name][t.partition_id] = (
             t.offsets_before,
             t.max_offsets)

    def __len__(self):
        """Length of the serialized message, in bytes"""
        size = self.HEADER_LEN + 4 + 4
        for topic, parts in iteritems(self._reqs):
            size += 2 + len(topic) + 4
            size += 16 * len(parts)

        return size

    def get_bytes(self):
        """Serialize the message
        :returns: Serialized message
        :rtype: :class:`bytearray`
        """
        output = bytearray(len(self))
        self._write_header(output, api_version=(self.API_VERSION))
        offset = self.HEADER_LEN
        struct.pack_into('!ii', output, offset, -1, len(self._reqs))
        offset += 8
        for topic_name, partitions in iteritems(self._reqs):
            fmt = '!h%dsi' % len(topic_name)
            struct.pack_into(fmt, output, offset, len(topic_name), topic_name, len(partitions))
            offset += struct.calcsize(fmt)
            for pnum, (offsets_before, max_offsets) in iteritems(partitions):
                struct.pack_into('!iqi', output, offset, pnum, offsets_before, max_offsets)
                offset += 16

        return output


class ListOffsetRequestV1(ListOffsetRequest):
    """ListOffsetRequestV1"""
    API_VERSION = 1

    def __init__(self, partition_requests):
        """Create a new offset request"""
        self._reqs = defaultdict(dict)
        for t in partition_requests:
            self._reqs[t.topic_name][t.partition_id] = t.offsets_before

    def __len__(self):
        """Length of the serialized message, in bytes"""
        size = self.HEADER_LEN + 4 + 4
        for topic, parts in iteritems(self._reqs):
            size += 2 + len(topic) + 4
            size += 12 * len(parts)

        return size

    def get_bytes(self):
        """Serialize the message
        :returns: Serialized message
        :rtype: :class:`bytearray`
        """
        output = bytearray(len(self))
        self._write_header(output, api_version=(self.API_VERSION))
        offset = self.HEADER_LEN
        struct.pack_into('!ii', output, offset, -1, len(self._reqs))
        offset += 8
        for topic_name, partitions in iteritems(self._reqs):
            fmt = '!h%dsi' % len(topic_name)
            struct.pack_into(fmt, output, offset, len(topic_name), topic_name, len(partitions))
            offset += struct.calcsize(fmt)
            for pnum, offsets_before in iteritems(partitions):
                struct.pack_into('!iq', output, offset, pnum, offsets_before)
                offset += 12

        return output


OffsetPartitionResponse = namedtuple('OffsetPartitionResponse', [
 'offset', 'err'])
OffsetPartitionResponseV1 = namedtuple('OffsetPartitionResponseV1', [
 'offset', 'timestamp', 'err'])

class ListOffsetResponse(Response):
    """ListOffsetResponse"""
    API_VERSION = 0
    API_KEY = 2

    @classmethod
    def get_versions(cls):
        return {0:ListOffsetResponse, 
         1:ListOffsetResponse}

    def __init__(self, buff):
        """Deserialize into a new Response
        :param buff: Serialized message
        :type buff: :class:`bytearray`
        """
        fmt = '[S [ih [q] ] ]'
        response = struct_helpers.unpack_from(fmt, buff, 0)
        self.topics = {}
        for topic_name, partitions in response:
            self.topics[topic_name] = {}
            for partition in partitions:
                self.topics[topic_name][partition[0]] = OffsetPartitionResponse(partition[2], partition[1])


class ListOffsetResponseV1(ListOffsetResponse):
    """ListOffsetResponseV1"""
    API_VERSION = 1

    def __init__(self, buff):
        """Deserialize into a new Response
        :param buff: Serialized message
        :type buff: :class:`bytearray`
        """
        fmt = '[S [ihq [q] ] ]'
        response = struct_helpers.unpack_from(fmt, buff, 0)
        self.topics = {}
        for topic_name, partitions in response:
            self.topics[topic_name] = {}
            for partition in partitions:
                self.topics[topic_name][partition[0]] = OffsetPartitionResponseV1(partition[3], partition[2], partition[1])