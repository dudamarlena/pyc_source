# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/content.py
# Compiled at: 2014-03-15 19:50:01
__docformat__ = 'restructuredtext'
from hurry.query.interfaces import IQuery
from z3c.language.switch.interfaces import II18n
from zope.intid.interfaces import IIntIds
from ztfy.base.interfaces import IBaseContent
from ztfy.base.interfaces.container import IOrderedContainer
from ztfy.skin.interfaces import IDefaultView, IContainedDefaultView
from ztfy.skin.layer import IZTFYBrowserLayer, IZTFYBackLayer
from z3c.jsonrpc.publisher import MethodPublisher
from zope.component import adapts, getUtility
from zope.interface import implements, Interface
from zope.traversing.browser import absoluteURL
from ztfy.utils.catalog.index import Text

class BaseContentDefaultViewAdapter(object):
    """Default front-office URL adapter"""
    adapts(IBaseContent, IZTFYBrowserLayer, Interface)
    implements(IDefaultView)
    viewname = ''

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def getAbsoluteURL(self):
        return absoluteURL(self.context, self.request)


class BaseContentDefaultBackViewAdapter(object):
    """Default back-office URL adapter"""
    adapts(IBaseContent, IZTFYBackLayer, Interface)
    implements(IDefaultView)
    viewname = '@@properties.html'

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def getAbsoluteURL(self):
        return '%s/%s' % (absoluteURL(self.context, self.request), self.viewname)


class BaseContainedDefaultBackViewAdapter(object):
    """Default container back-office URL adapter"""
    adapts(IOrderedContainer, IZTFYBackLayer, Interface)
    implements(IContainedDefaultView)
    viewname = '@@contents.html'

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def getAbsoluteURL(self):
        return '%s/%s' % (absoluteURL(self.context, self.request), self.viewname)


class BaseContentSearchView(MethodPublisher):
    """Base content XML-RPC search view"""

    def searchByTitle(self, query):
        if not query:
            return []
        query_util = getUtility(IQuery)
        intids = getUtility(IIntIds)
        result = []
        for obj in query_util.searchResults(Text(('Catalog', 'title'), {'query': query + '*', 'ranking': True})):
            result.append({'value': str(intids.register(obj)), 'caption': II18n(obj).queryAttribute('title')})

        return result