# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/serializers.py
# Compiled at: 2020-04-03 12:28:35
# Size of source mod 2**32: 883 bytes
import django.utils.translation as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from phonenumber_confirmation.fields import PhoneNumberSerializerField
from .models import PhoneNumber, PhoneNumberConfirmation

class PhoneNumberSerializer(serializers.Serializer):
    phone = PhoneNumberSerializerField()

    def validate(self, data):
        if PhoneNumber.objects.filter(phone=(data.get('phone', ''))):
            raise serializers.ValidationError(_('A user use this phone number before.'))
        return data


class PINConfirmationSerializer(serializers.Serializer):
    pin = serializers.IntegerField()

    def validate(self, data):
        if not PhoneNumberConfirmation.objects.filter(pin=(data.get('pin', ''))):
            raise serializers.ValidationError(_('Wrong pin.'))
        return data