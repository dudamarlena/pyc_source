# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/forms.py
# Compiled at: 2020-05-04 20:04:36
# Size of source mod 2**32: 1758 bytes
from django import forms
from .choices import COINS

class BaseCallbackForm(forms.Form):
    request_id = forms.IntegerField()
    nonce = forms.CharField(max_length=32)
    address_in = forms.CharField(max_length=128)
    address_out = forms.CharField(max_length=128)
    coin = forms.ChoiceField(choices=COINS)
    txid_in = forms.CharField(max_length=256)
    confirmations = forms.IntegerField()
    value = forms.DecimalField(max_digits=65, decimal_places=0)


class CallbackForm(BaseCallbackForm):
    txid_out = forms.CharField(max_length=256)
    value_forwarded = forms.DecimalField(max_digits=65, decimal_places=0)


class AddressCreatedForm(forms.Form):
    address_in = forms.CharField(max_length=128)
    address_out = forms.CharField(max_length=128)
    callback_url = forms.CharField(max_length=8192)
    status = forms.CharField(max_length=16)

    def __init__(self, initials, *args, **kwargs):
        (super(AddressCreatedForm, self).__init__)(*args, **kwargs)
        self.initials = initials

    def clean_address_out(self):
        if self.cleaned_data['address_out'] != self.initials['address_out']:
            raise forms.ValidationError('Address out mismatch')
        return self.cleaned_data['address_out']

    def clean_callback_url(self):
        if self.cleaned_data['callback_url'] != self.initials['callback_url']:
            raise forms.ValidationError('Callback URL mismatch')
        return self.cleaned_data['callback_url']

    def clean_status(self):
        if self.cleaned_data['status'] != 'success':
            raise forms.ValidationError('Status error')
        return self.cleaned_data['status']