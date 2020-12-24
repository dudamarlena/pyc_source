# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/serializers/annotations/tools.py
# Compiled at: 2019-10-28 01:53:14
# Size of source mod 2**32: 1223 bytes
from __future__ import unicode_literals
from rest_framework import serializers
from irekua_database.models import AnnotationTool

class SelectSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationTool
        fields = ('url', 'name')


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationTool
        fields = ('url', 'name', 'version', 'description', 'logo')


class DetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AnnotationTool
        fields = ('url', 'id', 'name', 'version', 'description', 'logo', 'website',
                  'configuration_schema', 'created_on', 'modified_on')


class CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationTool
        fields = ('name', 'version', 'description', 'logo', 'website', 'configuration_schema')