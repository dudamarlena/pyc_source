# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/forms/tests/test_key_value_form.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django import forms
from djblets.forms.forms import KeyValueForm
from djblets.testing.testcases import TestCase

class DummyForm(KeyValueForm):
    char_field = forms.CharField(initial=b'default', required=False)
    bool_field = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        self.saved = False
        super(DummyForm, self).__init__(*args, **kwargs)

    def create_instance(self):
        return {}

    def save_instance(self):
        self.saved = True


class KeyValueFormTests(TestCase):
    """Unit tests for djblets.forms.forms.KeyValueForm."""

    def test_load_without_instance(self):
        """Testing KeyValueForm load without instance"""
        form = DummyForm()
        self.assertEqual(form.fields[b'char_field'].initial, b'default')
        self.assertTrue(form.fields[b'bool_field'].initial)

    def test_load_with_instance(self):
        """Testing KeyValueForm.load with instance"""
        form = DummyForm(instance={b'char_field': b'new value', 
           b'bool_field': False})
        self.assertEqual(form.fields[b'char_field'].initial, b'new value')
        self.assertFalse(form.fields[b'bool_field'].initial)

    def test_load_with_load_blacklist(self):
        """Testing KeyValueForm.load with Meta.load_blacklist"""

        class LoadBlacklistForm(DummyForm):

            class Meta:
                load_blacklist = ('char_field', )
                save_blacklist = ('bool_field', )

        form = LoadBlacklistForm(instance={b'char_field': b'new value', 
           b'bool_field': False})
        self.assertEqual(form.fields[b'char_field'].initial, b'default')
        self.assertFalse(form.fields[b'bool_field'].initial)

    def test_load_with_save_blacklist(self):
        """Testing KeyValueForm.load with Meta.save_blacklist only"""

        class LoadBlacklistForm(DummyForm):

            class Meta:
                save_blacklist = ('char_field', )

        form = LoadBlacklistForm(instance={b'char_field': b'new value', 
           b'bool_field': False})
        self.assertEqual(form.fields[b'char_field'].initial, b'default')
        self.assertFalse(form.fields[b'bool_field'].initial)

    def test_load_with_disabled_fields(self):
        """Testing KeyValueForm.load with disabled_fields"""

        class DisabledFieldsForm(DummyForm):

            def load(self):
                self.disabled_fields[b'char_field'] = True
                super(DisabledFieldsForm, self).load()

            class Meta:
                save_blacklist = ('char_field', )

        form = DisabledFieldsForm(instance={b'char_field': b'new value', 
           b'bool_field': False})
        self.assertIn(b'disabled', form.fields[b'char_field'].widget.attrs)
        self.assertEqual(form.fields[b'char_field'].widget.attrs[b'disabled'], b'disabled')
        self.assertNotIn(b'disabled', form.fields[b'bool_field'].widget.attrs)

    def test_load_with_custom_deserialized_field(self):
        """Testing KeyValueForm.load with custom deserializer for field"""

        class DeserializerForm(DummyForm):
            custom = forms.CharField()

            def deserialize_custom_field(self, value):
                return value[b'value']

        form = DeserializerForm(instance={b'custom': {b'is_custom': True, 
                       b'value': b'my value'}})
        self.assertEqual(form.fields[b'custom'].initial, b'my value')

    def test_save_without_instance(self):
        """Testing KeyValueForm.save without existing instance"""
        form = DummyForm(data={b'char_field': b'new value', 
           b'bool_field': False})
        self.assertTrue(form.is_valid())
        result = form.save()
        self.assertEqual(result, {b'char_field': b'new value', 
           b'bool_field': False})
        self.assertTrue(form.saved)

    def test_save_with_instance(self):
        """Testing KeyValueForm.save with existing instance"""
        instance = {b'char_field': b'orig value', 
           b'bool_field': False}
        form = DummyForm(instance=instance, data={b'char_field': b'new value', 
           b'bool_field': False})
        self.assertTrue(form.is_valid())
        result = form.save()
        self.assertEqual(result, {b'char_field': b'new value', 
           b'bool_field': False})
        self.assertTrue(form.saved)
        self.assertTrue(instance is result)

    def test_save_with_instance_no_commit(self):
        """Testing KeyValueForm.save with existing instance and with
        commit=False
        """
        instance = {b'char_field': b'orig value', 
           b'bool_field': False}
        form = DummyForm(instance=instance, data={b'char_field': b'new value', 
           b'bool_field': False})
        self.assertTrue(form.is_valid())
        result = form.save(commit=False)
        self.assertEqual(result, {b'char_field': b'new value', 
           b'bool_field': False})
        self.assertFalse(form.saved)
        self.assertTrue(instance is result)

    def test_save_with_save_blacklist(self):
        """Testing KeyValueForm.save with Meta.save_blacklist"""

        class SaveBlacklistForm(DummyForm):

            class Meta:
                save_blacklist = ('char_field', )

        instance = {b'char_field': b'orig value', 
           b'bool_field': False}
        form = SaveBlacklistForm(instance=instance, data={b'char_field': b'new value', 
           b'bool_field': True})
        self.assertTrue(form.is_valid())
        result = form.save()
        self.assertEqual(result, {b'char_field': b'orig value', 
           b'bool_field': True})
        self.assertTrue(instance is result)

    def test_save_with_extra_save_blacklist(self):
        """Testing KeyValueForm.save with Meta.extra_save_blacklist"""

        class SaveBlacklistForm(DummyForm):

            class Meta:
                save_blacklist = ('char_field', )

        instance = {b'char_field': b'orig value', 
           b'bool_field': False}
        form = SaveBlacklistForm(instance=instance, data={b'char_field': b'new value', 
           b'bool_field': True})
        self.assertTrue(form.is_valid())
        result = form.save(extra_save_blacklist=('bool_field', ))
        self.assertEqual(result, {b'char_field': b'orig value', 
           b'bool_field': False})
        self.assertTrue(instance is result)

    def test_save_with_custom_serialized_field(self):
        """Testing KeyValueForm.save with custom serializer for field"""

        class SerializerForm(DummyForm):
            custom = forms.CharField()

            def serialize_custom_field(self, value):
                return {b'is_custom': True, 
                   b'value': value}

        instance = {b'custom': {b'is_custom': True, 
                       b'value': b'orig value'}}
        form = SerializerForm(instance=instance, data={b'custom': b'new value'})
        self.assertTrue(form.is_valid())
        result = form.save()
        self.assertTrue(instance is result)
        self.assertEqual(result[b'custom'], {b'is_custom': True, 
           b'value': b'new value'})