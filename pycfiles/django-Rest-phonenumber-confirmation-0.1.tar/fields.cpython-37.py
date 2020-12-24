# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/fields.py
# Compiled at: 2020-04-03 10:52:10
# Size of source mod 2**32: 563 bytes
import django.utils.translation as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from phonenumber_field.phonenumber import to_python

class PhoneNumberSerializerField(serializers.CharField):
    default_error_messages = {'invalid': _('Enter a valid phone number.')}

    def to_internal_value(self, data):
        phone_number = to_python(data)
        if phone_number:
            if not phone_number.is_valid():
                raise ValidationError(self.error_messages['invalid'])
        return phone_number