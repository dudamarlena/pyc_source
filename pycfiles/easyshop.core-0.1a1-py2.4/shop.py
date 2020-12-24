# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/shop.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface
from plone.app.portlets.interfaces import IColumn
from easyshop.core.interfaces import IFormatable

class IShop(IFormatable):
    """Marker interface to mark shop content objects.
    """
    __module__ = __name__


class IShopInformation(Interface):
    """Methods which provide information of an shop.
    """
    __module__ = __name__

    def getTermsAndConditions():
        """Returns terms and conditions as file and text.
        """
        pass


class IShopManagement(Interface):
    """
    """
    __module__ = __name__

    def getShop():
        """Returns the parent shop
        """
        pass


class ICountryVocabulary(Interface):
    """
    """
    __module__ = __name__


class IEasyShopTop(IColumn):
    """A portlet for EasyShop
    """
    __module__ = __name__


class IEasyShopBottom(IColumn):
    """A portlet for EasyShop
    """
    __module__ = __name__