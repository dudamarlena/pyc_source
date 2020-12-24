# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/slc.cart/src/slc/cart/tests/test_actions.py
# Compiled at: 2012-11-05 01:56:15
"""Testing ICartActions."""
from marshal import loads
from plone import api
from slc.cart.tests.base import IntegrationTestCase
from urllib import unquote
from zlib import decompress
from zope.interface import alsoProvides
import unittest2 as unittest

class TestActions(IntegrationTestCase):
    """Test ICartAction actions."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        from slc.cart.interfaces import ISlcCartLayer
        alsoProvides(self.layer['app'].REQUEST, ISlcCartLayer)
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.cart_view = self.portal.restrictedTraverse('@@cart')
        self.item1 = api.content.create(container=self.portal, id='item1', type='Document')
        self.item2 = api.content.create(container=self.portal, id='item2', type='Document')
        self.item3 = api.content.create(container=self.portal, id='item3', type='File', file='foo')
        self.item3.setFilename('foo.txt')

    def test_delete(self):
        """Test if delete action correctly deletes all items present in
        cart (and nothing else) and also clears the cart itself.
        """
        self.item1.restrictedTraverse('add-to-cart').render()
        self.item3.restrictedTraverse('add-to-cart').render()
        self.assertEquals(self.cart_view.item_count(), 2)
        self.cart_view.action = 'delete'
        self.cart_view._run_action()
        self.assertIsNone(self.portal.get('item1'))
        self.assertIsNone(self.portal.get('item3'))
        self.assertIsNotNone(self.portal.get('item2'))
        self.assertEquals(self.cart_view.item_count(), 0)

    def test_download(self):
        """Test for 'download' cart action."""
        self.item1.restrictedTraverse('add-to-cart').render()
        self.item2.restrictedTraverse('add-to-cart').render()
        self.item3.restrictedTraverse('add-to-cart').render()
        self.assertEquals(self.cart_view.item_count(), 3)
        self.cart_view.action = 'download'
        output = self.cart_view._run_action()
        self.assertIn('foo.txt', output)
        self.cart_view.clear()
        output = self.cart_view._run_action()
        self.assertIsNone(output)

    def test_copy(self):
        """Test if 'copy' cart action writes correct copydata to a cookie.
        """
        self.item1.restrictedTraverse('add-to-cart').render()
        self.item2.restrictedTraverse('add-to-cart').render()
        self.assertEquals(self.cart_view.item_count(), 2)
        self.cart_view.action = 'copy'
        self.cart_view._run_action()
        cookies = self.cart_view.response.cookies
        cp_cookie = cookies.get('__cp')
        self.assertIsNotNone(cp_cookie)
        val = cp_cookie.get('value')
        self.assertIsNotNone(val)
        try:
            val = loads(decompress(unquote(val)))
        except Exception, ex:
            self.fail(('Could not decode cookie value: {0}').format(ex.strerror))

        self.assertEquals(len(val[1]), 2)
        expected_val = (
         0, [('', 'plone', 'item1'), ('', 'plone', 'item2')])
        self.assertEquals(val[0], expected_val[0])
        self.assertIn(val[1][0], expected_val[1])
        self.assertIn(val[1][1], expected_val[1])
        self.assertNotIn(('', 'plone', 'item3'), val[1])

    def test_cut(self):
        """Test if 'cut' cart action writes correct cutdata to a cookie.
        """
        self.item1.restrictedTraverse('add-to-cart').render()
        self.item2.restrictedTraverse('add-to-cart').render()
        self.assertEquals(self.cart_view.item_count(), 2)
        self.cart_view.action = 'cut'
        self.cart_view._run_action()
        cookies = self.cart_view.response.cookies
        cp_cookie = cookies.get('__cp')
        self.assertIsNotNone(cp_cookie)
        val = cp_cookie.get('value')
        self.assertIsNotNone(val)
        try:
            val = loads(decompress(unquote(val)))
        except Exception, ex:
            self.fail(('Could not decode cookie value: {0}').format(ex.strerror))

        self.assertEquals(len(val[1]), 2)
        expected_val = (
         1, [('', 'plone', 'item1'), ('', 'plone', 'item2')])
        self.assertEquals(val[0], expected_val[0])
        self.assertIn(val[1][0], expected_val[1])
        self.assertIn(val[1][1], expected_val[1])
        self.assertNotIn(('', 'plone', 'item3'), val[1])


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)