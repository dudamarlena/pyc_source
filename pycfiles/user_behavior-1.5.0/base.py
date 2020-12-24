# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/6z/y737zg156f53v6d096dlmv500000gn/T/pip-build-YeCYrE/user-behavior/user_behavior/base.py
# Compiled at: 2016-11-17 22:38:22
from __future__ import absolute_import
from rest_framework import serializers
from django.utils import timezone
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class DateTimeFormatField(serializers.DateTimeField):

    def __init__(self, *args, **kwargs):
        kwargs['format'] = DATE_FORMAT
        super(DateTimeFormatField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFormatField, self).to_representation(value)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    created_at = DateTimeFormatField(format=DATE_FORMAT, read_only=True)
    updated_at = DateTimeFormatField(format=DATE_FORMAT, read_only=True)


class UserField(serializers.Field):

    def to_representation(self, obj):
        return {'username': obj.username, 
           'first_name': obj.first_name, 
           'last_name': obj.last_name, 
           'email': obj.email, 
           'is_superuser': obj.is_superuser}

    def to_internal_value(self, data):
        return super(UserField, self).to_internal_value(data)