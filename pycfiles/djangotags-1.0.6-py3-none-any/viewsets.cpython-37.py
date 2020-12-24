# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangotags\src\djangotags\rest_api\viewsets.py
# Compiled at: 2020-03-13 02:04:53
# Size of source mod 2**32: 977 bytes
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import DestroyAPIView
from taggit.models import Tag
from djangotags.rest_api.serializers import TagSerializer

class TagListViewSet(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveViewSet(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'tag_slug'


class TagUpdateViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'tag_slug'


class TagDestroyViewSet(DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'tag_slug'