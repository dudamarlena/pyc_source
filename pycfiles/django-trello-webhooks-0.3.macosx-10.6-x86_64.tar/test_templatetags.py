# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-trello-webhooks/lib/python2.7/site-packages/trello_webhooks/tests/test_templatetags.py
# Compiled at: 2014-12-02 03:21:47
from django.test import TestCase
from trello_webhooks.settings import TRELLO_API_KEY
from trello_webhooks.templatetags.trello_webhook_tags import trello_api_key, trello_updates

class TemplateTagTests(TestCase):

    def test_trello_api_key(self):
        self.assertEqual(trello_api_key(), TRELLO_API_KEY)

    def test_trello_updates(self):
        old = {'pos': 1}
        new = {'pos': 2, 'abc': 'xyz'}
        self.assertEqual(trello_updates(new, old), {'pos': (1, 2)})
        new = {}
        self.assertEqual(trello_updates(new, old), {'pos': (1, None)})
        return