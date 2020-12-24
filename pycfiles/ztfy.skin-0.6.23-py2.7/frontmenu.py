# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/viewlets/actions/frontmenu.py
# Compiled at: 2013-09-22 07:09:12
__docformat__ = 'restructuredtext'
from ztfy.skin.interfaces import IDefaultView
from ztfy.skin.layer import IZTFYBrowserLayer
from z3c.template.template import getViewTemplate
from zope.component import queryMultiAdapter
from zope.traversing.browser.absoluteurl import absoluteURL
from ztfy.skin.menu import MenuItem
from ztfy.skin import _

class BackToFrontMenu(MenuItem):
    title = _('Back to front-office')
    template = getViewTemplate()
    cssClass = 'last front'

    @property
    def url(self):
        result = self.viewURL
        if not result:
            result = absoluteURL(self.context, self.request)
        elif not result.startswith('/'):
            result = '%s/%s' % (absoluteURL(self.context, self.request), result)
        return result.replace('/++skin++ZMI', '')

    @property
    def viewURL(self):
        adapter = queryMultiAdapter((self.context, IZTFYBrowserLayer, self.__parent__), IDefaultView)
        if adapter is not None:
            return adapter.viewname
        else:
            return ''