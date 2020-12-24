# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/html/blockreferralspam/blockreferralspam/example/blockreferralspam/tests.py
# Compiled at: 2015-07-13 05:17:57
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

class BlockreferralspamTestCase(TestCase):

    def test_get_200(self):
        c = Client()
        index_url = reverse('index')
        index_res = c.get(index_url)
        self.assertEqual(index_res.status_code, 200)

    def test_get_404(self):
        c = Client(HTTP_REFERER='site5.floating-share-buttons.com')
        index_url = reverse('index')
        index_res = c.get(index_url)
        self.assertEqual(index_res.status_code, 404)
        c = Client(HTTP_REFERER='floating-share-buttons.com')
        index_url = reverse('index')
        index_res = c.get(index_url)
        self.assertEqual(index_res.status_code, 404)