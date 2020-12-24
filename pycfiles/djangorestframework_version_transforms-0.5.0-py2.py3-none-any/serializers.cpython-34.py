# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matthardwick/workspace/drf-representation-transforms/django-rest-framework-version-transforms/rest_framework_transforms/serializers.py
# Compiled at: 2015-10-27 20:12:50
# Size of source mod 2**32: 1480 bytes
from rest_framework import serializers
from rest_framework_transforms.exceptions import TransformBaseNotDeclaredException
from rest_framework_transforms.utils import get_transform_classes

class BaseVersioningSerializer(serializers.ModelSerializer):
    __doc__ = '\n    A base class for serializers that automatically demote resource representations\n    according to provided transform classes for the resource.\n    '
    transform_base = None

    def to_representation(self, instance):
        """
        Serializes the outgoing data as JSON and executes any available version transforms in backwards
        order against the serialized representation to convert the highest supported version into the
        requested version of the resource.
        """
        if not self.transform_base:
            raise TransformBaseNotDeclaredException('VersioningParser cannot correctly promote incoming resources with no transform classes.')
        data = super(BaseVersioningSerializer, self).to_representation(instance)
        if instance:
            request = self.context.get('request')
            if request:
                if hasattr(request, 'version'):
                    for transform in get_transform_classes(self.transform_base, base_version=request.version, reverse=True):
                        data = transform().backwards(data, request, instance)

        return data