# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/validate.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 30242 bytes
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
import betterproto

@dataclass
class FieldRules(betterproto.Message):
    __doc__ = '\n    FieldRules encapsulates the rules for each type of field. Depending on the\n    field, the correct set should be used to ensure proper validations.\n    '
    message = betterproto.message_field(17)
    message: 'MessageRules'
    float = betterproto.message_field(1, group='type')
    float: 'FloatRules'
    double = betterproto.message_field(2, group='type')
    double: 'DoubleRules'
    int32 = betterproto.message_field(3, group='type')
    int32: 'Int32Rules'
    int64 = betterproto.message_field(4, group='type')
    int64: 'Int64Rules'
    uint32 = betterproto.message_field(5, group='type')
    uint32: 'UInt32Rules'
    uint64 = betterproto.message_field(6, group='type')
    uint64: 'UInt64Rules'
    sint32 = betterproto.message_field(7, group='type')
    sint32: 'SInt32Rules'
    sint64 = betterproto.message_field(8, group='type')
    sint64: 'SInt64Rules'
    fixed32 = betterproto.message_field(9, group='type')
    fixed32: 'Fixed32Rules'
    fixed64 = betterproto.message_field(10, group='type')
    fixed64: 'Fixed64Rules'
    sfixed32 = betterproto.message_field(11, group='type')
    sfixed32: 'SFixed32Rules'
    sfixed64 = betterproto.message_field(12, group='type')
    sfixed64: 'SFixed64Rules'
    bool = betterproto.message_field(13, group='type')
    bool: 'BoolRules'
    string = betterproto.message_field(14, group='type')
    string: 'StringRules'
    bytes = betterproto.message_field(15, group='type')
    bytes: 'BytesRules'
    enum = betterproto.message_field(16, group='type')
    enum: 'EnumRules'
    repeated = betterproto.message_field(18, group='type')
    repeated: 'RepeatedRules'
    map = betterproto.message_field(19, group='type')
    map: 'MapRules'
    any = betterproto.message_field(20, group='type')
    any: 'AnyRules'
    duration = betterproto.message_field(21, group='type')
    duration: 'DurationRules'
    timestamp = betterproto.message_field(22, group='type')
    timestamp: 'TimestampRules'


@dataclass
class FloatRules(betterproto.Message):
    __doc__ = 'FloatRules describes the constraints applied to `float` values'
    const = betterproto.float_field(1)
    const: float
    lt = betterproto.float_field(2)
    lt: float
    lte = betterproto.float_field(3)
    lte: float
    gt = betterproto.float_field(4)
    gt: float
    gte = betterproto.float_field(5)
    gte: float
    in_ = betterproto.float_field(6)
    in_: List[float]
    not_in = betterproto.float_field(7)
    not_in: List[float]


@dataclass
class DoubleRules(betterproto.Message):
    __doc__ = 'DoubleRules describes the constraints applied to `double` values'
    const = betterproto.double_field(1)
    const: float
    lt = betterproto.double_field(2)
    lt: float
    lte = betterproto.double_field(3)
    lte: float
    gt = betterproto.double_field(4)
    gt: float
    gte = betterproto.double_field(5)
    gte: float
    in_ = betterproto.double_field(6)
    in_: List[float]
    not_in = betterproto.double_field(7)
    not_in: List[float]


@dataclass
class Int32Rules(betterproto.Message):
    __doc__ = 'Int32Rules describes the constraints applied to `int32` values'
    const = betterproto.int32_field(1)
    const: int
    lt = betterproto.int32_field(2)
    lt: int
    lte = betterproto.int32_field(3)
    lte: int
    gt = betterproto.int32_field(4)
    gt: int
    gte = betterproto.int32_field(5)
    gte: int
    in_ = betterproto.int32_field(6)
    in_: List[int]
    not_in = betterproto.int32_field(7)
    not_in: List[int]


