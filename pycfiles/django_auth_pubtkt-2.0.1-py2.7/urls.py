# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\urls.py
# Compiled at: 2017-07-28 08:40:03
from django.conf.urls import url, include
from .views import IndexView
urlpatterns = [
 url('^$', IndexView.as_view(), name='index'),
 url('', include('django_auth_pubtkt.urls'))]