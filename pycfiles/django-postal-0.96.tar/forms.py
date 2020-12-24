# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mick/src/django-postal/src/postal/forms/us/forms.py
# Compiled at: 2014-06-03 13:43:38
""" http://www.bitboost.com/ref/international-address-formats.html """
from django import forms
from django.utils.translation import ugettext_lazy as _
from localflavor.us.forms import USStateField, USStateSelect, USZipCodeField
from postal.forms import PostalAddressForm

class USPostalAddressForm(PostalAddressForm):
    line1 = forms.CharField(label=_('Street'), max_length=50)
    line2 = forms.CharField(label=_('Area'), required=False, max_length=100)
    city = forms.CharField(label=_('City'), max_length=50)
    state = USStateField(label=_('US State'), widget=USStateSelect)
    code = USZipCodeField(label=_('Zip Code'))

    def __init__(self, *args, **kwargs):
        super(USPostalAddressForm, self).__init__(*args, **kwargs)
        self.fields['country'].initial = 'US'