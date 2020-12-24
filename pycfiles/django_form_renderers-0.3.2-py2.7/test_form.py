# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/form_renderers/tests/test_form.py
# Compiled at: 2017-05-03 06:55:45
from django.test import TestCase
from django.conf import settings
from django import forms

class MyForm(forms.Form):
    required_field = forms.CharField(required=True)
    optional_field = forms.CharField(required=False)
    colours = forms.MultipleChoiceField(choices=(
     ('blue', 'Blue'), ('red', 'Red')), widget=forms.widgets.CheckboxSelectMultiple, required=False)
    some_date = forms.DateTimeField(widget=forms.widgets.SplitDateTimeWidget, required=False)
    a_colour = forms.ChoiceField(choices=(
     ('blue', 'Blue'), ('red', 'Red')), widget=forms.widgets.RadioSelect, required=False)


class FormTestCase(TestCase):

    def test_required_attr(self):
        """Only one field gets the required attribute"""
        form = MyForm()
        li = form.as_p().split('required="required"')
        self.assertEqual(len(li), 2)

    def test_as_div(self):
        form = MyForm()
        self.failUnless('<div class=" Form-item Field' in form.as_div())

    def test_as_some_renderer(self):
        form = MyForm()
        self.failUnless('<div class="field">' in form.as_some_renderer())