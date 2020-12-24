# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/protocol/produce.py
# Compiled at: 2018-08-15 14:22:35
# Size of source mod 2**32: 5385 bytes
import itertools, struct
from collections import namedtuple, defaultdict
from .base import Request, Response
from .message import MessageSet
from ..common import CompressionType
from ..utils import struct_helpers
from ..utils.compat import iteritems, itervalues

class ProduceRequest(Request):
    """ProduceRequest"""
    API_KEY = 0

    def __init__(self, compression_type=CompressionType.NONE, required_acks=1, timeout=10000, broker_version='0.9.0'):
        """Create a new ProduceRequest
        ``required_acks`` determines how many acknowledgement the server waits
        for before returning. This is useful for ensuring the replication factor
        of published messages. The behavior is::
            -1: Block until all servers acknowledge
            0: No waiting -- server doesn't even respond to the Produce request
            1: Wait for this server to write to the local log and then return
            2+: Wait for N servers to acknowledge
        :param partition_requests: Iterable of
            :class:`kafka.pykafka.protocol.PartitionProduceRequest` for this request
        :param compression_type: Compression to use for messages
        :param required_acks: see docstring
        :param timeout: timeout (in ms) to wait for the required acks
        """
        self.msets = defaultdict(lambda : defaultdict(lambda : MessageSet(compression_type=compression_type, broker_version=broker_version)))
        self.required_acks = required_acks
        self.timeout = timeout
        self._message_count = 0

    def __len__(self):
        """Length of the serialized message, in bytes"""
        size = self.HEADER_LEN + 2 + 4 + 4
        for topic, parts in iteritems(self.msets):
            size += 2 + len(topic) + 4
            size += sum(8 + len(mset) for mset in itervalues(parts))

        return size

    @property
    def messages(self):
        """Iterable of all messages in the Request"""
        return itertools.chain.from_iterable(mset.messages for topic, partitions in iteritems(self.msets) for partition_id, mset in iteritems(partitions))

    def add_message(self, message, topic_name, partition_id):
        """Add a list of :class:`kafka.common.Message` to the waiting request
        :param messages: an iterable of :class:`kafka.common.Message` to add
        :param topic_name: the name of the topic to publish to
        :param partition_id: the partition to publish to
        """
        self.msets[topic_name][partition_id].messages.append(message)
        self._message_count += 1

    def get_bytes(self):
        """Serialize the message
        :returns: Serialized message
        :rtype: :class:`bytearray`
        """
        output = bytearray(len(self))
        self._write_header(output)
        offset = self.HEADER_LEN
        struct.pack_into('!hii', output, offset, self.required_acks, self.timeout, len(self.msets))
        offset += 10
        for topic_name, partitions in iteritems(self.msets):
            fmt = '!h%dsi' % len(topic_name)
            struct.pack_into(fmt, output, offset, len(topic_name), topic_name, len(partitions))
            offset += struct.calcsize(fmt)
            for partition_id, message_set in iteritems(partitions):
                mset_len = len(message_set)
                struct.pack_into('!ii', output, offset, partition_id, mset_len)
                offset += 8
                message_set.pack_into(output, offset)
                offset += mset_len

        return output

    def message_count(self):
        """Get the number of messages across all MessageSets in the request."""
        return self._message_count


ProducePartitionResponse = namedtuple('ProducePartitionResponse', [
 'err', 'offset'])

class ProduceResponse(Response):
    """ProduceResponse"""

    def __init__(self, buff):
        """Deserialize into a new Response
        :param buff: Serialized message
        :type buff: :class:`bytearray`
        """
        fmt = '[S [ihq] ]'
        response = struct_helpers.unpack_from(fmt, buff, 0)
        self.topics = {}
        for topic, partitions in response:
            self.topics[topic] = {}
            for partition in partitions:
                pres = ProducePartitionResponse(partition[1], partition[2])
                self.topics[topic][partition[0]] = pres