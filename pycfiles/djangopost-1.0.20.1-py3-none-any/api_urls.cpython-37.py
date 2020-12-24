# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangopost\src\djangopost\rest_api\api_urls.py
# Compiled at: 2020-03-14 05:50:35
# Size of source mod 2**32: 1878 bytes
import djangopost.rest_api as views
from django.conf.urls import re_path
urlpatterns = [
 re_path('^article/all/$', (views.ArticleListViewset.as_view()), name='article_list_viewset'),
 re_path('^article/published/$', (views.ArticleListPublishedViewset.as_view()), name='article_list_published_viewset'),
 re_path('^article/promoted/$', (views.ArticleListPromotedViewset.as_view()), name='article_list_promoted_viewset'),
 re_path('^article/trending/$', (views.ArticleListTrendingViewset.as_view()), name='article_list_trending_viewset'),
 re_path('^article/promo/$', (views.ArticleListPromoViewset.as_view()), name='article_list_promo_viewset'),
 re_path('^article/create/$', (views.ArticleCreateViewset.as_view()), name='article_create_viewset'),
 re_path('^article/(?P<slug>[\\w-]+)/$', (views.ArticleRetrieveViewset.as_view()), name='article_retrieve_viewset'),
 re_path('^article/(?P<slug>[\\w-]+)/update/$', (views.ArticleUpdateViewset.as_view()), name='article_update_viewset'),
 re_path('^article/(?P<slug>[\\w-]+)/destroy/$', (views.ArticleDestroyViewset.as_view()), name='article_destroy_viewset'),
 re_path('^category/all/$', (views.CategoryListViewset.as_view()), name='category_list_viewset'),
 re_path('^category/published/$', (views.CategoryListPublishedViewset.as_view()), name='category_published_viewset'),
 re_path('^category/create/$', (views.CategoryCreateViewset.as_view()), name='category_create_viewset'),
 re_path('^category/(?P<slug>[\\w-]+)/$', (views.CategoryRetrieveViewset.as_view()), name='category_retrieve_viewset'),
 re_path('^category/(?P<slug>[\\w-]+)/update/$', (views.CategoryUpdateViewset.as_view()), name='category_update_viewset'),
 re_path('^category/(?P<slug>[\\w-]+)/destroy/$', (views.CategoryDestroyViewset.as_view()), name='category_destroy_viewset')]