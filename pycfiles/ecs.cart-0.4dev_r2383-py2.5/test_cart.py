# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ecs/cart/tests/test_cart.py
# Compiled at: 2009-01-13 06:18:21
import os, sys, unittest
dirname = os.path.dirname(__file__)
if dirname not in sys.path:
    sys.path.append(os.path.split(dirname)[0])
from ecs.cart import Cart
from ecs.cart.tests import database

class CartTest(unittest.TestCase):

    def setUp(self):
        Cart._sqluri_callback = database

    def test_add_del_product(self):
        cart = Cart('user_test_1')
        cart.add_product('cheeseburger', 3.5)
        cart.add_product('coca light', price='1.4', quantity=1)
        cart.add_product('glace', price=4, vat=19.6, quantity='3')
        self.assertEquals(cart.products['cheeseburger']['quantity'], 1)
        self.assertEquals(cart.products['coca light']['price']['included_tax'], 1.4)
        self.assertEquals(cart.products['coca light']['price']['vat'], 0.0)
        self.assertEquals(cart.products['glace']['quantity'], 3)
        self.assertEquals(cart.products['glace']['price']['vat'], 19.6)
        self.assertRaises(ValueError, cart.add_product)
        cart.del_product('cheeseburger')
        cart.del_product('coca light')
        cart.del_product('fantaisic object')
        self.assertRaises(ValueError, cart.get_product_property, 'cheesebuger', 'price')
        self.assertRaises(ValueError, cart.get_product_property, 'coca light', 'quantity')
        self.assertEquals(cart.get_product_property('glace', 'quantity'), 3)
        cart.del_all_product()

    def test_set_quantity(self):
        cart = Cart('user_test_2')
        cart.add_product('cheeseburger', 3.5)
        cart.set_quantity('cheeseburger', 10)
        self.assertEquals(cart.get_product_property('cheeseburger', 'quantity'), 10)
        self.assertRaises(ValueError, cart.set_quantity, 'fantaisic object', 42)
        cart.set_quantity('cheeseburger', 0)
        self.assertRaises(ValueError, cart.get_product_property, 'cheeseburger', 'quantity')
        cart.del_all_product()

    def test_get_cart_amount(self):
        cart = Cart('user_test_3')
        cart.add_product('sauce', price=0.42, quantity=10)
        cart.add_product('frite', price=1.5, quantity=20)
        cart.add_product('cheeseburger', price=3.5, quantity=20)
        self.assertEquals(cart.get_cart_amount(), 104.2)
        cart.del_all_product()


def test_suite():
    tests = [
     unittest.makeSuite(CartTest)]
    return unittest.TestSuite(tests)


if __name__ == '__main__':
    unittest.main()