# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/serializers.py
# Compiled at: 2016-03-10 17:43:47
# Size of source mod 2**32: 679 bytes
from rest_framework import serializers
from django.contrib.auth import get_user_model
Account = get_user_model()

class BasicAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', )


class ExtendedAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'email')


class AccountSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'email', 'auth_token', 'first_name', 'last_name')

    def get_auth_token(self, obj):
        return obj.auth_token.key