# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-trello-webhooks/lib/python2.7/site-packages/trello_webhooks/tests/test_views.py
# Compiled at: 2014-11-29 11:06:24
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from trello_webhooks.models import Webhook, CallbackEvent
from trello_webhooks.tests import get_sample_data

class WebhookViewTests(TestCase):

    def setUp(self):
        self.payload = {'auth_token': 'A', 'trello_model_id': '123'}
        self.url = reverse('trello_callback_url', kwargs=self.payload)

    def test_head(self):
        resp = self.client.head(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_post_404(self):
        resp = self.client.post(self.url, data={})
        self.assertEqual(resp.status_code, 404)

    def test_post_200(self):
        Webhook(auth_token=self.payload['auth_token'], trello_model_id=self.payload['trello_model_id']).save(sync=False)
        self.assertEqual(CallbackEvent.objects.count(), 0)
        test_payload = get_sample_data('commentCard', 'json')
        resp = self.client.post(self.url, data=json.dumps(test_payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(CallbackEvent.objects.count(), 1)
        self.assertEqual(CallbackEvent.objects.get().event_payload, test_payload)

    def test_get_405(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 405)