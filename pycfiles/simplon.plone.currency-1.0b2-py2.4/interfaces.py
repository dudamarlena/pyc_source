# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/simplon/plone/currency/interfaces.py
# Compiled at: 2007-09-08 18:44:19
from zope.interface import Attribute
from zope.interface import Interface
from zope.schema import Choice
from zope.schema import Container
from zope.schema import Float
from zope.app.container.interfaces import IContained
from zope.app.container.interfaces import IContainer
from zope.app.container.interfaces import IContainerNamesContainer
from zope.app.container.constraints import contains
from Products.CMFPlone import PloneMessageFactory as _

class ICurrencyInformation(Interface):
    __module__ = __name__
    code = Choice(title=_('label_currency_currency', default='Currency'), description=_('help_currency_currency', default='The base currency is used as the default currency as well as the base for currency rates. If you change the base currency all rates will be recalculated automatically.'), vocabulary='simplon.plone.currency.currencies', required=True)
    rate = Float(title=_('label_currency_rate', default='Rate'), description=_('help_currency_date', default="This is the conversion rate from this currency to a 'system' currency you configure."), min=0.0, default=1.0, required=True)
    symbol = Attribute('symbol', 'The symbol used to identify this currency. Since not allcurrencies have a symbol this can be an empty string.')
    description = Attribute('description', 'A short description of the currency.')


class ICurrency(IContained, ICurrencyInformation):
    """Currency information."""
    __module__ = __name__


class ICurrencyStorage(IContainer, IContainerNamesContainer):
    __module__ = __name__
    contains('simplon.plone.currency.interfaces.ICurrency')


class IGlobalCurrencySettings(Interface):
    __module__ = __name__
    currency = Choice(title=_('label_currencymanager_base_currency', default='Base currency'), description=_('help_currencymanager_base_currency', default='The base currency is used as the default currency as well as the base for currency rates.'), vocabulary='simplon.plone.currency.sitecurrencies', default='EUR', required=True)

    def SwitchCurrency(code):
        """Switch the base currency.

        This will take care of recalculating all conversion rates.
        """
        pass

    def Convert(from_currency, to_currency, amount):
        """Convert from one currency to another currency."""
        pass


class ICurrencyManager(IGlobalCurrencySettings):
    __module__ = __name__
    currencies = Container(title=_('label_currencymanager_currencies', default='Currencies'), description=_('help_currencymanager_currencies', default=''), required=True)