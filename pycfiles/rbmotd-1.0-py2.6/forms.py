# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/rbmotd/forms.py
# Compiled at: 2014-06-24 00:16:14
import hashlib
from django import forms
from django.utils.translation import ugettext as _
from djblets.extensions.forms import SettingsForm

class MotdSettingsForm(SettingsForm):
    enabled = forms.BooleanField(initial=False, required=False)
    message = forms.CharField(max_length=512, required=False, help_text=_('This field expects valid HTML. Entities must be properly escaped.'), widget=forms.TextInput(attrs={'size': 100}))

    def save(self):
        if not self.errors:
            self.siteconfig.set('message_id', hashlib.sha256(self.cleaned_data['message']).hexdigest())
        super(MotdSettingsForm, self).save()