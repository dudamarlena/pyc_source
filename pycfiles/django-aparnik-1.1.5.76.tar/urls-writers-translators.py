# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/books/api/urls-writers-translators.py
# Compiled at: 2018-11-05 07:19:14
from django.conf.urls import url, include
from .views import WriterTranslatorListAPIView, WriterTranslatorDetailAPIView
urlpatterns = [
 url('^$', WriterTranslatorListAPIView.as_view(), name='list'),
 url('^(?P<writer_translator_id>\\d+)/$', WriterTranslatorDetailAPIView.as_view(), name='details')]