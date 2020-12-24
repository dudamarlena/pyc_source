# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/protocol/admin.py
# Compiled at: 2018-07-25 17:55:59
# Size of source mod 2**32: 13119 bytes
import struct
from collections import namedtuple
from .base import Request, Response, ConsumerGroupProtocolMetadata, MemberAssignment
from ..utils import struct_helpers

class ListGroupsRequest(Request):
    """ListGroupsRequest"""
    API_KEY = 16

    def get_bytes(self):
        """Create a new list group request"""
        output = bytearray(len(self))
        self._write_header(output)
        return output

    def __len__(self):
        """Length of the serialized message, in bytes"""
        return self.HEADER_LEN


GroupListing = namedtuple('GroupListing', [
 'group_id', 'protocol_type'])

class ListGroupsResponse(Response):
    """ListGroupsResponse"""

    def __init__(self, buff):
        """Deserialize into a new Response

        :param buff: Serialized message
        :type buff: :class:`bytearray`
        """
        fmt = 'h [SS]'
        response = struct_helpers.unpack_from(fmt, buff, 0)
        self.error = response[0]
        self.groups = {}
        for group_info in response[1]:
            listing = GroupListing(*group_info)
            self.groups[listing.group_id] = listing


class DescribeGroupsRequest(Request):
    """DescribeGroupsRequest"""
    API_KEY = 15

    def __init__(self, group_ids):
        self.group_ids = group_ids

    def get_bytes(self):
        """Create a new list group request"""
        output = bytearray(len(self))
        self._write_header(output)
        offset = self.HEADER_LEN
        fmt = '!i'
        struct.pack_into(fmt, output, offset, len(self.group_ids))
        offset += struct.calcsize(fmt)
        for group_id in self.group_ids:
            fmt = '!h%ds' % len(group_id)
            struct.pack_into(fmt, output, offset, len(group_id), group_id)
            offset += struct.calcsize(fmt)

        return output

    def __len__(self):
        """Length of the serialized message, in bytes"""
        size = self.HEADER_LEN + 4
        for group_id in self.group_ids:
            size += 2 + len(group_id)

        return size


GroupMember = namedtuple('GroupMember', [
 'member_id', 'client_id', 'client_host', 'member_metadata', 'member_assignment'])
DescribeGroupResponse = namedtuple('DescribeGroupResponse', [
 'error_code', 'group_id', 'state', 'protocol_type', 'protocol', 'members'])

class DescribeGroupsResponse(Response):
    """DescribeGroupsResponse"""

    def __init__(self, buff):
        """Deserialize into a new Response

        :param buff: Serialized message
        :type buff: :class:`bytearray`
        """
        fmt = '[hSSSS [SSSYY ] ]'
        response = struct_helpers.unpack_from(fmt, buff, 0)
        self.groups = {}
        for group_info in response:
            members = {}
            for member_info in group_info[5]:
                member_metadata = ConsumerGroupProtocolMetadata.from_bytestring(member_info[3])
                member_assignment = MemberAssignment.from_bytestring(member_info[4])
                member = GroupMember(*member_info[:3] + (member_metadata,
                 member_assignment))
                members[member.member_id] = member

            group = DescribeGroupResponse(*group_info[:5] + (members,))
            self.groups[group.group_id] = group


_CreateTopicRequest = namedtuple('CreateTopicRequest', [
 'topic_name', 'num_partitions', 'replication_factor', 'replica_assignment',
 'config_entries'])

class CreateTopicRequest(_CreateTopicRequest):

    def __new__(cls, topic_name, num_partitions, replication_factor, replica_assignment, config_entries):
        return super(CreateTopicRequest, cls).__new__(cls, topic_name, num_partitions, replication_factor, replica_assignment, config_entries)


