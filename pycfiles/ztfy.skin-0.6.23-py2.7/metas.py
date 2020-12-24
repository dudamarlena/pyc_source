# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/metas.py
# Compiled at: 2014-05-11 04:40:35
from ztfy.skin.interfaces import ICustomBackOfficeInfoTarget
from ztfy.skin.layer import IZTFYBackLayer
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser.absoluteurl import absoluteURL
from ztfy.baseskin.metas import *
from ztfy.utils.traversing import getParent

class BaseContentMetasHeadersBackAdapter(object):
    """Base content back-office metas adapter"""
    adapts(Interface, IZTFYBackLayer)
    implements(IContentMetasHeaders)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def metas(self):
        result = []
        back_target = getParent(self.context, ICustomBackOfficeInfoTarget)
        if back_target is not None:
            back_info = removeSecurityProxy(back_target.back_interface)(back_target)
            if getattr(back_info, 'custom_icon', None):
                result.append(LinkMeta('icon', back_info.custom_icon.contentType, absoluteURL(back_info.custom_icon, self.request)))
            else:
                result.append(LinkMeta('icon', 'image/png', '/@@/favicon.ico'))
        else:
            result.append(LinkMeta('icon', 'image/png', '/@@/favicon.ico'))
        return result