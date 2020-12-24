# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/zmi/viewlets/header/crumbs.py
# Compiled at: 2012-06-20 12:11:31
__docformat__ = 'restructuredtext'
from z3c.language.switch.interfaces import II18n
from zope.dublincore.interfaces import IZopeDublinCore
from ztfy.skin.interfaces import IBreadcrumbInfo, IDefaultView
from zope.component import queryMultiAdapter
from zope.traversing.api import getParents, getName
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
                result.append({'title': info.title, 'path': info.path})
            else:
                name = getName(parent)
                if name:
                    name = '[ %s ]' % name
                else:
                    name = '[ root ]'
                i18n = II18n(parent, None)
                if i18n is not None:
                    name = i18n.queryAttribute('shortname', request=self.request) or i18n.queryAttribute('title', request=self.request) or name
                else:
                    dc = IZopeDublinCore(parent, None)
                    if dc is not None:
                        name = dc.title or name
                if name:
                    adapter = queryMultiAdapter((parent, self.request, self.__parent__), IDefaultView)
                    if adapter is not None and adapter.viewname:
                        self.viewname = '/' + adapter.viewname
                    result.append({'title': name, 'path': '%s%s' % (absoluteURL(parent, request=self.request),
                              self.viewname)})

        return result