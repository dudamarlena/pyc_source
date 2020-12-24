# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/app/serializers.py
# Compiled at: 2018-05-06 09:03:54
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import fields
from drf_serializer_cache import SerializerCacheMixin
from tests.app import models

class UserSerializer(SerializerCacheMixin, ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'name')


class FilmCategorySerializer(SerializerCacheMixin, ModelSerializer):

    class Meta:
        model = models.FilmCategory
        fields = ('id', 'name')


class FilmSerializer(SerializerCacheMixin, ModelSerializer):
    uploaded_by = UserSerializer()
    category = FilmCategorySerializer()

    class Meta:
        model = models.Film
        fields = ('id', 'name', 'category', 'year', 'uploaded_by')


class CategoryHierarchySerializer(SerializerCacheMixin, Serializer):
    category = FilmCategorySerializer()
    films = fields.SerializerMethodField()
    categories = fields.SerializerMethodField()

    def get_films(self, instance):
        serializer = FilmSerializer(instance.films, many=True)
        serializer.bind('*', self)
        return serializer.data

    def get_categories(self, instance):
        serializer = self.__class__(instance.categories, many=True)
        serializer.bind('*', self)
        return serializer.data