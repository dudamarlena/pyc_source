# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/drf-batch-requests/drf_batch_requests/urls.py
# Compiled at: 2018-02-12 08:36:05
try:
    from django.conf.urls import url
except:
    from django.urls import re_path as url

from drf_batch_requests import views
app_name = 'drt_batch_requests'
urlpatterns = [
 url('^', views.BatchView.as_view())]