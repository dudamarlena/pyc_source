# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.webhooks/unicore/webhooks/events.py
# Compiled at: 2016-06-21 11:57:16
import requests, json
from pyramid.events import subscriber
from unicore.webhooks.models import DBSession, Webhook

class WebhookOperation(object):

    def __init__(self, webhook, request):
        self.webhook = webhook
        self.request = request


class WebhookCreated(WebhookOperation):
    pass


class WebhookUpdated(WebhookOperation):
    pass


class WebhookDeleted(WebhookOperation):
    pass


class WebhookEvent(object):

    def __init__(self, owner, event_type, payload):
        self.owner = owner
        self.event_type = event_type
        self.payload = payload


@subscriber(WebhookEvent)
def fire_event(event):
    webhooks = DBSession.query(Webhook).filter(Webhook.owner == event.owner, Webhook.event_type == event.event_type)
    for webhook in webhooks:
        requests.post(webhook.url, data=json.dumps({'event_type': event.event_type, 
           'payload': event.payload}))