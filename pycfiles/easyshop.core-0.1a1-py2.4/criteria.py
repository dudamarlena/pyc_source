# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/criteria.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface

class ICriteria(Interface):
    """Base interface for criteria.
    """
    __module__ = __name__

    def getValue():
        """Returns the entered value for the criterion.
        """
        pass


class ICategoryCriteria(ICriteria):
    """Marker interface to mark category criteria content objects.
    """
    __module__ = __name__


class ICountryCriteria(ICriteria):
    """Marker interface to mark country criteria content objects.
    """
    __module__ = __name__


class ICustomerCriteria(ICriteria):
    """Marker interface to mark customer criteria content objects.
    """
    __module__ = __name__


class IDateCriteria(ICriteria):
    """Marker interface to mark date criteria content objects.
    """
    __module__ = __name__


class IGroupCriteria(ICriteria):
    """Marker interface to mark group criteria content objects.
    """
    __module__ = __name__


class IPaymentMethodCriteria(ICriteria):
    """Marker interface to mark payment criteria content objects.
    """
    __module__ = __name__


class IProductAmountCriteria(ICriteria):
    """Marker interface to mark product amount criteria content objects.
    """
    __module__ = __name__


class IProductCriteria(ICriteria):
    """Marker interface to mark product criteria content objects.
    """
    __module__ = __name__


class IPriceCriteria(ICriteria):
    """Marker interface to mark price criteria content objects.
    """
    __module__ = __name__


class IShippingMethodCriteria(ICriteria):
    """Marker interface to mark shipping method criteria content objects.
    """
    __module__ = __name__


class IStockAmountCriteria(ICriteria):
    """Marker interface to mark stock criteria content objects.
    """
    __module__ = __name__


class IWeightCriteria(ICriteria):
    """Marker interface to mark weight criteria content objects.
    """
    __module__ = __name__