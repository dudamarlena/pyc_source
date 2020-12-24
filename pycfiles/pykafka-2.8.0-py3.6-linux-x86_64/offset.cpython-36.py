# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = 'Offset request for a specific topic/partition\n    :ivar topic_name: Name of the topic to look up\n    :ivar partition_id: Id of the partition to look up\n    :ivar offsets_before: Retrieve offset information for messages before\n                          this timestamp (ms). -1 will retrieve the latest\n                          offsets and -2 will retrieve the earliest\n                          available offset. If -2,only 1 offset is returned\n    :ivar max_offsets: How many offsets to return\n    '


class ListOffsetRequest(Request):
    __doc__ = 'An offset request\n    Specification::\n        ListOffsetRequest => ReplicaId [TopicName [Partition Time MaxNumberOfOffsets]]\n          ReplicaId => int32\n          TopicName => string\n          Partition => int32\n          Time => int64\n          MaxNumberOfOffsets => int32\n    '
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
    __doc__ = '\n    Specification::\n        ListOffsetRequest => ReplicaId [TopicName [Partition Time]]\n          ReplicaId => int32\n          TopicName => string\n          Partition => int32\n          Time => int64\n    '
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
    __doc__ = 'An offset response\n    Specification::\n        ListOffsetResponse => [TopicName [PartitionOffsets]]\n          PartitionOffsets => Partition ErrorCode [Offset]\n          Partition => int32\n          ErrorCode => int16\n          Offset => int64\n    '
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
    __doc__ = '\n    Specification::\n        ListOffsetResponse => [TopicName [PartitionOffsets]]\n          PartitionOffsets => Partition ErrorCode Timestamp [Offset]\n          Partition => int32\n          ErrorCode => int16\n          Timestamp => int64\n          Offset => int64\n    '
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