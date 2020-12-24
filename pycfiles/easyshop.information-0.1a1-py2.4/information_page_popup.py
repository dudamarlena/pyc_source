# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/information/browser/information_page_popup.py
# Compiled at: 2008-09-03 11:14:54
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import IShopManagement

class InformationPagePopupView(BrowserView):
    """
    """
    __module__ = __name__

    def getInformation(self):
        """Returns information for information page which is given by request.
        """
        page_id = self.request.get('page_id')
        page = self.context.information.get(page_id)
        if page is None:
            return
        shop = IShopManagement(self.context).getShop()
        return {'shop_owner': shop.getShopOwner(), 'url': '%s/at_download/file' % page.absolute_url(), 'title': page.Title(), 'description': page.Description(), 'text': page.getText()}