# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/testapp/urls.py
# Compiled at: 2020-01-06 15:05:24
# Size of source mod 2**32: 216 bytes
from django.urls import include, path
from tests.testapp.food import views
urlpatterns = [
 path('', (views.index), name='index'),
 path('django_query_profiler/', include('django_query_profiler.client.urls'))]