@dataclass
class Int64Rules(betterproto.Message):
    __doc__ = 'Int64Rules describes the constraints applied to `int64` values'
    const = betterproto.int64_field(1)
    const: int
    lt = betterproto.int64_field(2)
    lt: int
    lte = betterproto.int64_field(3)
    lte: int
    gt = betterproto.int64_field(4)
    gt: int
    gte = betterproto.int64_field(5)
    gte: int
    in_ = betterproto.int64_field(6)
    in_: List[int]
    not_in = betterproto.int64_field(7)
    not_in: List[int]


@dataclass
class UInt32Rules(betterproto.Message):
    __doc__ = 'UInt32Rules describes the constraints applied to `uint32` values'
    const = betterproto.uint32_field(1)
    const: int
    lt = betterproto.uint32_field(2)
    lt: int
    lte = betterproto.uint32_field(3)
    lte: int
    gt = betterproto.uint32_field(4)
    gt: int
    gte = betterproto.uint32_field(5)
    gte: int
    in_ = betterproto.uint32_field(6)
    in_: List[int]
    not_in = betterproto.uint32_field(7)
    not_in: List[int]


@dataclass
class UInt64Rules(betterproto.Message):
    __doc__ = 'UInt64Rules describes the constraints applied to `uint64` values'
    const = betterproto.uint64_field(1)
    const: int
    lt = betterproto.uint64_field(2)
    lt: int
    lte = betterproto.uint64_field(3)
    lte: int
    gt = betterproto.uint64_field(4)
    gt: int
    gte = betterproto.uint64_field(5)
    gte: int
    in_ = betterproto.uint64_field(6)
    in_: List[int]
    not_in = betterproto.uint64_field(7)
    not_in: List[int]


@dataclass
class SInt32Rules(betterproto.Message):
    __doc__ = 'SInt32Rules describes the constraints applied to `sint32` values'
    const = betterproto.sint32_field(1)
    const: int
    lt = betterproto.sint32_field(2)
    lt: int
    lte = betterproto.sint32_field(3)
    lte: int
    gt = betterproto.sint32_field(4)
    gt: int
    gte = betterproto.sint32_field(5)
    gte: int
    in_ = betterproto.sint32_field(6)
    in_: List[int]
    not_in = betterproto.sint32_field(7)
    not_in: List[int]


@dataclass
class SInt64Rules(betterproto.Message):
    __doc__ = 'SInt64Rules describes the constraints applied to `sint64` values'
    const = betterproto.sint64_field(1)
    const: int
    lt = betterproto.sint64_field(2)
    lt: int
    lte = betterproto.sint64_field(3)
    lte: int
    gt = betterproto.sint64_field(4)
    gt: int
    gte = betterproto.sint64_field(5)
    gte: int
    in_ = betterproto.sint64_field(6)
    in_: List[int]
    not_in = betterproto.sint64_field(7)
    not_in: List[int]


@dataclass
class Fixed32Rules(betterproto.Message):
    __doc__ = 'Fixed32Rules describes the constraints applied to `fixed32` values'
    const = betterproto.fixed32_field(1)
    const: float
    lt = betterproto.fixed32_field(2)
    lt: float
    lte = betterproto.fixed32_field(3)
    lte: float
    gt = betterproto.fixed32_field(4)
    gt: float
    gte = betterproto.fixed32_field(5)
    gte: float
    in_ = betterproto.fixed32_field(6)
    in_: List[float]
    not_in = betterproto.fixed32_field(7)
    not_in: List[float]


@dataclass
class Fixed64Rules(betterproto.Message):
    __doc__ = 'Fixed64Rules describes the constraints applied to `fixed64` values'
    const = betterproto.fixed64_field(1)
    const: float
    lt = betterproto.fixed64_field(2)
    lt: float
    lte = betterproto.fixed64_field(3)
    lte: float
    gt = betterproto.fixed64_field(4)
    gt: float
    gte = betterproto.fixed64_field(5)
    gte: float
    in_ = betterproto.fixed64_field(6)
    in_: List[float]
    not_in = betterproto.fixed64_field(7)
    not_in: List[float]


