# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/tests/TestCurrenciesTemplateTags.py
# Compiled at: 2014-10-22 10:08:59
from __future__ import unicode_literals
from decimal import Decimal
from django.test.testcases import TestCase
from django.template import Template, Context

class TestCurrenciesTemplateTags(TestCase):

    def test_local_currency_converts_original_price(self):
        template = Template(b'{% load currencies %}{% local_currency original_price original_currency False %}')
        price = Decimal(b'59.90')
        rate = Decimal(b'1.277421448')
        context = Context({b'original_price': price, 
           b'original_currency': b'USD', 
           b'active_currency': b'EUR', 
           b'currency_rates': {b'USD': rate}})
        output = template.render(context).strip()
        self.assertEqual(output, str(price / rate))
        self.assertTrue(Decimal(output) < price)

    def test_local_currency_formats_currency_with_expected_symbol(self):
        template = Template(b'{% load currencies %}{% local_currency original_price original_currency %}')
        context = Context({b'original_price': Decimal(b'59.90'), 
           b'original_currency': b'USD', 
           b'active_currency': b'EUR', 
           b'currency_rates': {b'USD': Decimal(b'1.277421448')}})
        output = template.render(context).strip()
        self.assertTrue(output.startswith(b'€'))