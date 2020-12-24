# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/ZCurrency.py
# Compiled at: 2015-07-18 19:38:10
"""$id$"""
__version__ = '$Revision$'[11:-2]
import AccessControl, os
from currency import currency as base, CURRENCIES, UnsupportedCurrency
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view
from new import instance
__roles__ = None
__allow_access_to_unprotected_subobjects__ = 1
if os.environ.has_key('DEFAULT_CURRENCY'):
    DEFAULT_CURRENCY = os.environ['DEFAULT_CURRENCY']
else:
    DEFAULT_CURRENCY = ''

def Supported():
    return CURRENCIES


def widget(tag, currencies, value):
    return '<input type="text" name="%s:currency" value="%s" size="12">\n' % (tag, str(value))


class ZCurrency(base):
    """
    A Zope Currency Type

    You can set a default currency via the DEFAULT_CURRENCY environment variable
    """
    meta_type = 'ZCurrency'
    __ac_permissions__ = (
     (
      view, ('widget', )),)
    _currency = DEFAULT_CURRENCY
    __roles__ = None
    __allow_access_to_unprotected_subobjects__ = 1
    _security = ClassSecurityInfo()
    _security.declareObjectPublic()

    def __add__(self, other):
        return instance(ZCurrency, base.__add__(self, other).__dict__)

    def __mul__(self, other):
        return instance(ZCurrency, base.__mul__(self, other).__dict__)

    def __div__(self, other):
        return instance(ZCurrency, base.__div__(self, other).__dict__)

    def __neg__(self):
        return ZCurrency(self._currency, -self._amount)

    def __abs__(self):
        return ZCurrency(self._currency, abs(self._amount))

    def widget(self, tag, currencies=CURRENCIES):
        return widget(tag, currencies, self)

    amount = base.amount
    currency = base.currency
    strfcur = base.strfcur
    _security.declarePublic('amount')
    _security.declarePublic('currency')
    _security.declarePublic('strfcur')

    def X__cmp__(self, other):
        try:
            return base.__cmp__(self, other)
        except UnsupportedError:
            try:
                currency_service = self.Control_Panel.CurrencyTool
            except:
                raise

            rate = currency_service.getQuote(other.currency)
            if rate:
                return base.__cmp__(self, currency(self._currency, other._amount * rate))
            rate = currency_service.getQuote(self.currency)
            if rate:
                return base.__cmp__(other, currency(other._currency, self._amount * rate))
            raise


AccessControl.class_init.InitializeClass(ZCurrency)