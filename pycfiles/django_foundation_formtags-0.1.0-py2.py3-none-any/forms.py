# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cclarke/Dropbox/Development/django-foundation-formtags/foundation_formtags/tests/forms.py
# Compiled at: 2016-08-05 12:38:37
from django import forms
CHOICES = (
 ('a', 'Option 1'),
 ('b', 'Option 2'),
 ('c', 'Option 3'))

class SimpleForm(forms.Form):
    text = forms.CharField(label='text')


class ComplexForm(forms.Form):
    char_field = forms.CharField()
    char_field_widget = forms.CharField(widget=forms.TextInput(attrs={'class': 'foo'}))
    choice_field = forms.ChoiceField(choices=CHOICES)
    radio_choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    multiple_choice = forms.MultipleChoiceField(choices=CHOICES)
    multiple_checkbox = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple)
    file_field = forms.FileField()
    password_field = forms.CharField(widget=forms.PasswordInput)
    textarea = forms.CharField(widget=forms.Textarea)
    boolean_field = forms.BooleanField()