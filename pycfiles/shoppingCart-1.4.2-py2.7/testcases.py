# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/shoppingCart/tests/testcases.py
# Compiled at: 2015-08-10 04:44:00
import unittest
from shoppingCart.tests.product import Product, Option, OptionValue
from shoppingCart.tests.discount_coupon import DiscountCoupon
from shoppingCart import Cart

class CartTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.cart = Cart()
        self.cart.currency_rate = 1
        self.cart.price_accuracy = 2
        self.cart.currency_symbol = '€'
        self.cart.currency_code = 'EUR'
        self.cart.shipping_charge = 10.21
        self.option_value1 = OptionValue(id=1, name='option_value-1', code='ov1', price=5.0)
        self.option_value2 = OptionValue(id=2, name='option_value-2', code='ov2', price=10.0)
        self.option_value3 = OptionValue(id=3, name='option_value-3', code='ov3', price=15.0)
        self.option_value4 = OptionValue(id=4, name='option_value-4', code='ov4', price=20.0)
        self.option1 = Option(id=1, name='option-1', code='o1', values=[self.option_value1, self.option_value2])
        self.option2 = Option(id=2, name='option-2', code='o2', values=[self.option_value3, self.option_value4])
        self.product1 = Product(id=1, name='product-1', code='p1', price=10.0)
        self.product2 = Product(id=2, name='product-2', code='p2', price=12.25, options=[self.option1, self.option2])
        self.product3 = Product(id=3, name='product-3', code='p3', price=20.0)
        self.discount_coupon1 = DiscountCoupon(code='ByQ343X', expiry_date='2010-11-30 12:00:00', type='percentage', discount=30)
        self.discount_coupon2 = DiscountCoupon(code='Ax9812Y', expiry_date='2010-12-31', type='amount', discount=20)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.cart
        del self.product1
        del self.product2
        del self.product3
        del self.option_value1
        del self.option_value2
        del self.option_value3
        del self.option_value4
        del self.option1
        del self.option2
        del self.discount_coupon1
        del self.discount_coupon2

    def test_add_item(self):
        self.assertTrue(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 0)
        self.cart.add_item(product=1, price=10.0, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertFalse(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 3.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 1, 'quantity': 1}, {'product': 2, 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.0, quantity=1)
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.assertFalse(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 3.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-1', 'quantity': 1}, {'product': 'product-2', 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.0, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.assertFalse(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 3.5)
        self.assertEqual([ {'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-1', 'quantity': 1}, {'product': 'product-2', 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])

    def test_update_item(self):
        self.cart.add_item(product=1, price=10.0, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.update_item(product=1, quantity=3)
        self.cart.update_item(product=2, quantity=1.5)
        self.assertEqual(self.cart.count(), 4.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 1, 'quantity': 3}, {'product': 2, 'quantity': 1.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.0, quantity=1)
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.update_item(product='product-1', quantity=3)
        self.cart.update_item(product='product-2', quantity=1.5)
        self.assertEqual(self.cart.count(), 4.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-1', 'quantity': 3}, {'product': 'product-2', 'quantity': 1.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.0, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.update_item(product=self.product1, quantity=3)
        self.cart.update_item(product=self.product2, quantity=1.5)
        self.assertEqual(self.cart.count(), 4.5)
        self.assertEqual([ {'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-1', 'quantity': 3}, {'product': 'product-2', 'quantity': 1.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])

    def test_remove_item(self):
        self.cart.add_item(product=1, price=10.0, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.remove_item(product=1)
        self.assertEqual(self.cart.count(), 2.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 2, 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.0, quantity=1)
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.remove_item(product='product-1')
        self.assertEqual(self.cart.count(), 2.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-2', 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.0, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.remove_item(product=self.product1)
        self.assertEqual(self.cart.count(), 2.5)
        self.assertEqual([ {'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-2', 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])

    def test_find_item(self):
        self.cart.add_item(product=1, price=10.0, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.find_item(3), None)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item(1)] ], [{'product': 1, 'quantity': 1}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.0, quantity=1)
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.assertEqual(self.cart.find_item('product-3'), None)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item('product-1')] ], [{'product': 'product-1', 'quantity': 1}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.0, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.find_item(self.product3), None)
        self.assertEqual([ {'product': item.product.name, 'quantity': item.quantity} for item in [self.cart.find_item(self.product1)] ], [{'product': 'product-1', 'quantity': 1}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        return

    def test_add_item_with_options(self):
        self.assertTrue(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 0)
        self.cart.add_item(product=1, price=10.0, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.cart.add_item(product=2, price=12.25, quantity=1, options={2: {4: {'price': 20.0}}})
        self.cart.add_item(product=2, price=12.25, quantity=2, options={1: {1: {'price': 5.0}}, 2: {3: {'price': 15.0}}})
        self.cart.add_item(product=2, price=12.25, quantity=3.5, options={1: {2: {'price': 10.0}}, 2: {4: {'price': 20.0}}})
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity, 'price': item.price, 'options': item.get_options()} for item in self.cart.get_items() ], [{'product': 1, 'options': {}, 'price': 10.0, 'quantity': 1}, {'product': 2, 'options': {}, 'price': 12.25, 'quantity': 2.5}, {'product': 2, 'options': {2: {4: {'price': 20.0}}}, 'price': 12.25, 'quantity': 1}, {'product': 2, 'options': {1: {1: {'price': 5.0}}, 2: {3: {'price': 15.0}}}, 'price': 12.25, 'quantity': 2}, {'product': 2, 'options': {1: {2: {'price': 10.0}}, 2: {4: {'price': 20.0}}}, 'price': 12.25, 'quantity': 3.5}])
        self.assertEqual(self.cart.count(), 10.0)
        self.assertEqual('%s' % (self.cart.tax_type,), 'excluded')
        self.assertEqual('%s %s' % (self.cart.sub_total(), self.cart.currency_symbol), '285.26 €')
        self.assertEqual('%s %s' % (self.cart.total_untaxed_amount(), self.cart.currency_symbol), '285.26 €')
        self.assertEqual('%s %s' % (self.cart.total_tax(), self.cart.currency_symbol), '4.06 €')
        self.assertEqual('%s %s' % (self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        self.assertEqual('%s %s' % (self.cart.total(), self.cart.currency_symbol), '299.53 €')
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.0, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.cart.add_item(product='product-2', price=12.25, quantity=1, options={'option-2': {'option_value-4': {'price': 20.0}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=2, options={'option-1': {'option_value-1': {'price': 5.0}}, 'option-2': {'option_value-3': {'price': 15.0}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=3.5, options={'option-1': {'option_value-2': {'price': 10.0}}, 'option-2': {'option_value-4': {'price': 20.0}}})
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity, 'price': item.price, 'options': item.get_options()} for item in self.cart.get_items() ], [{'product': 'product-1', 'options': {}, 'price': 10.0, 'quantity': 1}, {'product': 'product-2', 'options': {}, 'price': 12.25, 'quantity': 2.5}, {'product': 'product-2', 'options': {'option-2': {'option_value-4': {'price': 20.0}}}, 'price': 12.25, 'quantity': 1}, {'product': 'product-2', 'options': {'option-1': {'option_value-1': {'price': 5.0}}, 'option-2': {'option_value-3': {'price': 15.0}}}, 'price': 12.25, 'quantity': 2}, {'product': 'product-2', 'options': {'option-1': {'option_value-2': {'price': 10.0}}, 'option-2': {'option_value-4': {'price': 20.0}}}, 'price': 12.25, 'quantity': 3.5}])
        self.assertEqual(self.cart.count(), 10.0)
        self.assertEqual('%s' % (self.cart.tax_type,), 'excluded')
        self.assertEqual('%s %s' % (self.cart.sub_total(), self.cart.currency_symbol), '285.26 €')
        self.assertEqual('%s %s' % (self.cart.total_untaxed_amount(), self.cart.currency_symbol), '285.26 €')
        self.assertEqual('%s %s' % (self.cart.total_tax(), self.cart.currency_symbol), '4.06 €')
        self.assertEqual('%s %s' % (self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        self.assertEqual('%s %s' % (self.cart.total(), self.cart.currency_symbol), '299.53 €')
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.0, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.cart.add_item(product=self.product2, price=12.25, quantity=1, options={self.option1: {self.option_value4: {'price': 20.0}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=2, options={self.option1: {self.option_value1: {'price': 5.0}}, self.option2: {self.option_value3: {'price': 15.0}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=3.5, options={self.option1: {self.option_value2: {'price': 10.0}}, self.option2: {self.option_value4: {'price': 20.0}}})
        options = {}
        self.assertEqual(self.cart.count(), 10.0)
        self.assertEqual('%s' % (self.cart.tax_type,), 'excluded')
        self.assertEqual('%s %s' % (self.cart.sub_total(), self.cart.currency_symbol), '285.26 €')
        self.assertEqual('%s %s' % (self.cart.total_untaxed_amount(), self.cart.currency_symbol), '285.26 €')
        self.assertEqual('%s %s' % (self.cart.total_tax(), self.cart.currency_symbol), '4.06 €')
        self.assertEqual('%s %s' % (self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        self.assertEqual('%s %s' % (self.cart.total(), self.cart.currency_symbol), '299.53 €')

    def test_update_item_with_options(self):
        self.cart.add_item(product=1, price=10.0, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.cart.add_item(product=2, price=12.25, quantity=1, options={2: {4: {'price': 20.0}}})
        self.cart.add_item(product=2, price=12.25, quantity=2, options={1: {1: {'price': 5.0}}, 2: {3: {'price': 15.0}}})
        self.cart.add_item(product=2, price=12.25, quantity=3.5, options={1: {2: {'price': 10.0}}, 2: {4: {'price': 20.0}}})
        self.assertEqual(self.cart.count(), 10)
        self.cart.update_item(product=1, quantity=3)
        self.cart.update_item(product=2, quantity=1.5)
        self.cart.update_item(product=2, quantity=2, option_values=[4])
        self.cart.update_item(product=2, quantity=3, option_values=[1, 3])
        self.cart.update_item(product=2, quantity=4, option_values=[2, 4])
        self.assertEqual(self.cart.count(), 13.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 1, 'quantity': 3}, {'product': 2, 'quantity': 1.5}, {'product': 2, 'quantity': 2}, {'product': 2, 'quantity': 3}, {'product': 2, 'quantity': 4}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.0, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.cart.add_item(product='product-2', price=12.25, quantity=1, options={'option-2': {'option_value-4': {'price': 20.0}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=2, options={'option-1': {'option_value-1': {'price': 5.0}}, 'option-2': {'option_value-3': {'price': 15.0}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=3.5, options={'option-1': {'option_value-2': {'price': 10.0}}, 'option-2': {'option_value-4': {'price': 20.0}}})
        self.assertEqual(self.cart.count(), 10)
        self.cart.update_item(product='product-1', quantity=3)
        self.cart.update_item(product='product-2', quantity=1.5)
        self.cart.update_item(product='product-2', quantity=2, option_values=['option_value-4'])
        self.cart.update_item(product='product-2', quantity=3, option_values=['option_value-1', 'option_value-3'])
        self.cart.update_item(product='product-2', quantity=4, option_values=['option_value-2', 'option_value-4'])
        self.assertEqual(self.cart.count(), 13.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-1', 'quantity': 3}, {'product': 'product-2', 'quantity': 1.5}, {'product': 'product-2', 'quantity': 2}, {'product': 'product-2', 'quantity': 3}, {'product': 'product-2', 'quantity': 4}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.0, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.cart.add_item(product=self.product2, price=12.25, quantity=1, options={self.option1: {self.option_value4: {'price': 20.0}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=2, options={self.option1: {self.option_value1: {'price': 5.0}}, self.option2: {self.option_value3: {'price': 15.0}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=3.5, options={self.option1: {self.option_value2: {'price': 10.0}}, self.option2: {self.option_value4: {'price': 20.0}}})
        self.assertEqual(self.cart.count(), 10.0)
        self.cart.update_item(product=self.product1, quantity=3)
        self.cart.update_item(product=self.product2, quantity=1.5)
        self.cart.update_item(product=self.product2, quantity=2, option_values=[self.option_value4])
        self.cart.update_item(product=self.product2, quantity=3, option_values=[self.option_value1, self.option_value3])
        self.cart.update_item(product=self.product2, quantity=4, option_values=[self.option_value2, self.option_value4])
        self.assertEqual(self.cart.count(), 13.5)
        self.assertEqual([ {'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-1', 'quantity': 3}, {'product': 'product-2', 'quantity': 1.5}, {'product': 'product-2', 'quantity': 2}, {'product': 'product-2', 'quantity': 3}, {'product': 'product-2', 'quantity': 4}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])

    def test_remove_item_with_options(self):
        self.cart.add_item(product=1, price=10.0, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.cart.add_item(product=2, price=12.25, quantity=1, options={2: {4: {'price': 20.0}}})
        self.cart.add_item(product=2, price=12.25, quantity=2, options={1: {1: {'price': 5.0}}, 2: {3: {'price': 15.0}}})
        self.cart.add_item(product=2, price=12.25, quantity=3.5, options={1: {2: {'price': 10.0}}, 2: {4: {'price': 20.0}}})
        self.assertEqual(self.cart.count(), 10)
        self.cart.remove_item(product=1)
        self.cart.remove_item(product=2, option_values=[2, 4])
        self.assertEqual(self.cart.count(), 5.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 2, 'quantity': 2.5}, {'product': 2, 'quantity': 1}, {'product': 2, 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.0, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.cart.add_item(product='product-2', price=12.25, quantity=1, options={'option-2': {'option_value-4': {'price': 20.0}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=2, options={'option-1': {'option_value-1': {'price': 5.0}}, 'option-2': {'option_value-3': {'price': 15.0}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=3.5, options={'option-1': {'option_value-2': {'price': 10.0}}, 'option-2': {'option_value-4': {'price': 20.0}}})
        self.assertEqual(self.cart.count(), 10)
        self.cart.remove_item(product='product-1')
        self.cart.remove_item(product='product-2', option_values=['option_value-2', 'option_value-4'])
        self.assertEqual(self.cart.count(), 5.5)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-2', 'quantity': 2.5}, {'product': 'product-2', 'quantity': 1}, {'product': 'product-2', 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.0, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.cart.add_item(product=self.product2, price=12.25, quantity=1, options={self.option1: {self.option_value4: {'price': 20.0}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=2, options={self.option1: {self.option_value1: {'price': 5.0}}, self.option2: {self.option_value3: {'price': 15.0}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=3.5, options={self.option1: {self.option_value2: {'price': 10.0}}, self.option2: {self.option_value4: {'price': 20.0}}})
        self.assertEqual(self.cart.count(), 10.0)
        self.cart.remove_item(product=self.product1)
        self.cart.remove_item(product=self.product2, option_values=[self.option_value2, self.option_value4])
        self.assertEqual(self.cart.count(), 5.5)
        self.assertEqual([ {'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items() ], [{'product': 'product-2', 'quantity': 2.5}, {'product': 'product-2', 'quantity': 1}, {'product': 'product-2', 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])

    def test_find_item_with_options(self):
        self.cart.add_item(product=1, price=10.0, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.cart.add_item(product=2, price=12.25, quantity=1, options={2: {4: {'price': 20.0}}})
        self.cart.add_item(product=2, price=12.25, quantity=2, options={1: {1: {'price': 5.0}}, 2: {3: {'price': 15.0}}})
        self.cart.add_item(product=2, price=12.25, quantity=3.5, options={1: {2: {'price': 10.0}}, 2: {4: {'price': 20.0}}})
        self.assertEqual(self.cart.find_item(3), None)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item(1)] ], [{'product': 1, 'quantity': 1}])
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item(2)] ], [{'product': 2, 'quantity': 2.5}])
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item(2, option_values=[1, 3])] ], [{'product': 2, 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.0, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.cart.add_item(product='product-2', price=12.25, quantity=1, options={'option-2': {'option_value-4': {'price': 20.0}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=2, options={'option-1': {'option_value-1': {'price': 5.0}}, 'option-2': {'option_value-3': {'price': 15.0}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=3.5, options={'option-1': {'option_value-2': {'price': 10.0}}, 'option-2': {'option_value-4': {'price': 20.0}}})
        self.assertEqual(self.cart.find_item('product-3'), None)
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item('product-1')] ], [{'product': 'product-1', 'quantity': 1}])
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item('product-2')] ], [{'product': 'product-2', 'quantity': 2.5}])
        self.assertEqual([ {'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item('product-2', option_values=['option_value-1', 'option_value-3'])] ], [{'product': 'product-2', 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.0, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.cart.add_item(product=self.product2, price=12.25, quantity=1, options={self.option1: {self.option_value4: {'price': 20.0}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=2, options={self.option1: {self.option_value1: {'price': 5.0}}, self.option2: {self.option_value3: {'price': 15.0}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=3.5, options={self.option1: {self.option_value2: {'price': 10.0}}, self.option2: {self.option_value4: {'price': 20.0}}})
        self.assertEqual(self.cart.find_item(self.product3), None)
        self.assertEqual([ {'product': item.product.name, 'quantity': item.quantity} for item in [self.cart.find_item(self.product1)] ], [{'product': 'product-1', 'quantity': 1}])
        self.assertEqual([ {'product': item.product.name, 'quantity': item.quantity} for item in [self.cart.find_item(self.product2)] ], [{'product': 'product-2', 'quantity': 2.5}])
        self.assertEqual([ {'product': item.product.name, 'quantity': item.quantity} for item in [self.cart.find_item(self.product2, option_values=[self.option_value1, self.option_value3])] ], [{'product': 'product-2', 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        return

    def test_add_multi_discount(self):
        self.assertFalse(self.cart.is_discount_applied)
        self.cart.add_discount(amount=30, type='percentage')
        self.cart.add_discount(amount=20, type='amount')
        self.assertTrue(self.cart.is_discount_applied)
        self.assertEqual([ discount for discount in self.cart.get_discounts() ], [{'amount': 30, 'type': 'percentage'}, {'amount': 20, 'type': 'amount'}])
        self.cart.remove_discounts()
        self.cart.add_discount(amount=self.discount_coupon1.discount, type=self.discount_coupon1.type)
        self.cart.add_discount(amount=self.discount_coupon2.discount, type=self.discount_coupon2.type)
        self.assertTrue(self.cart.is_discount_applied)
        self.assertEqual([ discount for discount in self.cart.get_discounts() ], [{'amount': 30, 'type': 'percentage'}, {'amount': 20, 'type': 'amount'}])

    def test_add_multi_tax(self):
        self.cart.add_item(product=1, price=10.0, quantity=1, taxes=[{'amount': 10.0, 'type': 'percentage'}, {'amount': 5.0, 'type': 'fixed'}])
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        self.assertTrue(self.cart.add_tax(20.1, type='fixed'))
        self.assertFalse(self.cart.add_tax(19.6, type='percentage'))
        self.assertEqual(self.cart.get_taxes(), [{'amount': 10.0, 'type': 'percentage'}, {'amount': 5.0, 'type': 'fixed'}, {'amount': 19.6, 'type': 'percentage'}, {'amount': 20.1, 'type': 'fixed'}])

    def test_remove_tax(self):
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        self.assertTrue(self.cart.add_tax(20.1, type='fixed'))
        self.assertFalse(self.cart.remove_tax(10))
        self.assertTrue(self.cart.remove_tax(20.1, type='fixed'))
        self.assertEqual(self.cart.get_taxes(), [{'amount': 19.6, 'type': 'percentage'}])

    def test_sub_total(self):
        self.cart.add_item(product=1, price=10.0, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual('%s %s' % (self.cart.sub_total(), self.cart.currency_symbol), '40.63 €')
        self.cart.currency_rate = 1.2714
        self.cart.price_accuracy = 2
        self.cart.currency_symbol = '$'
        self.cart.currency_code = 'USD'
        self.assertEqual('%s%s' % (self.cart.currency_symbol, self.cart.sub_total()), '$51.63')

    def test_total_discount(self):
        self.cart.add_item(product=1, price=10.0, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual('%s %s' % (self.cart.sub_total(), self.cart.currency_symbol), '40.63 €')
        self.cart.add_discount(self.discount_coupon1.discount, self.discount_coupon1.type)
        self.assertEqual('%s %s' % (self.cart.total_discount(), self.cart.currency_symbol), '12.19 €')

    def test_total_untaxed_amount(self):
        self.cart.add_item(product=1, price=10.0, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual('%s %s' % (self.cart.sub_total(), self.cart.currency_symbol), '40.63 €')
        self.cart.add_discount(self.discount_coupon1.discount, self.discount_coupon1.type)
        self.assertEqual('%s %s' % (self.cart.total_discount(), self.cart.currency_symbol), '12.19 €')
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        self.cart.tax_type = 'excluded'
        self.assertEqual('%s %s' % (self.cart.total_tax(), self.cart.currency_symbol), '5.57 €')
        self.assertEqual('%s %s' % (self.cart.total_untaxed_amount(), self.cart.currency_symbol), '28.44 €')
        self.cart.tax_type = 'included'
        self.assertEqual('%s %s' % (self.cart.total_tax(), self.cart.currency_symbol), '4.66 €')
        self.assertEqual('%s %s' % (self.cart.total_untaxed_amount(), self.cart.currency_symbol), '23.78 €')

    def test_total_tax(self):
        self.cart.add_item(product=1, price=10.0, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        self.cart.tax_type = 'excluded'
        self.assertEqual('%s %s' % (self.cart.total_tax(), self.cart.currency_symbol), '7.96 €')
        self.cart.tax_type = 'included'
        self.assertEqual('%s %s' % (self.cart.total_tax(), self.cart.currency_symbol), '6.66 €')

    def test_total_with_multi_currency(self):
        self.cart.add_item(product=1, price=10.0, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual('%s %s' % (self.cart.sub_total(), self.cart.currency_symbol), '40.63 €')
        self.cart.add_discount(self.discount_coupon1.discount, self.discount_coupon1.type)
        self.assertEqual('%s %s' % (self.cart.total_discount(), self.cart.currency_symbol), '12.19 €')
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        self.cart.tax_type = 'excluded'
        self.assertEqual('%s %s' % (self.cart.total_untaxed_amount(), self.cart.currency_symbol), '28.44 €')
        self.assertEqual('%s %s' % (self.cart.total_tax(), self.cart.currency_symbol), '5.57 €')
        self.assertEqual('%s %s' % (self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        self.assertEqual('%s %s' % (self.cart.total(), self.cart.currency_symbol), '44.22 €')
        self.cart.tax_type = 'included'
        self.assertEqual('%s %s' % (self.cart.total_untaxed_amount(), self.cart.currency_symbol), '23.78 €')
        self.assertEqual('%s %s' % (self.cart.total_tax(), self.cart.currency_symbol), '4.66 €')
        self.assertEqual('%s %s' % (self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        self.assertEqual('%s %s' % (self.cart.total(), self.cart.currency_symbol), '38.65 €')
        self.cart.currency_rate = 1.2714
        self.cart.price_accuracy = 2
        self.cart.currency_symbol = '$'
        self.cart.currency_code = 'USD'
        self.cart.tax_type = 'excluded'
        self.assertEqual('%s%s' % (self.cart.currency_symbol, self.cart.total_untaxed_amount()), '$36.14')
        self.assertEqual('%s%s' % (self.cart.currency_symbol, self.cart.total_tax()), '$7.08')
        self.assertEqual('%s%s' % (self.cart.currency_symbol, self.cart.shipping_charge), '$12.98')
        self.assertEqual('%s%s' % (self.cart.currency_symbol, self.cart.total()), '$56.2')
        self.cart.tax_type = 'included'
        self.assertEqual('%s%s' % (self.cart.currency_symbol, self.cart.total_untaxed_amount()), '$30.22')
        self.assertEqual('%s%s' % (self.cart.currency_symbol, self.cart.total_tax()), '$5.92')
        self.assertEqual('%s%s' % (self.cart.currency_symbol, self.cart.shipping_charge), '$12.98')
        self.assertEqual('%s%s' % (self.cart.currency_symbol, self.cart.total()), '$49.12')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CartTestCase))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())