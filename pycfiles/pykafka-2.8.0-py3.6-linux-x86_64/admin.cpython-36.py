# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/protocol/admin.py
# Compiled at: 2018-07-25 17:55:59
# Size of source mod 2**32: 13119 bytes
import struct
from collections import namedtuple
from .base import Request, Response, ConsumerGroupProtocolMetadata, MemberAssignment
from ..utils import struct_helpers

class ListGroupsRequest(Request):
    __doc__ = 'A list groups request\n\n    Specification::\n\n    ListGroupsRequest =>\n    '
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
    __doc__ = 'A list groups response\n\n    Specification::\n\n    ListGroupsResponse => ErrorCode Groups\n      ErrorCode => int16\n      Groups => [GroupId ProtocolType]\n        GroupId => string\n        ProtocolType => string\n    '

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
    __doc__ = 'A describe groups request\n\n    Specification::\n\n    DescribeGroupsRequest => [GroupId]\n      GroupId => string\n    '
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
    __doc__ = 'A describe groups response\n\n    Specification::\n\n\n    DescribeGroupsResponse => [ErrorCode GroupId State ProtocolType Protocol Members]\n      ErrorCode => int16\n      GroupId => string\n      State => string\n      ProtocolType => string\n      Protocol => string\n      Members => [MemberId ClientId ClientHost MemberMetadata MemberAssignment]\n        MemberId => string\n        ClientId => string\n        ClientHost => string\n        MemberMetadata => bytes\n        MemberAssignment => bytes\n    '

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
    __doc__ = 'A create topics request\n\n    Specification::\n\n    CreateTopics Request (Version: 0) => [create_topic_requests] timeout\n        create_topic_requests => topic num_partitions replication_factor [replica_assignment] [config_entries]\n            topic => STRING\n            num_partitions => INT32\n            replication_factor => INT16\n            replica_assignment => partition [replicas]\n                partition => INT32\n                replicas => INT32\n            config_entries => config_name config_value\n                config_name => STRING\n                config_value => NULLABLE_STRING\n        timeout => INT32\n    '
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
    __doc__ = 'A create topics response\n\n    Specification::\n\n    CreateTopics Response (Version: 0) => [topic_errors]\n        topic_errors => topic error_code\n            topic => STRING\n            error_code => INT16\n    '
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
    __doc__ = 'A delete topics request\n\n    Specification::\n\n    DeleteTopics Request (Version: 0) => [topics] timeout\n        topics => STRING\n        timeout => INT32\n    '
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
    __doc__ = 'A delete topics response\n\n    Specification::\n\n    DeleteTopics Response (Version: 0) => [topic_error_codes]\n        topic_error_codes => topic error_code\n            topic => STRING\n            error_code => INT16\n    '
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
    __doc__ = 'An api versions request\n\n    Specification::\n\n        ApiVersions Request (Version: 0) =>\n    '
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
    __doc__ = '\n    Specification::\n\n    ApiVersions Response (Version: 0) => error_code [api_versions]\n        error_code => INT16\n        api_versions => api_key min_version max_version\n            api_key => INT16\n            min_version => INT16\n            max_version => INT16\n    '
    API_KEY = 18

    @classmethod
    def get_versions(cls):
        return {0:ApiVersionsResponse,  1:ApiVersionsResponseV1}

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
    __doc__ = '\n    Specification::\n\n    ApiVersions Response (Version: 1) => error_code [api_versions] throttle_time_ms\n        error_code => INT16\n        api_versions => api_key min_version max_version\n            api_key => INT16\n            min_version => INT16\n            max_version => INT16\n        throttle_time_ms => INT32\n    '

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