@dataclass
class SFixed32Rules(betterproto.Message):
    __doc__ = 'SFixed32Rules describes the constraints applied to `sfixed32` values'
    const = betterproto.sfixed32_field(1)
    const: float
    lt = betterproto.sfixed32_field(2)
    lt: float
    lte = betterproto.sfixed32_field(3)
    lte: float
    gt = betterproto.sfixed32_field(4)
    gt: float
    gte = betterproto.sfixed32_field(5)
    gte: float
    in_ = betterproto.sfixed32_field(6)
    in_: List[float]
    not_in = betterproto.sfixed32_field(7)
    not_in: List[float]


@dataclass
class SFixed64Rules(betterproto.Message):
    __doc__ = 'SFixed64Rules describes the constraints applied to `sfixed64` values'
    const = betterproto.sfixed64_field(1)
    const: float
    lt = betterproto.sfixed64_field(2)
    lt: float
    lte = betterproto.sfixed64_field(3)
    lte: float
    gt = betterproto.sfixed64_field(4)
    gt: float
    gte = betterproto.sfixed64_field(5)
    gte: float
    in_ = betterproto.sfixed64_field(6)
    in_: List[float]
    not_in = betterproto.sfixed64_field(7)
    not_in: List[float]


@dataclass
class BoolRules(betterproto.Message):
    __doc__ = 'BoolRules describes the constraints applied to `bool` values'
    const = betterproto.bool_field(1)
    const: bool


@dataclass
class StringRules(betterproto.Message):
    __doc__ = 'StringRules describe the constraints applied to `string` values'
    const = betterproto.string_field(1)
    const: str
    len = betterproto.uint64_field(19)
    len: int
    min_len = betterproto.uint64_field(2)
    min_len: int
    max_len = betterproto.uint64_field(3)
    max_len: int
    len_bytes = betterproto.uint64_field(20)
    len_bytes: int
    min_bytes = betterproto.uint64_field(4)
    min_bytes: int
    max_bytes = betterproto.uint64_field(5)
    max_bytes: int
    pattern = betterproto.string_field(6)
    pattern: str
    prefix = betterproto.string_field(7)
    prefix: str
    suffix = betterproto.string_field(8)
    suffix: str
    contains = betterproto.string_field(9)
    contains: str
    not_contains = betterproto.string_field(23)
    not_contains: str
    in_ = betterproto.string_field(10)
    in_: List[str]
    not_in = betterproto.string_field(11)
    not_in: List[str]
    email = betterproto.bool_field(12, group='well_known')
    email: bool
    hostname = betterproto.bool_field(13, group='well_known')
    hostname: bool
    ip = betterproto.bool_field(14, group='well_known')
    ip: bool
    ipv4 = betterproto.bool_field(15, group='well_known')
    ipv4: bool
    ipv6 = betterproto.bool_field(16, group='well_known')
    ipv6: bool
    uri = betterproto.bool_field(17, group='well_known')
    uri: bool
    uri_ref = betterproto.bool_field(18, group='well_known')
    uri_ref: bool
    address = betterproto.bool_field(21, group='well_known')
    address: bool
    uuid = betterproto.bool_field(22, group='well_known')
    uuid: bool


@dataclass
class BytesRules(betterproto.Message):
    __doc__ = 'BytesRules describe the constraints applied to `bytes` values'
    const = betterproto.bytes_field(1)
    const: bytes
    len = betterproto.uint64_field(13)
    len: int
    min_len = betterproto.uint64_field(2)
    min_len: int
    max_len = betterproto.uint64_field(3)
    max_len: int
    pattern = betterproto.string_field(4)
    pattern: str
    prefix = betterproto.bytes_field(5)
    prefix: bytes
    suffix = betterproto.bytes_field(6)
    suffix: bytes
    contains = betterproto.bytes_field(7)
    contains: bytes
    in_ = betterproto.bytes_field(8)
    in_: List[bytes]
    not_in = betterproto.bytes_field(9)
    not_in: List[bytes]
    ip = betterproto.bool_field(10, group='well_known')
    ip: bool
    ipv4 = betterproto.bool_field(11, group='well_known')
    ipv4: bool
    ipv6 = betterproto.bool_field(12, group='well_known')
    ipv6: bool


