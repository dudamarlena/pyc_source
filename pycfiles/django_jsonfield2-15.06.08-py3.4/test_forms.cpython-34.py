# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonfield2/tests/test_forms.py
# Compiled at: 2015-06-04 10:41:05
# Size of source mod 2**32: 1977 bytes
from django.test import TestCase as DjangoTestCase
from django.forms import ValidationError
from jsonfield2.forms import JSONFormField
from jsonfield2.tests.jsonfield_test_app.forms import JSONTestForm

class JSONFormFieldTest(DjangoTestCase):

    def test_form_field_clean_empty_object(self):
        field = JSONFormField(required=False)
        self.assertEqual({}, field.clean('{}'))

    def test_form_field_clean_object(self):
        field = JSONFormField(required=False)
        self.assertEqual({'foo': 'bar',  'baz': 2}, field.clean('{"foo":"bar","baz":2}'))

    def test_form_field_widget(self):
        field = JSONFormField(required=False)
        self.assertIn('{\n  &quot;a&quot;: true\n}', field.widget.render('json', {'a': True}))

    def test_form_field_clean_empty_array(self):
        field = JSONFormField(required=False)
        self.assertEqual([], field.clean('[]'))

    def test_required_form_field_array(self):
        field = JSONFormField(required=True)
        self.assertEqual([], field.clean('[]'))

    def test_required_form_field_object(self):
        field = JSONFormField(required=True)
        self.assertEqual({}, field.clean('{}'))

    def test_required_form_field_empty(self):
        field = JSONFormField(required=True)
        with self.assertRaises(ValidationError):
            field.clean('')

    def test_invalid_json(self):
        field = JSONFormField(required=True)
        with self.assertRaises(ValidationError):
            field.clean('{"foo"}')


class JSONFormTest(DjangoTestCase):

    def test_form_clean(self):
        form = JSONTestForm({})
        self.assertFalse(form.is_valid())


class JSONFormMultipleSelectFieldTest(DjangoTestCase):

    def test_multiple_select_data(self):
        form = JSONTestForm({'json_data': ['SA', 'WA']})
        assert form.is_valid()
        self.assertEqual(['SA', 'WA'], form.cleaned_data['json_data'])