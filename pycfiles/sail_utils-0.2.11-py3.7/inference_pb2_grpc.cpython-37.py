# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sail_utils\cv\object\protobuf\inference_pb2_grpc.py
# Compiled at: 2020-04-07 01:46:40
# Size of source mod 2**32: 1656 bytes
import grpc
import sail_utils.cv.object.protobuf.inference_pb2 as inference__pb2

class KeyObjectDetectionStub(object):

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.DetectKeyObject = channel.unary_unary('/inference.KeyObjectDetection/DetectKeyObject',
          request_serializer=(inference__pb2.ObjectDetectionRequest.SerializeToString),
          response_deserializer=(inference__pb2.ObjectDetectionResponse.FromString))


class KeyObjectDetectionServicer(object):

    def DetectKeyObject(self, request, context):
        """unary-unary (In a single call, both client and server can only send and receive data once.)
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KeyObjectDetectionServicer_to_server(servicer, server):
    rpc_method_handlers = {'DetectKeyObject': grpc.unary_unary_rpc_method_handler((servicer.DetectKeyObject),
                          request_deserializer=(inference__pb2.ObjectDetectionRequest.FromString),
                          response_serializer=(inference__pb2.ObjectDetectionResponse.SerializeToString))}
    generic_handler = grpc.method_handlers_generic_handler('inference.KeyObjectDetection', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))