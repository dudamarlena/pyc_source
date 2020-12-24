# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/lazo_index/lazo_index_pb2_grpc.py
# Compiled at: 2019-06-01 23:00:55
# Size of source mod 2**32: 2423 bytes
import grpc
from . import lazo_index_pb2 as lazo__index__pb2

class LazoIndexStub(object):
    __doc__ = 'Service responsible for indexing the values of a textual or categorical\n  column using Lazo.\n  '

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.IndexData = channel.stream_unary('/lazo_index.LazoIndex/IndexData',
          request_serializer=(lazo__index__pb2.ColumnValue.SerializeToString),
          response_deserializer=(lazo__index__pb2.LazoSketchData.FromString))
        self.QueryData = channel.stream_unary('/lazo_index.LazoIndex/QueryData',
          request_serializer=(lazo__index__pb2.Value.SerializeToString),
          response_deserializer=(lazo__index__pb2.LazoQueryResults.FromString))


class LazoIndexServicer(object):
    __doc__ = 'Service responsible for indexing the values of a textual or categorical\n  column using Lazo.\n  '

    def IndexData(self, request_iterator, context):
        """Obtains a stream of values from a column and returns its
    corresponding Lazo sketch.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryData(self, request_iterator, context):
        """Obtains a stream of values from an input column, queries the Lazo index,
    and returns all the datasets that intersect with that input column.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LazoIndexServicer_to_server(servicer, server):
    rpc_method_handlers = {'IndexData':grpc.stream_unary_rpc_method_handler(servicer.IndexData,
       request_deserializer=lazo__index__pb2.ColumnValue.FromString,
       response_serializer=lazo__index__pb2.LazoSketchData.SerializeToString), 
     'QueryData':grpc.stream_unary_rpc_method_handler(servicer.QueryData,
       request_deserializer=lazo__index__pb2.Value.FromString,
       response_serializer=lazo__index__pb2.LazoQueryResults.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('lazo_index.LazoIndex', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))