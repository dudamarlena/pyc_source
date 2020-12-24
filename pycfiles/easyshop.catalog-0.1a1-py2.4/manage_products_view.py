# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/browser/manage_products_view.py
# Compiled at: 2008-09-03 11:14:28
import re
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IShopManagement

class ManageProductsView(BrowserView):
    """
    """
    __module__ = __name__

    def getLetters(self):
        """
        """
        return ('All', '0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z')

    def getProduct(self):
        """
        """
        uid = self.request.get('uid', '')
        if uid == '':
            return
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(UID=uid)
        try:
            brain = brains[0]
        except IndexError:
            return

        product = brain.getObject()
        related_products = []
        for related_product in product.getRelatedProducts():
            related_products.append({'title': related_product.Title(), 'article_id': related_product.getArticleId(), 'url': related_product.absolute_url()})

        categories = []
        for category in product.getCategories():
            categories.append({'title': category.Title(), 'url': category.absolute_url()})

        groups = []
        for group in product.getGroups():
            groups.append({'title': group.Title(), 'url': group.absolute_url()})

        cm = ICurrencyManagement(self.context)
        price = cm.priceToString(product.getPrice())
        return {'id': product.getId(), 'article_id': product.getArticleId(), 'description': product.Description(), 'title': product.Title(), 'short_title': product.getShortTitle() or product.Title(), 'url': product.absolute_url(), 'text': product.getText(), 'short_text': product.getShortText(), 'price': price, 'related_products': related_products, 'categories': categories, 'groups': groups}

    def getProducts(self):
        """Returns products as a list of brains.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        searchable_text = self.request.get('searchable_text', '')
        if searchable_text != '':
            result = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='Product', SearchableText=searchable_text, sort_on='sortable_title')
        else:
            letter = self.request.get('letter', None)
            if letter is None:
                return []
        result = []
        if letter == 'All':
            result = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='Product', sort_on='sortable_title')
        else:
            if letter == '0-9':
                brains = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='Product', sort_on='sortable_title')
                for brain in brains:
                    if re.match('\\d', brain.Title):
                        result.append(brain)

            brains = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='Product', Title='%s*' % letter, sort_on='sortable_title')
            for brain in brains:
                if brain.Title.upper().startswith(letter):
                    result.append(brain)

        lines = []
        line = []
        for (i, product) in enumerate(result):
            line.append(product)
            if (i + 1) % 3 == 0:
                lines.append(line)
                line = []

        if len(line) > 0:
            lines.append(line)
        return lines

    def getSearchableText(self):
        """
        """
        searchable_text = self.request.get('searchable_text', None)
        if searchable_text is None:
            return ''
        else:
            return searchable_text
        return

    def showNoProducts(self):
        """
        """
        if self.request.get('letter', None) is not None or self.request.get('searchable_text', None) is not None:
            return False
        shop = IShopManagement(self.context).getShop()
        products = IProductManagement(shop).getProducts()
        if len(products) > 0:
            return False
        else:
            return True
        return

    def showNoResult(self, lines):
        """
        """
        if len(lines) == 0 and (self.request.get('letter', None) is not None or self.request.get('searchable_text', None) is not None):
            return True
        return