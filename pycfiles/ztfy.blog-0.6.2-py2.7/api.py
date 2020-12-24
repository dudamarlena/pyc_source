# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/tal/api.py
# Compiled at: 2013-09-22 13:17:34
__docformat__ = 'restructuredtext'
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.blog.interfaces.google import IGoogleAnalytics, IGoogleAdSense
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.blog.tal.interfaces import ISiteManagerTalesAPI, IGoogleTalesAPI
from ztfy.skin.interfaces import IPresentationTarget
from zope.component import queryMultiAdapter
from zope.interface import implements
from ztfy.utils.traversing import getParent

class SiteManagerTalesAPI(object):
    implements(ISiteManagerTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def manager(self):
        return getParent(self.context, ISiteManager)

    def presentation(self):
        manager = self.manager()
        if manager is not None:
            adapter = queryMultiAdapter((manager, self.request), IPresentationTarget)
            if adapter is not None:
                interface = adapter.target_interface
                return interface(manager)
        return


class GoogleTalesAPI(object):
    implements(IGoogleTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def analytics(self):
        return IGoogleAnalytics(self.context, None)

    def adsense(self):
        return IGoogleAdSense(self.context, None)