class CreateTopicsRequest(Request):
    """CreateTopicsRequest"""
    API_KEY = 19

    def __init__(self, topic_requests, timeout=0):
        self.topic_requests = topic_requests
        self.timeout = timeout

    def __len__(self):
        """Length of the serialized message, in bytes"""
        size = self.HEADER_LEN + 4
        for topic_req in self.topic_requests:
            size += 2 + len(topic_req.topic_name)
            size += 10
            for partition, replicas in topic_req.replica_assignment:
                size += 8 + 4 * len(replicas)

            size += 4
            for config_name, config_value in topic_req.config_entries:
                size += 2 + len(config_name) + 2 + len(config_value)

        size += 4
        return size

    def get_bytes(self):
        """Create a new create topics request"""
        output = bytearray(len(self))
        self._write_header(output)
        offset = self.HEADER_LEN
        fmt = '!i'
        struct.pack_into(fmt, output, offset, len(self.topic_requests))
        offset += struct.calcsize(fmt)
        for topic_req in self.topic_requests:
            fmt = '!h%dsihi' % len(topic_req.topic_name)
            struct.pack_into(fmt, output, offset, len(topic_req.topic_name), topic_req.topic_name, topic_req.num_partitions, topic_req.replication_factor, len(topic_req.replica_assignment))
            offset += struct.calcsize(fmt)
            for partition, replicas in topic_req.replica_assignment:
                fmt = '!ii'
                struct.pack_into(fmt, output, offset, partition, len(replicas))
                offset += struct.calcsize(fmt)
                for replica in replicas:
                    fmt = '!i'
                    struct.pack_into(fmt, output, offset, replica)
                    offset += struct.calcsize(fmt)

            fmt = '!i'
            struct.pack_into(fmt, output, offset, len(topic_req.config_entries))
            offset += struct.calcsize(fmt)
            for config_name, config_value in topic_req.config_entries:
                fmt = '!h%dsh%ds' % (len(config_name), len(config_value))
                struct.pack_into(fmt, output, offset, len(config_name), config_name, len(config_value), config_value)
                offset += struct.calcsize(fmt)

        fmt = '!i'
        struct.pack_into(fmt, output, offset, self.timeout)
        offset += struct.calcsize(fmt)
        return output


class CreateTopicsResponse(Response):
    """CreateTopicsResponse"""
    API_KEY = 19

    def __init__(self, buff):
        """Deserialize into a new Response

        :param buff: Serialized message
        :type buff: :class:`bytearray`
        """
        fmt = '[Sh]'
        response = struct_helpers.unpack_from(fmt, buff, 0)
        for _, error_code in response:
            if error_code != 0:
                self.raise_error(error_code, response)


class DeleteTopicsRequest(Request):
    """DeleteTopicsRequest"""
    API_KEY = 20

    def __init__(self, topics, timeout=0):
        self.topics = topics
        self.timeout = timeout

    def __len__(self):
        """Length of the serialized message, in bytes"""
        size = self.HEADER_LEN + 4
        for topic in self.topics:
            size += 2 + len(topic)

        size += 4
        return size

    def get_bytes(self):
        """Create a new delete topics request"""
        output = bytearray(len(self))
        self._write_header(output)
        offset = self.HEADER_LEN
        fmt = '!i'
        struct.pack_into(fmt, output, offset, len(self.topics))
        offset += struct.calcsize(fmt)
        for topic in self.topics:
            fmt = '!h%ds' % len(topic)
            struct.pack_into(fmt, output, offset, len(topic), topic)
            offset += struct.calcsize(fmt)

        fmt = '!i'
        struct.pack_into(fmt, output, offset, self.timeout)
        offset += struct.calcsize(fmt)
        return output


class DeleteTopicsResponse(Response):
    """DeleteTopicsResponse"""
    API_KEY = 20

    def __init__(self, buff):
        """Deserialize into a new Response

        :param buff: Serialized message
        :type buff: :class:`bytearray`
        """
        fmt = '[Sh]'
        response = struct_helpers.unpack_from(fmt, buff, 0)
        for _, error_code in response:
            if error_code != 0:
                self.raise_error(error_code, response)


class ApiVersionsRequest(Request):
    """ApiVersionsRequest"""
    API_KEY = 18

    def get_bytes(self):
        """Create a new api versions request"""
        output = bytearray(len(self))
        self._write_header(output)
        return output

    def __len__(self):
        """Length of the serialized message, in bytes"""
        size = self.HEADER_LEN
        return size


ApiVersionsSpec = namedtuple('ApiVersionsSpec', ['key', 'min', 'max'])

class ApiVersionsResponse(Response):
    """ApiVersionsResponse"""
    API_KEY = 18

    @classmethod
    def get_versions(cls):
        return {0:ApiVersionsResponse, 
         1:ApiVersionsResponseV1}

    def __init__(self, buff):
        """Deserialize into a new Response

        :param buff: Serialized message
        :type buff: :class:`bytearray`
        """
        fmt = 'h [hhh]'
        response = struct_helpers.unpack_from(fmt, buff, 0)
        self.api_versions = {}
        for api_key, min_v, max_v in response[1]:
            self.api_versions[api_key] = ApiVersionsSpec(api_key, min_v, max_v)


class ApiVersionsResponseV1(ApiVersionsResponse):
    """ApiVersionsResponseV1"""

    def __init__(self, buff):
        """Deserialize into a new Response

        :param buff: Serialized message
        :type buff: :class:`bytearray`
        """
        fmt = 'h [hhh]i'
        response = struct_helpers.unpack_from(fmt, buff, 0)
        self.api_versions = {}
        for api_key, min_v, max_v in response[1]:
            self.api_versions[api_key] = ApiVersionsSpec(api_key, min_v, max_v)

        self.throttle_time = response[2]