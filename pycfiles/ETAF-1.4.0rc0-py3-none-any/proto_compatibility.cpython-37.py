# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/utils/proto_compatibility.py
# Compiled at: 2020-05-06 02:27:06
# Size of source mod 2**32: 454 bytes
from arch.api.utils import log_utils
try:
    from eggroll.core.proto import basic_meta_pb2
    from eggroll.core.proto import proxy_pb2, proxy_pb2_grpc
except ImportError as e:
    try:
        import arch.api.proto as basic_meta_pb2
        import arch.api.proto as proxy_pb2
        import arch.api.proto as proxy_pb2_grpc
    finally:
        e = None
        del e