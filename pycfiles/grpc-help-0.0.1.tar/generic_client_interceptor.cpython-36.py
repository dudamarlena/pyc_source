# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caowenbin/xuetangx/grpc-help/grpc_help/generic_client_interceptor.py
# Compiled at: 2018-12-26 03:00:28
# Size of source mod 2**32: 1905 bytes
import grpc

class _GenericClientInterceptor(grpc.UnaryUnaryClientInterceptor, grpc.UnaryStreamClientInterceptor, grpc.StreamUnaryClientInterceptor, grpc.StreamStreamClientInterceptor):

    def __init__(self, interceptor_function):
        self._fn = interceptor_function

    def intercept_unary_unary(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = self._fn(client_call_details, iter((request,)), False, False)
        response = continuation(new_details, next(new_request_iterator))
        if postprocess:
            return postprocess(response)
        else:
            return response

    def intercept_unary_stream(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = self._fn(client_call_details, iter((request,)), False, True)
        response_it = continuation(new_details, next(new_request_iterator))
        if postprocess:
            return postprocess(response_it)
        else:
            return response_it

    def intercept_stream_unary(self, continuation, client_call_details, request_iterator):
        new_details, new_request_iterator, postprocess = self._fn(client_call_details, request_iterator, True, False)
        response = continuation(new_details, new_request_iterator)
        if postprocess:
            return postprocess(response)
        else:
            return response

    def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        new_details, new_request_iterator, postprocess = self._fn(client_call_details, request_iterator, True, True)
        response_it = continuation(new_details, new_request_iterator)
        if postprocess:
            return postprocess(response_it)
        else:
            return response_it


def create(intercept_call):
    return _GenericClientInterceptor(intercept_call)