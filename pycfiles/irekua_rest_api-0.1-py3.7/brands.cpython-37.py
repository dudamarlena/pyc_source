# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/serializers/devices/brands.py
# Compiled at: 2019-10-28 01:53:14
# Size of source mod 2**32: 969 bytes
from __future__ import unicode_literals
from rest_framework import serializers
from irekua_database.models import DeviceBrand

class SelectSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceBrand
        fields = ('url', 'name')


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceBrand
        fields = ('url', 'name', 'logo')


class DetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DeviceBrand
        fields = ('url', 'name', 'website', 'logo', 'created_on', 'modified_on')


class CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceBrand
        fields = ('name', 'website', 'logo')