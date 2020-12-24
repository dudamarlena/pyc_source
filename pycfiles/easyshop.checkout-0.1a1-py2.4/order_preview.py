# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/checkout/browser/order_preview.py
# Compiled at: 2008-08-06 16:25:02
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser
from zope import schema
from zope.app.form.interfaces import WidgetInputError
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import Interface
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from easyshop.catalog.adapters.property_management import getTitlesByIds
from easyshop.core.config import _
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import IAsynchronPaymentMethod
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IDiscountsCalculation
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import IStockManagement
from easyshop.core.interfaces import ITaxes
from easyshop.payment.config import ERROR, PAYED

class IOrderPreviewForm(Interface):
    """
    """
    __module__ = __name__
    confirmation = schema.Bool()


class OrderPreviewForm(formbase.AddForm):
    """
    """
    __module__ = __name__
    template = pagetemplatefile.ZopeTwoPageTemplateFile('order_preview.pt')
    form_fields = form.Fields(IOrderPreviewForm)

    def validator(self, action, data):
        """
        """
        errors = []
        if self.request.get('form.confirmation', '') == '':
            error_msg = _('Please confirm our terms and conditions.')
            widget = self.widgets['confirmation']
            error = WidgetInputError(widget.name, widget.label, error_msg)
            widget._error = error
            widget.error = error_msg
            errors.append(error)
        return errors

    @form.action(_('label_buy', default='Buy'), validator=validator, name='buy')
    def handle_buy_action(self, action, data):
        """Buys a cart.
        """
        putils = getToolByName(self.context, 'plone_utils')
        om = IOrderManagement(self.context)
        new_order = om.addOrder()
        new_order.setMessage(self.context.request.get('form.message', ''))
        result = IPaymentProcessing(new_order).process()
        if result.code == ERROR:
            om.deleteOrder(new_order.id)
            putils.addPortalMessage(result.message, type='error')
            ICheckoutManagement(self.context).redirectToNextURL('ERROR_PAYMENT')
            return ''
        else:
            cm = ICartManagement(self.context)
            IStockManagement(self.context).removeCart(cm.getCart())
            cm.deleteCart()
            wftool = getToolByName(self.context, 'portal_workflow')
            wftool.doActionFor(new_order, 'submit')
            putils.addPortalMessage(MESSAGES['ORDER_RECEIVED'])
        if result.code == PAYED:
            wftool = getToolByName(self.context, 'portal_workflow')
            old_sm = getSecurityManager()
            tmp_user = UnrestrictedUser(old_sm.getUser().getId(), '', ['Manager'], '')
            portal = getToolByName(self.context, 'portal_url').getPortalObject()
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)
            wftool.doActionFor(new_order, 'pay_not_sent')
            setSecurityManager(old_sm)
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_payment_method = IPaymentInformationManagement(customer).getSelectedPaymentMethod()
        if not IAsynchronPaymentMethod.providedBy(selected_payment_method):
            ICheckoutManagement(self.context).redirectToNextURL('BUYED_ORDER')
        return

    def getCartItems(self):
        """Returns the items of the current cart.
        """
        cart = self._getCart()
        cm = ICurrencyManagement(self.context)
        im = IItemManagement(cart)
        result = []
        for cart_item in im.getItems():
            product = cart_item.getProduct()
            product_price = IPrices(cart_item).getPriceForCustomer() / cart_item.getAmount()
            product_price = cm.priceToString(product_price)
            price = IPrices(cart_item).getPriceForCustomer()
            properties = []
            pm = IPropertyManagement(product)
            for selected_property in cart_item.getProperties():
                property_price = pm.getPriceForCustomer(selected_property['id'], selected_property['selected_option'])
                titles = getTitlesByIds(product, selected_property['id'], selected_property['selected_option'])
                if titles is None:
                    continue
                if IProductVariant.providedBy(product) == True:
                    show_price = False
                else:
                    show_price = True
                properties.append({'id': selected_property['id'], 'selected_option': titles['option'], 'title': titles['property'], 'price': cm.priceToString(property_price), 'show_price': show_price})

            total_price = 0
            discount = IDiscountsCalculation(cart_item).getDiscount()
            if discount is not None:
                discount_price = getMultiAdapter((discount, cart_item)).getPriceForCustomer()
                discount = {'title': discount.Title(), 'value': cm.priceToString(discount_price, prefix='-')}
                total_price = price - discount_price
            data = IData(product).asDict()
            result.append({'product_title': data['title'], 'product_price': product_price, 'properties': properties, 'price': cm.priceToString(price), 'amount': cart_item.getAmount(), 'total_price': cm.priceToString(total_price), 'discount': discount})

        return result

    def getDiscounts(self):
        """
        """
        return []
        cart = self._getCart()
        if cart is None:
            return []
        cm = ICurrencyManagement(self.context)
        discounts = []
        for cart_item in IItemManagement(cart).getItems():
            discount = IDiscountsCalculation(cart_item).getDiscount()
            if discount is not None:
                value = getMultiAdapter((discount, cart_item)).getPriceForCustomer()
                discounts.append({'title': discount.Title(), 'value': cm.priceToString(value, prefix='-')})

        return discounts

    def getInvoiceAddress(self):
        """Returns invoice address of the current customer.
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        am = IAddressManagement(customer)
        address = am.getInvoiceAddress()
        return addressToDict(address)

    def getSelectedPaymentInformation(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        pm = IPaymentInformationManagement(customer)
        return pm.getSelectedPaymentInformation()

    def getPaymentMethodInfo(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_payment_method = customer.selected_payment_method
        pm = IPaymentMethodManagement(self.context)
        method = pm.getPaymentMethod(selected_payment_method)
        pp = IPaymentPriceManagement(self.context)
        payment_price = pp.getPriceGross()
        cm = ICurrencyManagement(self.context)
        price = cm.priceToString(payment_price)
        return {'type': method.portal_type, 'title': method.Title(), 'price': price, 'display': payment_price != 0}

    def getShippingAddress(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        am = IAddressManagement(customer)
        address = am.getShippingAddress()
        return addressToDict(address)

    def getShippingInfo(self):
        """
        """
        sm = IShippingPriceManagement(self.context)
        shipping_price = sm.getPriceForCustomer()
        cm = ICurrencyManagement(self.context)
        price = cm.priceToString(shipping_price)
        method = IShippingMethodManagement(self.context).getSelectedShippingMethod()
        return {'price': price, 'title': method.Title(), 'description': method.Description()}

    def getTotalPrice(self):
        """
        """
        cart = self._getCart()
        pm = IPrices(cart)
        total = pm.getPriceForCustomer()
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(total)

    def getTotalTax(self):
        """
        """
        cart = self._getCart()
        total = ITaxes(cart).getTaxForCustomer()
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(total)

    def hasCartItems(self):
        """
        """
        cart = self._getCart()
        if cart is None:
            return False
        im = IItemManagement(cart)
        if im.hasItems():
            return True
        return False

    def isCustomerComplete(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        return ICompleteness(customer).isComplete()

    def test(self, error, result_true, result_false):
        """
        """
        if error == True:
            return result_true
        else:
            return result_false

    @memoize
    def _getCart(self):
        """Returns current cart.
        """
        return ICartManagement(self.context).getCart()


def addressToDict(address):
    """
    """
    return {'name': address.getName(), 'address1': address.address_1, 'zipcode': address.zip_code, 'city': address.city, 'country': address.country, 'url': address.absolute_url(), 'is_complete': ICompleteness(address).isComplete()}