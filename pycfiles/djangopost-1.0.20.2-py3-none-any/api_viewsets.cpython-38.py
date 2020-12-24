# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangopost\src\djangopost\rest_api\api_viewsets.py
# Compiled at: 2020-04-03 01:03:27
# Size of source mod 2**32: 4464 bytes
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from djangopost.models import CategoryModel
from djangopost.models import ArticleModel
from djangopost.rest_api.api_serializers import CategorySerializer
from djangopost.rest_api.api_serializers import ArticleSerializer
from djangopost.rest_api.api_permissions import IsOwnerOrReadOnly

class CategoryListViewset(ListAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class CategoryListPublishedViewset(ListAPIView):
    queryset = CategoryModel.objects.published()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class CategoryRetrieveViewset(RetrieveAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class CategoryUpdateViewset(RetrieveUpdateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class CategoryDestroyViewset(DestroyAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class CategoryCreateViewset(CreateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer


class ArticleListViewset(ListAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleListPublishedViewset(ListAPIView):
    queryset = ArticleModel.objects.published()
    serializer_class = ArticleSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleListPromotedViewset(ListAPIView):
    queryset = ArticleModel.objects.promoted()
    serializer_class = ArticleSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleListTrendingViewset(ListAPIView):
    queryset = ArticleModel.objects.trending()
    serializer_class = ArticleSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleListPromoViewset(ListAPIView):
    queryset = ArticleModel.objects.promotional()
    serializer_class = ArticleSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleRetrieveViewset(RetrieveAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'


class ArticleUpdateViewset(RetrieveUpdateAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class ArticleDestroyViewset(DestroyAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class ArticleCreateViewset(CreateAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer


class CategoryDetailArticleListViewSet(ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return ArticleModel.objects.published().filter(category__slug=(self.kwargs['slug']))


class TaggitDetailArticleListViewSet(ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return ArticleModel.objects.published().filter(tags__slug=(self.kwargs['slug']))