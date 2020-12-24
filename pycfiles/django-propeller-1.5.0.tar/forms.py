# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller_demo/forms.py
# Compiled at: 2017-02-20 15:19:53
from __future__ import unicode_literals
from django import forms
from django.forms.formsets import BaseFormSet, formset_factory
from django_propeller.tests import TestForm
RADIO_CHOICES = (
 ('1', 'Radio 1'),
 ('2', 'Radio 2'))
MEDIA_CHOICES = (
 (
  b'Audio',
  (
   ('vinyl', 'Vinyl'),
   ('cd', 'CD'))),
 (
  b'Video',
  (
   ('vhs', 'VHS Tape'),
   ('dvd', 'DVD'))),
 ('unknown', 'Unknown'))

class ContactForm(TestForm):
    pass


class ContactBaseFormSet(BaseFormSet):

    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        raise forms.ValidationError(b'This error was added to show the non form errors styling')


ContactFormSet = formset_factory(TestForm, formset=ContactBaseFormSet, extra=2, max_num=4, validate_max=True)

class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file5 = forms.ImageField()
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError(b'This error was added to show the non field errors styling.')
        return cleaned_data