@dataclass
class EnumRules(betterproto.Message):
    __doc__ = 'EnumRules describe the constraints applied to enum values'
    const = betterproto.int32_field(1)
    const: int
    defined_only = betterproto.bool_field(2)
    defined_only: bool
    in_ = betterproto.int32_field(3)
    in_: List[int]
    not_in = betterproto.int32_field(4)
    not_in: List[int]


@dataclass
class MessageRules(betterproto.Message):
    __doc__ = '\n    MessageRules describe the constraints applied to embedded message values.\n    For message-type fields, validation is performed recursively.\n    '
    skip = betterproto.bool_field(1)
    skip: bool
    required = betterproto.bool_field(2)
    required: bool


@dataclass
class RepeatedRules(betterproto.Message):
    __doc__ = 'RepeatedRules describe the constraints applied to `repeated` values'
    min_items = betterproto.uint64_field(1)
    min_items: int
    max_items = betterproto.uint64_field(2)
    max_items: int
    unique = betterproto.bool_field(3)
    unique: bool
    items = betterproto.message_field(4)
    items: 'FieldRules'


@dataclass
class MapRules(betterproto.Message):
    __doc__ = 'MapRules describe the constraints applied to `map` values'
    min_pairs = betterproto.uint64_field(1)
    min_pairs: int
    max_pairs = betterproto.uint64_field(2)
    max_pairs: int
    no_sparse = betterproto.bool_field(3)
    no_sparse: bool
    keys = betterproto.message_field(4)
    keys: 'FieldRules'
    values = betterproto.message_field(5)
    values: 'FieldRules'


@dataclass
class AnyRules(betterproto.Message):
    __doc__ = '\n    AnyRules describe constraints applied exclusively to the\n    `google.protobuf.Any` well-known type\n    '
    required = betterproto.bool_field(1)
    required: bool
    in_ = betterproto.string_field(2)
    in_: List[str]
    not_in = betterproto.string_field(3)
    not_in: List[str]


@dataclass
class DurationRules(betterproto.Message):
    __doc__ = '\n    DurationRules describe the constraints applied exclusively to the\n    `google.protobuf.Duration` well-known type\n    '
    required = betterproto.bool_field(1)
    required: bool
    const = betterproto.message_field(2)
    const: timedelta
    lt = betterproto.message_field(3)
    lt: timedelta
    lte = betterproto.message_field(4)
    lte: timedelta
    gt = betterproto.message_field(5)
    gt: timedelta
    gte = betterproto.message_field(6)
    gte: timedelta
    in_ = betterproto.message_field(7)
    in_: List[timedelta]
    not_in = betterproto.message_field(8)
    not_in: List[timedelta]


@dataclass
class TimestampRules(betterproto.Message):
    __doc__ = '\n    TimestampRules describe the constraints applied exclusively to the\n    `google.protobuf.Timestamp` well-known type\n    '
    required = betterproto.bool_field(1)
    required: bool
    const = betterproto.message_field(2)
    const: datetime
    lt = betterproto.message_field(3)
    lt: datetime
    lte = betterproto.message_field(4)
    lte: datetime
    gt = betterproto.message_field(5)
    gt: datetime
    gte = betterproto.message_field(6)
    gte: datetime
    lt_now = betterproto.bool_field(7)
    lt_now: bool
    gt_now = betterproto.bool_field(8)
    gt_now: bool
    within = betterproto.message_field(9)
    within: timedelta