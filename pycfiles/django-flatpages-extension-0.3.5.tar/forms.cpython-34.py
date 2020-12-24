# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django-flatpages-extension/django-flatpages-extension/forms.py
# Compiled at: 2018-07-10 12:52:03
# Size of source mod 2**32: 439 bytes
from django import forms
from django.contrib.flatpages.forms import FlatpageForm
from .models import FlatPageExtended
TextField = forms.fields.TextInput
try:
    from ckeditor.fields import RichTextFormField
    TextField = RichTextFormField
except ImportError:
    pass

class FlatpageExtendedForm(FlatpageForm, forms.ModelForm):
    content = TextField()

    class Meta:
        model = FlatPageExtended
        fields = '__all__'