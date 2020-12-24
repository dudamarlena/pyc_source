# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ray/Work/Rumor/django-phone-login/phone_login/serializers.py
# Compiled at: 2017-08-01 15:49:20
# Size of source mod 2**32: 795 bytes
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import PhoneToken
User = get_user_model()

class PhoneTokenCreateSerializer(ModelSerializer):
    phone_number = serializers.CharField(validators=(PhoneNumberField().validators))

    class Meta:
        model = PhoneToken
        fields = ('pk', 'phone_number')


class PhoneTokenUser(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class PhoneTokenValidateSerializer(ModelSerializer):
    pk = serializers.IntegerField()
    otp = serializers.CharField(max_length=40)

    class Meta:
        model = PhoneToken
        fields = ('pk', 'otp')