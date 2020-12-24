# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/adapters/taxes.py
# Compiled at: 2008-09-03 11:14:27
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import ITaxManagement
from easyshop.core.interfaces import IValidity

class ProductTaxes(object):
    """Provides ITaxes for product content objects.
    """
    __module__ = __name__
    implements(ITaxes)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context
        self.shop = IShopManagement(context).getShop()

    def getTaxRate(self):
        """
        """
        return self._calcTaxRateForProduct()

    def getTaxRateForCustomer(self):
        """
        """
        return self._calcTaxRateForCustomer()

    def getTax(self, effective=True):
        """
        """
        if effective == True:
            return self._getEffectiveTax()
        else:
            return self._getStandardTax()

    def getTaxForCustomer(self, effective=True):
        """
        """
        if effective == True:
            return self._getEffectiveTaxForCustomer()
        else:
            return self._getStandardTaxForCustomer()

    def _getStandardTax(self):
        """Returns the standard tax of the product. Without taking care whether 
        the product is for sale or not. We need this in any case (whether the 
        product is for sale or not) to display the default price (e.g. stroked).
        """
        tax_rate = self._calcTaxRateForProduct()
        price = self.context.getPrice()
        if self.shop.getGrossPrices() == True:
            tax_abs = tax_rate / (tax_rate + 100) * price
        else:
            tax_abs = price * (tax_rate / 100)
        return tax_abs

    def _getStandardTaxForCustomer(self):
        """Returns the standard tax of the product and customer. Without taking 
        care whether the product is for sale or not. We need this in any case 
        (whether the  product is for sale or not) to display the default price 
        (e.g. stroked).
        """
        tax_product = self.getTax(effective=False)
        tax_rate_customer = self._calcTaxRateForCustomer()
        if self.shop.getGrossPrices() == True:
            price_net = self.context.getPrice() - tax_product
        else:
            price_net = self.context.getPrice()
        return tax_rate_customer / 100 * price_net

    def _getEffectiveTax(self):
        """Returns the effective tax of the product. This means it takes care 
        whether the product is for sale for not.
        """
        tax_rate = self._calcTaxRateForProduct()
        if self.context.getForSale() == True:
            price = self.context.getSalePrice()
        else:
            price = self.context.getPrice()
        if self.shop.getGrossPrices() == True:
            tax_abs = tax_rate / (tax_rate + 100) * price
        else:
            tax_abs = price * (tax_rate / 100)
        return tax_abs

    def _getEffectiveTaxForCustomer(self):
        """Returns the effective tax of the product and customer. This means it
        takes care whether the product is for sale for not.
        """
        tax_product = self.getTax()
        tax_rate_customer = self._calcTaxRateForCustomer()
        if self.context.getForSale() == True:
            price_net = self.context.getSalePrice()
        else:
            price_net = self.context.getPrice()
        if self.shop.getGrossPrices() == True:
            price_net = price_net - tax_product
        return tax_rate_customer / 100 * price_net

    def _calcTaxRateForProduct(self):
        """Calculates the default tax for a given product.
        """
        tm = ITaxManagement(self.shop)
        for tax in tm.getDefaultTaxes():
            if IValidity(tax).isValid(self.context) == True:
                return tax.getRate()

        return 0

    def _calcTaxRateForCustomer(self):
        """Calculates the special tax for a given product and customer.
        """
        tm = ITaxManagement(self.shop)
        for tax in tm.getCustomerTaxes():
            if IValidity(tax).isValid(self.context) == True:
                return tax.getRate()

        return self._calcTaxRateForProduct()


class ProductVariantTaxes(ProductTaxes):
    """Provides ITaxes for product variant content objects.
    For taxes always the parent Product variants content object is used.
    """
    __module__ = __name__
    implements(ITaxes)
    adapts(IProductVariant)

    def __init__(self, context):
        """
        """
        self.context = context
        self.shop = IShopManagement(context).getShop()