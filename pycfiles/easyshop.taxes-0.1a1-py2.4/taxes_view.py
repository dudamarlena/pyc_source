# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/taxes/browser/taxes_view.py
# Compiled at: 2008-09-03 11:15:45
from zope.component import queryUtility
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import ITaxManagement
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IShopManagement

class TaxesView(BrowserView):
    """
    """
    __module__ = __name__

    def getDefaultTaxes(self):
        """
        """
        tm = ITaxManagement(IShopManagement(self.context).getShop())
        nc = queryUtility(INumberConverter)
        result = []
        for tax in tm.getDefaultTaxes():
            result.append({'id': tax.getId(), 'title': tax.Title(), 'rate': nc.floatToTaxString(tax.getRate()), 'up_link': '%s/es_folder_position?position=up&id=%s' % (self.context.absolute_url(), tax.getId()), 'down_link': '%s/es_folder_position?position=down&id=%s' % (self.context.absolute_url(), tax.getId()), 'url': tax.absolute_url(), 'amount_of_criteria': self._getAmountOfCriteria(tax.getId())})

        return result

    def getCustomerTaxes(self):
        """
        """
        tm = ITaxManagement(IShopManagement(self.context).getShop())
        nc = queryUtility(INumberConverter)
        result = []
        for tax in tm.getCustomerTaxes():
            result.append({'id': tax.getId(), 'title': tax.Title(), 'rate': nc.floatToTaxString(tax.getRate()), 'up_link': '%s/es_folder_position?position=up&id=%s' % (self.context.absolute_url(), tax.getId()), 'down_link': '%s/es_folder_position?position=down&id=%s' % (self.context.absolute_url(), tax.getId()), 'url': tax.absolute_url(), 'amount_of_criteria': self._getAmountOfCriteria(tax.getId())})

        return result

    def _getAmountOfCriteria(self, id):
        """Returns amount of criteria for tax with given id.
        """
        try:
            tax = self.context[id]
        except KeyError:
            return 0

        return len(tax.objectIds())