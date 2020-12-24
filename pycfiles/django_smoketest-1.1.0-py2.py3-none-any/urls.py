# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/ccnmtl/django-smoketest/smoketest/urls.py
# Compiled at: 2017-06-18 04:08:30
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from .views import IndexView
urlpatterns = [
 url('^$', IndexView.as_view(), name='smoketest')]