# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/customers.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface
from zope.interface import Attribute
from zope import schema
from easyshop.core.config import _

class IAddress(Interface):
    """A address of a customer.
    """
    __module__ = __name__
    firstname = schema.TextLine(title=_('Firstname'), description=_('Please enter your firstname.'), default='', required=True)
    lastname = schema.TextLine(title=_('Lastname'), description=_('Please enter your lastname.'), default='', required=True)
    company_name = schema.TextLine(title=_('Company Name'), description=_('Please enter your company name.'), default='', required=False)
    address_1 = schema.TextLine(title=_('Address 1'), description=_('Please enter your address.'), default='', required=True)
    zip_code = schema.TextLine(title=_('Zip Code'), description=_('Please enter your zip code.'), default='', required=True)
    city = schema.TextLine(title=_('City'), description=_('Please enter your city.'), default='', required=True)
    country = schema.Choice(title=_('Country'), description=_('Please enter your country.'), vocabulary='easyshop.countries')
    email = schema.TextLine(title=_('E-Mail'), description=_('Please enter your e-mail address.'), default='', required=True)
    phone = schema.TextLine(title=_('Phone'), description=_('Please enter your phone number.'), default='', required=False)


class IAddressManagement(Interface):
    """Provides methods to manage address content objects.
    """
    __module__ = __name__

    def addAddress(a1, a2, z, ci, co):
        """Adds an address.
            
           Parameters:    
               a1 = address 1
               a2 = address 2
               z  = zipcode
               ci = city
               co = country           
        """
        pass

    def deleteAddress(id):
        """Deletes an address by given id.
        """
        pass

    def getAddress(id):
        """Returns address by given id. If it isn't exist returns None.
        """
        pass

    def getAddresses():
        """Returns all addresses.
        """
        pass

    def getEmailAddress():
        """Returns the email address of an customer.
        Which is saved in the corresponding member.
        """
        pass

    def getInvoiceAddress():
        """Returns the invoice address.
        """
        pass

    def getShippingAddress():
        """Returns the shipping address.
        """
        pass

    def hasAddresses():
        """Returns True if context has at least one address.
        """
        pass

    def hasInvoiceAddress():
        """Returns True if a invoice address exists.
        """
        pass

    def hasShippingAddress():
        """Returns True if a shipping address exists.
        """
        pass


class ICustomersContainer(Interface):
    """A marker interface for customer folder content objects.
    """
    __module__ = __name__


class ISessionsContainer(Interface):
    """A container which holds addresses for anonymous customers.
    """
    __module__ = __name__


class ICustomer(Interface):
    """A customer can buy products from the shop.
    """
    __module__ = __name__
    firstname = schema.TextLine(title=_('Firstname'), description=_('Please enter your firstname.'), default='', required=True)
    lastname = schema.TextLine(title=_('Lastname'), description=_('Please enter your lastname.'), default='', required=True)
    email = schema.TextLine(title=_('E-Mail'), description=_('Please enter your e-mail.'), default='', required=True)
    selected_invoice_address = Attribute('The selected invoice address.')
    selected_shipping_address = Attribute('The selected shipping address.')
    selected_payment_method = Attribute('The selected payment method.')
    selected_shipping_method = Attribute('The selected shipping method.')
    selected_country = Attribute('Country which is used to calculate the shipping price, if\n                     the customer has not yet entered a invoice address')
    selected_payment_method = Attribute('The payment is processed with this method.')
    selected_payment_information = Attribute('Some payment methods need additional information (e.g. \n                     Credit Card)')


class ICustomerManagement(Interface):
    """Provides methods to manage customer content objects.
    """
    __module__ = __name__

    def addCustomer():
        """Adds a new customer. Either one for the authenticated member or one 
        for an anonymous user.
        """
        pass

    def getAuthenticatedCustomer():
        """Returns the current authenticated or session customer.
       """
        pass

    def getCustomerById(member_id):
        """Returns customer object for the given member id.
        """
        pass

    def getCustomers():
        """Returns all existing customers for authenticated members.
       """
        pass

    def transformCustomer(mid, sid):
        """Transforms a session customer with the given session id (sid) to a 
        personalized customer with the given member id (mid)
        """
        pass