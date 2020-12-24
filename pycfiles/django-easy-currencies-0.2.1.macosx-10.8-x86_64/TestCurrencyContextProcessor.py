# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/tests/TestCurrencyContextProcessor.py
# Compiled at: 2014-10-22 10:26:03
from __future__ import unicode_literals
from django.test.testcases import TestCase

class TestCurrencyContextProcessor(TestCase):

    def test_processor_sets_expected_variables_in_context(self):
        response = self.client.get(b'/')
        self.assertEqual(response.context[b'active_currency'], b'USD')
        self.assertIsInstance(response.context[b'currency_rates'], dict)