# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/taxes.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface

class ITaxes(Interface):
    """
    """
    __module__ = __name__

    def getTax():
        """Returns default tax for a product
       """
        pass

    def getTaxForCustomer():
        """Returns tax for a customer
       """
        pass

    def getTaxRate():
        """Returns default tax for a product
       """
        pass

    def getTaxRateForCustomer():
        """Returns tax for a customer
       """
        pass


class ITax(Interface):
    """A marker interface to mark tax content objects.
    """
    __module__ = __name__


class ITaxManagement(Interface):
    """Provides methods to manage tax content objects.
    """
    __module__ = __name__

    def getCustomerTaxes():
        """Returns all customer taxes.
        """
        pass

    def getDefaultTaxes():
        """Returns all default taxes.
        """
        pass

    def getTax(id):
        """Returns tax object by given id.
        """
        pass


class ITaxesContainer(Interface):
    """A container which holds tax content objects.
    """
    __module__ = __name__