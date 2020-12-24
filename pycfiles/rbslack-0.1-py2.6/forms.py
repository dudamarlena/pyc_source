# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/rbslack/forms.py
# Compiled at: 2016-03-05 05:42:36
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.forms import SettingsForm

class SlackSettingsForm(SettingsForm):
    webhook_url = forms.URLField(label=_(b'Webhook URL'), help_text=_(b'Your unique Slack webhook URL. This can be found in the "Setup Instructions" box inside the Incoming WebHooks integration.'), widget=forms.TextInput(attrs={b'size': 110}))
    channel = forms.CharField(label=_(b'Send to Channel'), required=False, help_text=_(b'The optional name of the channel review request updates are sent to. By default, the configured channel on the Incoming Webhook will be used.'), widget=forms.TextInput(attrs={b'size': 40}))

    class Meta:
        fieldsets = (
         {b'description': _(b'To start, add a new "Incoming WebHooks" service integration on Slack. You can then provide the "Unique WebHook URL" below, and optionally choose a custom channel to send notifications to.'), 
            b'fields': ('webhook_url', 'channel'), 
            b'classes': ('wide', )},)