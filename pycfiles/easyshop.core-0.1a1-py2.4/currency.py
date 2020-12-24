# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/currency.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface

class ICurrencyManagement(Interface):
    """Provides methods to return different currency names.
    """
    __module__ = __name__

    def getLongName(id):
        """Returns long name for curreny with given id.
        """
        pass

    def getShortName(id):
        """Returns short name for curreny with given id.
        """
        pass

    def getSymbol(id):
        """Returns symbol for curreny with given id.
        """
        pass

    def priceToString(price, symbol='symbol', position='after'):
        """Returns given price as formated currency string.
        """
        pass