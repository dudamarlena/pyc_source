# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/communication/grpc/generated/logicmodule/logicmodule_pb2_grpc.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 134193 bytes
import grpc
import dataclay.communication.grpc.messages.common as dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2
import dataclay.communication.grpc.messages.logicmodule as dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2

class LogicModuleStub(object):
    __doc__ = 'Interface exported by the server.\n  '

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.autoregisterSL = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/autoregisterSL',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AutoRegisterSLRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.autoregisterEE = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/autoregisterEE',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AutoRegisterEERequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AutoRegisterEEResponse.FromString))
        self.unregisterStorageLocation = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/unregisterStorageLocation',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnregisterStorageLocationRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.unregisterExecutionEnvironment = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/unregisterExecutionEnvironment',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnregisterExecutionEnvironmentRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.checkAlive = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/checkAlive',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.performSetOfNewAccounts = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/performSetOfNewAccounts',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PerformSetAccountsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PerformSetAccountsResponse.FromString))
        self.performSetOfOperations = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/performSetOfOperations',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PerformSetOperationsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PerformSetOperationsResponse.FromString))
        self.publishAddress = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/publishAddress',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PublishAddressRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.newAccountNoAdmin = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newAccountNoAdmin',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewAccountNoAdminRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewAccountResponse.FromString))
        self.newAccount = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newAccount',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewAccountRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewAccountResponse.FromString))
        self.getAccountID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getAccountID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountIDResponse.FromString))
        self.getAccountList = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getAccountList',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountListRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountListResponse.FromString))
        self.newSession = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newSession',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewSessionRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewSessionResponse.FromString))
        self.getInfoOfSessionForDS = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getInfoOfSessionForDS',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInfoOfSessionForDSRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInfoOfSessionForDSResponse.FromString))
        self.newNamespace = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newNamespace',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewNamespaceRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewNamespaceResponse.FromString))
        self.removeNamespace = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/removeNamespace',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveNamespaceRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getNamespaceID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getNamespaceID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespaceIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespaceIDResponse.FromString))
        self.getNamespaceLang = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getNamespaceLang',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespaceLangRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespaceLangResponse.FromString))
        self.getObjectDataSetID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getObjectDataSetID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectDataSetIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectDataSetIDResponse.FromString))
        self.importInterface = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/importInterface',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ImportInterfaceRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.importContract = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/importContract',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ImportContractRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getInfoOfClassesInNamespace = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getInfoOfClassesInNamespace',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInfoOfClassesInNamespaceRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInfoOfClassesInNamespaceResponse.FromString))
        self.getImportedClassesInfoInNamespace = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getImportedClassesInfoInNamespace',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetImportedClassesInfoInNamespaceRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetImportedClassesInfoInNamespaceResponse.FromString))
        self.getClassIDfromImport = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getClassIDfromImport',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassIDFromImportRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassIDFromImportResponse.FromString))
        self.getNamespaces = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getNamespaces',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespacesRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespacesResponse.FromString))
        self.newDataSet = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newDataSet',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewDataSetRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewDataSetResponse.FromString))
        self.removeDataSet = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/removeDataSet',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveDataSetRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getDataSetID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getDataSetID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataSetIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataSetIDResponse.FromString))
        self.checkDataSetIsPublic = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/checkDataSetIsPublic',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CheckDataSetIsPublicRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CheckDataSetIsPublicResponse.FromString))
        self.getPublicDataSets = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getPublicDataSets',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetPublicDataSetsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetPublicDataSetsResponse.FromString))
        self.getAccountDataSets = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getAccountDataSets',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountDataSetsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountDataSetsResponse.FromString))
        self.newClass = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newClass',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewClassRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewClassResponse.FromString))
        self.newClassID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newClassID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewClassIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewClassIDResponse.FromString))
        self.removeClass = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/removeClass',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveClassRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.removeOperation = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/removeOperation',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveOperationRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.removeImplementation = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/removeImplementation',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveImplementationRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getOperationID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getOperationID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetOperationIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetOperationIDResponse.FromString))
        self.getPropertyID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getPropertyID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetPropertyIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetPropertyIDResponse.FromString))
        self.getClassID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getClassID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassIDResponse.FromString))
        self.getClassInfo = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getClassInfo',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassInfoRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassInfoResponse.FromString))
        self.newContract = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newContract',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewContractRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewContractResponse.FromString))
        self.registerToPublicContract = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/registerToPublicContract',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterToPublicContractRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.registerToPublicContractOfNamespace = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/registerToPublicContractOfNamespace',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterToPublicContractOfNamespaceRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterToPublicContractOfNamespaceResponse.FromString))
        self.getContractIDsOfApplicant = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getContractIDsOfApplicant',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDsOfApplicantRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDsOfApplicantResponse.FromString))
        self.getContractIDsOfProvider = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getContractIDsOfProvider',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDsOfProviderRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDsOfProviderResponse.FromString))
        self.getContractIDsOfApplicantWithProvider = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getContractIDsOfApplicantWithProvider',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractsOfApplicantWithProvRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractsOfApplicantWithProvResponse.FromString))
        self.newDataContract = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newDataContract',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewDataContractRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewDataContractResponse.FromString))
        self.registerToPublicDataContract = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/registerToPublicDataContract',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterToPublicDataContractRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getDataContractIDsOfApplicant = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getDataContractIDsOfApplicant',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractIDsOfApplicantRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractIDsOfApplicantResponse.FromString))
        self.getDataContractIDsOfProvider = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getDataContractIDsOfProvider',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractIDsOfProviderRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractIDsOfProviderResponse.FromString))
        self.getDataContractInfoOfApplicantWithProvider = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getDataContractInfoOfApplicantWithProvider',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractInfoOfApplicantWithProvRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractInfoOfApplicantWithProvResponse.FromString))
        self.newInterface = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newInterface',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewInterfaceRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewInterfaceResponse.FromString))
        self.getInterfaceInfo = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getInterfaceInfo',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInterfaceInfoRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInterfaceInfoResponse.FromString))
        self.removeInterface = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/removeInterface',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveInterfaceRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getExecutionEnvironmentsInfo = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getExecutionEnvironmentsInfo',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentsInfoRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentsInfoResponse.FromString))
        self.getExecutionEnvironmentsNames = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getExecutionEnvironmentsNames',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentsNamesRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentsNamesResponse.FromString))
        self.getExecutionEnvironmentForDS = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getExecutionEnvironmentForDS',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentForDSRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentForDSResponse.FromString))
        self.getStorageLocationForDS = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getStorageLocationForDS',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetStorageLocationForDSRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetStorageLocationForDSResponse.FromString))
        self.getObjectInfo = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getObjectInfo',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectInfoRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectInfoResponse.FromString))
        self.getObjectFromAlias = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getObjectFromAlias',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectFromAliasRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectFromAliasResponse.FromString))
        self.deleteAlias = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/deleteAlias',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.DeleteAliasRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getObjectsMetaDataInfoOfClassForNM = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getObjectsMetaDataInfoOfClassForNM',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectsMetaDataInfoOfClassForNMRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectsMetaDataInfoOfClassForNMResponse.FromString))
        self.addAlias = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/addAlias',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AddAliasRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.registerObjectFromGC = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/registerObjectFromGC',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterObjectForGCRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.unregisterObjects = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/unregisterObjects',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnregisterObjectsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.registerObject = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/registerObject',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterObjectRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.setDataSetIDFromGarbageCollector = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/setDataSetIDFromGarbageCollector',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SetDataSetIDFromGarbageCollectorRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.setDataSetID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/setDataSetID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SetDataSetIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.newVersion = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newVersion',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewVersionRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewVersionResponse.FromString))
        self.consolidateVersion = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/consolidateVersion',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ConsolidateVersionRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.newReplica = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/newReplica',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewReplicaRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewReplicaResponse.FromString))
        self.moveObject = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/moveObject',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.MoveObjectRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.MoveObjectResponse.FromString))
        self.setObjectReadOnly = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/setObjectReadOnly',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SetObjectReadOnlyRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.setObjectReadWrite = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/setObjectReadWrite',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SetObjectReadWriteRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getMetadataByOID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getMetadataByOID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetMetadataByOIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetMetadataByOIDResponse.FromString))
        self.executeImplementation = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/executeImplementation',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ExecuteImplementationRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ExecuteImplementationResponse.FromString))
        self.executeMethodOnTarget = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/executeMethodOnTarget',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ExecuteMethodOnTargetRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ExecuteMethodOnTargetResponse.FromString))
        self.synchronizeFederatedObject = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/synchronizeFederatedObject',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SynchronizeFederatedObjectRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getDataClayID = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getDataClayID',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataClayIDResponse.FromString))
        self.registerExternalDataClay = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/registerExternalDataClay',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterExternalDataClayRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterExternalDataClayResponse.FromString))
        self.notifyRegistrationOfExternalDataClay = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/notifyRegistrationOfExternalDataClay',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NotifyRegistrationOfExternalDataClayRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NotifyRegistrationOfExternalDataClayResponse.FromString))
        self.getExternalDataClayInfo = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getExternalDataClayInfo',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExtDataClayInfoRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExtDataClayInfoResponse.FromString))
        self.getExternalDataclayId = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getExternalDataclayId',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExternalDataclayIDRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExternalDataclayIDResponse.FromString))
        self.federateObject = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/federateObject',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.FederateObjectRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.unfederateObject = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/unfederateObject',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnfederateObjectRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.notifyUnfederatedObjects = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/notifyUnfederatedObjects',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NotifyUnfederatedObjectsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.notifyFederatedObjects = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/notifyFederatedObjects',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NotifyFederatedObjectsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.checkObjectIsFederatedWithDataClayInstance = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/checkObjectIsFederatedWithDataClayInstance',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CheckObjectFederatedWithDataClayInstanceRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CheckObjectFederatedWithDataClayInstanceResponse.FromString))
        self.getDataClaysObjectIsFederatedWith = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getDataClaysObjectIsFederatedWith',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataClaysObjectIsFederatedWithRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataClaysObjectIsFederatedWithResponse.FromString))
        self.getExternalSourceDataClayOfObject = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getExternalSourceDataClayOfObject',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExternalSourceDataClayOfObjectRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExternalSourceDataClayOfObjectResponse.FromString))
        self.unfederateAllObjects = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/unfederateAllObjects',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnfederateAllObjectsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.unfederateAllObjectsWithAllDCs = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/unfederateAllObjectsWithAllDCs',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnfederateAllObjectsWithAllDCsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.unfederateObjectWithAllDCs = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/unfederateObjectWithAllDCs',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnfederateObjectWithAllDCsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.migrateFederatedObjects = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/migrateFederatedObjects',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.MigrateFederatedObjectsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.federateAllObjects = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/federateAllObjects',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.FederateAllObjectsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getStubs = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getStubs',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetStubsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetStubsResponse.FromString))
        self.getBabelStubs = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getBabelStubs',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetBabelStubsRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetBabelStubsResponse.FromString))
        self.registerECA = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/registerECA',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterECARequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.adviseEvent = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/adviseEvent',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AdviseEventRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.isPrefetchingEnabled = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/isPrefetchingEnabled',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.IsPrefetchingEnabledResponse.FromString))
        self.getClassNameForDS = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getClassNameForDS',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassNameForDSRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassNameForDSResponse.FromString))
        self.getClassNameAndNamespaceForDS = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getClassNameAndNamespaceForDS',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassNameAndNamespaceForDSRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassNameAndNamespaceForDSResponse.FromString))
        self.getContractIDOfDataClayProvider = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getContractIDOfDataClayProvider',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDOfDataClayProviderRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDOfDataClayProviderResponse.FromString))
        self.objectExistsInDataClay = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/objectExistsInDataClay',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ObjectExistsInDataClayRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ObjectExistsInDataClayResponse.FromString))
        self.closeSession = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/closeSession',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CloseSessionRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getMetadataByOIDForDS = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getMetadataByOIDForDS',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetMetadataByOIDForDSRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetMetadataByOIDForDSResponse.FromString))
        self.activateTracing = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/activateTracing',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ActivateTracingRequest.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.deactivateTracing = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/deactivateTracing',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.getTraces = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/getTraces',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.GetTracesResponse.FromString))
        self.cleanMetaDataCaches = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/cleanMetaDataCaches',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.closeManagerDb = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/closeManagerDb',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))
        self.closeDb = channel.unary_unary('/dataclay.communication.grpc.logicmodule.LogicModule/closeDb',
          request_serializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.SerializeToString),
          response_deserializer=(dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.FromString))


