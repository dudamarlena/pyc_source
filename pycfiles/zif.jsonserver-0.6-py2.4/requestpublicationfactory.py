# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/requestpublicationfactory.py
# Compiled at: 2007-05-25 16:54:18
from zope.app.publication.interfaces import IRequestPublicationFactory
from interfaces import IJSONRPCRequestFactory
from zope import component
from jsonrpc import JSONRPCRequest, JSONRPCPublication
from zope.interface import implements

class JSONRPCFactory(object):
    __module__ = __name__
    implements(IRequestPublicationFactory)

    def canHandle(self, environment):
        return True

    def __call__(self):
        request_class = component.queryUtility(IJSONRPCRequestFactory, default=JSONRPCRequest)
        return (
         request_class, JSONRPCPublication)