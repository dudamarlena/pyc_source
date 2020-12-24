# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/information/browser/information_container_view.py
# Compiled at: 2008-09-03 11:14:54
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IInformationManagement

class InformationContainerView(BrowserView):
    """
    """
    __module__ = __name__

    def getInformationPages(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        im = IInformationManagement(shop)
        result = []
        for information in im.getInformationPages():
            result.append({'id': information.getId(), 'title': information.Title(), 'url': information.absolute_url(), 'description': information.Description(), 'up_url': '%s/es_folder_position?position=up&id=%s' % (self.context.absolute_url(), information.getId()), 'down_url': '%s/es_folder_position?position=down&id=%s' % (self.context.absolute_url(), information.getId()), 'amount_of_criteria': len(information.objectIds())})

        return result