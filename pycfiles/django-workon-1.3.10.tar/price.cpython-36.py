# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/utils/price.py
# Compiled at: 2018-08-30 03:50:35
# Size of source mod 2**32: 1485 bytes
import locale
__all__ = [
 'currency']
DEFAULT_CURRENCY = 'EUR'
CURRENCY_PATTERNS = {'EUR':{'format':'%s €', 
  'locale':'fr_FR',  'spacing':' ',  'decimal':',',  'placeholder':'EUR'}, 
 'USD':{'format':'$%s', 
  'locale':'en_US',  'spacing':',',  'decimal':'.',  'placeholder':'USD'}}

def currency(value, strip_zero=True, currency='EUR'):
    try:
        price = locale.currency((float(value)), grouping=True)
        if strip_zero:
            price = price
    except ValueError:
        price = price_format_decimal_to_currency(value, currency)

    return price


def price_format_decimal_to_currency(value, currency='EUR'):
    if value:
        try:
            if currency in CURRENCY_PATTERNS.keys():
                value = CURRENCY_PATTERNS[currency]['format'] % str(value).rstrip('.0').rstrip('.00')
            else:
                return value
        except:
            return value

    return value


def price_format_currency_to_decimal(value, currency='EUR'):
    if value == None:
        return
    value = unicode(value)
    if value.strip() == '':
        return
    float_value = ''
    float_lock = False
    for c in value[::-1]:
        if c.isdigit():
            float_value += c
        if not float_lock and (c == '.' or c == ','):
            float_value += '.'
            float_lock = True

    try:
        return float(float_value[::-1])
    except:
        return


def price(value, currency='EUR'):
    return price