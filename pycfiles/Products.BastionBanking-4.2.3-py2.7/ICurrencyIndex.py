# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/interfaces/ICurrencyIndex.py
# Compiled at: 2015-07-18 19:38:10
"""PluginIndexes z3 interfaces.

$Id: interfaces.py 33294 2005-07-13 10:56:36Z yuppie $
"""
from zope.interface import Interface
from zope.schema import Bool, Choice
from Products.BastionBanking.ZCurrency import CURRENCIES

class ICurrencyIndex(Interface):
    """Index for currencies.
    """
    base_currency = Choice(title='Base currency - only used if convert_to_base', values=CURRENCIES)
    convert_to_base = Bool(title='Convert to base currency on input?')