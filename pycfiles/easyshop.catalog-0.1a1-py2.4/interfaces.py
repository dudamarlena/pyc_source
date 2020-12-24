# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/viewlets/interfaces.py
# Compiled at: 2008-06-20 09:35:03
from zope.viewlet.interfaces import IViewletManager

class IProductsViewletManager(IViewletManager):
    """Viewlet manager for category selector view.
    """
    __module__ = __name__


class ICategoriesViewletManager(IViewletManager):
    """Viewlet manager for categories view.
    """
    __module__ = __name__


class IProductViewletManager(IViewletManager):
    """Viewlet manager for product view.
    """
    __module__ = __name__


class IProductSelectorViewletManager(IViewletManager):
    """Viewlet manager for product selector view.
    """
    __module__ = __name__