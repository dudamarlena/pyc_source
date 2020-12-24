# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/stocks/portlets/stock_information.py
# Compiled at: 2008-09-03 11:15:30
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from easyshop.core.config import _
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IStockManagement

class IStockInformationPortlet(IPortletDataProvider):
    """
    """
    __module__ = __name__


class Assignment(base.Assignment):
    """
    """
    __module__ = __name__
    implements(IStockInformationPortlet)

    def __init__(self):
        """
        """
        pass

    @property
    def title(self):
        """
        """
        return _('EasyShop: Stock Information')


class Renderer(base.Renderer):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('stock_information.pt')

    @property
    def stock_information(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        sm = IStockManagement(shop)
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants() == False:
            stock_information = sm.getStockInformationFor(self.context)
        else:
            product_variant = pvm.getSelectedVariant()
            stock_information = sm.getStockInformationFor(product_variant)
            if stock_information is None:
                stock_information = sm.getStockInformationFor(self.context)
        if stock_information is None:
            return
        return IData(stock_information).asDict()

    @property
    def available(self):
        """
        """
        return IProduct.providedBy(self.context)


class AddForm(base.NullAddForm):
    """
    """
    __module__ = __name__

    def create(self):
        """
        """
        return Assignment()