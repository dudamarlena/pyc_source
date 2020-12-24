# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/serializers/object_types/events.py
# Compiled at: 2019-10-28 01:53:14
# Size of source mod 2**32: 1528 bytes
from __future__ import unicode_literals
from rest_framework import serializers
from irekua_database.models import EventType
from . import terms

class SelectSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='rest-api:eventtype-detail')
    name = serializers.PrimaryKeyRelatedField(many=False,
      read_only=False,
      queryset=(EventType.objects.all()))

    class Meta:
        model = EventType
        fields = ('url', 'name')


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = ('url', 'name', 'description', 'icon')


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    term_types = terms.SelectSerializer(many=True,
      read_only=True)

    class Meta:
        model = EventType
        fields = ('url', 'name', 'description', 'icon', 'term_types', 'created_on',
                  'modified_on')


class CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = ('name', 'description', 'icon')


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = ('description', 'icon')