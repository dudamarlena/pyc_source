# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/proto/fate_proxy_pb2_grpc.py
# Compiled at: 2020-05-06 02:27:06
# Size of source mod 2**32: 5000 bytes
import grpc, fate_meta_pb2 as fate__meta__pb2, fate_proxy_pb2 as fate__proxy__pb2

class DataTransferServiceStub(object):
    __doc__ = 'data transfer service\n  '

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.push = channel.stream_unary('/com.webank.ai.fate.api.networking.proxy.DataTransferService/push',
          request_serializer=(fate__proxy__pb2.Packet.SerializeToString),
          response_deserializer=(fate__proxy__pb2.Metadata.FromString))
        self.pull = channel.unary_stream('/com.webank.ai.fate.api.networking.proxy.DataTransferService/pull',
          request_serializer=(fate__proxy__pb2.Metadata.SerializeToString),
          response_deserializer=(fate__proxy__pb2.Packet.FromString))
        self.unaryCall = channel.unary_unary('/com.webank.ai.fate.api.networking.proxy.DataTransferService/unaryCall',
          request_serializer=(fate__proxy__pb2.Packet.SerializeToString),
          response_deserializer=(fate__proxy__pb2.Packet.FromString))


class DataTransferServiceServicer(object):
    __doc__ = 'data transfer service\n  '

    def push(self, request_iterator, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def pull(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unaryCall(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataTransferServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'push':grpc.stream_unary_rpc_method_handler(servicer.push,
       request_deserializer=fate__proxy__pb2.Packet.FromString,
       response_serializer=fate__proxy__pb2.Metadata.SerializeToString), 
     'pull':grpc.unary_stream_rpc_method_handler(servicer.pull,
       request_deserializer=fate__proxy__pb2.Metadata.FromString,
       response_serializer=fate__proxy__pb2.Packet.SerializeToString), 
     'unaryCall':grpc.unary_unary_rpc_method_handler(servicer.unaryCall,
       request_deserializer=fate__proxy__pb2.Packet.FromString,
       response_serializer=fate__proxy__pb2.Packet.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('com.webank.ai.fate.api.networking.proxy.DataTransferService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


class RouteServiceStub(object):

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.query = channel.unary_unary('/com.webank.ai.fate.api.networking.proxy.RouteService/query',
          request_serializer=(fate__proxy__pb2.Topic.SerializeToString),
          response_deserializer=(fate__meta__pb2.Endpoint.FromString))


class RouteServiceServicer(object):

    def query(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RouteServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'query': grpc.unary_unary_rpc_method_handler((servicer.query),
                request_deserializer=(fate__proxy__pb2.Topic.FromString),
                response_serializer=(fate__meta__pb2.Endpoint.SerializeToString))}
    generic_handler = grpc.method_handlers_generic_handler('com.webank.ai.fate.api.networking.proxy.RouteService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))