# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eugene/Workspace/django-rest-framework-registration/rest_framework_registration/serializers.py
# Compiled at: 2016-04-03 11:54:12
# Size of source mod 2**32: 659 bytes
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        is_active = validated_data.pop('is_active')
        user = User.objects.create_user(**validated_data)
        user.is_active = is_active
        user.save()
        return user