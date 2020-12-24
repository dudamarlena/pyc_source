# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/serializers.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 8024 bytes
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from mycms.models import CMSContents
from mycms.models import CMSMarkUps
from mycms.models import CMSTemplates
from mycms.models import CMSPageTypes
from mycms.models import CMSEntries
from mycms.models import CMSPaths
import os

class LoremIpsumSerializer(serializers.Serializer):
    num_paragraphs = serializers.IntegerField()

    class Meta:
        fields = [
         'num_paragraphs']


class CMSPathsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CMSPaths
        fields = ('id', 'path', 'parent')


class CMSPageTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CMSPageTypes
        fields = ('id', 'page_type', 'text', 'view_class', 'view_template')


class CMSContentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CMSContents
        fields = ('id', 'content', 'timestamp', 'markup', 'title')


class CMSMarkUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CMSMarkUps
        fields = ('id', 'markup')


class CMSTemplatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CMSTemplates
        fields = ('id', 'name', 'template')


class CMSEntrySerializer(serializers.ModelSerializer):
    path = serializers.StringRelatedField()
    title = serializers.CharField(max_length=1024, help_text='The title of the page.')
    frontpage = serializers.BooleanField(default=False, help_text='default to False. Set True to display in frontpage')
    published = serializers.BooleanField(default=False, help_text='Published defaults to False')
    page_number = serializers.IntegerField(default=1, help_text='page_number')

    class Meta:
        model = CMSEntries
        fields = ('id', 'title', 'path', 'slug', 'content', 'date_created', 'page_type',
                  'frontpage', 'published', 'page_number')


class CMSEntryExpandedSerializer(serializers.ModelSerializer):
    path = serializers.StringRelatedField()
    template = serializers.IntegerField(default=1, help_text='Index value, pk for template')

    class Meta:
        model = CMSEntries
        fields = ('id', 'title', 'path', 'slug', 'content', 'date_created', 'page_type',
                  'template', 'frontpage', 'published', 'page_number', 'date_modified')


class EntryData(object):

    def __init__(self, **kwargs):
        for field in ('id', 'title', 'slug', 'parent'):
            setattr(self, field, kwargs.get(field, None))


class CMSChildEntrySerializer(serializers.ModelSerializer):
    template = serializers.IntegerField(required=False)
    content = CMSContentsSerializer(many=True, required=False)

    class Meta:
        model = CMSEntries
        fields = ('id', 'title', 'slug', 'content', 'date_created', 'page_type', 'template',
                  'frontpage', 'published', 'page_number')

    def make_path(self, slug, parent_id):
        """
        Creates a CMSPaths object for the current CMSEntry.
        """
        parent_obj = CMSEntries.objects.get(id=parent_id)
        path_str = os.path.join(parent_obj.path.path, slug)
        path_obj, c = CMSPaths.objects.get_or_create(path=path_str, parent=(parent_obj.path))
        if not c:
            print('Warning. Recreated {}'.format(path_str))
            entry = CMSEntries.objects.filter(path=path_obj)
            if entry:
                raise Exception('Article: {} already exists. Refuse to create. '.format(entry.title))
        return path_obj

    def create(self, validated_data, parent_id=None):
        title = validated_data['title']
        slug = validated_data['slug']
        try:
            content = validated_data['content']
        except KeyError as e:
            try:
                content = []
            finally:
                e = None
                del e

        template = validated_data.get('template', None)
        published = validated_data['published']
        frontpage = validated_data['frontpage']
        page_type = validated_data['page_type']
        child = CMSEntries()
        child.title = title
        child.slug = slug
        child.frontpage = frontpage
        child.published = published
        child.save()
        path_obj = self.make_path(slug, parent_id)
        child.path = path_obj
        child.template = template
        if len(content) == 0:
            content_entry = CMSContents(content='New Page. Please Edit Me!!!')
            content_entry.save()
            child.content.add(content_entry)
        else:
            child.content = content
        child.page_type = page_type
        child.save()
        child.on_create()
        return child


class CMSPathFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = CMSPaths
        fields = [
         'path', 'parent']


class CMSPageSerializer(serializers.ModelSerializer):
    path = CMSPathFullSerializer()
    content = CMSContentsSerializer(many=True)

    class Meta:
        model = CMSEntries
        title = serializers.CharField(max_length=1024, default=None)
        fields = ('id', 'title', 'slug', 'content', 'date_created', 'page_type', 'template',
                  'frontpage', 'published', 'page_number', 'path')


class CMSAuthTokenSerializer(serializers.Serializer):
    pass