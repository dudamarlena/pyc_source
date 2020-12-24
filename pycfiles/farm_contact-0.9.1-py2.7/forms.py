# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contact/forms.py
# Compiled at: 2014-03-26 08:39:13
from .models import Enquiry, EnquiryType
from django import forms
from django.forms import ModelForm

class EnquiryForm(ModelForm):
    name = forms.CharField(label='Your Name', widget=forms.TextInput(attrs={'required': ''}))
    email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={'required': ''}))
    phone = forms.CharField(label='Phone Number')
    enquiry_type = forms.ModelChoiceField(queryset=EnquiryType.objects.all(), label='I am a', widget=forms.Select(attrs={'required': ''}))
    message = forms.CharField(label='How can we help you?', widget=forms.Textarea(attrs={'required': ''}))

    class Meta:
        model = Enquiry
        exclude = ['ip']

    def save(self, commit=True, ip=None):
        instance = super(ModelForm, self).save(False)
        instance.ip = ip
        if commit:
            instance.save()
        return instance