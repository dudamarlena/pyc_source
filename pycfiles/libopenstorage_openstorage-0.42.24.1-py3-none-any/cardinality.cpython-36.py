# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/framework/common/cardinality.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 988 bytes
"""Defines an enum for classifying RPC methods by streaming semantics."""
import enum

@enum.unique
class Cardinality(enum.Enum):
    __doc__ = 'Describes the streaming semantics of an RPC method.'
    UNARY_UNARY = 'request-unary/response-unary'
    UNARY_STREAM = 'request-unary/response-streaming'
    STREAM_UNARY = 'request-streaming/response-unary'
    STREAM_STREAM = 'request-streaming/response-streaming'