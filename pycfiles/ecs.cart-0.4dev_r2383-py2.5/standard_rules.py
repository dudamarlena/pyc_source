# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ecs/cart/rules/standard_rules.py
# Compiled at: 2009-01-13 06:18:21
"""Rules modules for ecscart"""
import copy
from rules import Rules
from ecs.cart.price import Price

class FakeCart(object):
    products = {}
    cart = {}


class ObjectReduction(Rules):
    """This rule calculate reductions on products"""

    def rule(self, value, *args, **kwarg):
        for product in value.products.values():
            if 'reductions' in product:
                init_price = product['total']['included_tax']
                price = init_price
                for reduction in product['reductions']:
                    if reduction['percentage']:
                        price -= init_price * reduction['value'] / 100
                    else:
                        price -= reduction['value']

                price = Price(price, vat=product['total']['vat'])
                product['total'] = price()

        return value


class ObjectAmount(Rules):
    """This rule calculate the amount of products"""

    def rule(self, value, *args, **kwarg):
        for product in value.products.values():
            price = product['price']
            price = price['included_tax'] * product['quantity']
            price = Price(price, vat=product['price']['vat'])
            product['total'] = price()
            product['total_weight'] = product['weight'] * product['quantity']

        return value


class CartAmount(Rules):
    """This rule calculate the cart amount"""

    def rule(self, value, *args, **kwarg):
        amount = 0
        weight = 0
        amount_by_vat = {}
        quantity_total = 0
        for product in value.products.values():
            price = product['total']
            quantity_total += product['quantity']
            amount += price['included_tax']
            weight += product['total_weight']
            vat = price['vat']
            if vat not in amount_by_vat:
                amount_by_vat[vat] = price['included_tax']
            else:
                amount_by_vat[vat] += price['included_tax']

        cart = value.cart
        cart['amount'] = amount
        cart['weight'] = weight
        cart['price_by_vat'] = {}
        cart['quantity_total'] = int(quantity_total)
        for (vat, amount) in amount_by_vat.items():
            price = Price(amount, vat=vat)
            cart['price_by_vat'][vat] = price()

        return value


class CartReduction(Rules):
    """This rule calculate reductions on cart"""

    def rule(self, value, *args, **kwarg):
        if 'reductions' in value.cart:
            total_reduction = 0
            amount = value.cart['amount']
            for reduction in value.cart['reductions']:
                if reduction['percentage']:
                    total_reduction += amount * reduction['value'] / 100
                else:
                    total_reduction += reduction['value']

            products = copy.deepcopy(value.products)
            sum = 0
            amounts = {}
            for (ref, values) in products.items():
                total = values['total']
                vat = total['vat']
                if vat == 0:
                    vat = 1
                amount = total['included_tax'] * vat
                amounts[ref] = amount
                sum += amount

            for (ref, amount) in amounts.items():
                reduction = amount / sum * total_reduction
                product = products[ref]
                old_price = product['total']['included_tax']
                vat = product['total']['vat']
                product['total'] = Price(old_price - reduction, vat=vat)()

            fake_cart = FakeCart()
            fake_cart.products = products
            process = CartAmount()
            fake_cart = process(fake_cart)
            fake_cart.cart['reductions'] = value.cart['reductions']
            value.cart = fake_cart.cart
        return value