# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/information/browser/information_container_view_2.py
# Compiled at: 2008-08-06 16:25:29
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class InformationContainerView(BrowserView):
    """
    """
    __module__ = __name__

    def getInformationPages(self):
        """Returns all information pages.
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.checkPermission('Manage portal', self.context) == True:
            omit_edit_link = False
        else:
            omit_edit_link = True
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='InformationPage', sort_on='getObjPositionInParent')
        result = []
        for page in brains:
            result.append({'id': page.getId, 'title': page.Title, 'description': page.Description, 'omit_edit_link': omit_edit_link, 'url': page.getURL(), 'edit_url': '%s/edit' % page.getURL(), 'download_url': '%s/at_download/file' % page.getURL()})

        return result