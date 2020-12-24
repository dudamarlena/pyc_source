# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/browser/admin/export.py
# Compiled at: 2008-09-03 11:15:24
from zope.interface import Interface
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement

class IExportView(Interface):
    """
    """
    __module__ = __name__

    def getProducts():
        """
        """
        pass

    def getOrders():
        """
        """
        pass


class ExportView(BrowserView):
    """
    """
    __module__ = __name__
    implements(IExportView)

    def getProducts(self):
        """
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(portal_type='Product')
        result = []
        line = [
         'Title', 'Url', 'Price', 'Short Title', 'Article ID', 'Description', 'Weight', 'Text', 'Short Text', 'Image']
        line = [ '"%s"' % field for field in line ]
        line = ('\t').join(line)
        result.append(line)
        for brain in brains:
            product = brain.getObject()
            price = IPrices(product).getPriceGross()
            text = product.getText()
            text = text.replace('\n', '')
            text = text.replace('\r', '')
            text = text.replace('\t', '')
            short_text = product.getShortText()
            short_text = short_text.replace('\n', '')
            short_text = short_text.replace('\r', '')
            short_text = short_text.replace('\t', '')
            description = product.Description()
            description = description.replace('\n', '')
            description = description.replace('\r', '')
            description = description.replace('\t', '')
            line = [
             product.Title(), product.absolute_url(), price, product.getShortTitle(), product.getArticleId(), description, product.getWeight(), text, short_text]
            im = IImageManagement(product)
            for image in im.getImages():
                if image.absolute_url() == product.absolute_url():
                    url = image.absolute_url() + '/image'
                else:
                    url = image.absolute_url()
                line.append(url)

            line = [ '"%s"' % field for field in line ]
            line = ('\t').join(line)
            result.append(line)

        self.request.response.setHeader('Content-type', 'text/plain')
        self.request.response.setHeader('Content-disposition', 'attachment; filename=%s' % 'products.txt')
        return ('\r\n').join(result)

    def getOrders(self):
        """
        """
        om = IOrderManagement(IShopManagement(self.context).getShop())
        result = []
        for order in om.getOrders():
            wftool = getToolByName(self.context, 'portal_workflow')
            if wftool.getInfoFor(order, 'review_state') == 'closed':
                continue
            customer = order.getCustomer()
            im = IItemManagement(order)
            for item in im.getItems():
                product = item.getProduct()
                row = (
                 order.getId(), customer.getId(), product.getArticleId(), product.Title(), '%s' % item.getProductQuantity(), '%.2f' % item.getProductPriceGross(), '%.2f' % item.getProductPriceNet(), '%.2f' % item.getProductTax(), '%.2f' % item.getTax(), '%.2f' % item.getTaxRate(), '%.2f' % item.getPriceGross(), '%.2f' % item.getPriceNet())
                row = (';').join(row)
                result.append(row)

        self.request.response.setHeader('Content-type', 'text/plain')
        self.request.response.setHeader('Content-disposition', 'attachment; filename=%s' % 'orders.csv')
        return ('\n').join(result)