# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/defaultskin/social.py
# Compiled at: 2013-09-22 09:12:56
__docformat__ = 'restructuredtext'
from ztfy.blog.interfaces.google import IGoogleAnalytics
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.skin.interfaces import IPresentationTarget
from ztfy.skin.interfaces.metas import IContentMetasHeaders
from zope.component import adapts, queryMultiAdapter
from zope.interface import implements, Interface
from ztfy.skin.metas import ContentMeta, PropertyMeta
from ztfy.utils.traversing import getParent

class GoogleMetasSiteManagerAdapter(object):
    """Google site verification meta header adapter"""
    adapts(ISiteManager, Interface)
    implements(IContentMetasHeaders)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def metas(self):
        result = []
        google = IGoogleAnalytics(self.context, None)
        if google is not None:
            code = google.verification_code
            if code:
                result.append(ContentMeta('google-site-verification', code))
        return result


class FacebookMetasAdapter(object):
    """Facebook meta header adapter"""
    adapts(Interface, Interface)
    implements(IContentMetasHeaders)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def metas(self):
        result = []
        manager = getParent(self.context, ISiteManager)
        if manager is not None:
            adapter = queryMultiAdapter((manager, self.request), IPresentationTarget)
            if adapter is not None:
                interface = adapter.target_interface
                presentation = interface(manager)
                app_id = getattr(presentation, 'facebook_app_id', None)
                if app_id:
                    result.append(PropertyMeta('fb:app_id', app_id))
        return result