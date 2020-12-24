# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/voucherify/utils.py
# Compiled at: 2019-06-13 11:03:47
from __future__ import division

def round_money(value):
    if value is None or value < 0:
        raise Exception('Invalid value, amount should be a number and higher than zero.')
    return round(value, 2)


def validate_percent_discount(discount):
    if discount is None or discount < 0 or discount > 100:
        raise Exception('Invalid voucher, percent discount should be between 0-100.')
    return


def validate_amount_discount(discount=None):
    if discount is None or discount < 0:
        raise Exception('Invalid voucher, amount discount must be higher than zero.')
    return


def validate_unit_discount(discount=None):
    if discount is None or discount < 0:
        raise Exception('Invalid voucher, unit discount must be higher than zero.')
    return


def calculate_price(base_price, voucher, unit_price):
    e = 100
    if getattr(voucher, 'gift', None) is not None:
        discount = min(voucher['gift']['balance'] / e, base_price)
        return round_money(base_price - discount)
    else:
        if 'discount' not in voucher:
            raise Exception('Unsupported voucher type.')
        if voucher['discount']['type'] == 'PERCENT':
            discount = voucher['discount']['percent_off']
            validate_percent_discount(discount)
            price_discount = base_price * (discount / 100)
            return round_money(base_price - price_discount)
        if voucher['discount']['type'] == 'AMOUNT':
            discount = voucher['discount']['amount_off'] / e
            validate_amount_discount(discount)
            new_price = base_price - discount
            return round_money(new_price if new_price > 0 else 0)
        if voucher['discount']['type'] == 'UNIT':
            discount = voucher['discount']['unit_off']
            validate_unit_discount(discount)
            new_price = base_price - unit_price * discount
            return round_money(new_price if new_price > 0 else 0)
        raise Exception('Unsupported discount type.')
        return


def calculate_discount(base_price, voucher, unit_price):
    e = 100
    if getattr(voucher, 'gift', None) is not None:
        discount = min(voucher['gift']['balance'] / e, base_price)
        return round_money(discount)
    else:
        if 'discount' not in voucher:
            raise Exception('Unsupported voucher type.')
        if voucher['discount']['type'] == 'PERCENT':
            discount = voucher['discount']['percent_off']
            validate_percent_discount(discount)
            return round_money(base_price * (discount / 100))
        if voucher['discount']['type'] == 'AMOUNT':
            discount = voucher['discount']['amount_off'] / e
            validate_amount_discount(discount)
            new_price = base_price - discount
            return round_money(discount if new_price > 0 else base_price)
        if voucher['discount']['type'] == 'UNIT':
            discount = voucher['discount']['unit_off']
            validate_unit_discount(discount)
            price_discount = unit_price * discount
            return round_money(base_price if price_discount > base_price else price_discount)
        raise Exception('Unsupported discount type.')
        return


__all__ = ['calculate_price', 'calculate_discount']