# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/FinanceFields/config.py
# Compiled at: 2010-03-10 14:21:02
from Products.Archetypes.utils import DisplayList
ADD_CONTENT_PERMISSION = 'Add FinanceFields content'
PROJECTNAME = 'FinanceFields'
GLOBALS = globals()
I18N_DOMAIN = 'plone_accounting'
SKINS_DIR = 'skins'
from AccessControl import allow_module
allow_module('Products.FinanceFields.config')
allow_module('Products.FinanceFields.Money')
from Currency import CURRENCIES
l = DisplayList()
for cur in CURRENCIES.values():
    symbol = cur.int_currency_symbol
    l.add(symbol, symbol, symbol)

l._itor.sort()
CURRENCY_DISPLAY_LIST = l