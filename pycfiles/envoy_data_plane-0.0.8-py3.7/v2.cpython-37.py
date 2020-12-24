# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/envoy/type/tracing/v2.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 2949 bytes
from dataclasses import dataclass
import betterproto
from envoy_data_plane.envoy.type.metadata import v2

@dataclass
class CustomTag(betterproto.Message):
    __doc__ = 'Describes custom tags for the active span. [#next-free-field: 6]'
    tag = betterproto.string_field(1)
    tag: str
    literal = betterproto.message_field(2, group='type')
    literal: 'CustomTagLiteral'
    environment = betterproto.message_field(3, group='type')
    environment: 'CustomTagEnvironment'
    request_header = betterproto.message_field(4, group='type')
    request_header: 'CustomTagHeader'
    metadata = betterproto.message_field(5, group='type')
    metadata: 'CustomTagMetadata'


@dataclass
class CustomTagLiteral(betterproto.Message):
    __doc__ = 'Literal type custom tag with static value for the tag value.'
    value = betterproto.string_field(1)
    value: str


@dataclass
class CustomTagEnvironment(betterproto.Message):
    __doc__ = 'Environment type custom tag with environment name and default value.'
    name = betterproto.string_field(1)
    name: str
    default_value = betterproto.string_field(2)
    default_value: str


@dataclass
class CustomTagHeader(betterproto.Message):
    __doc__ = 'Header type custom tag with header name and default value.'
    name = betterproto.string_field(1)
    name: str
    default_value = betterproto.string_field(2)
    default_value: str


@dataclass
class CustomTagMetadata(betterproto.Message):
    __doc__ = '\n    Metadata type custom tag using :ref:`MetadataKey\n    <envoy_api_msg_type.metadata.v2.MetadataKey>` to retrieve the protobuf\n    value from :ref:`Metadata <envoy_api_msg_core.Metadata>`, and populate the\n    tag value with `the canonical JSON <https://developers.google.com/protocol-\n    buffers/docs/proto3#json>`_ representation of it.\n    '
    kind = betterproto.message_field(1)
    kind: v2.MetadataKind
    metadata_key = betterproto.message_field(2)
    metadata_key: v2.MetadataKey
    default_value = betterproto.string_field(3)
    default_value: str