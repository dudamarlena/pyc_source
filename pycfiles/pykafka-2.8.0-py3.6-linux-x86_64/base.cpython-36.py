# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/protocol/base.py
# Compiled at: 2018-07-25 17:55:59
# Size of source mod 2**32: 7099 bytes
import struct
from collections import namedtuple
from ..exceptions import ERROR_CODES
from ..utils import Serializable, ApiVersionAware, struct_helpers

class Request(Serializable, ApiVersionAware):
    __doc__ = 'Base class for all Requests. Handles writing header information'
    HEADER_LEN = 21
    CLIENT_ID = b'pykafka'
    API_KEY = -1

    @classmethod
    def get_versions(cls):
        return {}

    def _write_header(self, buff, api_version=0, correlation_id=0):
        """Write the header for an outgoing message.

        :param buff: The buffer into which to write the header
        :type buff: buffer
        :param api_version: The "kafka api version id", used for feature flagging
        :type api_version: int
        :param correlation_id: This is a user-supplied integer. It will be
            passed back in the response by the server, unmodified. It is useful
            for matching request and response between the client and server.
        :type correlation_id: int
        """
        fmt = '!ihhih%ds' % len(self.CLIENT_ID)
        struct.pack_into(fmt, buff, 0, len(buff) - 4, self.API_KEY, api_version, correlation_id, len(self.CLIENT_ID), self.CLIENT_ID)

    def get_bytes(self):
        """Serialize the message

        :returns: Serialized message
        :rtype: :class:`bytearray`
        """
        raise NotImplementedError()


class Response(ApiVersionAware):
    __doc__ = 'Base class for Response objects.'
    API_KEY = -1

    @classmethod
    def get_versions(cls):
        return {}

    def raise_error(self, err_code, response):
        """Raise an error based on the Kafka error code

        :param err_code: The error code from Kafka
        :param response: The unpacked raw data from the response
        """
        clsname = str(self.__class__).split('.')[(-1)].split("'")[0]
        raise ERROR_CODES[err_code]('Response Type: "%s"\tResponse: %s' % (
         clsname, response))


class MemberAssignment(object):
    __doc__ = '\n    Protocol specification::\n\n    MemberAssignment => Version PartitionAssignment\n        Version => int16\n        PartitionAssignment => [Topic [Partition]]\n            Topic => string\n            Partition => int32\n        UserData => bytes\n    '

    def __init__(self, partition_assignment, version=1):
        self.version = version
        self.partition_assignment = partition_assignment

    @classmethod
    def from_bytestring(cls, buff):
        if len(buff) == 0:
            return cls(tuple())
        else:
            fmt = 'h [S [i ] ]'
            response = struct_helpers.unpack_from(fmt, buff, 0)
            version = response[0]
            partition_assignment = response[1]
            return cls(partition_assignment, version=version)

    def __len__(self):
        size = 6
        for topic_name, partitions in self.partition_assignment:
            size += 2 + len(topic_name) + 4
            size += 4 * len(partitions)

        return size

    def get_bytes(self):
        output = bytearray(len(self))
        offset = 0
        fmt = '!hi'
        struct.pack_into(fmt, output, offset, self.version, len(self.partition_assignment))
        offset += struct.calcsize(fmt)
        for topic_name, partitions in self.partition_assignment:
            fmt = '!h%dsi' % len(topic_name)
            struct.pack_into(fmt, output, offset, len(topic_name), topic_name, len(partitions))
            offset += struct.calcsize(fmt)
            for partition_id in partitions:
                fmt = '!i'
                struct.pack_into(fmt, output, offset, partition_id)
                offset += struct.calcsize(fmt)

        return output


class ConsumerGroupProtocolMetadata(object):
    __doc__ = '\n    Protocol specification::\n\n    ProtocolMetadata => Version Subscription UserData\n        Version => int16\n        Subscription => [Topic]\n            Topic => string\n        UserData => bytes\n    '

    def __init__(self, version=0, topic_names=None, user_data=b'testuserdata'):
        self.version = version
        self.topic_names = topic_names or [b'dummytopic']
        self.user_data = user_data

    def __len__(self):
        size = 6
        for topic_name in self.topic_names:
            size += 2 + len(topic_name)

        size += 4 + len(self.user_data)
        return size

    def get_bytes(self):
        output = bytearray(len(self))
        offset = 0
        fmt = '!hi'
        struct.pack_into(fmt, output, offset, self.version, len(self.topic_names))
        offset += struct.calcsize(fmt)
        for topic_name in self.topic_names:
            fmt = '!h%ds' % len(topic_name)
            struct.pack_into(fmt, output, offset, len(topic_name), topic_name)
            offset += struct.calcsize(fmt)

        fmt = '!i%ds' % len(self.user_data)
        struct.pack_into(fmt, output, offset, len(self.user_data), self.user_data)
        offset += struct.calcsize(fmt)
        return output

    @classmethod
    def from_bytestring(cls, buff):
        if len(buff) == 0:
            return cls()
        else:
            fmt = 'h [S] Y'
            response = struct_helpers.unpack_from(fmt, buff, 0)
            version = response[0]
            topic_names = response[1]
            user_data = response[2]
            return cls(version, topic_names, user_data)


ApiVersionsSpec = namedtuple('ApiVersionsSpec', ['key', 'min', 'max'])
API_VERSIONS_080 = {0:ApiVersionsSpec(0, 0, 0), 
 1:ApiVersionsSpec(1, 0, 0), 
 2:ApiVersionsSpec(2, 0, 0), 
 3:ApiVersionsSpec(3, 0, 0), 
 4:ApiVersionsSpec(4, 0, 0), 
 5:ApiVersionsSpec(5, 0, 0), 
 6:ApiVersionsSpec(6, 0, 0), 
 7:ApiVersionsSpec(7, 0, 0), 
 8:ApiVersionsSpec(8, 0, 1), 
 9:ApiVersionsSpec(9, 0, 1), 
 10:ApiVersionsSpec(10, 0, 0), 
 11:ApiVersionsSpec(11, 0, 0), 
 12:ApiVersionsSpec(12, 0, 0), 
 13:ApiVersionsSpec(13, 0, 0), 
 14:ApiVersionsSpec(14, 0, 0), 
 15:ApiVersionsSpec(15, 0, 0), 
 16:ApiVersionsSpec(16, 0, 0)}
API_VERSIONS_090 = {0:ApiVersionsSpec(0, 0, 0), 
 1:ApiVersionsSpec(1, 0, 1), 
 2:ApiVersionsSpec(2, 0, 0), 
 3:ApiVersionsSpec(3, 0, 0), 
 4:ApiVersionsSpec(4, 0, 0), 
 5:ApiVersionsSpec(5, 0, 0), 
 6:ApiVersionsSpec(6, 0, 0), 
 7:ApiVersionsSpec(7, 0, 0), 
 8:ApiVersionsSpec(8, 0, 1), 
 9:ApiVersionsSpec(9, 0, 1), 
 10:ApiVersionsSpec(10, 0, 0), 
 11:ApiVersionsSpec(11, 0, 0), 
 12:ApiVersionsSpec(12, 0, 0), 
 13:ApiVersionsSpec(13, 0, 0), 
 14:ApiVersionsSpec(14, 0, 0), 
 15:ApiVersionsSpec(15, 0, 0), 
 16:ApiVersionsSpec(16, 0, 0)}