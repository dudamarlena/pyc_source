# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/serializers/terms/suggestions.py
# Compiled at: 2019-10-28 01:56:48
# Size of source mod 2**32: 1684 bytes
from __future__ import unicode_literals
from rest_framework import serializers
from irekua_database.models import TermSuggestion
from irekua_rest_api.serializers.object_types import terms
import irekua_rest_api.serializers.users as users

class SelectSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermSuggestion
        fields = ('url', 'id')


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermSuggestion
        fields = ('url', 'id', 'term_type', 'value')


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    term_type = terms.SelectSerializer(many=False, read_only=True)
    suggested_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = TermSuggestion
        fields = ('url', 'term_type', 'value', 'description', 'metadata', 'suggested_by',
                  'suggested_on')


class CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermSuggestion
        fields = ('term_type', 'value', 'description', 'metadata')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['suggested_by'] = user
        return super().create(validated_data)


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermSuggestion
        fields = ('description', 'metadata')