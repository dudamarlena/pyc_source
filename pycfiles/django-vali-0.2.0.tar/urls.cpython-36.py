# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/anyi/workspace/django-vali/vali/urls.py
# Compiled at: 2018-02-05 10:17:56
# Size of source mod 2**32: 139 bytes
from django.conf.urls import url
from .views import ValiDashboardView
urlpatterns = [url('^dashboard/', ValiDashboardView.as_view())]