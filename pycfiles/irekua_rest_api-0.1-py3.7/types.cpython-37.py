# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/serializers/object_types/sampling_events/types.py
# Compiled at: 2019-10-28 01:53:14
# Size of source mod 2**32: 1420 bytes
from __future__ import unicode_literals
from rest_framework import serializers
from irekua_database.models import SamplingEventType

class SelectSerializer(serializers.ModelSerializer):

    class Meta:
        model = SamplingEventType
        fields = ('url', 'name')


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SamplingEventType
        fields = ('url', 'name', 'icon', 'description')


class DetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SamplingEventType
        fields = ('url', 'name', 'description', 'icon', 'metadata_schema', 'restrict_device_types',
                  'restrict_site_types', 'created_on', 'modified_on')


class CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SamplingEventType
        fields = ('name', 'description', 'icon', 'metadata_schema', 'restrict_device_types',
                  'restrict_site_types')


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SamplingEventType
        fields = ('description', 'icon')