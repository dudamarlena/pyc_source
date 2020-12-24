# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/tal/api.py
# Compiled at: 2013-09-22 13:15:24
__docformat__ = 'restructuredtext'
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.skin.interfaces import IPresentationTarget
from ztfy.skin.interfaces.metas import IPageMetasHeaders
from ztfy.skin.tal.interfaces import ISkinTalesAPI, IContentMetasAPI
from zope.component import queryMultiAdapter
from zope.interface import implements

class SkinTalesAPI(object):
    implements(ISkinTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def presentation(self):
        adapter = queryMultiAdapter((self.context, self.request), IPresentationTarget)
        if adapter is not None:
            interface = adapter.target_interface
            return interface(self.context)
        else:
            return


class ContentMetasTalesAPI(object):
    implements(IContentMetasAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def items(self):
        headers = queryMultiAdapter((self.context, self.request), IPageMetasHeaders)
        if headers is None:
            return []
        else:
            return headers.metas
            return

    def render(self):
        headers = queryMultiAdapter((self.context, self.request), IPageMetasHeaders)
        if headers is None:
            return ''
        else:
            return ('\n').join(meta.render() for meta in headers.metas)
            return