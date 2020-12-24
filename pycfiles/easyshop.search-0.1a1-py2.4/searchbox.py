# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/search/viewlets/searchbox.py
# Compiled at: 2008-09-04 04:30:29
from plone.app.layout.viewlets.common import SearchBoxViewlet as Base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class SearchBoxViewlet(Base):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('searchbox.pt')

    def getShopUrl(self):
        """
        """
        utool = getToolByName(self.context, 'portal_url')
        portal = utool.getPortalObject().absolute_url()
        ptool = getToolByName(self.context, 'portal_properties')
        return portal + ptool.site_properties.easyshop_path