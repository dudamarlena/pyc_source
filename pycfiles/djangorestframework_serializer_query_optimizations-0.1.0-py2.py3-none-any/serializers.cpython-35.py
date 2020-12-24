# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mmm/kode/gorgonzo.la/djangorestframework-serializer-query-optimizations/drf_serializer_query_optimizations/serializers.py
# Compiled at: 2017-09-08 08:20:44
# Size of source mod 2**32: 2279 bytes
"""Serializers for query optimizations."""
from django.db import models
from rest_framework import serializers

class QueryOptimizingListSerializer(serializers.ListSerializer):
    __doc__ = '\n    A list serializer for query optimizations for model serializers.\n\n    The idea is to provide an easy way to utilize `select_related()` and\n    `prefetch_related()`.\n\n    There is no way to automatically determine the correct values for these\n    QuerySet methods.\n\n    This serializer makes it easy to do query optimizations in serialized\n    lists, by allowing you to define the values for `select_related()` and\n    `prefetch_related()` yourself as attributes on the child serializer as\n    simple lists. This serializer will then take care of adding the\n    optimizations to the query before it is executed.\n    '

    def to_representation(self, data):
        """
        Custom data handling, to support query optimizations.

        This one is based on the similar method of the DRF ListSerializer,
        but adds support for query optimizations.

        Currently based on the method from version 3.6.4 of DRF.
        """
        assert isinstance(self.child, serializers.ModelSerializer), 'The QueryOptimizingListSerializer can only be used as list  serializer for model serializers.'
        iterable = data.all() if isinstance(data, models.Manager) else data
        if hasattr(self.child.Meta, 'select_related'):
            iterable = iterable.select_related(*self.child.Meta.select_related)
        if hasattr(self.child.Meta, 'prefetch_related'):
            iterable = iterable.prefetch_related(*self.child.Meta.prefetch_related)
        return [self.child.to_representation(item) for item in iterable]