# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/mydjango/mysite/django_universe/urls.py
# Compiled at: 2016-09-09 12:04:32
from django.conf.urls import url
from . import views
urlpatterns = [
 url('^$', views.index, name='index')]