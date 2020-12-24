# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sail_utils\cv\head\protobuf\inference_head_detection_pb2_grpc.py
# Compiled at: 2020-03-27 07:10:09
# Size of source mod 2**32: 1772 bytes
import grpc
import sail_utils.cv.head.protobuf.inference_head_detection_pb2 as inference__head__detection__pb2

class HeadDetectionStub(object):

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.DetectHead = channel.unary_unary('/inference_head_detection.HeadDetection/DetectHead',
          request_serializer=(inference__head__detection__pb2.ObjectDetectionRequest.SerializeToString),
          response_deserializer=(inference__head__detection__pb2.ObjectDetectionResponse.FromString))


class HeadDetectionServicer(object):

    def DetectHead(self, request, context):
        """unary-unary (In a single call, both client and server can only send and receive data once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HeadDetectionServicer_to_server(servicer, server):
    rpc_method_handlers = {'DetectHead': grpc.unary_unary_rpc_method_handler((servicer.DetectHead),
                     request_deserializer=(inference__head__detection__pb2.ObjectDetectionRequest.FromString),
                     response_serializer=(inference__head__detection__pb2.ObjectDetectionResponse.SerializeToString))}
    generic_handler = grpc.method_handlers_generic_handler('inference_head_detection.HeadDetection', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))