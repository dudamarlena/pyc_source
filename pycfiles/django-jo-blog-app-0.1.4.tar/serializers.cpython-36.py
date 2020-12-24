# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/blog/api/serializers.py
# Compiled at: 2019-07-23 09:12:35
# Size of source mod 2**32: 626 bytes
from rest_framework import serializers
from blog.models import Post

class PostSerializers(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
         'id',
         'author',
         'title',
         'body']
        read_only_fields = [
         'id']

    def validate_title(self, value):
        qs = Post.objects.filter(title=value)
        if self.instance:
            qs = qs.exclude(title=(self.instance.title))
        if qs.exists():
            raise serializers.ValidationError('This title has already been used!')
        return value