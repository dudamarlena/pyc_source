# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/defaultskin/viewlets/header/crumbs.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from z3c.language.switch.interfaces import II18n
from zope.dublincore.interfaces import IZopeDublinCore
from hurry.workflow.interfaces import IWorkflowState
from ztfy.blog.interfaces import STATUS_DELETED
from ztfy.skin.interfaces import IBreadcrumbInfo, IDefaultView
from zope.component import queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.traversing.api import getParents
from ztfy.skin.viewlet import ViewletBase

class BreadcrumbsViewlet(ViewletBase):
    viewname = ''

    @property
    def crumbs(self):
        result = []
        state = IWorkflowState(self.context, None)
        if state is None or state.getState() != STATUS_DELETED:
            for parent in reversed([self.context] + getParents(self.context)):
                value = None
                info = queryMultiAdapter((parent, self.request, self.__parent__), IBreadcrumbInfo)
                if info is not None:
                    if info.visible:
                        value = {'title': info.title, 'path': info.path}
                else:
                    visible = getattr(parent, 'visible', True)
                    if visible:
                        i18n = II18n(parent, None)
                        if i18n is not None:
                            name = i18n.queryAttribute('shortname', request=self.request) or i18n.queryAttribute('title', request=self.request)
                        else:
                            name = IZopeDublinCore(parent).title
                        if name:
                            adapter = queryMultiAdapter((parent, self.request, self.__parent__), IDefaultView)
                            if adapter is not None and adapter.viewname:
                                self.viewname = '/' + adapter.viewname
                            value = {'title': name, 'path': '%s%s' % (absoluteURL(parent, request=self.request),
                                      self.viewname)}
                if value:
                    if result and value['title'] == result[(-1)]['title']:
                        result[-1] = value
                    else:
                        result.append(value)

        return result