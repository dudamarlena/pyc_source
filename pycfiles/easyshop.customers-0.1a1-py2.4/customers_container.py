# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/browser/customers_container.py
# Compiled at: 2008-09-03 11:14:43
import re, urllib
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IBankAccount
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IShopManagement

class CustomersContainerView(BrowserView):
    """
    """
    __module__ = __name__

    def getAddresses(self):
        """
        """
        customer = self._getCustomer()
        if customer is None:
            return
        goto = self.context.absolute_url()
        goto += '?letter=%s' % self.request.get('letter')
        goto += '&uid=%s' % customer.UID()
        goto = urllib.quote(goto)
        am = IAddressManagement(customer)
        addresses = []
        for address in am.getAddresses():
            name = address.getFirstname() + ' ' + address.getLastname()
            address1 = address.getAddress1()
            if address.getAddress2():
                address1 += ' / '
                address1 += address.getAddress2()
            addresses.append({'name': name, 'address1': address_1, 'phone': address.phone(), 'url': address.absolute_url() + '/@@edit?goto=' + goto})

        return addresses

    def getBankInformation(self):
        """
        """
        customer = self._getCustomer()
        if customer is None:
            return []
        result = []
        pm = IPaymentMethodManagement(customer)
        for payment_method in pm.getPaymentMethods(IBankAccount):
            result.append({'url': payment_method.absolute_url(), 'account_number': payment_method.getAccountNumber(), 'bic': payment_method.getBankIdentificationCode(), 'name': payment_method.getName(), 'bank_name': payment_method.getBankName()})

        return result

    def getCart(self):
        """
        """
        customer = self._getCustomer()
        if customer is None:
            return
        cart = ICartManagement(self._getShop()).getCartById(customer.getId())
        if cart is None:
            return
        else:
            return {'url': cart.absolute_url()}
        return

    def getCustomer(self):
        """
        """
        customer = self._getCustomer()
        if customer is None:
            return
        goto = self.context.absolute_url()
        goto += '?letter=%s' % self.request.get('letter')
        goto += '&uid=%s' % customer.UID()
        goto = urllib.quote(goto)
        return {'name': customer.Title(), 'email': customer.getEmail(), 'url': customer.absolute_url(), 'uid': customer.UID(), 'id': customer.getId(), 'goto': goto}

    def getCustomers(self):
        """
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        letter = self.request.get('letter', '')
        result = []
        searchable_text = self.request.get('searchable_text', '')
        if searchable_text != '':
            result = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='Customer', SearchableText=searchable_text, sort_on='sortable_title')
        elif letter == '':
            return []
        elif letter == 'All':
            result = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='Customer', sort_on='sortable_title')
        elif letter == '0-9':
            brains = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='Customer', sort_on='sortable_title')
            for brain in brains:
                if re.match('\\d', brain.Title):
                    result.append(brain)

        else:
            result = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), portal_type='Customer', lastname='%s*' % letter, sort_on='sortable_lastname')
        temp = []
        for customer in result:
            temp.append({'name': customer.Title, 'uid': customer.UID, 'url': customer.getURL()})

        return temp

    def getLetters(self):
        """
        """
        return ('All', '0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z')

    def getOrders(self):
        """
        """
        ttool = getToolByName(self.context, 'translation_service')
        wftool = getToolByName(self.context, 'portal_workflow')
        customer = self._getCustomer()
        if customer is None:
            return []
        om = IOrderManagement(self._getShop())
        orders = []
        for order in om.getOrdersForCustomer(customer.getId()):
            fullname = 'There is no customer.'
            customer = order.getCustomer()
            if customer is not None:
                am = IAddressManagement(customer)
                address = am.getInvoiceAddress()
                if address is not None:
                    fullname = address.getName(reverse=True)
            created = ttool.ulocalized_time(order.created(), long_format=True)
            orders.append({'id': order.getId(), 'url': order.absolute_url(), 'created': created, 'customer_name': fullname, 'review_state': wftool.getInfoFor(order, 'review_state')})

        return orders

    @memoize
    def _getCustomer(self):
        """
        """
        uid = self.request.get('uid')
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(UID=uid)
        try:
            return brains[0].getObject()
        except:
            return

        return

    @memoize
    def _getShop(self):
        """
        """
        return IShopManagement(self.context).getShop()