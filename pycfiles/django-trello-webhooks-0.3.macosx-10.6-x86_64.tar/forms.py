# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-trello-webhooks/lib/python2.7/site-packages/trello_webhooks/forms.py
# Compiled at: 2014-12-02 06:44:54
from django import forms
from django.utils.safestring import mark_safe
from trello_webhooks.models import Webhook

class TrelloTokenWidget(forms.TextInput):

    def __init__(self, *args, **kwargs):
        super(TrelloTokenWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        attrs['size'] = 85
        html = super(TrelloTokenWidget, self).render(name, value, attrs=attrs)
        html += "&nbsp;<a onclick='getTrelloToken()' href='#'>Get new token</a>"
        return mark_safe(html)


class WebhookForm(forms.ModelForm):

    class Meta:
        model = Webhook
        exclude = []

    auth_token = forms.CharField(widget=TrelloTokenWidget())