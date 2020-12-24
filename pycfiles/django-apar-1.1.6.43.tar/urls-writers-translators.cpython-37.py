# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/books/api/urls-writers-translators.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 331 bytes
from django.conf.urls import url, include
from .views import WriterTranslatorListAPIView, WriterTranslatorDetailAPIView
app_name = 'books'
urlpatterns = [
 url('^$', (WriterTranslatorListAPIView.as_view()), name='list'),
 url('^(?P<writer_translator_id>\\d+)/$', (WriterTranslatorDetailAPIView.as_view()), name='details')]