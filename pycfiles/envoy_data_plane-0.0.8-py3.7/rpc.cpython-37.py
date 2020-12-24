# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/google/rpc.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 1374 bytes
from dataclasses import dataclass
from typing import List
import betterproto
from envoy_data_plane.google import protobuf

@dataclass
class Status(betterproto.Message):
    __doc__ = '\n    The `Status` type defines a logical error model that is suitable for\n    different programming environments, including REST APIs and RPC APIs. It is\n    used by [gRPC](https://github.com/grpc). Each `Status` message contains\n    three pieces of data: error code, error message, and error details. You can\n    find out more about this error model and how to work with it in the [API\n    Design Guide](https://cloud.google.com/apis/design/errors).\n    '
    code = betterproto.int32_field(1)
    code: int
    message = betterproto.string_field(2)
    message: str
    details = betterproto.message_field(3)
    details: List[protobuf.Any]