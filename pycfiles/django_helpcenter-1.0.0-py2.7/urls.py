# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/urls.py
# Compiled at: 2016-09-30 00:56:02
from django.conf.urls import include, url
from helpcenter import views
app_name = 'helpcenter'
article_urls = [
 url('^create/$', views.ArticleCreateView.as_view(), name='article-create'),
 url('^(?P<article_pk>[0-9]+)/(?P<article_slug>[-\\w]+)/', include([
  url('^$', views.ArticleDetailView.as_view(), name='article-detail'),
  url('^delete/$', views.ArticleDeleteView.as_view(), name='article-delete'),
  url('^update/$', views.ArticleUpdateView.as_view(), name='article-update')]))]
category_urls = [
 url('^create/$', views.CategoryCreateView.as_view(), name='category-create'),
 url('^(?P<category_pk>[0-9]+)/(?P<category_slug>[-\\w]+)/', include([
  url('^$', views.CategoryDetailView.as_view(), name='category-detail'),
  url('^delete/$', views.CategoryDeleteView.as_view(), name='category-delete'),
  url('^update/$', views.CategoryUpdateView.as_view(), name='category-update')]))]
urlpatterns = [
 url('^api/', include('helpcenter.api.urls', app_name='helpcenter-api', namespace='api')),
 url('^articles/', include(article_urls)),
 url('^categories/', include(category_urls)),
 url('^$', views.IndexView.as_view(), name='index')]