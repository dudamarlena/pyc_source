# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/viewlets/product_selector.py
# Compiled at: 2008-09-03 11:14:26
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from easyshop.core.interfaces import ICategoriesContainer
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement

class ProductSelectorViewlet(ViewletBase):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('product_selector.pt')

    def getFormatInfo(self):
        """
        """
        return IFormats(self.context).getFormats()

    def getImages(self):
        """
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(path={'query': ('/').join(self.context.getPhysicalPath()), 'depth': 1}, portal_type='ESImage', sort_on='getObjPositionInParent')
        return brains

    def getSelectors(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        catalog = getToolByName(self.context, 'portal_catalog')
        selectors = []
        brains = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='ProductSelector', sort_on='getObjPositionInParent')
        for selector in brains:
            if selector.getId == 'thank-you':
                continue
            selector = selector.getObject()
            fi = IFormats(selector).getFormats()
            products_per_line = fi.get('products_per_line')
            lines = []
            products = []
            for (index, product) in enumerate(selector.getRefs()):
                if mtool.checkPermission('View', product) is None:
                    continue
                cm = ICurrencyManagement(self.context)
                p = IPrices(product)
                price = p.getPriceForCustomer()
                price = cm.priceToString(price, symbol='symbol', position='before')
                standard_price = p.getPriceForCustomer(effective=False)
                standard_price = cm.priceToString(standard_price, symbol='symbol', position='before')
                image = IImageManagement(product).getMainImage()
                if image is not None:
                    image = '%s/image_%s' % (image.absolute_url(), fi.get('image_size'))
                temp = fi.get('text')
                if temp == 'description':
                    text = product.getDescription()
                elif temp == 'short_text':
                    text = product.getShortText()
                elif temp == 'text':
                    text = product.getText()
                else:
                    text = ''
                temp = fi.get('title')
                if temp == 'title':
                    title = product.Title()
                elif temp == 'short_title':
                    title = product.getShortTitle()
                try:
                    chars = int(fi.get('chars'))
                except (ValueError, TypeError):
                    chars = 0

                if chars != 0 and len(title) > chars:
                    title = title[:chars]
                    title += '...'
                if (index + 1) % products_per_line == 0:
                    klass = 'last'
                else:
                    klass = 'notlast'
                products.append({'title': title, 'url': product.absolute_url(), 'for_sale': product.getForSale(), 'price': price, 'standard_price': standard_price, 'image': image, 'text': text, 'class': klass})
                if (index + 1) % products_per_line == 0:
                    lines.append(products)
                    products = []

            lines.append(products)
            selectors.append({'edit_url': '%s/base_edit' % selector.absolute_url(), 'show_title': selector.getShowTitle(), 'title': selector.Title(), 'lines': lines, 'products_per_line': products_per_line, 'product_height': fi.get('product_height'), 'td_width': '%s%%' % (100 / products_per_line)})

        return selectors

    @memoize
    def getBackToOverViewUrl(self):
        """
        """
        parent = self.context.aq_inner.aq_parent
        if ICategory.providedBy(parent):
            parent_url = parent.absolute_url()
        elif ICategoriesContainer.providedBy(parent):
            shop = IShopManagement(self.context).getShop()
            parent_url = shop.absolute_url()
        else:
            parent_url = None
        return parent_url

    @memoize
    def showEditLink(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.checkPermission('Manage portal', self.context):
            return True
        return False