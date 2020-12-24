# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: AppService_client.py
# Compiled at: 2018-06-29 21:47:06
from AppService_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
from ZSI.schema import GED, GTD
import ZSI

class AppServiceLocator:
    AppServicePort_address = 'http://ws.nbcr.net:8080/axis/services/AppServicePort'

    def getAppServicePortAddress(self):
        return AppServiceLocator.AppServicePort_address

    def getAppServicePort(self, url=None, **kw):
        return AppServicePortTypeSoapBindingSOAP((url or AppServiceLocator.AppServicePort_address), **kw)


class AppServicePortTypeSoapBindingSOAP:

    def __init__(self, url, **kw):
        kw.setdefault('readerclass', None)
        kw.setdefault('writerclass', None)
        self.binding = client.Binding(url=url, **kw)
        return

    def getAppMetadata(self, request, **kw):
        if isinstance(request, getAppMetadataRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='http://nbcr.sdsc.edu/opal/getAppMetadata', **kw)
        response = self.binding.Receive(getAppMetadataResponse.typecode)
        return response

    def getAppConfig(self, request, **kw):
        if isinstance(request, getAppConfigRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='http://nbcr.sdsc.edu/opal/getAppConfig', **kw)
        response = self.binding.Receive(getAppConfigResponse.typecode)
        return response

    def launchJob(self, request, **kw):
        if isinstance(request, launchJobRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='http://nbcr.sdsc.edu/opal/launchJob', **kw)
        response = self.binding.Receive(launchJobResponse.typecode)
        return response

    def launchJobBlocking(self, request, **kw):
        if isinstance(request, launchJobBlockingRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='http://nbcr.sdsc.edu/opal/launchJobBlocking', **kw)
        response = self.binding.Receive(launchJobBlockingResponse.typecode)
        return response

    def queryStatus(self, request, **kw):
        if isinstance(request, queryStatusRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='http://nbcr.sdsc.edu/opal/queryStatus', **kw)
        response = self.binding.Receive(queryStatusResponse.typecode)
        return response

    def getOutputs(self, request, **kw):
        if isinstance(request, getOutputsRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='http://nbcr.sdsc.edu/opal/getOutputs', **kw)
        response = self.binding.Receive(getOutputsResponse.typecode)
        return response

    def getOutputAsBase64ByName(self, request, **kw):
        if isinstance(request, getOutputAsBase64ByNameRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='http://nbcr.sdsc.edu/opal/getOutputAsBase64ByName', **kw)
        response = self.binding.Receive(getOutputAsBase64ByNameResponse.typecode)
        return getOutputAsBase64ByNameResponse(response)

    def destroy(self, request, **kw):
        if isinstance(request, destroyRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='http://nbcr.sdsc.edu/opal/destroy', **kw)
        response = self.binding.Receive(destroyResponse.typecode)
        return response


getAppMetadataRequest = GED('http://nbcr.sdsc.edu/opal/types', 'getAppMetadataInput').pyclass
getAppMetadataResponse = GED('http://nbcr.sdsc.edu/opal/types', 'getAppMetadataOutput').pyclass
getAppConfigRequest = GED('http://nbcr.sdsc.edu/opal/types', 'getAppConfigInput').pyclass
getAppConfigResponse = GED('http://nbcr.sdsc.edu/opal/types', 'getAppConfigOutput').pyclass
launchJobRequest = GED('http://nbcr.sdsc.edu/opal/types', 'launchJobInput').pyclass
launchJobResponse = GED('http://nbcr.sdsc.edu/opal/types', 'launchJobOutput').pyclass
launchJobBlockingRequest = GED('http://nbcr.sdsc.edu/opal/types', 'launchJobBlockingInput').pyclass
launchJobBlockingResponse = GED('http://nbcr.sdsc.edu/opal/types', 'launchJobBlockingOutput').pyclass
queryStatusRequest = GED('http://nbcr.sdsc.edu/opal/types', 'queryStatusInput').pyclass
queryStatusResponse = GED('http://nbcr.sdsc.edu/opal/types', 'queryStatusOutput').pyclass
getOutputsRequest = GED('http://nbcr.sdsc.edu/opal/types', 'getOutputsInput').pyclass
getOutputsResponse = GED('http://nbcr.sdsc.edu/opal/types', 'getOutputsOutput').pyclass
getOutputAsBase64ByNameRequest = GED('http://nbcr.sdsc.edu/opal/types', 'getOutputAsBase64ByNameInput').pyclass
getOutputAsBase64ByNameResponse = GED('http://nbcr.sdsc.edu/opal/types', 'getOutputAsBase64ByNameOutput').pyclass
destroyRequest = GED('http://nbcr.sdsc.edu/opal/types', 'destroyInput').pyclass
destroyResponse = GED('http://nbcr.sdsc.edu/opal/types', 'destroyOutput').pyclass