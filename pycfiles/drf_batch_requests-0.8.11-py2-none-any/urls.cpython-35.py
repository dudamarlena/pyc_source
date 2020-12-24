# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/drf-batch-requests/drf_batch/urls.py
# Compiled at: 2017-10-11 06:45:27
# Size of source mod 2**32: 114 bytes
from django.conf.urls import url
from . import views
urlpatterns = [
 url('^', views.BatchView.as_view())]