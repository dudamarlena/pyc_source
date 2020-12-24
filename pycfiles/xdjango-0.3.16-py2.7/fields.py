# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdjango/forms/fields.py
# Compiled at: 2016-06-20 12:45:24
from django.forms import TypedMultipleChoiceField, CharField, Field
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_text, force_text
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import MultipleHiddenInput, SelectMultiple
from xdjango.core import validators

class TypedMultipleField(TypedMultipleChoiceField):

    def validate(self, value):
        """
        Validates if the input is required.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')


class EmailOrPhoneNumberField(CharField):
    default_validators = [
     validators.validate_email_or_phone_number]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(EmailOrPhoneNumberField, self).clean(value)


class PhoneNumberField(CharField):
    default_validators = [
     validators.validate_phone_number]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(PhoneNumberField, self).clean(value)


class MultiCharField(Field):
    hidden_widget = MultipleHiddenInput
    widget = SelectMultiple
    default_error_messages = {'invalid_list': _('Enter a list of values.')}

    def to_python(self, value):
        if not value:
            return []
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        return [ smart_text(val) for val in value ]

    def validate(self, value):
        """
        Validates that the input is a list or tuple.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
        for val in value:
            pass

    def has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        else:
            initial_set = set(force_text(value) for value in initial)
            data_set = set(force_text(value) for value in data)
            return data_set != initial_set