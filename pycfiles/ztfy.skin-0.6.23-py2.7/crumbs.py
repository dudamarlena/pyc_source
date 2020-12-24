# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/viewlets/header/crumbs.py
# Compiled at: 2013-02-16 18:20:26
__docformat__ = 'restructuredtext'
from z3c.language.switch.interfaces import II18n
from zope.dublincore.interfaces import IZopeDublinCore
from ztfy.skin.interfaces import IDefaultView, IBreadcrumbInfo
from zope.component import queryMultiAdapter
from zope.traversing.api import getParents
from zope.traversing.browser import absoluteURL
from ztfy.skin.viewlet import ViewletBase

class BreadcrumbsViewlet(ViewletBase):
    viewname = ''

    @property
    def crumbs(self):
        result = []
        for parent in reversed([self.context] + getParents(self.context)):
            info = queryMultiAdapter((parent, self.request, self.__parent__), IBreadcrumbInfo)
            if info is not None:
                result.append({'title': info.title, 'path': info.path, 
                   'class': ''})
            else:
                i18n = II18n(parent, None)
                if i18n is not None:
                    name = i18n.queryAttribute('shortname', request=self.request) or i18n.queryAttribute('title', request=self.request)
                else:
                    dc = IZopeDublinCore(parent, None)
                    if dc is not None:
                        name = dc.title
                if name:
                    adapter = queryMultiAdapter((parent, self.request, self.__parent__), IDefaultView)
                    if adapter is not None and adapter.viewname:
                        self.viewname = '/' + adapter.viewname
                    result.append({'title': name, 'path': '%s%s' % (absoluteURL(parent, request=self.request),
                              self.viewname), 
                       'class': ''})

        if result:
            result[(-1)]['class'] = 'current'
        return result