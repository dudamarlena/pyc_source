# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/payment.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface
from zope.interface import Attribute
from zope import schema
from easyshop.core.config import _
from easyshop.core.config import CREDIT_CARDS_CHOICES
from easyshop.core.config import CREDIT_CARD_MONTHS_CHOICES
from easyshop.core.config import CREDIT_CARD_YEARS_CHOICES

class IPaymentMethod(Interface):
    """Marker interface for payment methods.
    """
    __module__ = __name__


class ISelectablePaymentMethod(Interface):
    """Marker interface for payment methods which can be selected by a customer.
    """
    __module__ = __name__


class IAsynchronPaymentMethod(Interface):
    """Marker interface for payment methods which redirect to the payment 
    service, e.g. PayPal.
    """
    __module__ = __name__


class ICreditCardPaymentMethod(IPaymentMethod):
    """Marker interface payment via credit card.
    """
    __module__ = __name__


class IDirectDebitPaymentMethod(IPaymentMethod):
    """Marker interface for payment via direct debit.
    """
    __module__ = __name__


class IPayPalPaymentMethod(IPaymentMethod, ISelectablePaymentMethod, IAsynchronPaymentMethod):
    """Marker interface for payment via PayPal.
    """
    __module__ = __name__


class IGenericPaymentMethod(IPaymentMethod, ISelectablePaymentMethod):
    """A generic payment method.
    """
    __module__ = __name__
    payed = Attribute('If checked an order gets the "payed"-state after \n        processing this payment method, otherwhise "not payed" ')


class IPaymentInformation(Interface):
    """Marker interface for payment information.
    """
    __module__ = __name__


class IBankAccount(IPaymentInformation):
    """Stores information of a bank account.
    """
    __module__ = __name__
    account_number = schema.TextLine(title=_('Account Number'), description=_('Please enter your account number'), default='', required=True)
    bank_identification_code = schema.TextLine(title=_('Bank Information Code'), description=_('Please enter your bank information code'), default='', required=True)
    depositor = schema.TextLine(title=_('Depositor'), description=_('Please enter the depositor of the account'), default='', required=True)
    bank_name = schema.TextLine(title=_('Bank Name'), description=_('Please enter the bank name'), default='', required=True)


class ICreditCard(IPaymentInformation):
    """Stores information of a credit card.
    """
    __module__ = __name__
    card_type = schema.Choice(title=_('Card Type'), description=_('Please select the type of the card.'), vocabulary=schema.vocabulary.SimpleVocabulary.fromItems(CREDIT_CARDS_CHOICES.items()))
    card_owner = schema.TextLine(title=_('Card Owner'), description=_('Please enter the name of the card owner.'), default='', required=True)
    card_number = schema.TextLine(title=_('Card Number'), description=_('Please enter your the card number.'), default='', required=True)
    card_expiration_date_month = schema.Choice(title=_('Expiration Date Month'), description=_('Please enter the expiration date of the card.'), vocabulary=schema.vocabulary.SimpleVocabulary.fromItems(CREDIT_CARD_MONTHS_CHOICES), default='01')
    card_expiration_date_year = schema.Choice(title=_('Expiration Date Year'), description=_('Please enter the expiration date of the card.'), vocabulary=schema.vocabulary.SimpleVocabulary.fromItems(CREDIT_CARD_YEARS_CHOICES), default='2007')


class IPaymentPrice(Interface):
    """A marker interface for payment price content objects.
    """
    __module__ = __name__


class IPaymentPriceManagement(Interface):
    """Provides all methods to manage the payment prices. This includes also 
    calculation of prices and taxes (maybe this will separated later to 
    different interfaces, e.g.: IPaymentPriceManagement, IPaymentPrices, 
    IPaymentTaxes).
    """
    __module__ = __name__

    def getPaymentPrices():
        """Return all payment prices.
        """
        pass

    def getPriceGross():
        """Returns the gross price for selected payment method.
        """
        pass

    def getPriceForCustomer():
        """Returns customer's price for selected payment method.
        """
        pass

    def getPriceNet():
        """Returns the net price for selected payment method.
        """
        pass

    def getTax():
        """Returns the default tax for the payment price.
        """
        pass

    def getTaxForCustomer():
        """Returns customer's tax for the payment price.
        """
        pass

    def getTaxRate():
        """Returns the default tax rate for the payment price.
        """
        pass

    def getTaxRateForCustomer():
        """Returns customer's tax rate for the payment price.
        """
        pass


class IPaymentMethodManagement(Interface):
    """Methods to manage payment methods on shop level. Payment methods are for
    instance: prepayment, direct debit, PayPal, credit card, cash on delivery.

    Some payment methods need additional payment information on customer level
    like: bank accounts for direct debit or credit cards (data of a credit card,
    like card number) for credit card (the payment method). Methods to manage 
    these payment information are provided by IPaymentInformationManagement. 
    See there for more.
    """
    __module__ = __name__

    def deletePaymentMethod(id):
        """Deletes a Payment Method by given id.
        """
        pass

    def getPaymentMethod(id):
        """Returns payment method by given id.
        """
        pass

    def getPaymentMethods():
        """Returns all payment informations.
        """
        pass


class IPaymentInformationManagement(Interface):
    """Provides methods to manage payment information.
    """
    __module__ = __name__

    def deletePaymentInformation(id):
        """Deletes a payment information by given id.
        """
        pass

    def getPaymentInformation(id):
        """Returns payment information by given id.
        """
        pass

    def getPaymentInformations(interface=None, check_validity=False):
        """Returns all payment information of a customer.
        """
        pass

    def getSelectedPaymentInformation(check_validity=False):
        """Returns the selected payment information.
        """
        pass

    def getSelectedPaymentMethod(check_validity=False):
        """Returns the selected payment method.
        """
        pass


class IPaymentProcessing(Interface):
    """Provides methods to processing a payment.
    """
    __module__ = __name__

    def process(order):
        """Processes a payment.
        """
        pass


class IPaymentMethodsContainer(Interface):
    """A marker interface for payment method folder content objects.
    """
    __module__ = __name__


class IPaymentPriceManagementContainer(Interface):
    """A marker interface for payment price folder objects.
    """
    __module__ = __name__


class IPaymentResult(Interface):
    """Result which is returned by payment processors.
    """
    __module__ = __name__
    code = Attribute('A code which indicates success and payment state or error\n            - PAYED\n            - NOT_PAYED\n            - ERROR')
    message = Attribute('Message which should be displayed to the user.')