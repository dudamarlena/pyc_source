# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-paymecash/paymecash/forms.py
# Compiled at: 2013-09-17 02:54:16
import conf
from django import forms
from .common import get_sign
from .models import Payment

class PayForm(forms.ModelForm):
    FIELDS_FOR_SIGN = ('wallet_id', 'product_price', 'product_currency', 'order_id')
    sign = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(PayForm, self).__init__(*args, **kwargs)
        data = {'wallet_id': self.fields['wallet_id'].initial, 
           'product_price': self.fields['product_price'].initial, 
           'product_currency': self.fields['product_currency'].initial, 
           'order_id': self.fields['order_id'].initial}
        data.update(self.initial)
        self.fields['sign'].initial = get_sign(data)
        if conf.PAYMECASH_HIDE_FORM:
            for name in self.fields:
                self.fields[name].widget = forms.HiddenInput()

        else:
            self.fields['wallet_id'].widget.attrs['readonly'] = True
            self.fields['product_price'].widget.attrs['readonly'] = True
            self.fields['order_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Payment
        fields = ('wallet_id', 'order_id', 'product_price', 'product_currency', 'cs1',
                  'cs2', 'cs3', 'payment_type_group_id')