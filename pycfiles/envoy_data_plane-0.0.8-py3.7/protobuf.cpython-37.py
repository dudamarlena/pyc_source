# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/google/protobuf.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 1079 bytes
from dataclasses import dataclass
import betterproto

@dataclass
class Any(betterproto.Message):
    type_url = betterproto.string_field(1)
    type_url: str
    value = betterproto.bytes_field(2)
    value: bytes


@dataclass
class Struct(betterproto.Message):
    fields = betterproto.map_field(1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    fields: betterproto.Dict[(str, 'Value')]


@dataclass
class Value(betterproto.Message):
    null_value = betterproto.enum_field(1, group='kind')
    null_value: 'NullValue'
    number_value = betterproto.double_field(2, group='kind')
    number_value: float
    string_value = betterproto.string_field(3, group='kind')
    string_value: str
    bool_value = betterproto.bool_field(4, group='kind')
    bool_value: bool
    struct_value = betterproto.message_field(5, group='kind')
    struct_value: 'Struct'
    list_value = betterproto.message_field(6, group='kind')
    list_value: 'ListValue'


@dataclass
class ListValue(betterproto.Message):
    values = betterproto.message_field(1)
    values: betterproto.List['Value']


@dataclass
class Empty(betterproto.Message):
    pass


class NullValue(betterproto.Enum):
    NULL_VALUE = 0