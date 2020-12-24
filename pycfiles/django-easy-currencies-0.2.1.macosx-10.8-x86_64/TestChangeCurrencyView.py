# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/tests/TestChangeCurrencyView.py
# Compiled at: 2014-10-22 10:19:37
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseNotAllowed
from django.test.testcases import TestCase

class TestChangeCurrencyView(TestCase):

    def setUp(self):
        self.url = reverse(b'change_currency')

    def test_get_is_not_allowed(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response, HttpResponseNotAllowed)

    def test_view_set_received_currency_in_session(self):
        self.assertIsNone(self.client.session.get(b'currency'))
        self.client.post(self.url, {b'currency': b'EUR'})
        self.assertEqual(self.client.session.get(b'currency'), b'EUR')

    def test_view_set_usd_as_default_currency_if_currency_was_not_defined(self):
        self.assertIsNone(self.client.session.get(b'currency'))
        self.client.post(self.url, {})
        self.assertEqual(self.client.session.get(b'currency'), b'USD')