# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/metas.py
# Compiled at: 2014-05-12 04:24:12
from z3c.language.switch.interfaces import II18n
from ztfy.baseskin.interfaces.metas import IContentMetasHeaders
from zope.component import adapts
from zope.interface import implements, Interface
from ztfy.baseskin.metas import HTTPEquivMeta, ContentMeta
from ztfy.i18n.interfaces.content import II18nBaseContent

class I18nBaseContentMetasHeadersAdapter(object):
    """Base content metas adapter"""
    adapts(II18nBaseContent, Interface)
    implements(IContentMetasHeaders)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def metas(self):
        result = []
        result.append(HTTPEquivMeta('Content-Type', 'text/html; charset=UTF-8'))
        i18n = II18n(self.context, None)
        if i18n is None:
            return result
        else:
            description = i18n.queryAttribute('description', request=self.request)
            if description:
                result.append(ContentMeta('description', description.replace('\n', ' ')))
            keywords = i18n.queryAttribute('keywords', request=self.request)
            if keywords:
                result.append(ContentMeta('keywords', keywords))
            return result