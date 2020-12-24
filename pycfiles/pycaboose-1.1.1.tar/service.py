# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/cabig/cabio/service.py
# Compiled at: 2010-06-24 16:12:02
import cabig.cabio.CaBioWSQueryService_client as services
from cabig.cacore.ws.axis import AxisReader, ZSIDebugStreamReader
from cabig.cacore.ws.proxy import *
from cabig.cabio.pathways import *
from cabig.cabio.common.domain import *
from cabig.cabio.common.provenance.domain import *
from cabig.cabio.domain import *

class CaBioApplicationService:

    def __init__(self, url=None, debug=False):
        locator = services.CaBioWSQueryServiceLocator()
        tracefile = None
        if debug:
            tracefile = ZSIDebugStreamReader()
        self.wsq = locator.getcaBIOService(url=url, readerclass=AxisReader, tracefile=tracefile)
        return

    def wrap(self, holder):
        try:
            (pkg, className) = holder.typecode.type
        except AttributeError:
            return holder

        clazz = globals()[className]
        return clazz(holder, self)

    def search(self, in0):
        q = services.searchRequest()
        q._in0 = in0
        v = self.wsq.search(q)
        return [ self.wrap(i) for i in v.SearchReturn.Item ]

    def getRecordsPerQuery(self):
        q = services.getRecordsPerQueryRequest()
        v = self.wsq.getRecordsPerQuery(q)
        return v.GetRecordsPerQueryReturn

    def getAssociation(self, source, associationName, startIndex):
        q = services.getAssociationRequest()
        q._source = source.holder
        q._associationName = associationName
        q._startIndex = startIndex
        v = self.wsq.getAssociation(q)
        return [ self.wrap(i) for i in v.GetAssociationReturn.Item ]

    def getMaximumRecordsPerQuery(self):
        q = services.getMaximumRecordsPerQueryRequest()
        v = self.wsq.getMaximumRecordsPerQuery(q)
        return v.GetMaximumRecordsPerQueryReturn

    def exist(self, in0):
        q = services.existRequest()
        q._in0 = in0
        v = self.wsq.exist(q)
        return v.ExistReturn

    def query(self, targetClassName, criteria, startIndex):
        q = services.queryRequest()
        q._targetClassName = targetClassName
        q._criteria = criteria.holder
        q._startIndex = startIndex
        v = self.wsq.query(q)
        return [ self.wrap(i) for i in v.QueryReturn.Item ]

    def getVersion(self):
        q = services.getVersionRequest()
        v = self.wsq.getVersion(q)
        return v.GetVersionReturn

    def getDataObject(self, in0):
        q = services.getDataObjectRequest()
        q._in0 = in0
        v = self.wsq.getDataObject(q)
        return self.wrap(v.GetDataObjectReturn)

    def queryObject(self, targetClassName, criteria):
        q = services.queryObjectRequest()
        q._targetClassName = targetClassName
        q._criteria = criteria.holder
        v = self.wsq.queryObject(q)
        return [ self.wrap(i) for i in v.QueryObjectReturn.Item ]

    def getTotalNumberOfRecords(self, targetClassName, criteria):
        q = services.getTotalNumberOfRecordsRequest()
        q._targetClassName = targetClassName
        q._criteria = criteria.holder
        v = self.wsq.getTotalNumberOfRecords(q)
        return v.GetTotalNumberOfRecordsReturn