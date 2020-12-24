# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mvob/InfoBlad/browser/infoblad_view.py
# Compiled at: 2010-12-15 05:37:45
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

class InfoBladView(BrowserView):
    """ View class for InfoBlad type """

    def getInnerMedia(self):
        """Catalog search for media inside the infoblad"""
        catalog = getToolByName(self, 'portal_catalog')
        folder_url = ('/').join(self.context.getPhysicalPath())
        results = catalog.searchResults(path={'query': folder_url, 'depth': 1}, sort_on='getObjPositionInParent', sort_order='descending', portal_type='Image')
        return results