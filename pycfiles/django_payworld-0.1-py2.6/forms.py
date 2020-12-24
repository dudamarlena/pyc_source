# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/django_payworld/forms.py
# Compiled at: 2012-02-15 01:02:17
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class PaymentForm(forms.Form):
    order_id = forms.CharField(widget=forms.HiddenInput())
    order_total = forms.DecimalField(widget=forms.HiddenInput())
    order_details = forms.CharField(widget=forms.HiddenInput())
    seller_name = forms.CharField(widget=forms.HiddenInput())
    shop_id = forms.CharField(widget=forms.HiddenInput())