# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/tests/test_error_messages.py
# Compiled at: 2017-11-28 02:59:59
from django.test import TestCase
from formfactory import models

class CustomErrorMessageTestCase(TestCase):

    def test_custom_error_message(self):
        field = models.FormField.objects.create(title='Number', slug='number', field_type='django.forms.fields.IntegerField')
        error_message = models.CustomErrorMessage.objects.create(key='required', value='Please do not leave this field empty.')
        field.error_messages.add(error_message)
        group = models.FormFieldGroup.objects.create(title='Test field group', show_title=False)
        models.FieldGroupThrough.objects.create(field=field, field_group=group, order=0)
        form = models.Form.objects.create(title='Form 1', slug='slug-1')
        models.FieldGroupFormThrough.objects.create(form=form, field_group=group, order=0)
        bound_form = form.as_form(data={'number': ''})
        self.assertFalse(bound_form.is_valid())
        self.assertEqual(bound_form.errors['number'][0], 'Please do not leave this field empty.')