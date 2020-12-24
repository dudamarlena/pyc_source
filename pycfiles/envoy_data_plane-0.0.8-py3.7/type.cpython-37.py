# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/envoy/type.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 3047 bytes
from dataclasses import dataclass
import betterproto

class FractionalPercentDenominatorType(betterproto.Enum):
    HUNDRED = 0
    TEN_THOUSAND = 1
    MILLION = 2


class CodecClientType(betterproto.Enum):
    HTTP1 = 0
    HTTP2 = 1
    HTTP3 = 2


@dataclass
class Percent(betterproto.Message):
    __doc__ = 'Identifies a percentage, in the range [0.0, 100.0].'
    value = betterproto.double_field(1)
    value: float


@dataclass
class FractionalPercent(betterproto.Message):
    __doc__ = '\n    A fractional percentage is used in cases in which for performance reasons\n    performing floating point to integer conversions during randomness\n    calculations is undesirable. The message includes both a numerator and\n    denominator that together determine the final fractional value. *\n    **Example**: 1/100 = 1%. * **Example**: 3/10000 = 0.03%.\n    '
    numerator = betterproto.uint32_field(1)
    numerator: int
    denominator = betterproto.enum_field(2)
    denominator: 'FractionalPercentDenominatorType'


@dataclass
class SemanticVersion(betterproto.Message):
    __doc__ = '\n    Envoy uses SemVer (https://semver.org/). Major/minor versions indicate\n    expected behaviors and APIs, the patch version field is used only for\n    security fixes and can be generally ignored.\n    '
    major_number = betterproto.uint32_field(1)
    major_number: int
    minor_number = betterproto.uint32_field(2)
    minor_number: int
    patch = betterproto.uint32_field(3)
    patch: int


@dataclass
class Int64Range(betterproto.Message):
    __doc__ = '\n    Specifies the int64 start and end of the range using half-open interval\n    semantics [start, end).\n    '
    start = betterproto.int64_field(1)
    start: int
    end = betterproto.int64_field(2)
    end: int


@dataclass
class Int32Range(betterproto.Message):
    __doc__ = '\n    Specifies the int32 start and end of the range using half-open interval\n    semantics [start, end).\n    '
    start = betterproto.int32_field(1)
    start: int
    end = betterproto.int32_field(2)
    end: int


@dataclass
class DoubleRange(betterproto.Message):
    __doc__ = '\n    Specifies the double start and end of the range using half-open interval\n    semantics [start, end).\n    '
    start = betterproto.double_field(1)
    start: float
    end = betterproto.double_field(2)
    end: float