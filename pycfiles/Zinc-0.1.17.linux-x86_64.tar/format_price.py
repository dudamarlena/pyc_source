# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/zinc/format_price.py
# Compiled at: 2014-01-22 02:54:05


def format_price(price):
    price = str(price)
    is_negative = False
    if len(price) > 0 and price[0] == '-':
        is_negative = True
        price = price[1:]
    if len(price) > 2:
        result = '$' + price[:-2] + '.' + price[-2:]
    elif len(price) == 2:
        result = '$0.' + price
    else:
        result = '$0.0' + price
    if is_negative:
        return '-' + result
    else:
        return result