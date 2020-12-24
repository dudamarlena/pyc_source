# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/discounts.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface

class IDiscount(Interface):
    """A marker interface to mark discount content objects.
    """
    __module__ = __name__


class IDiscountsContainer(Interface):
    """A marker interface for container which holds discount content objects.
    """
    __module__ = __name__


class IDiscountsManagement(Interface):
    """Provides management of discount content objects.
    """
    __module__ = __name__

    def getDiscounts():
        """Returns discount content objects.
        """
        pass


class IDiscountsCalculation(Interface):
    """Provides calculation of discounts.
    """
    __module__ = __name__

    def getDiscounts():
        """Returns calculated discounts as dictionary.
        """
        pass