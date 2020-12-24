# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/forms.py
# Compiled at: 2019-02-19 21:49:51
# Size of source mod 2**32: 1339 bytes
"""
Free as freedom will be 2/9/2016

@author: luisza
"""
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Product, Reservation

class ReservationForm(forms.ModelForm):

    def clean(self):
        if hasattr(self, 'request'):
            if hasattr(self.request, 'reservation'):
                raise forms.ValidationError(_('You can not create reservation with active reservation'))
            cleaned_data = super(ReservationForm, self).clean()

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['user', 'status']


class ProductForm(forms.ModelForm):
    model_instance = forms.CharField(widget=forms.HiddenInput)
    available_amount = forms.FloatField(widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        if cleaned_data['amount'] <= 0:
            raise forms.ValidationError(_('You amount correct, requested 0 or negative value'))
        if cleaned_data['amount'] > cleaned_data['available_amount']:
            raise forms.ValidationError(_('You requested more than product available'))

    class Meta:
        model = Product
        fields = ['amount']