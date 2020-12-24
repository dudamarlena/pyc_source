# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/kss/catalog.py
# Compiled at: 2008-09-03 11:14:57
import cgi, re
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from Products.CMFPlone.utils import safe_unicode
from Products.CMFCore.utils import getToolByName
from snippets import *
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import ICurrencyManagement

class CatalogKSSView(PloneKSSView):
    """
    """
    __module__ = __name__

    @kssaction
    def showProducts(self, letter=None, form={}):
        """
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        kss_core = self.getCommandSet('core')
        searchable_text = form.get('searchable_text', '')
        products = []
        if searchable_text != '':
            products = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), object_provides='easyshop.core.interfaces.catalog.IProduct', SearchableText=searchable_text, sort_on='sortable_title')
            form = '\n                <form id="search-products-form"\n                      action="."\n                      method="post"\n                      style="display:inline">\n                    <input type="text"\n                           name="searchable_text"\n                           value="%s" />\n                    <input id="search-products"\n                           type="submit"\n                           value="OK" />\n                </form>' % searchable_text
            kss_core.replaceHTML('#search-products-form', safe_unicode(form))
        elif letter == 'All':
            products = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), object_provides='easyshop.core.interfaces.catalog.IProduct', sort_on='sortable_title')
        else:
            if letter == '0-9':
                brains = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), object_provides='easyshop.core.interfaces.catalog.IProduct', sort_on='sortable_title')
                for brain in brains:
                    if re.match('\\d', brain.Title):
                        products.append(brain)

            brains = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), object_provides='easyshop.core.interfaces.catalog.IProduct', Title='%s*' % letter, sort_on='sortable_title')
            for brain in brains:
                if brain.Title.upper().startswith(letter):
                    products.append(brain)

        html = '<table class="products-list"><tr>'
        for (i, product) in enumerate(products):
            html += '<td>'
            html += '<img class="product-details kssattr-uid-%s" alt="info" src="info_icon.gif" />' % product.UID
            html += '<div><a href="%s">%s</a></div>' % (product.getURL(), cgi.escape(product.Title))
            html += '</td><td class="image">'
            html += '<img src="%s/image_tile" /> ' % product.getURL()
            html += '</td>'
            if (i + 1) % 3 == 0:
                html += '</tr><tr>'

        if len(products) == 0:
            html += '<td>%s</td>' % cgi.escape(MESSAGES['NO_PRODUCTS_FOUND'])
        html += '</tr></table>'
        html = safe_unicode(html)
        kss_core.replaceInnerHTML('#products', html)
        kss_core.replaceInnerHTML('#product-details-box', '')

    @kssaction
    def showProductDetails(self, uid):
        """
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(UID=uid)
        try:
            product = brains[0].getObject()
        except IndexError:
            return

        cm = ICurrencyManagement(self.context)
        price = cm.priceToString(product.getPrice())
        info = {'title': product.Title(), 'short_title': product.getShortTitle(), 'short_text': product.getText(), 'url': product.absolute_url(), 'article_id': product.getArticleId(), 'price': price}
        pd = PRODUCT_DETAILS % info
        related_products = product.getRelatedProducts()
        if len(related_products) > 0:
            pd += RELATED_PRODUCTS_HEADER
            for related_product in related_products:
                pd += RELATED_PRODUCTS_BODY % {'title': cgi.escape(related_product.Title()), 'article_id': related_product.getArticleId(), 'url': related_product.absolute_url()}

            pd += RELATED_PRODUCTS_FOOTER
        categories = product.getCategories()
        if len(categories) > 0:
            pd += CATEGORIES_HEADER
            for category in categories:
                pd += CATEGORIES_BODY % {'title': cgi.escape(category.Title()), 'url': category.absolute_url()}

            pd += CATEGORIES_FOOTER
        groups = product.getGroups()
        if len(groups) > 0:
            pd += GROUPS_HEADER
            for group in groups:
                pd += GROUPS_BODY % {'title': cgi.escape(group.Title()), 'url': group.absolute_url()}

            pd += GROUPS_FOOTER
        kss_core = self.getCommandSet('core')
        pd = safe_unicode(pd)
        kss_core.replaceInnerHTML('#product-details-box', pd)