# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-trello-webhooks/lib/python2.7/site-packages/trello_webhooks/tests/test_admin.py
# Compiled at: 2014-11-29 11:06:11
from django.test import TestCase
from trello_webhooks.admin import CallbackEventAdmin
from trello_webhooks.models import Webhook, CallbackEvent

class CallbackEventAdminTests(TestCase):

    def setUp(self):
        self.webhook = Webhook(auth_token='ABC').save(sync=False)
        self.event = CallbackEvent(webhook=self.webhook, event_type='commentCard').save()
        self.admin = CallbackEventAdmin(CallbackEvent, None)
        return

    def test_webhook_(self):
        self.assertEqual(self.admin.webhook_(self.event), self.webhook.id)

    def test_has_template(self):
        self.assertTrue(self.admin.has_template(self.event))
        self.event.event_type = 'X'
        self.assertFalse(self.admin.has_template(self.event))

    def test_rendered(self):
        self.assertIsNotNone(self.admin.rendered(self.event))
        self.event.event_type = 'X'
        self.assertIsNone(self.admin.rendered(self.event))