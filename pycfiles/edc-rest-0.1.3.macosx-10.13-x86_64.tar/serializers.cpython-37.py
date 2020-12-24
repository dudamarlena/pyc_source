# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/edc_rest/serializers.py
# Compiled at: 2017-04-08 11:31:14
# Size of source mod 2**32: 918 bytes
from rest_framework import serializers

class BaseModelSerializerMixin:
    model_class = None
    user_created = serializers.CharField(max_length=50,
      allow_blank=True)
    user_modified = serializers.CharField(max_length=50,
      allow_blank=True)
    hostname_created = serializers.CharField(max_length=50,
      allow_blank=True)
    hostname_modified = serializers.CharField(max_length=50,
      allow_blank=True)
    revision = serializers.CharField(max_length=75)

    def create(self, validated_data):
        return (self.model_class.objects.create)(**validated_data)

    def update(self, instance, validated_data):
        for fieldname in [fld.name for fld in self.model_class._meta.fields]:
            setattr(instance, fieldname, validated_data.get(fieldname, getattr(instance, fieldname)))

        instance.save()
        return instance