# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/interfaces/ICurrencyIndex.py
# Compiled at: 2015-07-18 19:38:10
__doc__ = 'PluginIndexes z3 interfaces.\n\n$Id: interfaces.py 33294 2005-07-13 10:56:36Z yuppie $\n'
from zope.interface import Interface
from zope.schema import Bool, Choice
from Products.BastionBanking.ZCurrency import CURRENCIES

class ICurrencyIndex(Interface):
    """Index for currencies.
    """
    base_currency = Choice(title='Base currency - only used if convert_to_base', values=CURRENCIES)
    convert_to_base = Bool(title='Convert to base currency on input?')