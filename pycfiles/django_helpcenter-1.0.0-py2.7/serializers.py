# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/api/serializers.py
# Compiled at: 2016-09-30 00:56:02
from rest_framework import serializers
from helpcenter import models

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for the Article model """
    category_id = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=models.Category.objects.all(), required=False, source='category')

    class Meta:
        extra_kwargs = {'category': {'view_name': 'helpcenter:helpcenter-api:category-detail'}, 
           'url': {'view_name': 'helpcenter:helpcenter-api:article-detail'}}
        fields = ('body', 'category', 'category_id', 'id', 'time_published', 'title',
                  'url')
        model = models.Article
        read_only_fields = ('category', 'id')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for the Category model """
    parent_id = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=models.Category.objects.all(), required=False, source='parent')

    class Meta:
        extra_kwargs = {'parent': {'view_name': 'helpcenter:helpcenter-api:category-detail'}, 
           'url': {'view_name': 'helpcenter:helpcenter-api:category-detail'}}
        fields = ('id', 'parent', 'parent_id', 'title', 'url')
        model = models.Category
        read_only_fields = ('id', 'parent')