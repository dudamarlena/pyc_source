# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/interfaces.py
# Compiled at: 2007-05-25 16:54:18
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.http import IHTTPApplicationRequest, IHTTPCredentials
from zope.interface import Interface
from zope.component.interfaces import IView
from zope.interface import Attribute
from zope.app.publisher.xmlrpc import IMethodPublisher
from zope.publisher.interfaces.xmlrpc import IXMLRPCPublication
from zope.app.publication.interfaces import IRequestFactory
from zope.publisher.interfaces.browser import IDefaultBrowserLayer, IBrowserPage
from zope.schema.interfaces import TextLine

class IJSONRPCRequestFactory(IRequestFactory):
    """Browser request factory"""
    __module__ = __name__


class IJSONRPCPublisher(IPublishTraverse):
    """JSON-RPC Publisher
    like zope.publisher.interfaces.xmlrpc.IXMLRPCPublisher
    """
    __module__ = __name__


class IJSONRPCPublication(IXMLRPCPublication):
    """Object publication framework.
    like zope.publisher.interfaces.xmlrpc.IXMLRPCPublication
    """
    __module__ = __name__


class IJSONRPCRequest(IHTTPApplicationRequest, IHTTPCredentials, IDefaultBrowserLayer):
    """JSON-RPC Request
    like zope.publisher.interfaces.xmlrpc.IXMLRPCRequest
    """
    __module__ = __name__
    jsonID = Attribute('JSON-RPC ID for the request')


class IJSONReader(Interface):
    __module__ = __name__

    def read(aString):
        """read and interpret a string in JSON as python"""
        pass


class IJSONWriter(Interface):
    __module__ = __name__

    def write(anObject, encoding=None):
        """return a JSON unicode string representation of a python object
           Encode if encoding is provided.
        """
        pass


class IJSON(IJSONReader, IJSONWriter):
    """read and write JSON"""
    __module__ = __name__


class IJSONRPCView(IView):
    """JSONRPC View
    like zope.app.publisher.interfaces.xmlrpc.IXMLRPCView
    """
    __module__ = __name__


class IJSONRPCPremarshaller(Interface):
    """Premarshaller to remove security proxies"""
    __module__ = __name__

    def __call__():
        """return the object without proxies"""
        pass


class IJSONView(IBrowserPage):
    """A view that is a JSON representation of an object"""
    __module__ = __name__
    contentType = TextLine(title='content-type', default='application/json')

    def doResponse():
        """return the list or dict that is response for this view"""
        pass

    def doCacheControl():
        """set any cache headers that may be needed.  Default sends 'no-cache'
        to KHTML browsers.  May be extended/overridden in subclasses"""
        pass