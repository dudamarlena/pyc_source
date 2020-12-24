# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/proto/admission_control_pb2_grpc.py
# Compiled at: 2019-09-11 21:20:08
# Size of source mod 2**32: 3233 bytes
import grpc, admission_control_pb2 as admission__control__pb2, get_with_proof_pb2 as get__with__proof__pb2

class AdmissionControlStub(object):
    __doc__ = '-----------------------------------------------------------------------------\n  ---------------- Service definition\n  -----------------------------------------------------------------------------\n  '

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.SubmitTransaction = channel.unary_unary('/admission_control.AdmissionControl/SubmitTransaction',
          request_serializer=(admission__control__pb2.SubmitTransactionRequest.SerializeToString),
          response_deserializer=(admission__control__pb2.SubmitTransactionResponse.FromString))
        self.UpdateToLatestLedger = channel.unary_unary('/admission_control.AdmissionControl/UpdateToLatestLedger',
          request_serializer=(get__with__proof__pb2.UpdateToLatestLedgerRequest.SerializeToString),
          response_deserializer=(get__with__proof__pb2.UpdateToLatestLedgerResponse.FromString))


class AdmissionControlServicer(object):
    __doc__ = '-----------------------------------------------------------------------------\n  ---------------- Service definition\n  -----------------------------------------------------------------------------\n  '

    def SubmitTransaction(self, request, context):
        """Public API to submit transaction to a validator.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateToLatestLedger(self, request, context):
        """This API is used to update the client to the latest ledger version and
    optionally also request 1..n other pieces of data.  This allows for batch
    queries.  All queries return proofs that a client should check to validate
    the data. Note that if a client only wishes to update to the latest
    LedgerInfo and receive the proof of this latest version, they can simply
    omit the requested_items (or pass an empty list)
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AdmissionControlServicer_to_server(servicer, server):
    rpc_method_handlers = {'SubmitTransaction':grpc.unary_unary_rpc_method_handler(servicer.SubmitTransaction,
       request_deserializer=admission__control__pb2.SubmitTransactionRequest.FromString,
       response_serializer=admission__control__pb2.SubmitTransactionResponse.SerializeToString), 
     'UpdateToLatestLedger':grpc.unary_unary_rpc_method_handler(servicer.UpdateToLatestLedger,
       request_deserializer=get__with__proof__pb2.UpdateToLatestLedgerRequest.FromString,
       response_serializer=get__with__proof__pb2.UpdateToLatestLedgerResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('admission_control.AdmissionControl', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))