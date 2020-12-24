# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/portlets/related_products.py
# Compiled at: 2008-09-03 11:14:29
from zope import schema
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProduct

class IRelatedProductsPortlet(IPortletDataProvider):
    __module__ = __name__
    count = schema.Int(title=_('Number of products to display'), description=_('How many products to list. 0 for all.'), required=True, default=5)


class Assignment(base.Assignment):
    """
    """
    __module__ = __name__
    implements(IRelatedProductsPortlet)

    def __init__(self, count=5):
        """
        """
        self.count = count

    @property
    def title(self):
        """
        """
        return _('EasyShop: Related Products')


class Renderer(base.Renderer):
    __module__ = __name__
    render = ViewPageTemplateFile('related_products.pt')

    @property
    def available(self):
        """
        """
        if IProduct.providedBy(self.context) and len(self._data()) > 0:
            return True
        else:
            return False

    def related_products(self):
        """
        """
        return self._data()

    @memoize
    def _data(self):
        """
        """
        limit = self.data.count
        if limit != 0:
            products = self.context.getRefs('products_products')[:limit]
        else:
            products = self.context.getRefs('products_products')
        result = []
        for product in products:
            mtool = getToolByName(self.context, 'portal_membership')
            if mtool.checkPermission('View', product) == True:
                image = IImageManagement(product).getMainImage()
                image_url = image.absolute_url() + '/image_thumb'
                price = IPrices(product).getPriceGross()
                cm = ICurrencyManagement(product)
                price = cm.priceToString(price)
                result.append({'title': product.Title(), 'url': product.absolute_url(), 'image_url': image_url, 'price': price})

        return result


class AddForm(base.AddForm):
    """
    """
    __module__ = __name__
    form_fields = form.Fields(IRelatedProductsPortlet)
    label = _('Add Related Products Portlet')
    description = _('This portlet displays related products.')

    def create(self, data):
        return Assignment(count=data.get('count', 5))


class EditForm(base.EditForm):
    """
    """
    __module__ = __name__
    form_fields = form.Fields(IRelatedProductsPortlet)
    label = _('Edit Related Products Portlet')
    description = _('This portlet displays related products.')