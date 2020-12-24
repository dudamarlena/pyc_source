# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_shop_cart.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICartManagement

class TestCartManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestCartManagement, self).afterSetUp()
        self.cm = ICartManagement(self.shop)

    def testCreateCart_1(self):
        """Create cart for anonymous.
        """
        self.logout()
        sid = self.portal.REQUEST.SESSION = utils.TestSession('123')
        cart = self.cm.createCart()
        self.assertEqual(cart.getId(), '123')

    def testCreateCart_2(self):
        """Create cart for member.
        """
        self.login('newmember')
        cart = self.cm.createCart()
        self.assertEqual(cart.getId(), 'newmember')

    def testDeleteCart_1(self):
        """Without given id.
        """
        self.login('newmember')
        self.cm.createCart()
        self.failUnless(self.shop.carts.get('newmember'))
        self.cm.deleteCart()
        self.failIf(self.shop.carts.get('newmember'))

    def testDeleteCart_2(self):
        """With given id.
        """
        self.login('newmember')
        self.cm.createCart()
        self.failUnless(self.shop.carts.get('newmember'))
        self.cm.deleteCart('newmember')
        self.failIf(self.shop.carts.get('newmember'))

    def testGetCart_1(self):
        """Cart for anonmyous. There is no cart yet.
        """
        self.logout()
        sid = self.portal.REQUEST.SESSION = utils.TestSession('123')
        cart = self.cm.getCart()
        self.assertEqual(cart, None)
        return

    def testGetCart_2(self):
        """Cart for anonymous. There is a cart
        """
        self.logout()
        sid = self.portal.REQUEST.SESSION = utils.TestSession('123')
        self.cm.createCart()
        cart = self.cm.getCart()
        self.assertEqual(cart.getId(), '123')

    def testGetCart_3(self):
        """Cart for member. There is no anonymous cart. Carts are only created
        when items are added to it.
        """
        self.login('newmember')
        cart = self.cm.getCart()
        self.assertEqual(cart, None)
        return

    def testGetCart_4(self):
        """Cart for member. There is an anonymous cart.
        """
        self.logout()
        sid = self.portal.REQUEST.SESSION = utils.TestSession('123')
        self.cm.createCart()
        cart = self.cm.getCart()
        self.assertEqual(cart.getId(), '123')
        self.login('newmember')
        cart = self.cm.getCart()
        self.assertEqual(cart.getId(), 'newmember')
        self.failIf(self.shop.carts.get('123'))

    def testGetCarts(self):
        """
        """
        self.login('newmember')
        self.cm.createCart()
        self.setRoles(('Manager', ))
        ids = [ c.getId for c in self.cm.getCarts() ]
        self.assertEqual(ids, ['newmember'])

    def testGetCartById(self):
        """
        """
        self.login('newmember')
        self.cm.createCart()
        cart = self.cm.getCartById('newmember')
        self.assertEqual(cart.getId(), 'newmember')

    def testGetCartByUID(self):
        """
        """
        self.login('newmember')
        cart = self.cm.createCart()
        cart = self.cm.getCartByUID(cart.UID())
        self.assertEqual(cart.getId(), 'newmember')

    def testHasCart(self):
        """
        """
        self.assertEqual(self.cm.hasCart(), False)
        self.login('newmember')
        cart = self.cm.createCart()
        self.assertEqual(self.cm.hasCart(), True)

    def test_getCartId(self):
        """
        """
        self.logout()
        sid = self.portal.REQUEST.SESSION = utils.TestSession('123')
        cart_id = self.cm._getCartId()
        self.assertEqual(cart_id, '123')
        self.login('newmember')
        cart_id = self.cm._getCartId()
        self.assertEqual(cart_id, 'newmember')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCartManagement))
    return suite