class LogicModuleServicer(object):
    __doc__ = 'Interface exported by the server.\n  '

    def autoregisterSL(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def autoregisterEE(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unregisterStorageLocation(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unregisterExecutionEnvironment(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkAlive(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def performSetOfNewAccounts(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def performSetOfOperations(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def publishAddress(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newAccountNoAdmin(self, request, context):
        """Account Manager
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newAccount(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAccountID(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAccountList(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newSession(self, request, context):
        """Session Manager
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getInfoOfSessionForDS(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newNamespace(self, request, context):
        """Namespace Manager
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeNamespace(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getNamespaceID(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getNamespaceLang(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getObjectDataSetID(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def importInterface(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def importContract(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getInfoOfClassesInNamespace(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getImportedClassesInfoInNamespace(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getClassIDfromImport(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getNamespaces(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newDataSet(self, request, context):
        """DataSet Manager
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeDataSet(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getDataSetID(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkDataSetIsPublic(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getPublicDataSets(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAccountDataSets(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newClass(self, request, context):
        """Class Manager
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newClassID(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeClass(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeOperation(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeImplementation(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getOperationID(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getPropertyID(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getClassID(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getClassInfo(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newContract(self, request, context):
        """Contract Manager
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerToPublicContract(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerToPublicContractOfNamespace(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getContractIDsOfApplicant(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getContractIDsOfProvider(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getContractIDsOfApplicantWithProvider(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newDataContract(self, request, context):
        """DataContract Manager
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerToPublicDataContract(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getDataContractIDsOfApplicant(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getDataContractIDsOfProvider(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getDataContractInfoOfApplicantWithProvider(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newInterface(self, request, context):
        """Interface Manager
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getInterfaceInfo(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeInterface(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getExecutionEnvironmentsInfo(self, request, context):
        """EE-SL information
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getExecutionEnvironmentsNames(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getExecutionEnvironmentForDS(self, request, context):
        """TODO: modify next functions also called from Python to more scalable information
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getStorageLocationForDS(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getObjectInfo(self, request, context):
        """Object Metadata
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getObjectFromAlias(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteAlias(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getObjectsMetaDataInfoOfClassForNM(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addAlias(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerObjectFromGC(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unregisterObjects(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerObject(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setDataSetIDFromGarbageCollector(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setDataSetID(self, request, context):
        """Storage Location
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newVersion(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def consolidateVersion(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newReplica(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def moveObject(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setObjectReadOnly(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setObjectReadWrite(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMetadataByOID(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def executeImplementation(self, request, context):
        """Execution Environment
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def executeMethodOnTarget(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def synchronizeFederatedObject(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getDataClayID(self, request, context):
        """Federation 
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerExternalDataClay(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def notifyRegistrationOfExternalDataClay(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getExternalDataClayInfo(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getExternalDataclayId(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def federateObject(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unfederateObject(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def notifyUnfederatedObjects(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def notifyFederatedObjects(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkObjectIsFederatedWithDataClayInstance(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getDataClaysObjectIsFederatedWith(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getExternalSourceDataClayOfObject(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unfederateAllObjects(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unfederateAllObjectsWithAllDCs(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unfederateObjectWithAllDCs(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def migrateFederatedObjects(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def federateAllObjects(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getStubs(self, request, context):
        """Stubs
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getBabelStubs(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerECA(self, request, context):
        """Notification Manager
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def adviseEvent(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def isPrefetchingEnabled(self, request, context):
        """Prefetching 
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getClassNameForDS(self, request, context):
        """Others
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getClassNameAndNamespaceForDS(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getContractIDOfDataClayProvider(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def objectExistsInDataClay(self, request, context):
        """Testing
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def closeSession(self, request, context):
        """Others
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMetadataByOIDForDS(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def activateTracing(self, request, context):
        """Paraver
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deactivateTracing(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getTraces(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def cleanMetaDataCaches(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def closeManagerDb(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def closeDb(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LogicModuleServicer_to_server(servicer, server):
    rpc_method_handlers = {'autoregisterSL':grpc.unary_unary_rpc_method_handler(servicer.autoregisterSL,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AutoRegisterSLRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'autoregisterEE':grpc.unary_unary_rpc_method_handler(servicer.autoregisterEE,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AutoRegisterEERequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AutoRegisterEEResponse.SerializeToString), 
     'unregisterStorageLocation':grpc.unary_unary_rpc_method_handler(servicer.unregisterStorageLocation,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnregisterStorageLocationRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'unregisterExecutionEnvironment':grpc.unary_unary_rpc_method_handler(servicer.unregisterExecutionEnvironment,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnregisterExecutionEnvironmentRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'checkAlive':grpc.unary_unary_rpc_method_handler(servicer.checkAlive,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'performSetOfNewAccounts':grpc.unary_unary_rpc_method_handler(servicer.performSetOfNewAccounts,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PerformSetAccountsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PerformSetAccountsResponse.SerializeToString), 
     'performSetOfOperations':grpc.unary_unary_rpc_method_handler(servicer.performSetOfOperations,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PerformSetOperationsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PerformSetOperationsResponse.SerializeToString), 
     'publishAddress':grpc.unary_unary_rpc_method_handler(servicer.publishAddress,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.PublishAddressRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'newAccountNoAdmin':grpc.unary_unary_rpc_method_handler(servicer.newAccountNoAdmin,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewAccountNoAdminRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewAccountResponse.SerializeToString), 
     'newAccount':grpc.unary_unary_rpc_method_handler(servicer.newAccount,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewAccountRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewAccountResponse.SerializeToString), 
     'getAccountID':grpc.unary_unary_rpc_method_handler(servicer.getAccountID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountIDResponse.SerializeToString), 
     'getAccountList':grpc.unary_unary_rpc_method_handler(servicer.getAccountList,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountListRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountListResponse.SerializeToString), 
     'newSession':grpc.unary_unary_rpc_method_handler(servicer.newSession,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewSessionRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewSessionResponse.SerializeToString), 
     'getInfoOfSessionForDS':grpc.unary_unary_rpc_method_handler(servicer.getInfoOfSessionForDS,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInfoOfSessionForDSRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInfoOfSessionForDSResponse.SerializeToString), 
     'newNamespace':grpc.unary_unary_rpc_method_handler(servicer.newNamespace,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewNamespaceRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewNamespaceResponse.SerializeToString), 
     'removeNamespace':grpc.unary_unary_rpc_method_handler(servicer.removeNamespace,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveNamespaceRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getNamespaceID':grpc.unary_unary_rpc_method_handler(servicer.getNamespaceID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespaceIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespaceIDResponse.SerializeToString), 
     'getNamespaceLang':grpc.unary_unary_rpc_method_handler(servicer.getNamespaceLang,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespaceLangRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespaceLangResponse.SerializeToString), 
     'getObjectDataSetID':grpc.unary_unary_rpc_method_handler(servicer.getObjectDataSetID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectDataSetIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectDataSetIDResponse.SerializeToString), 
     'importInterface':grpc.unary_unary_rpc_method_handler(servicer.importInterface,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ImportInterfaceRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'importContract':grpc.unary_unary_rpc_method_handler(servicer.importContract,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ImportContractRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getInfoOfClassesInNamespace':grpc.unary_unary_rpc_method_handler(servicer.getInfoOfClassesInNamespace,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInfoOfClassesInNamespaceRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInfoOfClassesInNamespaceResponse.SerializeToString), 
     'getImportedClassesInfoInNamespace':grpc.unary_unary_rpc_method_handler(servicer.getImportedClassesInfoInNamespace,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetImportedClassesInfoInNamespaceRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetImportedClassesInfoInNamespaceResponse.SerializeToString), 
     'getClassIDfromImport':grpc.unary_unary_rpc_method_handler(servicer.getClassIDfromImport,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassIDFromImportRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassIDFromImportResponse.SerializeToString), 
     'getNamespaces':grpc.unary_unary_rpc_method_handler(servicer.getNamespaces,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespacesRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetNamespacesResponse.SerializeToString), 
     'newDataSet':grpc.unary_unary_rpc_method_handler(servicer.newDataSet,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewDataSetRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewDataSetResponse.SerializeToString), 
     'removeDataSet':grpc.unary_unary_rpc_method_handler(servicer.removeDataSet,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveDataSetRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getDataSetID':grpc.unary_unary_rpc_method_handler(servicer.getDataSetID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataSetIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataSetIDResponse.SerializeToString), 
     'checkDataSetIsPublic':grpc.unary_unary_rpc_method_handler(servicer.checkDataSetIsPublic,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CheckDataSetIsPublicRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CheckDataSetIsPublicResponse.SerializeToString), 
     'getPublicDataSets':grpc.unary_unary_rpc_method_handler(servicer.getPublicDataSets,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetPublicDataSetsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetPublicDataSetsResponse.SerializeToString), 
     'getAccountDataSets':grpc.unary_unary_rpc_method_handler(servicer.getAccountDataSets,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountDataSetsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetAccountDataSetsResponse.SerializeToString), 
     'newClass':grpc.unary_unary_rpc_method_handler(servicer.newClass,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewClassRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewClassResponse.SerializeToString), 
     'newClassID':grpc.unary_unary_rpc_method_handler(servicer.newClassID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewClassIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewClassIDResponse.SerializeToString), 
     'removeClass':grpc.unary_unary_rpc_method_handler(servicer.removeClass,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveClassRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'removeOperation':grpc.unary_unary_rpc_method_handler(servicer.removeOperation,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveOperationRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'removeImplementation':grpc.unary_unary_rpc_method_handler(servicer.removeImplementation,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveImplementationRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getOperationID':grpc.unary_unary_rpc_method_handler(servicer.getOperationID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetOperationIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetOperationIDResponse.SerializeToString), 
     'getPropertyID':grpc.unary_unary_rpc_method_handler(servicer.getPropertyID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetPropertyIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetPropertyIDResponse.SerializeToString), 
     'getClassID':grpc.unary_unary_rpc_method_handler(servicer.getClassID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassIDResponse.SerializeToString), 
     'getClassInfo':grpc.unary_unary_rpc_method_handler(servicer.getClassInfo,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassInfoRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassInfoResponse.SerializeToString), 
     'newContract':grpc.unary_unary_rpc_method_handler(servicer.newContract,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewContractRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewContractResponse.SerializeToString), 
     'registerToPublicContract':grpc.unary_unary_rpc_method_handler(servicer.registerToPublicContract,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterToPublicContractRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'registerToPublicContractOfNamespace':grpc.unary_unary_rpc_method_handler(servicer.registerToPublicContractOfNamespace,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterToPublicContractOfNamespaceRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterToPublicContractOfNamespaceResponse.SerializeToString), 
     'getContractIDsOfApplicant':grpc.unary_unary_rpc_method_handler(servicer.getContractIDsOfApplicant,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDsOfApplicantRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDsOfApplicantResponse.SerializeToString), 
     'getContractIDsOfProvider':grpc.unary_unary_rpc_method_handler(servicer.getContractIDsOfProvider,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDsOfProviderRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDsOfProviderResponse.SerializeToString), 
     'getContractIDsOfApplicantWithProvider':grpc.unary_unary_rpc_method_handler(servicer.getContractIDsOfApplicantWithProvider,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractsOfApplicantWithProvRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractsOfApplicantWithProvResponse.SerializeToString), 
     'newDataContract':grpc.unary_unary_rpc_method_handler(servicer.newDataContract,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewDataContractRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewDataContractResponse.SerializeToString), 
     'registerToPublicDataContract':grpc.unary_unary_rpc_method_handler(servicer.registerToPublicDataContract,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterToPublicDataContractRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getDataContractIDsOfApplicant':grpc.unary_unary_rpc_method_handler(servicer.getDataContractIDsOfApplicant,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractIDsOfApplicantRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractIDsOfApplicantResponse.SerializeToString), 
     'getDataContractIDsOfProvider':grpc.unary_unary_rpc_method_handler(servicer.getDataContractIDsOfProvider,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractIDsOfProviderRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractIDsOfProviderResponse.SerializeToString), 
     'getDataContractInfoOfApplicantWithProvider':grpc.unary_unary_rpc_method_handler(servicer.getDataContractInfoOfApplicantWithProvider,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractInfoOfApplicantWithProvRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataContractInfoOfApplicantWithProvResponse.SerializeToString), 
     'newInterface':grpc.unary_unary_rpc_method_handler(servicer.newInterface,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewInterfaceRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewInterfaceResponse.SerializeToString), 
     'getInterfaceInfo':grpc.unary_unary_rpc_method_handler(servicer.getInterfaceInfo,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInterfaceInfoRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetInterfaceInfoResponse.SerializeToString), 
     'removeInterface':grpc.unary_unary_rpc_method_handler(servicer.removeInterface,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RemoveInterfaceRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getExecutionEnvironmentsInfo':grpc.unary_unary_rpc_method_handler(servicer.getExecutionEnvironmentsInfo,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentsInfoRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentsInfoResponse.SerializeToString), 
     'getExecutionEnvironmentsNames':grpc.unary_unary_rpc_method_handler(servicer.getExecutionEnvironmentsNames,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentsNamesRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentsNamesResponse.SerializeToString), 
     'getExecutionEnvironmentForDS':grpc.unary_unary_rpc_method_handler(servicer.getExecutionEnvironmentForDS,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentForDSRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExecutionEnvironmentForDSResponse.SerializeToString), 
     'getStorageLocationForDS':grpc.unary_unary_rpc_method_handler(servicer.getStorageLocationForDS,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetStorageLocationForDSRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetStorageLocationForDSResponse.SerializeToString), 
     'getObjectInfo':grpc.unary_unary_rpc_method_handler(servicer.getObjectInfo,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectInfoRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectInfoResponse.SerializeToString), 
     'getObjectFromAlias':grpc.unary_unary_rpc_method_handler(servicer.getObjectFromAlias,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectFromAliasRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectFromAliasResponse.SerializeToString), 
     'deleteAlias':grpc.unary_unary_rpc_method_handler(servicer.deleteAlias,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.DeleteAliasRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getObjectsMetaDataInfoOfClassForNM':grpc.unary_unary_rpc_method_handler(servicer.getObjectsMetaDataInfoOfClassForNM,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectsMetaDataInfoOfClassForNMRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetObjectsMetaDataInfoOfClassForNMResponse.SerializeToString), 
     'addAlias':grpc.unary_unary_rpc_method_handler(servicer.addAlias,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AddAliasRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'registerObjectFromGC':grpc.unary_unary_rpc_method_handler(servicer.registerObjectFromGC,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterObjectForGCRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'unregisterObjects':grpc.unary_unary_rpc_method_handler(servicer.unregisterObjects,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnregisterObjectsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'registerObject':grpc.unary_unary_rpc_method_handler(servicer.registerObject,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterObjectRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'setDataSetIDFromGarbageCollector':grpc.unary_unary_rpc_method_handler(servicer.setDataSetIDFromGarbageCollector,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SetDataSetIDFromGarbageCollectorRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'setDataSetID':grpc.unary_unary_rpc_method_handler(servicer.setDataSetID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SetDataSetIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'newVersion':grpc.unary_unary_rpc_method_handler(servicer.newVersion,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewVersionRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewVersionResponse.SerializeToString), 
     'consolidateVersion':grpc.unary_unary_rpc_method_handler(servicer.consolidateVersion,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ConsolidateVersionRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'newReplica':grpc.unary_unary_rpc_method_handler(servicer.newReplica,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewReplicaRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NewReplicaResponse.SerializeToString), 
     'moveObject':grpc.unary_unary_rpc_method_handler(servicer.moveObject,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.MoveObjectRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.MoveObjectResponse.SerializeToString), 
     'setObjectReadOnly':grpc.unary_unary_rpc_method_handler(servicer.setObjectReadOnly,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SetObjectReadOnlyRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'setObjectReadWrite':grpc.unary_unary_rpc_method_handler(servicer.setObjectReadWrite,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SetObjectReadWriteRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getMetadataByOID':grpc.unary_unary_rpc_method_handler(servicer.getMetadataByOID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetMetadataByOIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetMetadataByOIDResponse.SerializeToString), 
     'executeImplementation':grpc.unary_unary_rpc_method_handler(servicer.executeImplementation,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ExecuteImplementationRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ExecuteImplementationResponse.SerializeToString), 
     'executeMethodOnTarget':grpc.unary_unary_rpc_method_handler(servicer.executeMethodOnTarget,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ExecuteMethodOnTargetRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ExecuteMethodOnTargetResponse.SerializeToString), 
     'synchronizeFederatedObject':grpc.unary_unary_rpc_method_handler(servicer.synchronizeFederatedObject,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.SynchronizeFederatedObjectRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getDataClayID':grpc.unary_unary_rpc_method_handler(servicer.getDataClayID,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataClayIDResponse.SerializeToString), 
     'registerExternalDataClay':grpc.unary_unary_rpc_method_handler(servicer.registerExternalDataClay,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterExternalDataClayRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterExternalDataClayResponse.SerializeToString), 
     'notifyRegistrationOfExternalDataClay':grpc.unary_unary_rpc_method_handler(servicer.notifyRegistrationOfExternalDataClay,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NotifyRegistrationOfExternalDataClayRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NotifyRegistrationOfExternalDataClayResponse.SerializeToString), 
     'getExternalDataClayInfo':grpc.unary_unary_rpc_method_handler(servicer.getExternalDataClayInfo,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExtDataClayInfoRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExtDataClayInfoResponse.SerializeToString), 
     'getExternalDataclayId':grpc.unary_unary_rpc_method_handler(servicer.getExternalDataclayId,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExternalDataclayIDRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExternalDataclayIDResponse.SerializeToString), 
     'federateObject':grpc.unary_unary_rpc_method_handler(servicer.federateObject,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.FederateObjectRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'unfederateObject':grpc.unary_unary_rpc_method_handler(servicer.unfederateObject,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnfederateObjectRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'notifyUnfederatedObjects':grpc.unary_unary_rpc_method_handler(servicer.notifyUnfederatedObjects,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NotifyUnfederatedObjectsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'notifyFederatedObjects':grpc.unary_unary_rpc_method_handler(servicer.notifyFederatedObjects,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.NotifyFederatedObjectsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'checkObjectIsFederatedWithDataClayInstance':grpc.unary_unary_rpc_method_handler(servicer.checkObjectIsFederatedWithDataClayInstance,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CheckObjectFederatedWithDataClayInstanceRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CheckObjectFederatedWithDataClayInstanceResponse.SerializeToString), 
     'getDataClaysObjectIsFederatedWith':grpc.unary_unary_rpc_method_handler(servicer.getDataClaysObjectIsFederatedWith,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataClaysObjectIsFederatedWithRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetDataClaysObjectIsFederatedWithResponse.SerializeToString), 
     'getExternalSourceDataClayOfObject':grpc.unary_unary_rpc_method_handler(servicer.getExternalSourceDataClayOfObject,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExternalSourceDataClayOfObjectRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetExternalSourceDataClayOfObjectResponse.SerializeToString), 
     'unfederateAllObjects':grpc.unary_unary_rpc_method_handler(servicer.unfederateAllObjects,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnfederateAllObjectsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'unfederateAllObjectsWithAllDCs':grpc.unary_unary_rpc_method_handler(servicer.unfederateAllObjectsWithAllDCs,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnfederateAllObjectsWithAllDCsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'unfederateObjectWithAllDCs':grpc.unary_unary_rpc_method_handler(servicer.unfederateObjectWithAllDCs,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.UnfederateObjectWithAllDCsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'migrateFederatedObjects':grpc.unary_unary_rpc_method_handler(servicer.migrateFederatedObjects,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.MigrateFederatedObjectsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'federateAllObjects':grpc.unary_unary_rpc_method_handler(servicer.federateAllObjects,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.FederateAllObjectsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getStubs':grpc.unary_unary_rpc_method_handler(servicer.getStubs,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetStubsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetStubsResponse.SerializeToString), 
     'getBabelStubs':grpc.unary_unary_rpc_method_handler(servicer.getBabelStubs,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetBabelStubsRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetBabelStubsResponse.SerializeToString), 
     'registerECA':grpc.unary_unary_rpc_method_handler(servicer.registerECA,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.RegisterECARequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'adviseEvent':grpc.unary_unary_rpc_method_handler(servicer.adviseEvent,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.AdviseEventRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'isPrefetchingEnabled':grpc.unary_unary_rpc_method_handler(servicer.isPrefetchingEnabled,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.IsPrefetchingEnabledResponse.SerializeToString), 
     'getClassNameForDS':grpc.unary_unary_rpc_method_handler(servicer.getClassNameForDS,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassNameForDSRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassNameForDSResponse.SerializeToString), 
     'getClassNameAndNamespaceForDS':grpc.unary_unary_rpc_method_handler(servicer.getClassNameAndNamespaceForDS,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassNameAndNamespaceForDSRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetClassNameAndNamespaceForDSResponse.SerializeToString), 
     'getContractIDOfDataClayProvider':grpc.unary_unary_rpc_method_handler(servicer.getContractIDOfDataClayProvider,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDOfDataClayProviderRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetContractIDOfDataClayProviderResponse.SerializeToString), 
     'objectExistsInDataClay':grpc.unary_unary_rpc_method_handler(servicer.objectExistsInDataClay,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ObjectExistsInDataClayRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ObjectExistsInDataClayResponse.SerializeToString), 
     'closeSession':grpc.unary_unary_rpc_method_handler(servicer.closeSession,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.CloseSessionRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getMetadataByOIDForDS':grpc.unary_unary_rpc_method_handler(servicer.getMetadataByOIDForDS,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetMetadataByOIDForDSRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.GetMetadataByOIDForDSResponse.SerializeToString), 
     'activateTracing':grpc.unary_unary_rpc_method_handler(servicer.activateTracing,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_logicmodule_dot_logicmodule__messages__pb2.ActivateTracingRequest.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'deactivateTracing':grpc.unary_unary_rpc_method_handler(servicer.deactivateTracing,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'getTraces':grpc.unary_unary_rpc_method_handler(servicer.getTraces,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.GetTracesResponse.SerializeToString), 
     'cleanMetaDataCaches':grpc.unary_unary_rpc_method_handler(servicer.cleanMetaDataCaches,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'closeManagerDb':grpc.unary_unary_rpc_method_handler(servicer.closeManagerDb,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString), 
     'closeDb':grpc.unary_unary_rpc_method_handler(servicer.closeDb,
       request_deserializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.EmptyMessage.FromString,
       response_serializer=dataclay_dot_communication_dot_grpc_dot_messages_dot_common_dot_common__messages__pb2.ExceptionInfo.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('dataclay.communication.grpc.logicmodule.LogicModule', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))