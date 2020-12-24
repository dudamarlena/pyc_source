# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/sloop/serializers.py
# Compiled at: 2019-06-27 10:51:09
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .utils import get_device_model

class DeviceSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    push_token = serializers.CharField(required=True)
    platform = serializers.CharField(required=True)
    model = serializers.CharField(required=False, default='')
    locale = serializers.CharField(required=False, default='')

    def create(self, validated_data):
        device_model = get_device_model()
        user = validated_data['user']
        device, created = device_model._default_manager.update_or_create(push_token=validated_data['push_token'], platform=validated_data['platform'], defaults={'user': user, 
           'locale': validated_data.get('locale'), 
           'model': validated_data.get('model')})
        return device