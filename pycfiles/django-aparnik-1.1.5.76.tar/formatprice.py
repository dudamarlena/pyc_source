# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/utils/formattings/formatprice.py
# Compiled at: 2019-02-15 10:47:13
from __future__ import unicode_literals
from aparnik.settings import Setting
import humanize
from num2words import num2word_FA

def format_price(price, price_format=None):
    formatted_price = b''
    price_value = price
    input_currency = {b'%ic=r': b'r', b'%ic=t': b't'}
    currency = {b'%cu=r': b'ریال', b'%cu=t': b'تومان', b'%cu=': b''}
    seperator = {b'%se=,': b',', b'%se=/': b'/', b'%se=': b''}
    grouping = {b'%gr=3': 3, b'%gr=0': 0}
    precision = {b'%pr=1': 1, b'%pr=2': 2, b'%pr=3': 3}
    translate = {b'%tr=True': True, b'%tr=False': False}
    abbriviation = {b'%abbr=True': True, b'%abbr=False': False}
    translate_str = {b'%StrTr=True': True, b'%StrTr=False': False}
    if not price_format:
        try:
            price_format = Setting.objects.get(key=b'PRICE_FORMAT').get_value()
        except:
            price_format = str(b'%ic=t:%se=,:%cu=t:%gr=3:%tr=True:%abbr=True')

    price_format = list(str(x) for x in price_format.split(b':') if x)
    if get_parameter(b'%ic', price_format):
        if input_currency[get_parameter(b'%ic=', price_format)] == b'r' and get_parameter(b'%cu=', price_format) == b'%cu=t':
            price_value = price / 10
    if get_parameter(b'%cu', price_format):
        if get_parameter(b'%ic=', price_format) == b'%ic=t' and get_parameter(b'%cu=', price_format) == b'%cu=r':
            price_value = price * 10
        currency = currency[get_parameter(b'%cu=', price_format)]
    if get_parameter(b'%tr', price_format):
        if translate[get_parameter(b'%tr', price_format)]:
            if price_value >= 1000:
                formatted_price = num2word_FA.to_card(price_value)
                price = b''
    if get_parameter(b'%StrTr', price_format):
        if translate_str[get_parameter(b'%StrTr', price_format)]:
            formatted_price = num2word_FA.to_card_str(price_value)
            price = b''
    if get_parameter(b'%abbr', price_format):
        if abbriviation[get_parameter(b'%abbr=', price_format)]:
            humanize.i18n.activate(b'fa_FA')
            formatted_price = str(humanize.intword(price_value, b'%.3f'))
            price = b''
    if get_parameter(b'%gr', price_format):
        if get_parameter(b'%se', price_format):
            seperator = seperator[get_parameter(b'%se=', price_format)]
            humanize.i18n.activate(b'fa_FA')
            formatted_price = humanize.intcomma(price_value, seperator)
            price = b''
    if get_parameter(b'%price_str_abbriviation', price_format):
        formatted_price = num2word_FA.to_ord(price_value)
    return formatted_price.decode(b'utf8') + str(price) + b' ' + currency


def get_parameter(parameter, price_format):
    for word in price_format:
        if parameter in word:
            return word

    return False