# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/serializers/annotations/votes.py
# Compiled at: 2019-10-28 01:56:48
# Size of source mod 2**32: 1847 bytes
from __future__ import unicode_literals
from rest_framework import serializers
from irekua_database.models import AnnotationVote
import irekua_rest_api.serializers.users as users
from . import annotations

class SelectSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationVote
        fields = ('url', 'id')


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationVote
        fields = ('url', 'id', 'label')


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    annotation = annotations.SelectSerializer(many=False,
      read_only=True)
    created_by = users.SelectSerializer(many=False,
      read_only=True)

    class Meta:
        model = AnnotationVote
        fields = ('url', 'id', 'annotation', 'label', 'created_by', 'created_on', 'modified_on')


class CreateSerializer(serializers.ModelSerializer):
    label = serializers.JSONField()

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        try:
            annotation = self.context['annotation']
            previous_label = annotation.label
            self.fields['label'].initial = previous_label
        except (KeyError, AttributeError):
            pass

    class Meta:
        model = AnnotationVote
        fields = ('label', )

    def create(self, validated_data):
        annotation = self.context['annotation']
        user = self.context['request'].user
        validated_data['annotation'] = annotation
        validated_data['created_by'] = user
        return super().create(validated_data)