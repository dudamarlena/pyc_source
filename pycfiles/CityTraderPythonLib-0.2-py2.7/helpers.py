# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/citytrader/helpers.py
# Compiled at: 2015-09-24 12:18:39
"""
functions that could be useful in many places
"""
import math

def price_to_decimal(price, display_factor, base_factor):
    if not price or not display_factor or not base_factor or not price or not display_factor or not base_factor or price == '' or display_factor == '' or base_factor == '':
        return None
    if len(str(display_factor).replace('.', '')) > 15:
        display_factor = round(display_factor, 15)
    if len(str(base_factor).replace('.', '')) > 15:
        base_factor = round(base_factor, 15)
    if len(str(price).replace('.', '')) > 15:
        price = round(price, 15)
    price = price * display_factor
    if price > 0:
        whole_decimal = math.floor(price)
    else:
        whole_decimal = math.ceil(price)
    fraction = price - whole_decimal
    converted_fraction = fraction * base_factor
    return str(converted_fraction + whole_decimal)