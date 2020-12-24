# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/rest/serializers.py
# Compiled at: 2018-08-06 11:42:24
# Size of source mod 2**32: 624 bytes
from rest_framework import serializers
from django_blogposts.models import BlogPost, Tags

class TagsSerializer(serializers.ModelSerializer):
    absolute_url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Tags
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    absolute_url = serializers.CharField(source='get_absolute_url')
    image = serializers.CharField(source='image.url')
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        exclude = ('content', 'meta_title', 'meta_kw', 'meta_desc', 'de')