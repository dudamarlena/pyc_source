# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/proto/model_service_pb2_grpc.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 2991 bytes
import grpc, model_service_pb2 as model__service__pb2

class ModelServiceStub(object):

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.publishLoad = channel.unary_unary('/com.webank.ai.fate.api.mlmodel.manager.ModelService/publishLoad',
          request_serializer=(model__service__pb2.PublishRequest.SerializeToString),
          response_deserializer=(model__service__pb2.PublishResponse.FromString))
        self.publishBind = channel.unary_unary('/com.webank.ai.fate.api.mlmodel.manager.ModelService/publishBind',
          request_serializer=(model__service__pb2.PublishRequest.SerializeToString),
          response_deserializer=(model__service__pb2.PublishResponse.FromString))


class ModelServiceServicer(object):

    def publishLoad(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def publishBind(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ModelServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'publishLoad':grpc.unary_unary_rpc_method_handler(servicer.publishLoad,
       request_deserializer=model__service__pb2.PublishRequest.FromString,
       response_serializer=model__service__pb2.PublishResponse.SerializeToString), 
     'publishBind':grpc.unary_unary_rpc_method_handler(servicer.publishBind,
       request_deserializer=model__service__pb2.PublishRequest.FromString,
       response_serializer=model__service__pb2.PublishResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('com.webank.ai.fate.api.mlmodel.manager.ModelService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))