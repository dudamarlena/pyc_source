# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/carts/interfaces.py
# Compiled at: 2008-09-01 03:09:26
from zope.viewlet.interfaces import IViewletManager

class ICartPortletViewletManager(IViewletManager):
    """
    """
    __module__ = __name__


class ICartViewletManager(IViewletManager):
    """Viewlet manager for the cart.
    """
    __module__ = __name__