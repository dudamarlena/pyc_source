# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangotags\src\djangotags\rest_api\serializers.py
# Compiled at: 2020-04-02 22:31:44
# Size of source mod 2**32: 909 bytes
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField
from taggit.models import Tag

class TagSerializer(ModelSerializer):
    api_detail_url = HyperlinkedIdentityField(view_name='djangotags:tag_retrieve_viewset',
      lookup_field='slug',
      lookup_url_kwarg='tag_slug')
    api_update_url = HyperlinkedIdentityField(view_name='djangotags:tag_update_viewset',
      lookup_field='slug',
      lookup_url_kwarg='tag_slug')
    api_delete_url = HyperlinkedIdentityField(view_name='djangotags:tag_destroy_viewset',
      lookup_field='slug',
      lookup_url_kwarg='tag_slug')

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'api_detail_url', 'api_update_url', 'api_delete_url']