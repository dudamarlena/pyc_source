# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/urls/urls.py
# Compiled at: 2018-11-05 07:19:14
from django.conf.urls import url, include
urlpatterns = [
 url('^shops/', include('aparnik.packages.shops.urls.urls', namespace='shops'))]