# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/Reporting.py
# Compiled at: 2011-01-11 16:22:56
import Globals
from AccessControl.Permissions import access_contents_information
from Products.CMFCore.utils import UniqueObject, getToolByName, registerToolInterface
from Products.CMFCore.permissions import View
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from zope.interface import implements
try:
    from Products.BastionBase.PortalFolder import PortalFolder
except:
    from Products.CMFPlone.PloneFolder import PloneFolder as PortalFolder

from config import ZENREPORTS_TOOL
from interfaces import IZenReportTool

class ReportsTool(UniqueObject, ActionProviderBase, PortalFolder):
    """
    The zport wrapped thingy

    This is essentially a place-holder until we fully skin Zenoss
    """
    __module__ = __name__
    implements(IZenReportTool)
    meta_type = portal_type = 'ZenReportsTool'
    id = ZENREPORTS_TOOL
    _actions = ()
    __ac_permissions__ = ActionProviderBase.__ac_permissions__ + ((View, ('availableReports', )),) + PortalFolder.__ac_permissions__
    manage_options = ActionProviderBase.manage_options + PortalFolder.manage_options

    def __init__(self, id=ZENREPORTS_TOOL):
        PortalFolder.__init__(self, id, 'Zenoss Reporting Tool')

    def availableReports(self):
        """
        returns a list of reports available for this particular user
        """
        results = []
        pat = getToolByName(self, 'portal_actions')
        for rpt in pat.listActionInfos(categories=('zenoss_reports', )) + self.listActionInfos():
            if rpt['visible'] and rpt['available'] and rpt['allowed']:
                results.append({'id': rpt['id'], 'url': rpt['url'], 'icon': rpt['icon'] or 'document_icon.gif', 'title': rpt['title'], 'description': rpt['description']})

        return results

    def passthruUrlBase(self):
        """
        returns the url which works to pass through the zentinel window
        """
        portal_url = getToolByName(self, 'portal_url').getPortalObject().absolute_url()
        return '%s/zentinel/show_window?url=' % portal_url


Globals.InitializeClass(ReportsTool)
registerToolInterface(ZENREPORTS_TOOL, IZenReportTool)