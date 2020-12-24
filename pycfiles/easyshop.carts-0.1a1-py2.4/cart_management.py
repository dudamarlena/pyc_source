# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/carts/adapters/cart_management.py
# Compiled at: 2008-09-03 11:14:22
from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import ISessionManagement
from easyshop.core.interfaces import IShop

class CartManagement(object):
    """Adapter which provides ICartManagement for shop content objects.
    """
    __module__ = __name__
    implements(ICartManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.carts = self.context.carts

    def createCart(self):
        """
        """
        cart_id = self._getCartId()
        self.carts.manage_addProduct['easyshop.core'].addCart(id=cart_id)
        return self.carts[cart_id]

    def deleteCart(self, id=None):
        """Deletes a cart
        """
        if id is None:
            id = self._getCartId()
        self.carts._delObject(id)
        return

    def getCart(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        sid = getUtility(ISessionManagement).getSID(self.context.REQUEST)
        try:
            anonymous_cart = self.carts[sid]
        except KeyError:
            anonymous_cart = None

        if mtool.getAuthenticatedMember().getId() is None:
            cart = anonymous_cart
        else:
            mid = mtool.getAuthenticatedMember().getId()
            if anonymous_cart is None:
                try:
                    cart = self.carts[mid]
                except KeyError:
                    cart = None

            else:
                try:
                    cart = self.carts[mid]
                except KeyError:
                    cart = self.createCart()

                im = IItemManagement(cart).addItemsFromCart(anonymous_cart)
                self.deleteCart(sid)
        return cart

    def getCarts(self, sort_on='created', sort_order='descending'):
        """
        """
        path = ('/').join(self.carts.getPhysicalPath())
        query = {'path': path, 'portal_type': 'Cart', 'sort_on': sort_on, 'sort_order': sort_order}
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.unrestrictedSearchResults(query)
        return brains

    def getCartById(self, id):
        """
        """
        return self.carts.get(id)

    def getCartByUID(self, uid):
        """Returns a cart by given uid.        
        """
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        lazy_cat = uid_catalog(UID=uid)
        o = lazy_cat[0].getObject()
        return o

    def hasCart(self):
        """
        """
        try:
            self.carts[self._getCartId()]
        except KeyError:
            return False
        else:
            return True

    def _getCartId(self):
        """Returns cart id for current cart. This is either the session id
        (anonymous user) or the member id of the authenticated user.
        """
        mtool = getToolByName(self.context, 'portal_membership')
        cart_id = mtool.getAuthenticatedMember().getId()
        if cart_id is not None:
            return cart_id
        else:
            return getUtility(ISessionManagement).getSID(self.context.REQUEST)
        return