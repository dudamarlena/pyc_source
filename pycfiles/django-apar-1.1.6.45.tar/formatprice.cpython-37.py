# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/utils/formattings/formatprice.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 3333 bytes
from aparnik.settings import Setting
from . import humanize
from .num2words import num2word_FA

def format_price(price, price_format=None):
    formatted_price = ''
    price_value = price
    input_currency = {'%ic=r':'r',  '%ic=t':'t'}
    currency = {'%cu=r':'ریال',  '%cu=t':'تومان',  '%cu=':''}
    seperator = {'%se=,':',',  '%se=/':'/',  '%se=':''}
    grouping = {'%gr=3':3,  '%gr=0':0}
    precision = {'%pr=1':1,  '%pr=2':2,  '%pr=3':3}
    translate = {'%tr=True':True,  '%tr=False':False}
    abbriviation = {'%abbr=True':True,  '%abbr=False':False}
    translate_str = {'%StrTr=True':True,  '%StrTr=False':False}
    if not price_format:
        try:
            price_format = Setting.objects.get(key='PRICE_FORMAT').get_value()
        except:
            price_format = str('%ic=t:%se=,:%cu=t:%gr=3:%tr=True:%abbr=True')

    price_format = list((str(x) for x in price_format.split(':') if x))
    if get_parameter('%ic', price_format):
        if input_currency[get_parameter('%ic=', price_format)] == 'r':
            if get_parameter('%cu=', price_format) == '%cu=t':
                price_value = price / 10
    if get_parameter('%cu', price_format):
        if get_parameter('%ic=', price_format) == '%ic=t':
            if get_parameter('%cu=', price_format) == '%cu=r':
                price_value = price * 10
        currency = currency[get_parameter('%cu=', price_format)]
    if get_parameter('%tr', price_format):
        if translate[get_parameter('%tr', price_format)]:
            if price_value >= 1000:
                formatted_price = num2word_FA.to_card(price_value)
                price = ''
    if get_parameter('%StrTr', price_format):
        if translate_str[get_parameter('%StrTr', price_format)]:
            formatted_price = num2word_FA.to_card_str(price_value)
            price = ''
    if get_parameter('%abbr', price_format):
        if abbriviation[get_parameter('%abbr=', price_format)]:
            humanize.i18n.activate('fa_FA')
            formatted_price = str(humanize.intword(price_value, '%.3f'))
            price = ''
    if get_parameter('%gr', price_format):
        if get_parameter('%se', price_format):
            seperator = seperator[get_parameter('%se=', price_format)]
            humanize.i18n.activate('fa_FA')
            formatted_price = humanize.intcomma(price_value, seperator)
            price = ''
    if get_parameter('%price_str_abbriviation', price_format):
        formatted_price = num2word_FA.to_ord(price_value)
    return formatted_price + str(price) + ' ' + currency


def get_parameter(parameter, price_format):
    for word in price_format:
        if parameter in word:
            return word

    return False