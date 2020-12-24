# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/context_processors.py
# Compiled at: 2014-10-16 04:19:59
from __future__ import unicode_literals
from django_easy_currencies.models.CurrencyRate import CurrencyRate

def currency(request):
    """
    Add active_currency and currency_rates rates into context_data.

    :param request:
    :return: :rtype:
    """
    cur = request.session.get(b'currency', b'USD')
    rates = CurrencyRate.objects.get_rate_values(cur)
    return {b'active_currency': cur, 
       b'currency_rates': rates}