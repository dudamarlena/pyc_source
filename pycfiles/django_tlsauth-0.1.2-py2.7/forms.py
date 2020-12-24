# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_tlsauth/forms.py
# Compiled at: 2013-03-24 20:34:55
from django import forms

class UserForm(forms.Form):
    """ (FLASK) simple registration WTForm
    """
    name = forms.CharField()
    email = forms.CharField()
    org = forms.CharField()


class CSRForm(forms.Form):
    """ (FLASK) even simpler CSR submission WTForm
    """
    csr = forms.CharField(widget=forms.Textarea)