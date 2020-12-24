# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/zmi/skin.py
# Compiled at: 2012-06-20 12:11:31
__docformat__ = 'restructuredtext'
from ztfy.skin.interfaces import IDefaultView
from ztfy.zmi.layer import IZMILayer
from zope.app.publisher.browser.managementviewselector import ManagementViewSelector
from zope.browsermenu.menu import getFirstMenuItem
from zope.component import adapts
from zope.interface import implements, Interface
from zope.traversing.browser import absoluteURL

class DefaultViewAdapter(object):
    adapts(Interface, IZMILayer, Interface)
    implements(IDefaultView)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    @property
    def viewname(self):
        return '@@SelectedManagementView.html'

    def getAbsoluteURL(self):
        return '%s/%s' % (absoluteURL(self.context, self.request), self.viewname)


class ZMIManagementViewSelector(ManagementViewSelector):
    """Custom ZMI management view selector"""

    def __call__(self):
        redirect_url = absoluteURL(self.context, self.request)
        item = getFirstMenuItem('zmi_views', self.context, self.request)
        if item:
            action = item['action']
            if not (action.startswith('../') or action.lower().startswith('javascript:') or action.lower().startswith('++')):
                redirect_url = '%s/%s' % (redirect_url, action)
        self.request.response.redirect(redirect_url)
        return ''