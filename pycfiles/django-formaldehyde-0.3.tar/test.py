# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kraken/Projects/websites/django-formaldehyde/formaldehyde/formaldehyde/tests/test.py
# Compiled at: 2015-01-30 09:32:54
from __future__ import unicode_literals
import django
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils import six
from formaldehyde.conf import settings
from formaldehyde.fieldsets import FieldsetFormMixin
from formaldehyde.readonly import ReadonlyFormMixin
from formaldehyde.whitespace import StripWhitespaceFormMixin

class TestFieldsetForm(FieldsetFormMixin, forms.Form):
    first_name = forms.CharField(label=b'First name', max_length=100)
    middle_name = forms.CharField(label=b'Middle name', max_length=100)
    last_name = forms.CharField(label=b'Last name', max_length=100)
    street = forms.CharField(label=b'Street name', max_length=100)

    class MetaForm:
        fieldsets = (
         (
          None,
          {b'fields': (('first_name', 'middle_name'), 'last_name'), 
             b'layout': ((4, 6), 2), 
             b'classes': b'form-control'}),
         (
          b'Address',
          {b'fields': ('street', )}))


class TestFieldsetModelForm(FieldsetFormMixin, forms.ModelForm):

    class Meta:
        model = ContentType
        fields = b'__all__'


class TestFieldsetFormRaises(FieldsetFormMixin):
    pass


class TestReadonlyForm(ReadonlyFormMixin, forms.Form):
    first_name = forms.CharField(label=b'First name', max_length=100)


class TestReadonlyModelForm(ReadonlyFormMixin, forms.ModelForm):

    class Meta:
        model = ContentType
        fields = b'__all__'


class TestWhitespaceForm(StripWhitespaceFormMixin, forms.Form):
    first_name = forms.CharField(label=b'First name', max_length=100)
    last_name = forms.CharField(label=b'Last name', max_length=100)

    def full_clean(self):
        self.strip_whitespace_from_data()
        super(TestWhitespaceForm, self).full_clean()


class TestWhitespaceModelForm(StripWhitespaceFormMixin, forms.ModelForm):

    class Meta:
        model = ContentType
        fields = b'__all__'

    def full_clean(self):
        self.strip_whitespace_from_data()
        super(TestWhitespaceModelForm, self).full_clean()


class FormalehydeTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        pass

    def test_fieldset_form(self):
        form = TestFieldsetForm()
        fieldsets = form.fieldsets()
        self.assertIsNotNone(fieldsets)
        fieldset01 = six.next(fieldsets)
        self.assertIsNone(fieldset01.legend)
        self.assertEqual(fieldset01.description, b'')
        self.assertEqual(fieldset01.classes, b'form-control')
        fieldset01_line01 = six.next(fieldset01)
        fieldset01_line01_field01, fieldset01_line01_layout01 = six.next(fieldset01_line01)
        self.assertEqual(b'first_name', fieldset01_line01_field01.name)
        self.assertEqual(4, fieldset01_line01_layout01)
        fieldset01_line01_field02, fieldset01_line01_layout02 = six.next(fieldset01_line01)
        self.assertEqual(b'middle_name', fieldset01_line01_field02.name)
        self.assertEqual(6, fieldset01_line01_layout02)
        fieldset01_line02 = six.next(fieldset01)
        fieldset01_line02_field01, fieldset01_line02_layout01 = six.next(fieldset01_line02)
        self.assertEqual(b'last_name', fieldset01_line02_field01.name)
        self.assertEqual(2, fieldset01_line02_layout01)
        fieldset02 = six.next(fieldsets)
        self.assertEqual(fieldset02.legend, b'Address')
        self.assertEqual(fieldset02.description, b'')
        self.assertEqual(fieldset02.classes, b'')
        fieldset02_line01 = six.next(fieldset02)
        fieldset02_line01_field01, fieldset02_line01_layout01 = six.next(fieldset02_line01)
        self.assertEqual(b'street', fieldset02_line01_field01.name)
        self.assertEqual(fieldset02_line01.layout_cols, fieldset02_line01_layout01)

    def test_fieldset_model_form(self):
        form = TestFieldsetModelForm()
        if form.fieldsets:
            fieldsets = form.fieldsets()
            six.next(fieldsets)

    def test_raises_form(self):
        with self.assertRaises(AssertionError):
            form = TestFieldsetFormRaises()

    def test_readonly_form(self):
        form = TestReadonlyForm()
        form.set_readonly(True)
        self.assertTrue(form.fields[b'first_name'].is_readonly)
        form.set_readonly(False)
        self.assertFalse(form.fields[b'first_name'].is_readonly)

    def test_readonly_model_form(self):
        instance = ContentType.objects.get_for_model(ContentType)
        form = TestReadonlyModelForm(instance=instance)
        form.set_readonly(True)
        self.assertTrue(form.fields[b'app_label'].is_readonly)
        form.set_readonly(False)
        self.assertFalse(form.fields[b'app_label'].is_readonly)

    def test_whitespace_form(self):
        form = TestWhitespaceForm(data={b'first_name': b' John    ', b'last_name': b'   '})
        self.assertFalse(form.is_valid())
        form = TestWhitespaceForm(data={b'first_name': b' Foo    ', b'last_name': b'   Bar ack'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'first_name'], b'Foo')
        self.assertEqual(form.cleaned_data[b'last_name'], b'Bar ack')

    def test_whitespace_model_form(self):
        instance = ContentType.objects.get_for_model(ContentType)
        form = TestWhitespaceModelForm(instance=instance, data={b'name': b' content type ', b'app_label': b' contenttypes    ', 
           b'model': b'     '})
        self.assertFalse(form.is_valid())
        form = TestWhitespaceModelForm(instance=instance, data={b'name': b' content type ', b'app_label': b' contenttypes    ', 
           b'model': b'   contenttype  '})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'app_label'], b'contenttypes')
        self.assertEqual(form.cleaned_data[b'model'], b'contenttype')