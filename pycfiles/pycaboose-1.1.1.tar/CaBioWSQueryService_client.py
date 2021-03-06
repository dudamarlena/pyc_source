# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/cabig/cabio/CaBioWSQueryService_client.py
# Compiled at: 2010-06-24 16:12:02
from CaBioWSQueryService_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
from ZSI.schema import GED, GTD
import ZSI
from ZSI.generate.pyclass import pyclass_type

class CaBioWSQueryServiceLocator:
    caBIOService_address = 'http://cabioapi.nci.nih.gov/cabio43/services/caBIOService'

    def getcaBIOServiceAddress(self):
        return CaBioWSQueryServiceLocator.caBIOService_address

    def getcaBIOService(self, url=None, **kw):
        return caBIOServiceSoapBindingSOAP((url or CaBioWSQueryServiceLocator.caBIOService_address), **kw)


class caBIOServiceSoapBindingSOAP:

    def __init__(self, url, **kw):
        kw.setdefault('readerclass', None)
        kw.setdefault('writerclass', None)
        self.binding = client.Binding(url=url, **kw)
        return

    def search(self, request, **kw):
        if isinstance(request, searchRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(searchResponse.typecode)
        return response

    def getVersion(self, request, **kw):
        if isinstance(request, getVersionRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(getVersionResponse.typecode)
        return response

    def exist(self, request, **kw):
        if isinstance(request, existRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(existResponse.typecode)
        return response

    def getDataObject(self, request, **kw):
        if isinstance(request, getDataObjectRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(getDataObjectResponse.typecode)
        return response

    def query(self, request, **kw):
        if isinstance(request, queryRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(queryResponse.typecode)
        return response

    def getAssociation(self, request, **kw):
        if isinstance(request, getAssociationRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(getAssociationResponse.typecode)
        return response

    def getRecordsPerQuery(self, request, **kw):
        if isinstance(request, getRecordsPerQueryRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(getRecordsPerQueryResponse.typecode)
        return response

    def getMaximumRecordsPerQuery(self, request, **kw):
        if isinstance(request, getMaximumRecordsPerQueryRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(getMaximumRecordsPerQueryResponse.typecode)
        return response

    def getTotalNumberOfRecords(self, request, **kw):
        if isinstance(request, getTotalNumberOfRecordsRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(getTotalNumberOfRecordsResponse.typecode)
        return response

    def queryObject(self, request, **kw):
        if isinstance(request, queryObjectRequest) is False:
            raise TypeError, '%s incorrect request type' % request.__class__
        self.binding.Send(None, None, request, soapaction='', **kw)
        response = self.binding.Receive(queryObjectResponse.typecode)
        return response


_searchRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov', 'search'), ofwhat=[ns0.SearchQuery_Def(pname='in0', aname='_in0', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class searchRequest:
    typecode = _searchRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        in0 -- part in0
        """
        self._in0 = kw.get('in0')


searchRequest.typecode.pyclass = searchRequest
_searchResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov', 'searchResponse'), ofwhat=[ns1.ArrayOf_xsd_anyType_Def(pname='searchReturn', aname='_searchReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class searchResponse:
    typecode = _searchResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        searchReturn -- part searchReturn
        """
        self._searchReturn = kw.get('searchReturn')


searchResponse.typecode.pyclass = searchResponse
_getVersionRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                           'getVersion'), ofwhat=[], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getVersionRequest:
    typecode = _getVersionRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        """
        pass


getVersionRequest.typecode.pyclass = getVersionRequest
_getVersionResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                            'getVersionResponse'), ofwhat=[ZSI.TC.String(pname='getVersionReturn', aname='_getVersionReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getVersionResponse:
    typecode = _getVersionResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        getVersionReturn -- part getVersionReturn
        """
        self._getVersionReturn = kw.get('getVersionReturn')


getVersionResponse.typecode.pyclass = getVersionResponse
_existRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov', 'exist'), ofwhat=[ZSI.TC.String(pname='in0', aname='_in0', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class existRequest:
    typecode = _existRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        in0 -- part in0
        """
        self._in0 = kw.get('in0')


existRequest.typecode.pyclass = existRequest
_existResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov', 'existResponse'), ofwhat=[ZSI.TC.Boolean(pname='existReturn', aname='_existReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class existResponse:
    typecode = _existResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        existReturn -- part existReturn
        """
        self._existReturn = kw.get('existReturn')


existResponse.typecode.pyclass = existResponse
_getDataObjectRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                              'getDataObject'), ofwhat=[ZSI.TC.String(pname='in0', aname='_in0', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getDataObjectRequest:
    typecode = _getDataObjectRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        in0 -- part in0
        """
        self._in0 = kw.get('in0')


getDataObjectRequest.typecode.pyclass = getDataObjectRequest
_getDataObjectResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                               'getDataObjectResponse'), ofwhat=[ZSI.TC.AnyType(pname='getDataObjectReturn', aname='_getDataObjectReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getDataObjectResponse:
    typecode = _getDataObjectResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        getDataObjectReturn -- part getDataObjectReturn
        """
        self._getDataObjectReturn = kw.get('getDataObjectReturn')


getDataObjectResponse.typecode.pyclass = getDataObjectResponse
_queryRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov', 'query'), ofwhat=[ZSI.TC.String(pname='targetClassName', aname='_targetClassName', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), ZSI.TC.AnyType(pname='criteria', aname='_criteria', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), ZSI.TCnumbers.Iint(pname='startIndex', aname='_startIndex', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class queryRequest:
    typecode = _queryRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        targetClassName -- part targetClassName
        criteria -- part criteria
        startIndex -- part startIndex
        """
        self._targetClassName = kw.get('targetClassName')
        self._criteria = kw.get('criteria')
        self._startIndex = kw.get('startIndex')


queryRequest.typecode.pyclass = queryRequest
_queryResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov', 'queryResponse'), ofwhat=[ns1.ArrayOf_xsd_anyType_Def(pname='queryReturn', aname='_queryReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class queryResponse:
    typecode = _queryResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        queryReturn -- part queryReturn
        """
        self._queryReturn = kw.get('queryReturn')


queryResponse.typecode.pyclass = queryResponse
_getAssociationRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                               'getAssociation'), ofwhat=[ZSI.TC.AnyType(pname='source', aname='_source', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), ZSI.TC.String(pname='associationName', aname='_associationName', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), ZSI.TCnumbers.Iint(pname='startIndex', aname='_startIndex', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getAssociationRequest:
    typecode = _getAssociationRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        source -- part source
        associationName -- part associationName
        startIndex -- part startIndex
        """
        self._source = kw.get('source')
        self._associationName = kw.get('associationName')
        self._startIndex = kw.get('startIndex')


getAssociationRequest.typecode.pyclass = getAssociationRequest
_getAssociationResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                                'getAssociationResponse'), ofwhat=[ns1.ArrayOf_xsd_anyType_Def(pname='getAssociationReturn', aname='_getAssociationReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getAssociationResponse:
    typecode = _getAssociationResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        getAssociationReturn -- part getAssociationReturn
        """
        self._getAssociationReturn = kw.get('getAssociationReturn')


getAssociationResponse.typecode.pyclass = getAssociationResponse
_getRecordsPerQueryRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                                   'getRecordsPerQuery'), ofwhat=[], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getRecordsPerQueryRequest:
    typecode = _getRecordsPerQueryRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        """
        pass


getRecordsPerQueryRequest.typecode.pyclass = getRecordsPerQueryRequest
_getRecordsPerQueryResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                                    'getRecordsPerQueryResponse'), ofwhat=[ZSI.TCnumbers.Iint(pname='getRecordsPerQueryReturn', aname='_getRecordsPerQueryReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getRecordsPerQueryResponse:
    typecode = _getRecordsPerQueryResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        getRecordsPerQueryReturn -- part getRecordsPerQueryReturn
        """
        self._getRecordsPerQueryReturn = kw.get('getRecordsPerQueryReturn')


getRecordsPerQueryResponse.typecode.pyclass = getRecordsPerQueryResponse
_getMaximumRecordsPerQueryRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                                          'getMaximumRecordsPerQuery'), ofwhat=[], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getMaximumRecordsPerQueryRequest:
    typecode = _getMaximumRecordsPerQueryRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        """
        pass


getMaximumRecordsPerQueryRequest.typecode.pyclass = getMaximumRecordsPerQueryRequest
_getMaximumRecordsPerQueryResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                                           'getMaximumRecordsPerQueryResponse'), ofwhat=[ZSI.TCnumbers.Iint(pname='getMaximumRecordsPerQueryReturn', aname='_getMaximumRecordsPerQueryReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getMaximumRecordsPerQueryResponse:
    typecode = _getMaximumRecordsPerQueryResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        getMaximumRecordsPerQueryReturn -- part getMaximumRecordsPerQueryReturn
        """
        self._getMaximumRecordsPerQueryReturn = kw.get('getMaximumRecordsPerQueryReturn')


getMaximumRecordsPerQueryResponse.typecode.pyclass = getMaximumRecordsPerQueryResponse
_getTotalNumberOfRecordsRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                                        'getTotalNumberOfRecords'), ofwhat=[ZSI.TC.String(pname='targetClassName', aname='_targetClassName', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), ZSI.TC.AnyType(pname='criteria', aname='_criteria', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getTotalNumberOfRecordsRequest:
    typecode = _getTotalNumberOfRecordsRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        targetClassName -- part targetClassName
        criteria -- part criteria
        """
        self._targetClassName = kw.get('targetClassName')
        self._criteria = kw.get('criteria')


getTotalNumberOfRecordsRequest.typecode.pyclass = getTotalNumberOfRecordsRequest
_getTotalNumberOfRecordsResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                                         'getTotalNumberOfRecordsResponse'), ofwhat=[ZSI.TCnumbers.Iint(pname='getTotalNumberOfRecordsReturn', aname='_getTotalNumberOfRecordsReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class getTotalNumberOfRecordsResponse:
    typecode = _getTotalNumberOfRecordsResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        getTotalNumberOfRecordsReturn -- part getTotalNumberOfRecordsReturn
        """
        self._getTotalNumberOfRecordsReturn = kw.get('getTotalNumberOfRecordsReturn')


getTotalNumberOfRecordsResponse.typecode.pyclass = getTotalNumberOfRecordsResponse
_queryObjectRequestTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                            'queryObject'), ofwhat=[ZSI.TC.String(pname='targetClassName', aname='_targetClassName', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), ZSI.TC.AnyType(pname='criteria', aname='_criteria', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class queryObjectRequest:
    typecode = _queryObjectRequestTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        targetClassName -- part targetClassName
        criteria -- part criteria
        """
        self._targetClassName = kw.get('targetClassName')
        self._criteria = kw.get('criteria')


queryObjectRequest.typecode.pyclass = queryObjectRequest
_queryObjectResponseTypecode = Struct(pname=('http://webservice.system.nci.nih.gov',
                                             'queryObjectResponse'), ofwhat=[ns1.ArrayOf_xsd_anyType_Def(pname='queryObjectReturn', aname='_queryObjectReturn', typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded='http://webservice.system.nci.nih.gov')

class queryObjectResponse:
    typecode = _queryObjectResponseTypecode
    __metaclass__ = pyclass_type

    def __init__(self, **kw):
        """Keyword parameters:
        queryObjectReturn -- part queryObjectReturn
        """
        self._queryObjectReturn = kw.get('queryObjectReturn')


queryObjectResponse.typecode.pyclass = queryObjectResponse